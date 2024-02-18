import streamlit as st
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
import json
import uuid as uuid_g

import cassandra
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings

from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.llm import LLMChain
from langchain.callbacks.base import BaseCallbackHandler

from typing import Any, Dict, List, Optional
from langchain_core.outputs import LLMResult
from langchain_community.callbacks.utils import import_pandas
import time

TOKEN_USAGE = "token_usage"
PROMPT = "prompt"
RESPONSE = "response"
TOTAL_TOKENS = "total_tokens"
PROMPT_TOKENS = "prompt_tokens"
COMPLETION_TOKENS = "completion_tokens"
DURATION = "duration"
RUN_ID = "run_id"
MODEL_NAME = "model_name"
URL = 'https://demo.fiddler.ai'
ORG_NAME = 'demo'
FIDDLER_API_TOKEN = os.environ.get('FIDDLER_API_TOKEN')

_re_dict = {
    PROMPT : ["fiddler"] * 10,
    RESPONSE : ["fiddler"] * 10,
    MODEL_NAME : ["gpt-3.5-turbo-instruct"] * 10,
    RUN_ID : ['123e4567-e89b-12d3-a456-426614174000'] * 10,
    TOTAL_TOKENS : [0, 65536] * 5,
    PROMPT_TOKENS : [0, 65536] * 5,
    COMPLETION_TOKENS : [0, 4096] * 5,
    DURATION : [1, 120] * 5,
}

def import_fiddler() -> Any:
    """Import the fiddler python package and raise an error if it is not installed."""
    try:
        import fiddler  # noqa: F401
    except ImportError:
        raise ImportError(
            "To use the fiddler callback manager you need to have the `fiddler-client` python "
            "package installed. Please install it with `pip install fiddler-client`"
        )
    return fiddler

# First, define custom callback handler implementations
class FiddlerCallbackHandler(BaseCallbackHandler):
    def __init__(
        self,
        url : Optional[str] = None,
        org: Optional[str] = None,
        project: Optional[str] = None,
        model : Optional[str] = None,
        API_KEY: Optional[str] = None,
    ) -> None:
        """Initialize callback handler."""
        super().__init__()
        # Initialize Fiddler client and other necessary properties
        self.fdl = import_fiddler()
        self.pd = import_pandas()
        
        self.url = url
        self.org = org
        self.project = project
        self.model = model
        self.api_key = API_KEY
        self._df = self.pd.DataFrame(_re_dict)

        self.run_id_prompts : Dict[str, List[str]] = {}
        self.run_id_starttime : Dict[str, int] = {}

        # Initialize Fiddler client here
        self.fiddler_client = self.fdl.FiddlerApi(url, org_id=org, auth_token=API_KEY)

        if self.project not in self.fiddler_client.get_project_names():
            print(f'adding project {self.project}')
            self.fiddler_client.add_project(self.project)

        dataset_info = self.fdl.DatasetInfo.from_dataframe(self._df, max_inferred_cardinality=0)
        if self.model not in self.fiddler_client.get_dataset_names(self.project):
            print(f'adding dataset {self.model} to project {self.project}. Only has to be done once.')
            self.fiddler_client.upload_dataset(
                project_id=self.project,
                dataset_id=self.model,
                dataset={
                    'train': self._df
                },
                info=dataset_info
            )
            
        model_info = self.fdl.ModelInfo.from_dataset_info(
            dataset_info=dataset_info,
            dataset_id='train',
            model_task=self.fdl.ModelTask.LLM,
            features=[PROMPT, RESPONSE],
            metadata_cols=[RUN_ID, TOTAL_TOKENS, PROMPT_TOKENS, COMPLETION_TOKENS, MODEL_NAME],
            custom_features=self.custom_features
        )
        
        if self.model not in self.fiddler_client.get_model_names(self.project):
            print(f'adding model {self.model} to project {self.project}. Only has to be done once.')
            self.fiddler_client.add_model(
                project_id=self.project,
                dataset_id=self.model,
                model_id=self.model,
                model_info=model_info,
            )

    @property
    def custom_features(self):
        return [
            self.fdl.Enrichment(
                name='Prompt Embedding',
                enrichment='embedding',
                columns=[PROMPT],
            ),
            self.fdl.TextEmbedding(
                name='Prompt CF',
                source_column=PROMPT,
                column='Prompt Embedding',
            ),
            self.fdl.Enrichment(
                name='Response Embedding',
                enrichment='embedding',
                columns=[RESPONSE],
            ),
            self.fdl.TextEmbedding(
                name='Response CF',
                source_column=RESPONSE,
                column='Response Embedding',
            ),
            self.fdl.Enrichment(
                name='Text Statistics',
                enrichment='textstat',
                columns=[PROMPT, RESPONSE],
                config = {
                    "statistics" : [
                        "automated_readability_index",
                        "coleman_liau_index",
                        "dale_chall_readability_score",
                        "difficult_words",
                        "flesch_reading_ease",
                        "flesch_kincaid_grade",
                        "gunning_fog",
                        "linsear_write_formula",
                    ]
                }
            ),
            self.fdl.Enrichment(
                name='PII',
                enrichment='pii',
                columns=[PROMPT, RESPONSE],
            ),
            self.fdl.Enrichment(
                name='Sentiment',
                enrichment='sentiment',
                columns=[PROMPT, RESPONSE],
            )
        ]
            
    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        run_id = kwargs[RUN_ID]
        self.run_id_prompts[run_id] = prompts
        self.run_id_starttime[run_id] = int(time.time())

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:        
        flattened_llmresult = response.flatten()
        token_usage_dict = {}
        run_id = kwargs[RUN_ID]
        run_duration = self.run_id_starttime[run_id] - int(time.time())
        prompt_responses = []
        model_name = ''
        
        if isinstance(response.llm_output, dict):
            if TOKEN_USAGE in response.llm_output:
                token_usage_dict = response.llm_output[TOKEN_USAGE]
            if MODEL_NAME in response.llm_output:
                model_name = response.llm_output[MODEL_NAME]

        for llmresult in flattened_llmresult:
            prompt_responses.append(llmresult.generations[0][0].text)

        df = self.pd.DataFrame( 
            {
                PROMPT : self.run_id_prompts[run_id],
                RESPONSE : prompt_responses,
            }
        )

        if TOTAL_TOKENS in token_usage_dict:
            df[PROMPT_TOKENS] = int(token_usage_dict[TOTAL_TOKENS])

        if PROMPT_TOKENS in token_usage_dict:
            df[TOTAL_TOKENS] = int(token_usage_dict[PROMPT_TOKENS])

        if COMPLETION_TOKENS in token_usage_dict:
            df[COMPLETION_TOKENS] = token_usage_dict[COMPLETION_TOKENS]

        df[MODEL_NAME] = model_name
        df[RUN_ID] = str(run_id)
        df[DURATION] = run_duration

        self.fiddler_client.publish_events_batch(self.project, self.model, df)


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)

        
ASTRA_DB_SECURE_BUNDLE_PATH = 'datastax_auth/secure-connect-fiddlerai.zip'
ASTRA_DB_KEYSPACE = 'fiddlerai'
ASTRA_DB_TABLE_NAME = 'fiddler_doc_snippets_openai'
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
ASTRA_DB_APPLICATION_TOKEN = os.environ.get('ASTRA_DB_APPLICATION_TOKEN')

# models
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"


MEMORY = 'memory'
QA = "qa"
ANSWER = 'answer'
COL_RANGE = 'A:F'
THUMB_UP = "thumbs_up_button"
THUMB_DOWN = "thumbs_down_button"
WHATEVER = "neutral"
COMMENT = "comment"
UUID = 'uuid'
SESSION_ID = 'session_id'
DB_CONN = 'db_conn'

template = """You are a tool called Fiddler Chatbot. 
Your purpose is to use the below documentation from the company Fiddler to answer the subsequent documentation questions.
Also, if possible, give the reference URLs according to the following instructions. 
The way to create the URLs is: add "https://docs.fiddler.ai/docs/" before the "slug" value of the document. 
For any URL references that start with "doc:" or "ref:" 
use its value to create a URL by adding "https://docs.fiddler.ai/docs/" before that value.
For reference URLs about release notes add "https://docs.fiddler.ai/changelog/" before the "slug" value of the document. 
For any URLs found immediately after "BlogLink:" just provide that URL in the output.
Do not use page titles to create urls. 
Note that if a user asks about uploading events, it means the same as publishing events.
If the answer cannot be found in the documentation, write "I could not find an answer.
Join our [Slack community](https://www.fiddler.ai/slackinvite) for further clarifications." Do not make up an answer
or give an answer that does not exist in the provided context.

{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

#Connect to DataStax Cassandra
cloud_config= {
  "secure_connect_bundle": ASTRA_DB_SECURE_BUNDLE_PATH
}

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)



non_stream_llm = ChatOpenAI(model_name=GPT_MODEL, temperature=0)
memory = ConversationSummaryBufferMemory(llm=non_stream_llm, memory_key="chat_history", return_messages=True, max_tokens_limit=50, output_key='answer')
question_generator = LLMChain(llm=non_stream_llm, prompt=CONDENSE_QUESTION_PROMPT)


if THUMB_DOWN not in st.session_state:
    st.session_state[THUMB_DOWN] = None

if THUMB_UP not in st.session_state:
    st.session_state[THUMB_UP] = None

if WHATEVER not in st.session_state:
    st.session_state[WHATEVER] = None

if MEMORY not in st.session_state:
    st.session_state[MEMORY] = memory

if COMMENT not in st.session_state:
    st.session_state[COMMENT] = ""

if ANSWER not in st.session_state:
    st.session_state[ANSWER] = None
    
if UUID not in st.session_state:
    st.session_state[UUID] = None
    
if SESSION_ID not in st.session_state:
    st.session_state[SESSION_ID] = None

if DB_CONN not in st.session_state:
    st.session_state[DB_CONN] = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state[DB_CONN] or st.session_state[DB_CONN] is None:
    auth_provider=PlainTextAuthProvider("token", ASTRA_DB_APPLICATION_TOKEN)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    st.session_state[DB_CONN] = cluster.connect()
    
docsearch_preexisting = Cassandra(
    embedding=embeddings,
    session=st.session_state[DB_CONN],
    keyspace=ASTRA_DB_KEYSPACE,
    table_name=ASTRA_DB_TABLE_NAME,
)
    
def get_embeddings(text: str):
    
    
    # Define the maximum length you want
    max_length = 8192  # This is the longest length of text that OpenAI can produce embeddings for.

    # Truncate the string
    if len(text) > max_length:
        text = text[:max_length]
    
    response = client.embeddings.create(input=[text], model=EMBEDDING_MODEL)
    return response.data[0].embedding


def store_query(
        query: str,
        response: str,
        source_docs: list
        ):
    
    sd = ''
    st.session_state[UUID] = uuid_g.uuid4()
    for document in source_docs:
        for key in document:
            value = document.page_content
            sd = sd + "  Document:  " + value

    sd = sd.replace("'","''")
    
    astraSession = st.session_state[DB_CONN]
    astraSession.execute(
                "INSERT INTO fiddlerai.fiddler_chatbot_history \
                (row_id, session_id, question, question_vector, source_docs, source_docs_vector, response, response_vector, ts) \
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s, toTimestamp(now())) " ,
                [str(st.session_state[UUID]), str(st.session_state[SESSION_ID]), query.replace("'","''"), get_embeddings(query), sd, \
                 get_embeddings(sd), response.replace("'","''"), get_embeddings(response)]
    )
    return
    
    
def store_feedback(uuid, feedback=-1):

    astraSession = st.session_state[DB_CONN]
    astraSession.execute(
                f"UPDATE fiddlerai.fiddler_chatbot_history SET feedback = {feedback} WHERE row_id = '{uuid}'"
    )
    return


def store_comment(uuid):

    comment = str(st.session_state[COMMENT]).replace("'","''")
    astraSession = st.session_state[DB_CONN]
    astraSession.execute(
                f"UPDATE fiddlerai.fiddler_chatbot_history SET comment = '{comment}' WHERE row_id = '{uuid}'"
    )
    st.session_state[COMMENT] = ""
    return


def erase_history():
    st.session_state[MEMORY].clear()
    st.session_state.messages = []
    st.session_state[ANSWER] = None
    st.session_state[COMMENT] = ""
    st.session_state[UUID] = None
    st.session_state[SESSION_ID] = None


def main():
    text=''
    # st.image('images/poweredby.jpg', width=550)
    st.title("Fiddler Chatbot")
    if not st.session_state[UUID] or st.session_state[UUID] is None:
        st.session_state[UUID] = uuid_g.uuid4()
    
    if not st.session_state[SESSION_ID] or st.session_state[SESSION_ID] is None:
        st.session_state[SESSION_ID] = uuid_g.uuid4()
    
    if st.session_state.messages:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask your questions about Fiddler platform here."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="images/logo.png"):
            callback = StreamHandler(st.empty())
            fiddler_handler = FiddlerCallbackHandler(url=URL, org=ORG_NAME,  project='docs_chatbot', model = 'chat', API_KEY=FIDDLER_API_TOKEN)
            llm = ChatOpenAI(model_name=GPT_MODEL, streaming=True, callbacks=[callback, fiddler_handler], temperature=0)
            doc_chain = load_qa_chain(llm, chain_type="stuff", prompt=QA_CHAIN_PROMPT)

            qa = ConversationalRetrievalChain(combine_docs_chain=doc_chain,
                                              question_generator=question_generator,
                                              retriever=docsearch_preexisting.as_retriever(search_kwargs={'k': 5}),
                                              memory=st.session_state[MEMORY], max_tokens_limit=4000,return_source_documents=True)

            full_response = qa(prompt)
            

        st.session_state.messages.append({"role": "assistant", "content": full_response["answer"]})
        #text = str(full_response["source_documents"])
        st.session_state[ANSWER] = full_response["answer"]
        store_query(full_response["question"], full_response["answer"], full_response["source_documents"])

    if st.session_state[ANSWER] is not None:
        
        # Display thumbs up and thumbs down buttons
        col1, col2, col3, col4 = st.columns([0.5, 0.5, 0.5, 4.5])
        with col1:
            if not st.session_state[THUMB_UP] or st.session_state[THUMB_UP] is None:
                st.button("👍", key="thumbs_up_button", on_click=store_feedback, kwargs={'uuid': st.session_state[UUID], 'feedback': 1})
        with col2:
            if not st.session_state[THUMB_DOWN] or st.session_state[THUMB_DOWN] is None:
                st.button("👎", key="thumbs_down_button", on_click=store_feedback, kwargs={'uuid': st.session_state[UUID], 'feedback': 0})
        with col3:
            if not st.session_state[WHATEVER] or st.session_state[WHATEVER] is None:
                st.button("🤷", key="neutral", on_click=store_feedback, kwargs={'uuid': st.session_state[UUID]})
        with col4:
            st.button("Reset Chat History", on_click=erase_history)
        
        with st.expander("Click here to leave your feedback on the chatbot response"):
            st.text_input("Leave your comments here.", key="comment", on_change=store_comment, kwargs={'uuid': st.session_state[UUID]}, value="")
            
        hide = """
        <style>
            ul.streamlit-expander {
                border: 0 !important;
        </style>
        """

        st.markdown(hide, unsafe_allow_html=True)

if __name__ == "__main__":
    main()



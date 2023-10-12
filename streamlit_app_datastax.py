import streamlit as st
import os
import openai
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


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)

        
ASTRA_DB_SECURE_BUNDLE_PATH = 'datastax_auth/secure-connect-fiddlerai.zip'
ASTRA_DB_TOKEN_JSON_PATH = 'datastax_auth/danny@fiddler.ai-token.json'
ASTRA_DB_KEYSPACE = 'fiddlerai'
ASTRA_DB_TABLE_NAME = 'fiddler_doc_snippets_openai'
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# models
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"

template = """You are a tool called Fiddler Chatbot. 
Your purpose is to use the below documentation from the company Fiddler to answer the subsequent documentation questions.
Also, if possible, give the reference URLs according to the following instructions. 
The way to create the URLs is: add "https://docs.fiddler.ai/docs/" before the "slug" value of the document. 
For any URL references that start with "doc:" or "ref:" 
use its value to create a URL by adding "https://docs.fiddler.ai/docs/" before that value.
For reference URLs about release notes add "https://docs.fiddler.ai/changelog/" before the "slug" value of the document. 
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

with open(ASTRA_DB_TOKEN_JSON_PATH) as f:
    secrets = json.load(f)
ASTRA_DB_APPLICATION_TOKEN = secrets["token"] # token is pulled from your token json file

auth_provider=PlainTextAuthProvider("token", ASTRA_DB_APPLICATION_TOKEN)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
astraSession = cluster.connect()

#index_name = "fiddlerchat"
#pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment="gcp-starter")
#index = pinecone.Index(index_name)

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
#docsearch = Pinecone.from_existing_index(index_name, embeddings)


docsearch_preexisting = Cassandra(
    embedding=embeddings,
    session=astraSession,
    keyspace=ASTRA_DB_KEYSPACE,
    table_name=ASTRA_DB_TABLE_NAME,
)


non_stream_llm = ChatOpenAI(model_name=GPT_MODEL, temperature=0)
memory = ConversationSummaryBufferMemory(llm=non_stream_llm, memory_key="chat_history", return_messages=True, max_tokens_limit=50, output_key='answer')
question_generator = LLMChain(llm=non_stream_llm, prompt=CONDENSE_QUESTION_PROMPT)

openai.api_key = os.environ.get('OPENAI_API_KEY')
MEMORY = 'memory'
QA = "qa"
ANSWER = 'answer'
COL_RANGE = 'A:F'
THUMB_UP = "thumbs_up_button"
THUMB_DOWN = "thumbs_down_button"
WHATEVER = "neutral"
COMMENT = "comment"
UUID = 'uuid'


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

if "messages" not in st.session_state:
    st.session_state.messages = []

    
def get_embeddings(text: str):
    
    response = openai.Embedding.create(model=EMBEDDING_MODEL, input=text)
    return response["data"][0]["embedding"]


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
    
    astraSession.execute(
                "INSERT INTO fiddlerai.fiddler_chatbot_history \
                (row_id, question, question_vector, source_docs, source_docs_vector, response, response_vector, ts) \
                VALUES (%s,%s,%s,%s,%s,%s,%s, toTimestamp(now())) " ,
                [str(st.session_state[UUID]), query.replace("'","''"), get_embeddings(query), sd, get_embeddings(sd), response.replace("'","''"), get_embeddings(response)]
    )
    return
    
    
def store_feedback(uuid, feedback=-1):

    astraSession.execute(
                f"UPDATE fiddlerai.fiddler_chatbot_history SET feedback = {feedback} WHERE row_id = '{uuid}'"
    )
    return


def store_comment(uuid):

    comment = str(st.session_state[COMMENT]).replace("'","''")
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


def main():
    text=''
    # st.image('images/poweredby.jpg', width=550)
    st.title("Fiddler Chatbot")
    if not st.session_state[UUID] or st.session_state[UUID] is None:
        st.session_state[UUID] = uuid_g.uuid4()
    
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
            llm = ChatOpenAI(model_name=GPT_MODEL, streaming=True, callbacks=[callback],
                             temperature=0)
            doc_chain = load_qa_chain(llm, chain_type="stuff", prompt=QA_CHAIN_PROMPT)

            qa = ConversationalRetrievalChain(combine_docs_chain=doc_chain,
                                              question_generator=question_generator,
                                              retriever=docsearch_preexisting.as_retriever(search_kwargs={'k': 5}),
                                              memory=st.session_state[MEMORY], max_tokens_limit=4000,return_source_documents=True)

            full_response = qa(prompt)
            

        st.session_state.messages.append({"role": "assistant", "content": full_response["answer"]})
        text = str(full_response["source_documents"])
        st.session_state[ANSWER] = full_response["answer"]
        store_query(full_response["question"], full_response["answer"], full_response["source_documents"])

    if st.session_state[ANSWER] is not None:
        st.button("Reset Chat History", on_click=erase_history)
        st.text_input("Any comments on the bot response?", key="comment", on_change=store_comment, kwargs={'uuid': st.session_state[UUID]}, value="")
        # Display thumbs up and thumbs down buttons
        col1, col2, col3 = st.columns([0.5, 0.5, 5])
        with col1:
            if not st.session_state[THUMB_UP] or st.session_state[THUMB_UP] is None:
                st.button("👍", key="thumbs_up_button", on_click=store_feedback, kwargs={'uuid': st.session_state[UUID], 'feedback': 1})
        with col2:
            if not st.session_state[THUMB_DOWN] or st.session_state[THUMB_DOWN] is None:
                st.button("👎", key="thumbs_down_button", on_click=store_feedback, kwargs={'uuid': st.session_state[UUID], 'feedback': 0})
        with col3:
            if not st.session_state[WHATEVER] or st.session_state[WHATEVER] is None:
                st.button("🤷", key="neutral", on_click=store_feedback, kwargs={'uuid': st.session_state[UUID]})
            # User input
            
    st.markdown(text)

if __name__ == "__main__":
    main()



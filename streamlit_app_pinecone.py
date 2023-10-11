import streamlit as st
import os
import openai
import gspread
from google.oauth2 import service_account
import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
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

index_name = "fiddlerchat"
pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment="gcp-starter")
index = pinecone.Index(index_name)
embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
docsearch = Pinecone.from_existing_index(index_name, embeddings)


non_stream_llm = ChatOpenAI(model_name=GPT_MODEL, temperature=0)
memory = ConversationSummaryBufferMemory(llm=non_stream_llm,
                                         memory_key="chat_history", return_messages=True, max_tokens_limit=50)
question_generator = LLMChain(llm=non_stream_llm, prompt=CONDENSE_QUESTION_PROMPT)



# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"
    ],
)

client = gspread.authorize(credentials)
openai.api_key = os.environ.get('OPENAI_API_KEY')
MEMORY = 'memory'
QA = "qa"
ANSWER = 'answer'
COL_RANGE = 'A:F'
THUMB_UP = "thumbs_up_button"
THUMB_DOWN = "thumbs_down_button"
WHATEVER = "neutral"
COMMENT = "comment"


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

if "messages" not in st.session_state:
    st.session_state.messages = []


def store_query(
        query: str,
        response: str,
        ):

    sheet_url = st.secrets["private_gsheets_url"]  # this information should be included in streamlit secret
    sheet = client.open_by_url(sheet_url).get_worksheet(4)
    sheet.append_row([query, response, '', ''], table_range=COL_RANGE)
    return


def store_feedback(feedback=-1):

    sheet_url = st.secrets["private_gsheets_url"]  # this information should be included in streamlit secret
    sheet = client.open_by_url(sheet_url).get_worksheet(4)
    q_list = sheet.col_values(2)
    rows = len(q_list)
    if q_list[rows-1] == st.session_state[ANSWER]:
        sheet.update(f'C{rows}', feedback)
    return

def store_comment():

    sheet_url = st.secrets["private_gsheets_url"]  # this information should be included in streamlit secret
    sheet = client.open_by_url(sheet_url).get_worksheet(4)
    q_list = sheet.col_values(2)
    rows = len(q_list)
    if q_list[rows-1] == st.session_state[ANSWER]:
        sheet.update(f'D{rows}', st.session_state[COMMENT])
    st.session_state[COMMENT] = ""
    return


def erase_history():
    st.session_state[MEMORY].clear()
    st.session_state.messages = []
    st.session_state[ANSWER] = None


def main():
    # st.image('poweredby.jpg', width=550)
    st.title("Fiddler Chatbot")

    if st.session_state.messages:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask your questions about Fiddler platform here."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="logo.png"):
            callback = StreamHandler(st.empty())
            llm = ChatOpenAI(model_name=GPT_MODEL, streaming=True, callbacks=[callback],
                             temperature=0)
            doc_chain = load_qa_chain(llm, chain_type="stuff", prompt=QA_CHAIN_PROMPT)

            qa = ConversationalRetrievalChain(combine_docs_chain=doc_chain,
                                              question_generator=question_generator,
                                              retriever=docsearch.as_retriever(search_kwargs={'k': 5}),
                                              memory=st.session_state[MEMORY], max_tokens_limit=4000)

            full_response = qa(prompt)
        st.session_state.messages.append({"role": "assistant", "content": full_response["answer"]})
        st.session_state[ANSWER] = full_response["answer"]
        store_query(full_response["question"], full_response["answer"])

    if st.session_state[ANSWER] is not None:
        st.button("Reset Chat History", on_click=erase_history)
        st.text_input("Any comments on the bot response?", key="comment", on_change=store_comment, value="")
        # Display thumbs up and thumbs down buttons
        col1, col2, col3 = st.columns([0.5, 0.5, 5])
        with col1:
            if not st.session_state[THUMB_UP] or st.session_state[THUMB_UP] is None:
                st.button("👍", key="thumbs_up_button", on_click=store_feedback, kwargs={'feedback': 1})
        with col2:
            if not st.session_state[THUMB_DOWN] or st.session_state[THUMB_DOWN] is None:
                st.button("👎", key="thumbs_down_button", on_click=store_feedback, kwargs={'feedback': 0})
        with col3:
            if not st.session_state[WHATEVER] or st.session_state[WHATEVER] is None:
                st.button("🤷", key="neutral", on_click=store_feedback)
            # User input


if __name__ == "__main__":
    main()



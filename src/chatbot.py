"""
# Fiddler Chatbot - A Streamlit app for RAG-based Q&A using Fiddler documentation.

- Streamlit for the web UI
- LangChain as the orchestration framework
- OpenAI's GPT-4-turbo for language understanding and generation
- DataStax Cassandra as the vector database
- Fiddler AI Platform for monitoring and guardrails

## Key Architectural Patterns

1. Safety-First Design: Every query goes through a jailbreak detection system before processing
2. Streaming Responses: Real-time token streaming for better user experience
3. Conversational Memory: Maintains context across the entire session
4. Dual Persistence: Both Cassandra and Fiddler platform store interaction data
5. Feedback Loop: Built-in user feedback collection system


## Features

1. Guardrail System
   - Pre-flight safety checks (jailbreak detection)
   - Post-generation faithfulness validation
   - Visual indicators for scores

2. Comprehensive Monitoring
   - Every interaction tracked with unique IDs
   - Token counting and latency measurement
   - Integration with Fiddler's ML monitoring platform

"""

import os
import time
import uuid as uuid_g
import pandas as pd
import streamlit as st
import fiddler as fdl
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts import PromptTemplate
from langchain.vectorstores.cassandra import Cassandra
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from openai import OpenAI
from streamlit.logger import get_logger

from agentic_tools.fiddler_gaurdrails import get_safety_guardrail_results, get_faithfulness_guardrail_results

from config import CONFIG_CHATBOT_OLD as config

FIDDLER_CHATBOT_PROJECT_NAME = config["PROJECT_NAME"]
FIDDLER_CHATBOT_MODEL_NAME   = config["MODEL_NAME"]
FIDDLER_URL                  = config["FIDDLER_URL"]

ASTRA_DB_SECURE_BUNDLE_PATH = config["ASTRA_DB_SECURE_BUNDLE_PATH"]
ASTRA_DB_KEYSPACE           = config["ASTRA_DB_KEYSPACE"]
ASTRA_DB_TABLE_NAME         = config["ASTRA_DB_TABLE_NAME"]
ASTRA_DB_LEDGER_TABLE_NAME  = config["ASTRA_DB_LEDGER_TABLE_NAME"]

EMBEDDING_MODEL = config["OPENAI_EMBEDDING_MODEL"]
LLM_MODEL       = config["OPENAI_LLM_MODEL"]

# Chat instance Global state inits # todo - this is not the best pattern , to use global vars for state management as such
CHAT_INSTANCE__PROMPT = "prompt"
CHAT_INSTANCE__RESPONSE = "response"
CHAT_INSTANCE__SESSION_ID = "session_id"
CHAT_INSTANCE__ROW_ID = "row_id"
CHAT_INSTANCE__RUN_ID = "run_id"
CHAT_INSTANCE__SOURCE_DOC0 = "source_doc0"
CHAT_INSTANCE__SOURCE_DOC1 = "source_doc1"
CHAT_INSTANCE__SOURCE_DOC2 = "source_doc2"
CHAT_INSTANCE__COMMENT = "comment"
CHAT_INSTANCE__FEEDBACK = "feedback"
CHAT_INSTANCE__FEEDBACK2 = "feedback2"
CHAT_INSTANCE__PROMPT_TOKENS = "prompt_tokens"
CHAT_INSTANCE__TOTAL_TOKENS = "total_tokens"
CHAT_INSTANCE__COMPLETION_TOKENS = "completion_tokens"
CHAT_INSTANCE__DURATION = "duration"
CHAT_INSTANCE__MODEL_NAME = "model_name"

# Chat instance Global state inits # todo - this is not the best pattern , to use global vars for state management as such
CHAT_INSTANCE__MEMORY = "memory"
CHAT_INSTANCE__QA = "qa"
CHAT_INSTANCE__ANSWER = "answer"
CHAT_INSTANCE__THUMB_UP = "thumbs_up_button"
CHAT_INSTANCE__THUMB_DOWN = "thumbs_down_button"
CHAT_INSTANCE__COMMENT = "comment"
CHAT_INSTANCE__UUID = "uuid"
CHAT_INSTANCE__SESSION_ID = "session_id"
CHAT_INSTANCE__DB_CONN = "db_conn"

# Read the system instructions template
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up 2 levels from src/chatbot.py to project root ./
with open(os.path.join(PROJECT_ROOT, "src", "system_instructions_LEGACY.md"), "r") as f:
    TEMPLATE = f.read().strip()

QA_CHAIN_PROMPT = PromptTemplate.from_template(TEMPLATE)


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY environment variable is required")
client = OpenAI(api_key=OPENAI_API_KEY)

logger = get_logger(__name__)

FIDDLER_API_KEY            = os.environ.get( "FIDDLER_API_KEY"          )
OPENAI_API_KEY             = os.environ.get( "OPENAI_API_KEY"             )
ASTRA_DB_APPLICATION_TOKEN = os.environ.get( "ASTRA_DB_APPLICATION_TOKEN" )

# Connect to DataStax Cassandra
cloud_config = {"secure_connect_bundle": ASTRA_DB_SECURE_BUNDLE_PATH}

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, dimensions=1536)

non_stream_llm = ChatOpenAI(model=LLM_MODEL, temperature=0)
memory = ConversationSummaryBufferMemory(
    llm=non_stream_llm,
    memory_key="chat_history",
    return_messages=True,
    max_token_limit=50,
    output_key="answer",
)
question_generator = LLMChain(llm=non_stream_llm, prompt=CONDENSE_QUESTION_PROMPT)


if CHAT_INSTANCE__THUMB_DOWN not in st.session_state:
    st.session_state[CHAT_INSTANCE__THUMB_DOWN] = None

if CHAT_INSTANCE__THUMB_UP not in st.session_state:
    st.session_state[CHAT_INSTANCE__THUMB_UP] = None

if CHAT_INSTANCE__MEMORY not in st.session_state:
    st.session_state[CHAT_INSTANCE__MEMORY] = memory

if CHAT_INSTANCE__COMMENT not in st.session_state:
    st.session_state[CHAT_INSTANCE__COMMENT] = ""

if CHAT_INSTANCE__ANSWER not in st.session_state:
    st.session_state[CHAT_INSTANCE__ANSWER] = None

if CHAT_INSTANCE__UUID not in st.session_state:
    st.session_state[CHAT_INSTANCE__UUID] = None

if CHAT_INSTANCE__SESSION_ID not in st.session_state:
    st.session_state[CHAT_INSTANCE__SESSION_ID] = None

if CHAT_INSTANCE__DB_CONN not in st.session_state:
    st.session_state[CHAT_INSTANCE__DB_CONN] = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state[CHAT_INSTANCE__DB_CONN] or st.session_state[CHAT_INSTANCE__DB_CONN] is None:
    if ASTRA_DB_APPLICATION_TOKEN is None:
        raise ValueError("ASTRA_DB_APPLICATION_TOKEN environment variable is required")
    auth_provider = PlainTextAuthProvider("token", ASTRA_DB_APPLICATION_TOKEN)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    st.session_state[CHAT_INSTANCE__DB_CONN] = cluster.connect()


class StreamHandler(BaseCallbackHandler):
    """Callback handler for streaming LLM responses."""

    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)


docsearch_preexisting = Cassandra(
    embedding=embeddings,
    session=st.session_state[CHAT_INSTANCE__DB_CONN],
    keyspace=ASTRA_DB_KEYSPACE,
    table_name=ASTRA_DB_TABLE_NAME,
    )

def publish_and_store(
    query: str,
    response: str,
    source_docs: list,
    duration: float,
    ):
    """Publishes the RAG trace to Fiddler and stores it in the database."""
    # Break out the source docs into a list
    source_docs_list = []
    for document in source_docs:
        source_docs_list.append(document.page_content)

    # Capture the values for storage and publication
    st.session_state[CHAT_INSTANCE__UUID] = uuid_g.uuid4()
    row_id = str(st.session_state[CHAT_INSTANCE__UUID])
    run_id = str(st.session_state[CHAT_INSTANCE__UUID])
    session_id = str(st.session_state[CHAT_INSTANCE__SESSION_ID])
    model_name = LLM_MODEL
    prompt = query.replace("'", "''")
    response = response.replace("'", "''")
    source_doc0 = source_docs_list[0].replace("'", "''")
    source_doc1 = source_docs_list[1].replace("'", "''")
    source_doc2 = source_docs_list[2].replace("'", "''")
    prompt_tokens = len(prompt.split())
    completion_tokens = len(response.split())
    total_tokens = prompt_tokens + completion_tokens

    # Create the trace/event dict
    trace_dict = {
        CHAT_INSTANCE__PROMPT: prompt,
        CHAT_INSTANCE__RESPONSE: response,
        CHAT_INSTANCE__SESSION_ID: session_id,
        CHAT_INSTANCE__ROW_ID: row_id,
        CHAT_INSTANCE__RUN_ID: run_id,
        CHAT_INSTANCE__SOURCE_DOC0: source_doc0,
        CHAT_INSTANCE__SOURCE_DOC1: source_doc1,
        CHAT_INSTANCE__SOURCE_DOC2: source_doc2,
        CHAT_INSTANCE__PROMPT_TOKENS: prompt_tokens,
        CHAT_INSTANCE__TOTAL_TOKENS: total_tokens,
        CHAT_INSTANCE__COMPLETION_TOKENS: completion_tokens,
        CHAT_INSTANCE__DURATION: duration,
        CHAT_INSTANCE__MODEL_NAME: model_name,
        }

    # Sore the trace/event to DataStax
    astra_session = st.session_state[CHAT_INSTANCE__DB_CONN]
    astra_session.execute(
        "INSERT INTO fiddlerai.fiddler_chatbot_ledger \
        (row_id, run_id, session_id, prompt, source_doc0, source_doc1, source_doc2, response, model_name, duration, prompt_tokens, completion_tokens, total_tokens, ts) \
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,toTimestamp(now())) ",
        [
            row_id,
            run_id,
            session_id,
            prompt,
            source_doc0,
            source_doc1,
            source_doc2,
            response,
            model_name,
            duration,
            prompt_tokens,
            completion_tokens,
            total_tokens,
            ],
        )

    trace_df = pd.DataFrame([trace_dict])
    trace_df["ts"] = pd.Timestamp.today()

    # get Fiddler client
    if FIDDLER_API_KEY is None:
        raise ValueError("FIDDLER_API_KEY environment variable is required")
    fdl.init(url=FIDDLER_URL, token=FIDDLER_API_KEY)

    # Publish the trace/event to Fiddler
    project = fdl.Project.from_name(name=FIDDLER_CHATBOT_PROJECT_NAME)
    if project.id is None:
        raise ValueError(f"Could not find project {FIDDLER_CHATBOT_PROJECT_NAME}")
    model = fdl.Model.from_name(name=FIDDLER_CHATBOT_MODEL_NAME, project_id=project.id)

    model.event_ts_col = "ts"
    model.event_id_col = "row_id"

    model.publish(trace_df)
    return


def store_feedback(uuid, feedback=-1):
    """Stores user feedback (like/dislike) in the database."""
    feedback2 = ""
    if feedback == 1:
        feedback2 = "like"
    elif feedback == 0:
        feedback2 = "dislike"

    astra_session = st.session_state[CHAT_INSTANCE__DB_CONN]
    astra_session.execute(
        "UPDATE fiddlerai.fiddler_chatbot_ledger "
        f"SET feedback = {feedback}, feedback2 = '{feedback2}' "
        f"WHERE row_id = '{uuid}'"
        )
    return


def store_comment(uuid):
    """Stores user comments in the database."""
    comment = str(st.session_state[CHAT_INSTANCE__COMMENT]).replace("'", "''")
    astra_session = st.session_state[CHAT_INSTANCE__DB_CONN]
    astra_session.execute(
        "UPDATE fiddlerai.fiddler_chatbot_ledger "
        f"SET comment = '{comment}' "
        f"WHERE row_id = '{uuid}'"
    )
    st.session_state[CHAT_INSTANCE__COMMENT] = ""
    return


def erase_history():
    """Clears the chat history and resets the session."""
    st.session_state[CHAT_INSTANCE__MEMORY].clear()
    st.session_state.messages = []
    st.session_state[CHAT_INSTANCE__ANSWER] = None
    st.session_state[CHAT_INSTANCE__COMMENT] = ""
    st.session_state[CHAT_INSTANCE__UUID] = None
    st.session_state[CHAT_INSTANCE__SESSION_ID] = None


def main():
    """Main function to run the Streamlit chatbot application."""
    st.image('public/poweredby.jpg', width=550)
    st.title("Fiddler AI Assistant")
    if not st.session_state[CHAT_INSTANCE__UUID] or st.session_state[CHAT_INSTANCE__UUID] is None:
        st.session_state[CHAT_INSTANCE__UUID] = uuid_g.uuid4()

    if not st.session_state[CHAT_INSTANCE__SESSION_ID] or st.session_state[CHAT_INSTANCE__SESSION_ID] is None:
        st.session_state[CHAT_INSTANCE__SESSION_ID] = uuid_g.uuid4()

    if st.session_state.messages:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    if prompt := st.chat_input("Ask your questions about Fiddler platform here."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        JAILBREAK_SCORE, SAFETY_GUARDRAIL_LATENCY = get_safety_guardrail_results(prompt)
        if JAILBREAK_SCORE > 0.5:
            old_prompt = prompt
            prompt = "Rejected"

        with st.chat_message("assistant", avatar="public/logo.png"):
            callback = StreamHandler(st.empty())
            llm = ChatOpenAI(
                model=LLM_MODEL, streaming=True, callbacks=[callback], temperature=0
            )
            doc_chain = load_qa_chain(llm, chain_type="stuff", prompt=QA_CHAIN_PROMPT)

            start_time = time.time()
            qa = ConversationalRetrievalChain(
                combine_docs_chain=doc_chain,
                question_generator=question_generator,
                retriever=docsearch_preexisting.as_retriever(search_kwargs={"k": config["TOP_K_RETRIEVAL"]}),
                memory=st.session_state[CHAT_INSTANCE__MEMORY],
                max_tokens_limit=8000,
                return_source_documents=True,
            )
            full_response = qa(prompt)
            end_time = time.time()

        st.session_state.messages.append( {"role": "assistant", "content": full_response["answer"] })
        st.session_state[CHAT_INSTANCE__ANSWER] = full_response["answer"]
        logger.info(st.session_state[CHAT_INSTANCE__ANSWER])
        if JAILBREAK_SCORE > 0.5:
            FAITHFULNESS_SCORE = 0.0
            publish_and_store(
                old_prompt,
                full_response["answer"],
                full_response["source_documents"],
                (end_time - start_time),
            )
        else:
            FAITHFULNESS_SCORE, faithfulness_guardrail_latency = (
                get_faithfulness_guardrail_results(
                    full_response["answer"],
                    full_response["source_documents"],
                )
            )
            publish_and_store(
                full_response["question"],
                full_response["answer"],
                full_response["source_documents"],
                (end_time - start_time),
            )

    if st.session_state[CHAT_INSTANCE__ANSWER] is not None and st.session_state[CHAT_INSTANCE__THUMB_UP] is None and st.session_state[CHAT_INSTANCE__THUMB_DOWN] is None:
        # Display thumbs up and thumbs down buttons

        col1, col2, col3 = st.columns([3.5, 3.5, 3.5])
        with col1:
            output_str = f"Answer Faithfulness:  {FAITHFULNESS_SCORE:.3f}"
            if FAITHFULNESS_SCORE < 0.5:
                st.markdown(f""":red-background[{output_str}]""")
            else:
                st.markdown(f""":green-background[{output_str}]""")
        with col2:
            output_str = f"Jailbreak Likelihood:  {JAILBREAK_SCORE:.3f}"
            if JAILBREAK_SCORE > 0.5:
                st.markdown(f""":red-background[{output_str}]""")
            else:
                st.markdown(f""":green-background[{output_str}]""")
        with col3:
            output_str = f"Guardrails Latency:  {SAFETY_GUARDRAIL_LATENCY * 1000:.1f} ms"
            st.markdown(f""":green-background[{output_str}]""")

        hide = """
        <style>
            ul.streamlit-expander {
                border: 0 !important;
        </style>
        """
        st.markdown(hide, unsafe_allow_html=True)

    if st.session_state[CHAT_INSTANCE__ANSWER] is not None:
        # Display thumbs up and thumbs down buttons
        col1, col2, col3 = st.columns([0.5, 0.5, 3.0])
        with col1:
            if not st.session_state[CHAT_INSTANCE__THUMB_UP] or st.session_state[CHAT_INSTANCE__THUMB_UP] is None:
                st.button(
                    "👍",
                    key="thumbs_up_button",
                    on_click=store_feedback,
                    kwargs={"uuid": st.session_state[CHAT_INSTANCE__UUID], "feedback": 1},
                    )
        with col2:
            if not st.session_state[CHAT_INSTANCE__THUMB_DOWN] or st.session_state[CHAT_INSTANCE__THUMB_DOWN] is None:
                st.button(
                    "👎",
                    key="thumbs_down_button",
                    on_click=store_feedback,
                    kwargs={"uuid": st.session_state[CHAT_INSTANCE__UUID], "feedback": 0},
                    )
        with col3:
            st.button("Reset Chat History", on_click=erase_history)

        with st.expander("Click here to leave your feedback on the chatbot response"):
            st.text_input(
                "Leave your comments here.",
                key="comment",
                on_change=store_comment,
                kwargs={"uuid": st.session_state[CHAT_INSTANCE__UUID]},
                value="",
            )
        hide = """
        <style>
            ul.streamlit-expander {
                border: 0 !important;
        </style>
        """
        st.markdown(hide, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

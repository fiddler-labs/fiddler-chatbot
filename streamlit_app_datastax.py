"""Fiddler Chatbot - A Streamlit app for RAG-based Q&A using Fiddler documentation."""

# Standard library imports
import json
import os
import time
import uuid as uuid_g

# Third-party imports
import fiddler as fdl  # type: ignore
import pandas as pd  # type: ignore
import requests  # type: ignore
import streamlit as st
from cassandra.auth import PlainTextAuthProvider  # type: ignore
from cassandra.cluster import Cluster  # type: ignore
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

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

logger = get_logger(__name__)

FIDDLER_CHATBOT_PROJECT_NAME = "fiddler_chatbot_v3"
FIDDLER_CHATBOT_MODEL_NAME = "fiddler_rag_chatbot"
FIDDLER_URL = "https://demo.fiddler.ai"
FIDDLER_ORG_NAME = "demo"
FIDDLER_API_TOKEN = os.environ.get("FIDDLER_API_TOKEN")

ASTRA_DB_SECURE_BUNDLE_PATH = "datastax_auth/secure-connect-fiddlerai.zip"
ASTRA_DB_KEYSPACE = "fiddlerai"
ASTRA_DB_TABLE_NAME = "fiddler_doc_snippets_openai"
ASTRA_DB_LEDGER_TABLE_NAME = "fiddler_chatbot_ledger"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")

# models
EMBEDDING_MODEL = "text-embedding-3-large"
LLM_MODEL = "gpt-4-turbo"

MEMORY = "memory"
QA = "qa"
ANSWER = "answer"
COL_RANGE = "A:F"
THUMB_UP = "thumbs_up_button"
THUMB_DOWN = "thumbs_down_button"

COMMENT = "comment"
UUID = "uuid"
SESSION_ID = "session_id"
DB_CONN = "db_conn"

FAITHFULNESS_SCORE = 0.0
JAILBREAK_SCORE = 0.0
SAFETY_GUARDRAIL_LATENCY = 0.0
REQUESTS_TIMEOUT = 30

FDL_PROMPT = "prompt"
FDL_RESPONSE = "response"
FDL_SESSION_ID = "session_id"
FDL_ROW_ID = "row_id"
FDL_RUN_ID = "run_id"
FDL_SOURCE_DOC0 = "source_doc0"
FDL_SOURCE_DOC1 = "source_doc1"
FDL_SOURCE_DOC2 = "source_doc2"
FDL_COMMENT = "comment"
FDL_FEEDBACK = "feedback"
FDL_FEEDBACK2 = "feedback2"
FDL_PROMPT_TOKENS = "prompt_tokens"
FDL_TOTAL_TOKENS = "total_tokens"
FDL_COMPLETION_TOKENS = "completion_tokens"
FDL_DURATION = "duration"
FDL_MODEL_NAME = "model_name"

TEMPLATE = """You are Fiddler Chatbot, an expert assistant for Fiddler AI's product documentation.
Your task is to provide a detailed, accurate answer to the user's question based ONLY on the provided "Context" documents.
After your answer, you MUST list the sources you used in a clearly labeled "Sources:" section.

---

**Answer Generation Rules:**

1. Provide a clear, informative answer using only the provided context. Your answer should be at least 800 characters long and demonstrate thorough understanding.
2. If relevant code examples appear in the context, include 2–5 of the most helpful ones in your answer. Prefer Python client examples unless the user specifically requests REST API examples.
3. Interpret "uploading events" or "uploading data" as "publishing events" if mentioned by the user.
4. If the context does not answer the question, respond with:  
   > "I could not find an answer in the documentation. For more help, please join our [Slack community](https://www.fiddler.ai/slackinvite)."  
   **Do not generate speculative or fabricated answers.**
5. Combine insights from multiple documents into a coherent, organized answer when applicable.
6. Use **section headers**, bullet points, and code formatting to structure complex responses.
7. If the context suggests related content exists elsewhere, mention it and recommend follow-up browsing.
8. Do not mention or include information about third-party tools (e.g., Snowflake, Databricks) unless explicitly referenced by the user.

---

**Source & URL Formatting Rules:**

- Every source document referenced must be cited in a "Sources:" section at the end of the response.
- To extract source URLs:
  - Look for a line starting with `DOC_URL:` at the very beginning of each context document.
  - Remove the prefix `documentation_data/fiddler-docs/` from the DOC_URL.
  - Remove the trailing `/README.md` or `.md` suffix.
  - Prepend the remainder with `https://docs.fiddler.ai/`.

  Example:
  - Context: `DOC_URL:documentation_data/fiddler-docs/product-guide/monitoring-platform/alerts-platform.md`
  - Output: `https://docs.fiddler.ai/product-guide/monitoring-platform/alerts-platform`

  - Context: `DOC_URL:documentation_data/fiddler-docs/technical-reference/python-client-guides/model-onboarding/README.md`
  - Output: `https://docs.fiddler.ai/technical-reference/python-client-guides/model-onboarding`

- If a document begins with `BlogLink:`, extract and use the link as-is:
  - Context: `BlogLink: https://www.fiddler.ai/blog/my-post`
  - Output: `https://www.fiddler.ai/blog/my-post`

- If a chunk is missing a DOC_URL, but clearly relates to another chunk that contains one, attempt to match based on title or path if possible.

---

Context:
{context}

Question: {question}

Helpful Answer:
"""

QA_CHAIN_PROMPT = PromptTemplate.from_template(TEMPLATE)

# Connect to DataStax Cassandra
cloud_config = {"secure_connect_bundle": ASTRA_DB_SECURE_BUNDLE_PATH}

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, model_kwargs={"dimensions": 1536})

non_stream_llm = ChatOpenAI(model=LLM_MODEL, temperature=0)
memory = ConversationSummaryBufferMemory(
    llm=non_stream_llm,
    memory_key="chat_history",
    return_messages=True,
    max_token_limit=50,
    output_key="answer",
)
question_generator = LLMChain(llm=non_stream_llm, prompt=CONDENSE_QUESTION_PROMPT)


if THUMB_DOWN not in st.session_state:
    st.session_state[THUMB_DOWN] = None

if THUMB_UP not in st.session_state:
    st.session_state[THUMB_UP] = None

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
    auth_provider = PlainTextAuthProvider("token", ASTRA_DB_APPLICATION_TOKEN)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    st.session_state[DB_CONN] = cluster.connect()


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
    session=st.session_state[DB_CONN],
    keyspace=ASTRA_DB_KEYSPACE,
    table_name=ASTRA_DB_TABLE_NAME,
)


def get_faithfulness_guardrail_results(response: str, source_docs: list):
    """Calculates the faithfulness score for a response given a query and source documents."""
    url_faithfulness = "https://demo.fiddler.ai/v3/guardrails/ftl-response-faithfulness"
    token = FIDDLER_API_TOKEN

    source_docs_list = []
    for document in source_docs:
        source_docs_list.append(document.page_content)

    response = response.replace("'", "''")
    source_doc0 = source_docs_list[0].replace("'", "''")
    source_doc1 = source_docs_list[1].replace("'", "''")
    source_doc2 = source_docs_list[2].replace("'", "''")

    payload = json.dumps(
        {
            "data": {
                "response": response,
                "context": source_doc0 + source_doc1 + source_doc2,
            }
        }
    )
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    guardrail_start_time = time.time()
    guardrail_response_faithfulness = requests.request(
        "POST", url_faithfulness, headers=headers, data=payload, timeout=REQUESTS_TIMEOUT
    )
    guardrail_end_time = time.time()
    guardrail_latency = guardrail_end_time - guardrail_start_time

    response_dict = guardrail_response_faithfulness.json()
    return response_dict["fdl_faithful_score"], guardrail_latency


def get_safety_guardrail_results(query: str):
    """Calculates the safety score for a given query."""
    url_safety = "https://demo.fiddler.ai/v3/guardrails/ftl-safety"
    token = FIDDLER_API_TOKEN

    payload = json.dumps({"data": {"input": query}})
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    guardrail_start_time = time.time()
    guardrail_response_safety = requests.request(
        "POST", url_safety, headers=headers, data=payload, timeout=REQUESTS_TIMEOUT
    )
    guardrail_end_time = time.time()
    guardrail_latency = guardrail_end_time - guardrail_start_time

    response_dict = guardrail_response_safety.json()
    return response_dict["fdl_jailbreaking"], guardrail_latency


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
    st.session_state[UUID] = uuid_g.uuid4()
    row_id = str(st.session_state[UUID])
    run_id = str(st.session_state[UUID])
    session_id = str(st.session_state[SESSION_ID])
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
        FDL_PROMPT: prompt,
        FDL_RESPONSE: response,
        FDL_SESSION_ID: session_id,
        FDL_ROW_ID: row_id,
        FDL_RUN_ID: run_id,
        FDL_SOURCE_DOC0: source_doc0,
        FDL_SOURCE_DOC1: source_doc1,
        FDL_SOURCE_DOC2: source_doc2,
        FDL_PROMPT_TOKENS: prompt_tokens,
        FDL_TOTAL_TOKENS: total_tokens,
        FDL_COMPLETION_TOKENS: completion_tokens,
        FDL_DURATION: duration,
        FDL_MODEL_NAME: model_name,
    }

    # Sore the trace/event to DataStax
    astra_session = st.session_state[DB_CONN]
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
    fdl.init(url=FIDDLER_URL, token=FIDDLER_API_TOKEN)

    # Publish the trace/event to Fiddler
    project = fdl.Project.from_name(name=FIDDLER_CHATBOT_PROJECT_NAME)
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

    astra_session = st.session_state[DB_CONN]
    astra_session.execute(
        "UPDATE fiddlerai.fiddler_chatbot_ledger "
        f"SET feedback = {feedback}, feedback2 = '{feedback2}' "
        f"WHERE row_id = '{uuid}'"
    )
    return


def store_comment(uuid):
    """Stores user comments in the database."""
    comment = str(st.session_state[COMMENT]).replace("'", "''")
    astra_session = st.session_state[DB_CONN]
    astra_session.execute(
        "UPDATE fiddlerai.fiddler_chatbot_ledger "
        f"SET comment = '{comment}' "
        f"WHERE row_id = '{uuid}'"
    )
    st.session_state[COMMENT] = ""
    return


def erase_history():
    """Clears the chat history and resets the session."""
    st.session_state[MEMORY].clear()
    st.session_state.messages = []
    st.session_state[ANSWER] = None
    st.session_state[COMMENT] = ""
    st.session_state[UUID] = None
    st.session_state[SESSION_ID] = None


def main():
    """Main function to run the Streamlit chatbot application."""
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
        JAILBREAK_SCORE, SAFETY_GUARDRAIL_LATENCY = get_safety_guardrail_results(prompt)
        if JAILBREAK_SCORE > 0.5:
            old_prompt = prompt
            prompt = "Rejected"

        with st.chat_message("assistant", avatar="images/logo.png"):
            callback = StreamHandler(st.empty())
            llm = ChatOpenAI(
                model=LLM_MODEL, streaming=True, callbacks=[callback], temperature=0
            )
            doc_chain = load_qa_chain(llm, chain_type="stuff", prompt=QA_CHAIN_PROMPT)

            start_time = time.time()
            qa = ConversationalRetrievalChain(
                combine_docs_chain=doc_chain,
                question_generator=question_generator,
                retriever=docsearch_preexisting.as_retriever(search_kwargs={"k": 3}),
                memory=st.session_state[MEMORY],
                max_tokens_limit=8000,
                return_source_documents=True,
            )
            full_response = qa(prompt)
            end_time = time.time()

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response["answer"]}
        )
        st.session_state[ANSWER] = full_response["answer"]
        logger.info(st.session_state[ANSWER])
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

    if (
        st.session_state[ANSWER] is not None
        and st.session_state[THUMB_UP] is None
        and st.session_state[THUMB_DOWN] is None
    ):
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

    if st.session_state[ANSWER] is not None:
        # Display thumbs up and thumbs down buttons
        col1, col2, col3 = st.columns([0.5, 0.5, 3.0])
        with col1:
            if not st.session_state[THUMB_UP] or st.session_state[THUMB_UP] is None:
                st.button(
                    "👍",
                    key="thumbs_up_button",
                    on_click=store_feedback,
                    kwargs={"uuid": st.session_state[UUID], "feedback": 1},
                )
        with col2:
            if not st.session_state[THUMB_DOWN] or st.session_state[THUMB_DOWN] is None:
                st.button(
                    "👎",
                    key="thumbs_down_button",
                    on_click=store_feedback,
                    kwargs={"uuid": st.session_state[UUID], "feedback": 0},
                )
        with col3:
            st.button("Reset Chat History", on_click=erase_history)

        with st.expander("Click here to leave your feedback on the chatbot response"):
            st.text_input(
                "Leave your comments here.",
                key="comment",
                on_change=store_comment,
                kwargs={"uuid": st.session_state[UUID]},
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

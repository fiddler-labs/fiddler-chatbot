import logging
import json
from typing import Any, cast
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Cassandra as CassandraVectorStore
from langchain_core.tools import Tool, tool  # noqa: F401
# from langchain.tools.retriever import create_retriever_tool

from src.vector_index_mgmt import open_cassandra_connection, close_cassandra_connection
from src.config import CONFIG_VECTOR_INDEX_MGMT , CONFIG_CHATBOT_NEW

logger = logging.getLogger(__name__)

_cassandra_cluster = None
_cassandra_session = None
_embedding: OpenAIEmbeddings | None = None
_vector_store: CassandraVectorStore | None = None

def init_rag_resources() -> tuple[bool, str]:
    """Initialize global Cassandra vector store resources once for reuse."""
    global _cassandra_cluster, _cassandra_session, _embedding, _vector_store
    if _vector_store is not None and _cassandra_session is not None:
        return True, "Already initialized"
    try:
        _embedding = OpenAIEmbeddings(
            model=CONFIG_VECTOR_INDEX_MGMT["embedding_model"],
            dimensions=CONFIG_VECTOR_INDEX_MGMT["embedding_dimensions"],
            )
        _cassandra_cluster, _cassandra_session = cast(tuple[Any, Any], open_cassandra_connection())
        _vector_store = CassandraVectorStore(
            embedding=_embedding,
            session=_cassandra_session,
            keyspace=CONFIG_VECTOR_INDEX_MGMT["keyspace"],
            table_name=CONFIG_VECTOR_INDEX_MGMT["TABLE_NAME"],
            )
        logger.info("✓ RAG resources initialized (persistent Cassandra session)")
        return True, "Initialized"
    except Exception as e:
        logger.error(f"Error initializing RAG resources: {e}")
        # Ensure globals are cleared on failure
        _vector_store = None
        _embedding = None
        if _cassandra_cluster or _cassandra_session:
            try:
                close_cassandra_connection(_cassandra_cluster, _cassandra_session)
            except Exception:
                pass
        _cassandra_cluster = None
        _cassandra_session = None
        return False, str(e)

def shutdown_rag_resources() -> None:
    """Shutdown global Cassandra vector store resources safely."""
    global _cassandra_cluster, _cassandra_session, _embedding, _vector_store
    try:
        if _cassandra_cluster or _cassandra_session:
            close_cassandra_connection(_cassandra_cluster, _cassandra_session)
    finally:
        _cassandra_cluster = None
        _cassandra_session = None
        _embedding = None
        _vector_store = None
        logger.info("✓ RAG resources shut down")

@tool
def rag_over_fiddler_knowledge_base(query: str) -> str:
    """RAG Knowledge Retrieval - PRIMARY INFORMATION SOURCE
    PURPOSE: Search Fiddler's documentation vector database for relevant information.

    WHEN TO USE:
    - For ANY question about Fiddler AI Observability Platform
    - When user asks about features, APIs, integrations, or best practices
    - To gather context before formulating responses

    QUERY OPTIMIZATION STRATEGY: strip filler words and stop words from the user input to form the RAG inputquery

    MANDATORY WORKFLOW - ALWAYS FOLLOW THIS SEQUENCE:
    1. Call this tool with optimized query
    2. IMMEDIATELY call tool_fiddler_guardrail_faithfulness to validate retrieval quality

    Input(str): Optimized search query with only key terms for maximum cosine similarity
    Output(str): Concatenated relevant documents with metadata
    """
    try:
        global _vector_store
        if _vector_store is None:
            ok, msg = init_rag_resources()
            logger.warning(f"RAG resources initialized during query stage (not during chat start): {msg}")
            if not ok or _vector_store is None:
                logger.error(f"Error: RAG resources not initialized: {msg}")
                return f"Error: RAG resources not initialized: {msg}"

        documents = _vector_store.similarity_search(query, k=CONFIG_CHATBOT_NEW['TOP_K_RETRIEVAL'])

        if not documents:
            return "No relevant documents found in the knowledge base."

        formatted_results = {}
        for i, doc in enumerate(documents, 1):
            content = doc.page_content
            metadata = doc.metadata if doc.metadata else {}
            formatted_results[f"Document {i}"] = {
                "metadata": metadata,
                "content": content
                }

        return json.dumps(formatted_results , indent=4)

    except Exception as e:
        logger.error(f"Error in Cassandra search: {e}")
        return f"Error: {str(e)}\n Please fix your mistakes."


"""

def make_cassandra_rag_retriever_tool() -> Tool:
    retriever_tool = Tool(
        name="retrieval_tool",
        description="Search and return information from the cassandra data corpus.",
        func=cassandra_search_function
        )

    return retriever_tool

def make_local_rag_retriever_tool() -> Tool:
    glob_pattern = "local_assets/vector_index_feed_*.csv"
    latest_file = max(glob.glob(glob_pattern))
    doc_splits = pd.read_csv(latest_file)
    doc_splits = doc_splits["text"].to_list()
    doc_splits = [Document(page_content=split) for split in doc_splits]

    doc_splits = doc_splits[-100:]

    vectorstore = InMemoryVectorStore.from_documents( documents=doc_splits, embedding=OpenAIEmbeddings() )
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    retriever_tool = create_retriever_tool(
        retriever,
        "retrieval_tool",
        "Search and return information from the local csv data corpus.",
        # document_prompt=RAG_PROMPT
        )

    return retriever_tool


import glob
import pandas as pd
from typing import Dict, Any
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.vectorstores import InMemoryVectorStore
from agentic_tools.state_data_model import ChatbotState
from fiddler_langgraph.tracing.instrumentation import set_llm_context

def LEGACY_cassandra_rag_node(state: ChatbotState) -> Dict[str, Any]:
    # Retrieve relevant documents from the Cassandra vector database using RAG.

    # Args: state: Current conversation state containing messages
    # Returns: Dictionary with updated messages including retrieved context
    try:
        # Get the last user message for retrieval
        last_message = None
        for msg in reversed(state["messages"]):
            if isinstance(msg, HumanMessage):
                last_message = msg
                break

        if not last_message:
            logger.warning("No user message found for RAG retrieval")
            return {"messages": [AIMessage(content="No query found for document retrieval.")]}

        query = str(last_message.content)  # Ensure query is a string
        logger.info(f"Performing RAG retrieval for query: '{query[:100]}...'")

        # Set up embeddings and vector store
        llm, embedding = setup_llm_and_embeddings()

        with cassandra_connection() as (cassandra_cluster, cassandra_session):
            vector_store = CassandraVectorStore(
                embedding=embedding,
                session=cassandra_session,
                keyspace=CONFIG_VECTOR_INDEX_MGMT["keyspace"],
                table_name=CONFIG_VECTOR_INDEX_MGMT["TABLE_NAME"]
            )


        # Perform similarity search
        k = 5  # Number of documents to retrieve
        documents = vector_store.similarity_search(query, k=k)

        if not documents:
            logger.warning("No relevant documents found")
            return {"messages": [AIMessage(content="No relevant documents found in the knowledge base.")]}

        # Format retrieved documents
        retrieved_context = []
        for i, doc in enumerate(documents, 1):
            content = doc.page_content[:50]  # Truncate for brevity
            metadata = doc.metadata

            # Extract useful metadata
            source = metadata.get('source', 'Unknown')
            title = metadata.get('title', 'Untitled')

            retrieved_context.append(
                f"Document {i} (Source: {source}, Title: {title}):\n{content}..."
            )

        # Create context message
        context_message = (
            f"📚 Retrieved {len(documents)} relevant documents for your query:\n\n" +
            "\n\n".join(retrieved_context) +
            "\n\n🤖 I'll use this information to provide you with a comprehensive answer."
        )

        logger.info(f"Successfully retrieved {len(documents)} documents")

        set_llm_context(llm, context_message)

        # Store retrieved documents in state for use by other nodes
        return {
            "messages": [AIMessage(content=context_message)],
            "retrieved_documents": documents,  # Store for potential use by other nodes
            "retrieval_query": query
        }

    except Exception as e:
        logger.error(f"Error in RAG retrieval: {e}")
        error_message = f"❌ Error retrieving documents: {str(e)}"
        return {"messages": [AIMessage(content=error_message)]}

"""

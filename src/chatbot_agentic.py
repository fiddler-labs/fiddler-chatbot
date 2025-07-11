"""
Fiddler Agentic Chatbot - Phase 1: Foundation
A simple CLI chatbot using LangGraph with integrated Fiddler monitoring
Part of the FiddleJam hackathon to stress test Fiddler's agentic monitoring capabilities
"""

import os
import sys
import uuid
import logging
from typing import Sequence, Dict, Any, Optional
from typing_extensions import TypedDict, Annotated

from pydantic import SecretStr

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from fiddler_langgraph import FiddlerClient
from fiddler_langgraph.tracing.instrumentation import LangGraphInstrumentor, set_conversation_id, set_llm_context

from dotenv import load_dotenv
load_dotenv()

from utils.custom_logging import setup_logging
# Import vector store utilities
from vector_index_mgmt import cassandra_connection, setup_llm_and_embeddings, CONFIG, TABLE_NAME
from langchain_community.vectorstores import Cassandra as CassandraVectorStore


setup_logging(log_level="DEBUG")
logger = logging.getLogger(__name__)


FIDDLER_URL = os.getenv("FIDDLER_URL")
FIDDLER_API_KEY = os.getenv("FIDDLER_API_KEY")
FIDDLER_APPLICATION_ID = os.getenv("FIDDLER_APPLICATION_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY or not FIDDLER_API_KEY or not FIDDLER_APPLICATION_ID or not FIDDLER_URL:
    logger.error("Error: OPENAI_API_KEY, FIDDLER_API_KEY, FIDDLER_URL, or FIDDLER_APPLICATION_ID environment variables are required")
    sys.exit(1)

logger.info("Initializing Fiddler monitoring...")
try:
    fdl_client = FiddlerClient(
        api_key=FIDDLER_API_KEY,
        application_id=FIDDLER_APPLICATION_ID,
        url=FIDDLER_URL,
        console_tracer=False,  # Set to True for debugging ; Enabling console tracer will prevent data from being sent to Fiddler.
        )
    
    # Instrument the application
    instrumentor = LangGraphInstrumentor(fdl_client)
    instrumentor.instrument()
    logger.info("✓ Fiddler monitoring initialized successfully")
except Exception as e:
    logger.error(f"Warning: Failed to initialize Fiddler monitoring: {e}")
    logger.info("Continuing without monitoring...")
    fdl_client = None
    instrumentor = None


# Define the state schema for our chatbot
class ChatbotState(TypedDict):
    """Enhanced state schema for the chatbot conversation"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    retrieved_documents: Optional[list]  # Store retrieved documents
    retrieval_query: Optional[str]  # Store the query used for retrieval


# Initialize the language model
logger.info("Initializing language model...")
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=SecretStr(OPENAI_API_KEY) if OPENAI_API_KEY else None,
)

# Define the RAG Retrieval Function
def rag_retrieval_node(state: ChatbotState) -> Dict[str, Any]:
    """
    Retrieve relevant documents from the Cassandra vector database using RAG.
    
    Args:
        state: Current conversation state containing messages
        
    Returns:
        Dictionary with updated messages including retrieved context
    """
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
        
        # Connect to Cassandra and perform retrieval
        with cassandra_connection() as (cluster, session):
            # Initialize vector store
            vector_store = CassandraVectorStore(
                embedding=embedding,
                session=session,
                keyspace=CONFIG["keyspace"],
                table_name=TABLE_NAME
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
                content = doc.page_content[:500]  # Truncate for brevity
                metadata = doc.metadata
                
                # Extract useful metadata
                source = metadata.get('source', 'Unknown')
                title = metadata.get('title', 'Untitled')
                
                retrieved_context.append(
                    f"Document {i} (Source: {source}, Title: {title}):\n{content}..."
                )
            
            set_llm_context(llm, retrieved_context)
            
            # Create context message
            context_message = (
                f"📚 Retrieved {len(documents)} relevant documents for your query:\n\n" +
                "\n\n".join(retrieved_context) +
                "\n\n🤖 I'll use this information to provide you with a comprehensive answer."
            )
            
            logger.info(f"Successfully retrieved {len(documents)} documents")
            
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


# Enhanced chatbot node that can use retrieved context
def chatbot_node(state: ChatbotState) -> Dict[str, Any]:
    """
    Process the conversation state and generate a response using the LLM.
    Enhanced to use retrieved context from RAG when available.
    
    Args: 
        state: Current conversation state containing messages
        
    Returns: 
        Dictionary with updated messages including the LLM response
    """
    # Check if we have retrieved documents
    retrieved_docs = state.get("retrieved_documents", [])
    
    # Create enhanced context for the LLM
    context_parts = []
    
    # Add conversation context
    conversation_context = " | ".join([
        f"{msg.__class__.__name__}: {msg.content[:100]}..." 
        if len(msg.content) > 100 else f"{msg.__class__.__name__}: {msg.content}"
        for msg in state["messages"][-10:]  # Last 10 messages for context
    ])
    context_parts.append(f"Conversation: {conversation_context}")
    
    # Add retrieved documents context if available
    if retrieved_docs:
        doc_context = " | ".join([
            f"Doc {i}: {doc.page_content[:150]}..." 
            for i, doc in enumerate(retrieved_docs[:3], 1)  # Top 3 docs
        ])
        context_parts.append(f"Retrieved Knowledge: {doc_context}")
        
        # Add system message with retrieved context
        system_message = (
            "You are a helpful AI assistant with access to a knowledge base. "
            "Use the retrieved documents to provide accurate, contextual responses. "
            "If the retrieved information is relevant, reference it in your answer. "
            "If the retrieved information is not relevant, rely on your general knowledge."
        )
        
        # Insert system message at the beginning
        messages_with_context = [SystemMessage(content=system_message)] + list(state["messages"])
    else:
        messages_with_context = state["messages"]
    
    # Set context for Fiddler monitoring
    full_context = " | ".join(context_parts)
    set_llm_context(llm, full_context)
    
    # Generate response from the LLM
    response = llm.invoke(messages_with_context)
    
    # Return the updated state with the new message
    return {"messages": [response]}


# Build the LangGraph workflow
logger.info("Building LangGraph workflow...")
workflow = StateGraph(ChatbotState)

# Add the chatbot node
workflow.add_node("rag_retrieval", rag_retrieval_node)
workflow.add_node("chatbot", chatbot_node)

# Define the graph flow
workflow.add_edge(START, "rag_retrieval")
workflow.add_edge("rag_retrieval", "chatbot")
workflow.add_edge("chatbot", END)

# Compile the graph
app = workflow.compile()
logger.info("✓ Workflow compiled successfully")


def run_chatbot():
    """
    Main function to run the interactive CLI chatbot.
    """
    print("\n" + "="*60)
    print("🤖 Fiddler Agentic Chatbot - Phase 1")
    session_id = str(uuid.uuid4())
    print(f"Session ID: {session_id}\n")
    print("Type 'quit', 'exit', or 'q' to end the conversation.")
    print("="*60 + "\n")
    
    set_conversation_id(app, session_id) # for Fiddler monitoring
    
    # Initialize conversation state
    messages = []
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n👋 Goodbye! Thank you for chatting.")
                break
            
            # Skip empty inputs
            if not user_input:
                continue
            
            # Add user message to conversation
            messages.append(HumanMessage(content=user_input))
            
            # Process through the graph
            try:
                result = app.invoke({"messages": messages})
                
                # Extract and display the assistant's response
                assistant_message = result["messages"][-1]
                if isinstance(assistant_message, AIMessage):
                    print(f"\nAssistant: {assistant_message.content}\n")
                    # Add assistant message to conversation history
                    messages.append(assistant_message)
                
            except Exception as e:
                print(f"\n❌ Error generating response: {e}")
                print("Please try again.\n")
                # Remove the last user message if there was an error
                if messages and isinstance(messages[-1], HumanMessage):
                    messages.pop()
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except EOFError:
            print("\n\n👋 Goodbye!")
            break
    
    # Clean up instrumentation
    if instrumentor:
        try:
            instrumentor.uninstrument()
            logger.info("\n✓ Fiddler instrumentation cleaned up")
        except Exception as e:
            logger.error(f"Error cleaning up Fiddler instrumentation: {e}")
            pass


def verify_setup():
    """
    Verify that the setup is correct and all components are working.
    """
    logger.info("\n🔍 Verifying setup...")
    
    # Check OpenAI connection
    try:
        test_response = llm.invoke([HumanMessage(content="Say 'Hello, I'm working!'")])
        logger.info("✓ OpenAI connection: OK")
        logger.info(test_response.content)
    except Exception as e:
        logger.error(f"❌ OpenAI connection: FAILED - {e}")
        return False
    
    # Check Fiddler connection
    if fdl_client:
        logger.info("✓ Fiddler client: Initialized")
        logger.info(f"  - Application ID: {FIDDLER_APPLICATION_ID}")
        logger.info(f"  - URL: {FIDDLER_URL}")
    else:
        logger.error("❌ Fiddler client: Not initialized")
    
    # Test the graph
    try:
        test_result = app.invoke({"messages": [HumanMessage(content="Test message")]})
        logger.info("✓ LangGraph workflow: OK")
        logger.info(test_result)
    except Exception as e:
        logger.error(f"❌ LangGraph workflow: FAILED - {e}")
        return False
    
    logger.info("\n✅ All systems operational!")
    return True


if __name__ == "__main__":
    # Run verification first, then start chatbot
    try:
        if verify_setup():
            run_chatbot()
        else:
            logger.error("\n❌ Setup verification failed. Please check your configuration.")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)

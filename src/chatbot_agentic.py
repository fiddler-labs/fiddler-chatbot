"""
Fiddler Agentic Chatbot - CURRENT PHASE: Phase 2: RAG Integration
A simple CLI chatbot using LangGraph with integrated Fiddler monitoring
Part of the FiddleJam hackathon to stress test Fiddler's agentic monitoring capabilities
"""

import os
import sys
import uuid
import logging

from pydantic import SecretStr
from typing import Annotated, Sequence, Dict, Any
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from fiddler_langgraph import FiddlerClient
from fiddler_langgraph.tracing.instrumentation import LangGraphInstrumentor, set_conversation_id, set_llm_context

from utils.custom_logging import setup_logging

setup_logging(log_level="INFO")
logger = logging.getLogger(__name__)


FIDDLER_URL = 'https://preprod.cloud.fiddler.ai'

FIDDLER_API_KEY = os.getenv("FIDDLER_API_KEY")
FIDDLER_APPLICATION_ID = os.getenv("FIDDLER_APP_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY or not FIDDLER_API_KEY or not FIDDLER_APPLICATION_ID:
    logger.error("Error: OPENAI_API_KEY, FIDDLER_API_KEY, or FIDDLER_APP_ID environment variables are required")
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
    """State schema for the chatbot conversation"""
    messages: Annotated[Sequence[BaseMessage], add_messages]


# Initialize the language model
logger.info("Initializing language model...")
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=SecretStr(OPENAI_API_KEY) if OPENAI_API_KEY else None,
)

# Define the chatbot node function
def chatbot_node(state: ChatbotState) -> Dict[str, Any]:
    """
    Process the conversation state and generate a response using the LLM.
    Args: state: Current conversation state containing messages
    Returns: Dictionary with updated messages including the LLM response
    """
    # Create a context string from recent messages
    context = " | ".join([
        f"{msg.__class__.__name__}: {msg.content[:100]}..." 
        if len(msg.content) > 100 else f"{msg.__class__.__name__}: {msg.content}"
        for msg in state["messages"][-15:]  # Last 15 messages for context
    ])
    set_llm_context(llm, context)
    
    # Generate response from the LLM
    response = llm.invoke(state["messages"])
    
    # Return the updated state with the new message
    return {"messages": [response]}


# Build the LangGraph workflow
logger.info("Building LangGraph workflow...")
workflow = StateGraph(ChatbotState)

# Add the chatbot node
workflow.add_node("chatbot", chatbot_node)

# Define the graph flow
workflow.add_edge(START, "chatbot")
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
            logger.info("✓ Fiddler instrumentation cleaned up")
        except Exception as e:
            logger.error(f"Error cleaning up Fiddler instrumentation: {e}")
            pass

if __name__ == "__main__":
    # Run verification
    try :
        run_chatbot()
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)

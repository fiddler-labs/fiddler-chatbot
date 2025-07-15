"""
Fiddler Agentic Chatbot - CURRENT PHASE: Phase 2: RAG Integration
A simple CLI chatbot using LangGraph with integrated Fiddler monitoring
Part of the FiddleJam hackathon to stress test Fiddler's agentic monitoring capabilities
"""

import os
import sys
import uuid
import logging
from dotenv import load_dotenv
from typing import Dict, Any, List
from datetime import datetime
import argparse
import traceback

from langchain_core.prompts import PromptTemplate
from pydantic import SecretStr

from langchain_core.tools import Tool
from langchain_core.runnables.config import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage #, BaseMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command #, interrupt
# from langgraph.graph.message import add_messages

# from langchain.chat_models import init_chat_model 
    # llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")
    # response_model = init_chat_model("openai:gpt-4.1", temperature=0)

from fiddler_langgraph import FiddlerClient
from fiddler_langgraph.tracing.instrumentation import LangGraphInstrumentor, set_conversation_id, set_llm_context

from utils.custom_logging import setup_logging

from agentic_tools.state_data_model import ChatbotState
from agentic_tools.rag import make_local_rag_retriever_tool, make_cassandra_rag_retriever_tool #, LEGACY_cassandra_rag_node

from config import CONFIG_CHATBOT_NEW as config

load_dotenv()

setup_logging(log_level="INFO")
logger = logging.getLogger(__name__)

FIDDLER_URL     = config.get("FIDDLER_URL")
FIDDLER_API_KEY = os.getenv("FIDDLER_API_KEY")
FIDDLER_APP_ID  = os.getenv("FIDDLER_APP_ID")
OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY or not FIDDLER_API_KEY or not FIDDLER_APP_ID :
    logger.error("Error: OPENAI_API_KEY, FIDDLER_API_KEY, or FIDDLER_APP_ID environment variables are required")
    sys.exit(1)


logger.info("Initializing Fiddler monitoring...")
fdl_client = FiddlerClient(
    api_key=FIDDLER_API_KEY,
    application_id=FIDDLER_APP_ID,
    url=str(FIDDLER_URL),
    console_tracer=False,  # Set to True for debugging ; Enabling console tracer will prevent data from being sent to Fiddler.
    )

# Instrument the application
instrumentor = LangGraphInstrumentor(fdl_client)
instrumentor.instrument()
logger.info("✓ Fiddler monitoring initialized successfully")


checkpointer = MemorySaver()

# Read the system instructions template
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up 2 levels from src/chatbot.py to project root ./
with open(os.path.join(PROJECT_ROOT, "src", "system_instructions.md"), "r") as f:
    SYSTEM_INSTRUCTIONS_PROMPT = PromptTemplate.from_template(f.read().strip())

logger.info("Initializing language model...")
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=SecretStr(OPENAI_API_KEY) if OPENAI_API_KEY else None,
    )

logger.info("Initializing tools...")
tools : List[Tool] = [
    Tool(
        name="get a system time",
        description="Get the current system time",
        func=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
    ]


rag_retriever_tool_selector = {
    "local"     : ToolNode([make_local_rag_retriever_tool()     ], name="local_rag_retriever_tool"),
    "cassandra" : ToolNode([make_cassandra_rag_retriever_tool() ], name="cassandra_rag_retriever_tool"),
    # "LEGACY"    : ToolNode([LEGACY_cassandra_rag_node           ], name="LEGACY_cassandra_rag_node"),
    }

all_tools = tools + [make_local_rag_retriever_tool() , make_cassandra_rag_retriever_tool()]

logger.debug("Binding tools to language model...")
llm.bind_tools(all_tools)
logger.debug("✓ Tools bound to language model successfully")


def human_node(state: ChatbotState) -> Command:
    """
    Human input node that uses interrupt to get user input and directs the flow.
    In automated mode, it takes messages from a list ( that was parsed via argparse).
    Args: state: Current conversation state
    Returns: Command with user input and next node to execute
    """
    # Display prompt to user
    print("You: ", end="", flush=True)
    if automation_messages:
        user_input = automation_messages.pop(0)
        print(f"👤 You (automated): {user_input}")
    else:
        user_input = input("Please enter your message (or 'quit' to exit): ")
    
    # Check for exit commands
    if user_input and user_input.lower() in ["quit", "exit", "q"]:
        print("👋 Goodbye! Thank you for chatting.\n")
        return Command(update={"messages": [HumanMessage(content="Goodbye!")]}, goto=END)
    
    # Return command with user input and next node
    return Command( update={"messages": [HumanMessage(content=user_input)]}, goto="rag_retrieval" )

# Enhanced chatbot node that can use retrieved context
def chatbot_node(state: ChatbotState) -> Dict[str, Any]:
    """
    Process the conversation state and generate a response using the LLM.
    Enhanced to use retrieved context from RAG when available.
    
    Args: state: Current conversation state containing messages
    Returns: Dictionary with updated messages including the LLM response
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
        
        messages_with_context = [SystemMessage(
            content=SYSTEM_INSTRUCTIONS_PROMPT.format(
                context=doc_context,
                question=state["messages"][-1].content
            ))] + list(state["messages"])
    else:
        messages_with_context = state["messages"]
    
    # Set context for Fiddler monitoring
    full_context = " | ".join(context_parts)
    set_llm_context(llm, full_context)
    
    # Generate response from the LLM
    response = llm.invoke(messages_with_context)

    # Create an AIMessage from the response
    ai_message = AIMessage(content=response.content)

    # Display the response immediately
    print(f"🤖 Assistant: {response.content}\n")

    # Return the updated state with the new AIMessage
    return {"messages": [ai_message]}

def build_chatbot_graph():
    # Build the LangGraph workflow
    logger.info("Building LangGraph workflow...")
    workflow_builder = StateGraph(ChatbotState)

    # Component entities
    workflow_builder.add_node("human", human_node)
    workflow_builder.add_node("chatbot", chatbot_node)
    workflow_builder.add_node("tools", ToolNode(tools=tools))
    workflow_builder.add_node("rag_retrieval", rag_retriever_tool_selector["local"])

    # Define the graph flow
    workflow_builder.add_edge(START, "human")
    workflow_builder.add_edge("human", "rag_retrieval")
    workflow_builder.add_edge("rag_retrieval", "chatbot")
    workflow_builder.add_conditional_edges("chatbot", tools_condition)
    workflow_builder.add_edge("tools", "chatbot")

    workflow_builder.add_edge("chatbot", "human")
    workflow_builder.add_edge("human",END)

    # Compile the graph with checkpointer
    chatbot_graph = workflow_builder.compile(checkpointer=checkpointer)

    return chatbot_graph

def visualize_chatbot_graph(chatbot_graph):
    logger.info("✓ Workflow compiled successfully")

    output_path = "workflow_graph.png"
    try:
        image_data = chatbot_graph.get_graph().draw_mermaid_png()
        with open(output_path, "wb") as file:
            file.write(image_data)
        logger.info(f"Workflow graph saved to {output_path}")
    except Exception as e:
        logger.error(f"Workflow visualization failed: {e}")


def run_chatbot():
    """
    Main function to run the interactive CLI chatbot.
    """

    def get_thread_config() -> RunnableConfig:
        """
        Generate a thread configuration for the conversation.
        Returns: RunnableConfig with thread ID
        """
        thread_id = str(uuid.uuid4())
        return RunnableConfig(configurable={"thread_id": thread_id})

    print("\n" + "="*60)
    print("🤖 Fiddler Agentic Chatbot (Human-in-the-Loop)")
    thread_config = get_thread_config()
    session_id = thread_config.get("configurable", {}).get("thread_id", str(uuid.uuid4()))
    print(f"Session ID: {session_id}\n")
    print("Type 'quit', 'exit', or 'q' to end the conversation.")
    print("="*60 + "\n")
    
    chatbot_graph = build_chatbot_graph()
    visualize_chatbot_graph(chatbot_graph)
    
    set_conversation_id(chatbot_graph, session_id)  # for Fiddler monitoring
        
    exec_state = ChatbotState(messages=[])

    try:
        for yeilded_event in chatbot_graph.stream(exec_state, thread_config, stream_mode="values"):
            logger.debug("Graph executed node, continuing...")
            
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
    except Exception as e:
        logger.error(f"Error in conversation: {e}")
        logger.error(traceback.format_exc())
        print(f"\n❌ Error: {e}")
        print(traceback.format_exc())
        raise e
    
    finally:
        # Clean up instrumentation
        if instrumentor:
            try:
                instrumentor.uninstrument()
                logger.info("✓ Fiddler instrumentation cleaned up")
            except Exception as e:
                logger.error(f"Error cleaning up Fiddler instrumentation: {e}")
                logger.error(traceback.format_exc())
                raise e

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fiddler Agentic Chatbot")
    parser.add_argument("args", nargs="*")
    automation_messages = parser.parse_args().args or []
    print(f"Automation messages: {automation_messages}")

    try:
        run_chatbot()
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)

"""
Fiddler Agentic Chatbot - CURRENT PHASE: Phase 2: RAG Integration
A simple CLI chatbot using LangGraph with integrated Fiddler monitoring
Part of the FiddleJam hackathon to stress test Fiddler's agentic monitoring capabilities
"""

import os
import json
import sys
import uuid
import logging
from dotenv import load_dotenv
from typing import Any, List
from datetime import datetime
import argparse
import traceback

from langchain_core.prompts import PromptTemplate
from pydantic import SecretStr

from langchain_core.tools import Tool
from langchain_core.runnables.config import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage #, BaseMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
# from langgraph.graph.message import add_messages

# from langchain.chat_models import init_chat_model 
    # llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")
    # response_model = init_chat_model("openai:gpt-4.1", temperature=0)

from fiddler_langgraph import FiddlerClient
from fiddler_langgraph.tracing.instrumentation import LangGraphInstrumentor, set_conversation_id, set_llm_context

from utils.custom_logging import setup_logging

from agentic_tools.state_data_model import ChatbotState
from agentic_tools.rag import make_local_rag_retriever_tool #, make_cassandra_rag_retriever_tool #, LEGACY_cassandra_rag_node

from config import CONFIG_CHATBOT_NEW as config

load_dotenv()

setup_logging(log_level="DEBUG")
logger = logging.getLogger(__name__)

def try_pretty_foramtting(incoming_str : Any) -> str:
    try:
        return json.dumps(incoming_str, indent=4)
    except Exception:
        try:
            return json.dumps(str(incoming_str), indent=4)
        except Exception:
            try:
                return str(incoming_str)
            except Exception:
                return incoming_str
        

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

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=SecretStr(OPENAI_API_KEY) if OPENAI_API_KEY else None,
    )
logger.info("✓ language model initialized successfully")

tools : List[Tool] = [
    Tool(
        name="get_system_time",
        description="Get the current system time",
        func=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
    ]
logger.info("✓ tools initialized successfully")


rag_retriever_tool_node = ToolNode([make_local_rag_retriever_tool()], name="retrieval_tool")
# rag_retriever_tool = ToolNode([make_cassandra_rag_retriever_tool() ], name="retrieval_tool"),

all_tools = tools #+ [make_local_rag_retriever_tool() , make_cassandra_rag_retriever_tool()]

llm.bind_tools(all_tools)
logger.info("✓ Tools bound to language model successfully")


def human_node(state: ChatbotState) -> ChatbotState:
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
        sys.exit(0)
        # return Command(update={"messages": [HumanMessage(content="Goodbye!")]}, goto=END)
    
    # return Command( update={"messages": [HumanMessage(content=user_input)]}, goto="force_rag_tool_call" )
    return {"messages": [HumanMessage(content=user_input)]}


def chatbot_node(state: ChatbotState) -> ChatbotState:
    """
    Processes the conversation state to generate a response using the LLM.
    It dynamically constructs a context from the conversation history and any retrieved documents from tool calls
    """
    # Start with a base of messages from the current state
    all_messages_in_State = list(state["messages"])

    # Extract the most recent tool call outputs to build the context
    tool_outputs = []
    for msg in reversed(all_messages_in_State):
        if isinstance(msg, ToolMessage):
            tool_outputs.append(msg.content)

    # Construct a unified context for both LLM and monitoring
    fiddler_context_store = []
    
    conversation_history = " | ".join([ f"{msg.__class__.__name__}: {msg.content[:100]}..." for msg in all_messages_in_State[-10:] ])
    fiddler_context_store.append(f"Conversation: {conversation_history}")
    logger.debug(f"CHATBOT_NODE: Debug - Conversation History: {try_pretty_foramtting(conversation_history)}")

    if tool_outputs:
        retrieved_docs = " | ".join(tool_outputs)
        fiddler_context_store.append(f"Retrieved Docs: {retrieved_docs}")
        logger.debug(f"CHATBOT_NODE: Debug - Retrieved Docs: {try_pretty_foramtting(retrieved_docs)}")

        system_message = SystemMessage( content=SYSTEM_INSTRUCTIONS_PROMPT.format( context=retrieved_docs, question=all_messages_in_State[-1].content ) )
        all_messages_in_State.insert(0, system_message)

    # Set the unified context for Fiddler monitoring
    set_llm_context(llm, " | ".join(fiddler_context_store))
    
    # Generate response from the LLM
    logger.debug(f"CHATBOT_NODE: Debug - All Messages in State: {try_pretty_foramtting(all_messages_in_State)}")
    response = llm.invoke(all_messages_in_State)

    ai_message = AIMessage(content=response.content)
    print(f"🤖 Assistant: {response.content}\n")
    logger.debug(f"CHATBOT_NODE: Debug - Response: \n\t{try_pretty_foramtting(response.content)}")

    return {"messages": [ai_message]}

def force_rag_tool_call_node(state: ChatbotState) -> ChatbotState:
    """
    Node that takes the last HumanMessage and returns an AIMessage with a tool call for the RAG retriever.
    """
    if not state["messages"] or not isinstance(state["messages"][-1], HumanMessage):
        raise ValueError("No HumanMessage found in state for tool call generation.")
    user_msg = state["messages"][-1]
    tool_call = {
        "name": "retrieval_tool",
        "args": {"query": user_msg.content},
        "id": str(uuid.uuid4()),
        "type": "tool_call"
        }
    ai_msg = AIMessage(content="", tool_calls=[tool_call])
    return {"messages": [ai_msg]}


def build_chatbot_graph():
    # Build the LangGraph workflow
    logger.info("Building LangGraph workflow...")
    workflow_builder = StateGraph(ChatbotState)

    # Component entities
    workflow_builder.add_node("human", human_node)
    workflow_builder.add_node("force_rag_tool_call", force_rag_tool_call_node)
    workflow_builder.add_node("chatbot", chatbot_node)
    workflow_builder.add_node("tools", ToolNode(tools=tools))
    workflow_builder.add_node("rag_retrieval", rag_retriever_tool_node)

    # Define the graph flow
    workflow_builder.add_edge(START, "human")
    workflow_builder.add_edge("human",END)
    workflow_builder.add_edge("human", "force_rag_tool_call")
    workflow_builder.add_edge("force_rag_tool_call", "rag_retrieval")
    workflow_builder.add_edge("rag_retrieval", "chatbot")
    workflow_builder.add_conditional_edges( "chatbot", tools_condition)
    workflow_builder.add_edge("tools", "chatbot")
    workflow_builder.add_edge("chatbot", "human")
    workflow_builder.add_edge("chatbot", END)

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
        thread_id = str(datetime.now().strftime("%Y%m%d%H%M%S"))+'_'+str(uuid.uuid4())
        return RunnableConfig(configurable={"thread_id": thread_id})

    print("\n" + "="*60)
    print("🤖 Fiddler Agentic Chatbot")
    thread_config = get_thread_config()
    session_id = thread_config.get("configurable", {}).get("thread_id",'NO_SESSION_ID_PROVIDED')
    print(f"Session ID: {session_id}\n")
    print("Type 'quit', 'exit', or 'q' to end the conversation.")
    print("="*60 + "\n")
    
    chatbot_graph = build_chatbot_graph()
    visualize_chatbot_graph(chatbot_graph)
    
    set_conversation_id(chatbot_graph, session_id)  # for Fiddler monitoring
        
    # Start with a HumanMessage if automation_messages is not empty
    if automation_messages:
        exec_state = ChatbotState(messages=[HumanMessage(content=automation_messages.pop(0))])
    else:
        exec_state = ChatbotState(messages=[])

    try:
        for yeilded_event in chatbot_graph.stream(exec_state, thread_config, stream_mode="values"):
            logger.info("Graph executed node, continuing... ")
            logger.debug(f"RUN_CHATBOT: Debug - Yeilded Event: {try_pretty_foramtting(yeilded_event)}")
            
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

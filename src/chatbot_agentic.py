"""
Fiddler Agentic Chatbot
A simple CLI chatbot using LangGraph with integrated Fiddler monitoring
"""

import os
import json
import sys
import uuid
import logging
from dotenv import load_dotenv
from typing import Any #, List
from datetime import datetime
import argparse
import traceback
from pydantic import SecretStr

from langchain_core.tools import tool # , Tool
from langchain_core.runnables.config import RunnableConfig
from langchain_core.messages import HumanMessage, ToolMessage , SystemMessage , AIMessage #, BaseMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
# from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
# from langgraph.graph.message import add_messages

# from langchain.chat_models import init_chat_model 
    # llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")
    # response_model = init_chat_model("openai:gpt-4.1", temperature=0)

from fiddler_langgraph import FiddlerClient
from fiddler_langgraph.tracing.instrumentation import LangGraphInstrumentor, set_conversation_id, set_llm_context # todo - ause this later  # noqa: F401

from utils.custom_logging import setup_logging

from agentic_tools.state_data_model import ChatbotState
from agentic_tools.rag import rag_over_fiddler_knowledge_base
from agentic_tools.fiddler_gaurdrails import tool_fiddler_guardrail_safety, tool_fiddler_guardrail_faithfulness

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
with open(os.path.join(PROJECT_ROOT, "src", "system_instructions_AGENTIC.md"), "r") as f:
    SYSTEM_INSTRUCTIONS_PROMPT = f.read()

base_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=SecretStr(OPENAI_API_KEY) if OPENAI_API_KEY else None,
    )
logger.info("✓ language model initialized successfully")

@tool
def get_system_time() -> str:
    """
    Get the current system time
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

tools = [
    get_system_time, 
    rag_over_fiddler_knowledge_base, 
    tool_fiddler_guardrail_safety, 
    tool_fiddler_guardrail_faithfulness,
    ]
llm = base_llm.bind_tools(tools)
logger.info("✓ Tools bound to language model successfully")


def human_node(state: ChatbotState):
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
        return Command(update={"messages": [HumanMessage(content="USER EXITTED")]}, goto=END)
        # sys.exit(0)
    
    return Command( update={"messages": [HumanMessage(content=user_input)]}, goto="chatbot" )

def chatbot_node(state: ChatbotState):
    """
    Processes the conversation state to generate a response using the LLM.
    It dynamically constructs a context from the conversation history and any retrieved documents from tool calls
    """
    all_messages_in_state = state["messages"]
    # last_message = all_messages_in_State[-1]
    
    # Add the system instructions to the messages
    # all_messages_in_state.append( [SystemMessage(content=SYSTEM_INSTRUCTIONS_PROMPT)] )
    
    logger.debug(f"CHATBOT_NODE: Debug - All Messages in State: {try_pretty_foramtting(all_messages_in_state)}")
    
    response = llm.invoke(all_messages_in_state)
    set_llm_context(base_llm, str(response.content))

    print(f"🤖 Assistant: {response.content}\n")
    logger.debug(f"CHATBOT_NODE: Debug - Response: \n\t{try_pretty_foramtting(response.content)}")

    if hasattr(response, "tool_calls") and response.tool_calls and len(response.tool_calls) > 0: # type: ignore
        logger.debug('Tool calls detected - transferring to tool_execution node')
        return Command(update={"messages": [response]}, goto="tool_execution")
    else:
        logger.debug('No tool calls - transferring to human node')
        return Command(update={"messages": [response]}, goto="human")
    
def tool_execution_node(state: ChatbotState):
    """Custom tool node to execute tool calls"""
    # Get the last AI message that contains tool calls
    last_ai_message = None
    for msg in reversed(state["messages"]):
        if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls") and msg.tool_calls:
            last_ai_message = msg
            break
    
    if not last_ai_message:
        raise ValueError("No AI message with tool calls found in state")
    
    tool_outputs = []
    for tool_call in (last_ai_message.tool_calls) or []: # type: ignore
        logger.debug(f"Executing tool: {tool_call['name']} with args: {tool_call['args']}")
        match tool_call['name']:
            case "get_system_time":
                output = get_system_time.invoke(tool_call['args'])
            case "rag_over_fiddler_knowledge_base":
                output = rag_over_fiddler_knowledge_base.invoke(tool_call['args'])
            case "tool_fiddler_guardrail_safety":
                output = tool_fiddler_guardrail_safety.invoke(tool_call['args'])
            case "tool_fiddler_guardrail_faithfulness":
                output = tool_fiddler_guardrail_faithfulness.invoke(tool_call['args'])
            case _:
                raise ValueError(f"Unknown tool: {tool_call['name']}")
            
        # Create a ToolMessage for each tool call
        tool_message = ToolMessage(
            content=json.dumps(output),
            name=tool_call['name'],
            tool_call_id=tool_call['id'],
            )
        tool_outputs.append(tool_message)
        logger.debug(f"Created tool message for {tool_call['name']}: {tool_message}")
    
    return Command(update={"messages": tool_outputs}, goto="chatbot")


def build_chatbot_graph():
    logger.info("Building LangGraph workflow...")
    workflow_builder = StateGraph(ChatbotState)

    # Component entities
    workflow_builder.add_node("human", human_node)
    workflow_builder.add_node("chatbot", chatbot_node)
    workflow_builder.add_node("tool_execution", tool_execution_node)

    # Define the graph flow
    workflow_builder.add_edge(START, "human")
    # workflow_builder.add_edge("human", "chatbot")
    # workflow_builder.add_edge("chatbot", "human")
    # workflow_builder.add_edge("chatbot", "tool_execution")
    # workflow_builder.add_edge("tool_execution", "chatbot")
    workflow_builder.add_edge("human", END)

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
    
    set_conversation_id(session_id)  # for Fiddler monitoring
    
    # Start with a HumanMessage if automation_messages is not empty
    if automation_messages:
        exec_state = ChatbotState(messages=[
            SystemMessage(content=SYSTEM_INSTRUCTIONS_PROMPT),
            HumanMessage(content=automation_messages.pop(0))
            ])
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

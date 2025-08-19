"""
Fiddler Agentic Chatbot - Chainlit Interface
A Chainlit-based interface for the Fiddler chatbot using LangGraph with integrated monitoring
"""
import os
import json
import sys
import traceback
import uuid
import logging
from dotenv import load_dotenv
from datetime import datetime
from pydantic import SecretStr
import chainlit as cl

from langchain_core.messages import (  # , BaseMessage
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
    )
from langchain_core.runnables.config import RunnableConfig
from langchain_core.tools import tool  # , Tool
from langchain_openai import ChatOpenAI

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command

from fiddler_langgraph import FiddlerClient
from fiddler_langgraph.tracing.instrumentation import (  # todo - use this later  # noqa: F401
    LangGraphInstrumentor,
    set_conversation_id,
    set_llm_context,
    )

from agentic_tools.rag import rag_over_fiddler_knowledge_base
from agentic_tools.state_data_model import ChatbotState
from agentic_tools.validator_url import validate_url
from agentic_tools.fiddler_gaurdrails import (
    tool_fiddler_guardrail_faithfulness,
    tool_fiddler_guardrail_safety,
    )

from utils.custom_logging import setup_logging
from utils.pretty_formatter import try_pretty_formatting
from config import CONFIG_CHATBOT_NEW as config  # noqa: N811


load_dotenv()

setup_logging(log_level="DEBUG")
logger = logging.getLogger(__name__)

FIDDLER_URL    = config.get("FIDDLER_URL")
FIDDLER_APP_ID = config.get("FIDDLER_APP_ID")
FIDDLER_API_KEY = os.getenv("FIDDLER_API_KEY")
OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY")

URL_TO_AGENTIC_MONITORING = str(FIDDLER_URL) + '/genai-applications/' + str(FIDDLER_APP_ID)

if not OPENAI_API_KEY or not FIDDLER_API_KEY or not FIDDLER_APP_ID :
    logger.error("Error: OPENAI_API_KEY, FIDDLER_API_KEY, or FIDDLER_APP_ID environment variables are required")
    sys.exit(1)


logger.info("Initializing Fiddler monitoring...")
fdl_client = FiddlerClient(
    api_key=FIDDLER_API_KEY,
    application_id=str(FIDDLER_APP_ID),
    url=str(FIDDLER_URL),
    console_tracer=False,  # Set to True for debugging ; Enabling console tracer will prevent data from being sent to Fiddler.
    )

# Instrument the application
instrumentor = LangGraphInstrumentor(fdl_client)
instrumentor.instrument()
logger.info("✓ Fiddler monitoring initialized successfully")

# Read the system instructions template
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up 2 levels from src/chatbot.py to project root ./
with open(os.path.join(PROJECT_ROOT, "src", "system_instructions_AGENTIC.md")) as f:
    SYSTEM_INSTRUCTIONS_PROMPT = f.read()

base_llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0.4,
    api_key=SecretStr(OPENAI_API_KEY) if OPENAI_API_KEY else None,
    streaming=True,
    )
logger.info("✓ language model initialized successfully")

@tool
def get_system_time() -> str:
    """Get the current system time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

tools = [
    get_system_time,
    rag_over_fiddler_knowledge_base,
    tool_fiddler_guardrail_safety,
    tool_fiddler_guardrail_faithfulness,
    validate_url,
    ]
llm = base_llm.bind_tools(tools)
logger.info("✓ Tools bound to language model successfully")

set_llm_context(base_llm, "agentic chatbot")


"""
def human_node(state: ChatbotState):
    '''
    Human input node that uses interrupt to get user input and directs the flow.
    In automated mode, it takes messages from a list ( that was parsed via argparse).
    Args: state: Current conversation state
    Returns: Command with user input and next node to execute
    '''
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
"""

def chatbot_node(state: ChatbotState):
    """Processes the conversation state to generate a response using the LLM."""
    all_messages_in_state = state["messages"]

    # Get the LLM from session
    llm = cl.user_session.get("llm")
    if not llm:
        raise ValueError("LLM not found in session")

    # Add the system instructions to the messages
    # all_messages_in_state.append( [SystemMessage(content=SYSTEM_INSTRUCTIONS_PROMPT)] ) #todo

    logger.debug(f"CHATBOT_NODE: Debug - All Messages in State: {try_pretty_formatting(all_messages_in_state)}")

    response = llm.invoke(all_messages_in_state)

    print(f"🤖 Assistant: {response.content}\n")
    logger.debug(f"CHATBOT_NODE: Debug - Response: \n\t{try_pretty_formatting(response.content)}")

    if (
        hasattr(response, "tool_calls")
        and response.tool_calls
        and len(response.tool_calls) > 0
        ):  # type: ignore
        logger.debug("Tool calls detected - transferring to tool_execution node")
        return Command(update={"messages": [response]}, goto="tool_execution")
    else:
        logger.debug("No tool calls - ending conversation turn")
        return Command(update={"messages": [response]}, goto=END)

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
    for tool_call in last_ai_message.tool_calls:  # type: ignore
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
            case "validate_url":
                output = validate_url.invoke(tool_call['args'])
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
    """Build the LangGraph workflow for Chainlit"""
    logger.info("Building LangGraph workflow...")
    workflow_builder = StateGraph(ChatbotState)

    # Component entities
    # workflow_builder.add_node("human", human_node)
    workflow_builder.add_node("chatbot", chatbot_node)
    workflow_builder.add_node("tool_execution", tool_execution_node)

    # Define the graph flow
    workflow_builder.add_edge(START, "chatbot")
    workflow_builder.add_edge("chatbot", END)

    """
    Note: In Chainlit, we don't use static edges for conditional flow.
    The chatbot_node and tool_execution_node use Command objects with goto

    IMPORTANT: Do NOT add static edges from chatbot or tool_execution
    The Command objects with goto control the dynamic routing:
    - chatbot_node returns Command(goto="tool_execution") when tools needed
    - chatbot_node returns Command(goto=END) when no tools needed
    - tool_execution_node returns Command(goto="chatbot") to continue processing

    This enables the guardrail workflows:
    1. User message → chatbot → safety check tool → chatbot → RAG tool → chatbot → faithfulness tool → chatbot → response
    2. User message → chatbot → RAG tool → chatbot → faithfulness tool → chatbot → retry RAG → chatbot → response

    # LEGACY CODE - for reference only
    # This allows conditional routing based on whether tools are needed.
    # workflow_builder.add_edge(START, "human")
    # workflow_builder.add_edge("human", "chatbot")
    # workflow_builder.add_edge("chatbot", "human")
    # workflow_builder.add_edge("chatbot", "tool_execution")
    # workflow_builder.add_edge("tool_execution", "chatbot")
    # workflow_builder.add_edge("human", END)
    """

    checkpointer = MemorySaver()
    chatbot_graph = workflow_builder.compile(checkpointer=checkpointer)

    logger.info("✓ Workflow compiled successfully")

    output_path = "workflow_graph.png"
    try:
        image_data = chatbot_graph.get_graph().draw_mermaid_png()
        with open(output_path, "wb") as file:
            file.write(image_data)
        logger.info(f"Workflow graph saved to {output_path}")
    except Exception as e:
        logger.error(f"Workflow visualization failed: {e}")

    return chatbot_graph


@cl.on_chat_start
async def on_chat_start():
    """Initialize a new chat session"""
    logger.info("New chat session started")

    chatbot_graph = build_chatbot_graph()

    session_id = str(datetime.now().strftime("%Y%m%d%H%M%S")) + "_" + str(uuid.uuid4())
    set_conversation_id(session_id)

    thread_config = RunnableConfig(configurable={"thread_id": session_id})

    # Store in session
    cl.user_session.set("llm", llm)
    cl.user_session.set("chatbot_graph", chatbot_graph)
    cl.user_session.set("session_id", session_id)
    cl.user_session.set("thread_config", thread_config)

    # Send welcome message
    await cl.Message(
        content="🤖 **Welcome to Fiddler AI Assistant!**\n"
            "I'm your intelligent companion for AI observability, monitoring, and model insights. \n"
            "I can help you with Fiddler platform questions, ML monitoring best practices, and technical guidance.\n\n"
            f"**Session ID:** `{session_id}`\n"
            f"{URL_TO_AGENTIC_MONITORING}\n\n"
            "What would you like to explore today?"
            ).send()

@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming messages"""
    chatbot_graph = cl.user_session.get("chatbot_graph")
    thread_config = cl.user_session.get("thread_config")

    if not chatbot_graph:
        await cl.Message(content="❌ Error: Chat session not initialized").send()
        return

    # Get existing conversation state or create new one
    conversation_state = cl.user_session.get("conversation_state")
    if not conversation_state:
        # Initialize with system message for new conversations
        conversation_state = ChatbotState(
            messages=[SystemMessage(content=SYSTEM_INSTRUCTIONS_PROMPT)]
            )
        cl.user_session.set("conversation_state", conversation_state)

    # Add the new user message to existing conversation
    user_message = HumanMessage(content=message.content)
    conversation_state = ChatbotState(
        messages=list(conversation_state["messages"]) + [user_message]
        )

    # Create a message for streaming
    msg = cl.Message(content="")
    await msg.send()

    try:
        # Stream the response
        final_ai_message = None
        final_state = None

        async for event in chatbot_graph.astream(
            conversation_state,
            thread_config,
            stream_mode="values",
            ):
            # Capture the final state from each event
            final_state = event
            # Get the last message from the state
            messages = event.get("messages", [])
            if messages:
                last_message = messages[-1]

                # Handle AI messages
                if isinstance(last_message, AIMessage):
                    final_ai_message = last_message

                    # Stream the content if available
                    if last_message.content:
                        msg.content = str(last_message.content)
                        await msg.update()

                    # Show tool calls if any
                    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                        tool_info = "\n\n🔧 **Using tools:**"
                        for tool_call in last_message.tool_calls:
                            tool_info += f"\n- {tool_call['name']}"
                        msg.content = tool_info + "\n\n" + (msg.content or "Processing...")
                        await msg.update()

                # Handle Tool messages
                elif isinstance(last_message, ToolMessage):
                    # Show tool results in a step
                    async with cl.Step(name=f"Tool: {last_message.name}", type="tool") as step:
                        step.output = str(last_message.content)

        # Final update if we have content
        if final_ai_message and final_ai_message.content:
            msg.content = str(final_ai_message.content)
            await msg.update()

        # Update the persistent conversation state with the final result from graph execution
        if final_state:
            cl.user_session.set("conversation_state", final_state)

    except Exception as e:
        logger.error(f"Error in conversation: {e}", exc_info=True)
        logger.error(traceback.format_exc())
        print(f"\n❌ Error: {e}")
        print(traceback.format_exc())
        await cl.Message(content=f"❌ Error: {str(e)}").send()
        raise e

@cl.on_chat_end
async def on_chat_end():
    """Clean up when chat ends"""
    logger.info("Chat session ended")

    # Clean up instrumentation if needed
    if instrumentor:
        try:
            instrumentor.uninstrument()
            logger.info("✓ Fiddler instrumentation cleaned up")
        except Exception as e:
            logger.error(f"Error cleaning up Fiddler instrumentation: {e}")
            logger.error(traceback.format_exc())
            raise e


if __name__ == "__main__":
    logger.error("❌ Error: run this file with chainlit using the command: uv run chainlit run src/chatbot_chainlit.py")
    sys.exit(1)

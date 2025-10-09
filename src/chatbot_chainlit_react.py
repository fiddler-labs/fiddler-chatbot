"""
Fiddler Agentic Chatbot - Chainlit Interface
A Chainlit-based interface for the Fiddler chatbot using LangGraph with integrated monitoring
"""
import os
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
    ToolMessage,
    # SystemMessage,
    )
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.config import RunnableConfig
from langchain_core.tools import tool  # , Tool

from langchain_openai import ChatOpenAI

from langgraph.checkpoint.memory import MemorySaver # todo- , MemorySaverAsync , SqliteSaver , CassandraSaver
from langgraph.prebuilt import create_react_agent

from fiddler_langgraph import FiddlerClient
from fiddler_langgraph.tracing.instrumentation import (  # todo - use this later  # noqa: F401
    LangGraphInstrumentor,
    set_conversation_id,
    set_llm_context,
    )

from agentic_tools.rag import (
    rag_over_fiddler_knowledge_base,
    init_rag_resources,
    shutdown_rag_resources,
    )
from agentic_tools.validator_url import validate_url
from agentic_tools.fiddler_gaurdrails import (
    tool_fiddler_guardrail_faithfulness,
    tool_fiddler_guardrail_safety,
    )

from utils.custom_logging import setup_logging
# from utils.pretty_formatter import try_pretty_formatting
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
    model="gpt-4o",
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

checkpointer = MemorySaver()

prompt_template = ChatPromptTemplate.from_messages([
    ('system',SYSTEM_INSTRUCTIONS_PROMPT),
    MessagesPlaceholder(variable_name='messages'),
    ])


app = create_react_agent(
    model=llm,
    tools = [
            get_system_time,
            rag_over_fiddler_knowledge_base,
            tool_fiddler_guardrail_safety,
            tool_fiddler_guardrail_faithfulness,
            validate_url,
        ],
    prompt=prompt_template,
    checkpointer=checkpointer
    )

set_llm_context(base_llm, "ReAct chatbot agent powered by OpenAI Model gpt-4.1")

ok, msg = init_rag_resources()
if not ok:
    logger.error(f"RAG initialization failed: {msg}")

@cl.on_chat_start
async def on_chat_start():
    """Initialize a new chat session"""
    logger.info("New chat session started")

    session_id = str(datetime.now().strftime("%Y%m%d%H%M%S")) + "_" + str(uuid.uuid4())
    set_conversation_id(session_id)

    thread_config = RunnableConfig(configurable={"thread_id": session_id})

    # Store in session
    cl.user_session.set("llm", llm)
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
    thread_config = cl.user_session.get("thread_config")

    # Add the new user message to existing conversation
    user_message = HumanMessage(content=message.content)

    msg = cl.Message(content="")
    await msg.send()

    try:
        # Stream the response
        final_ai_message = None
        async for event in app.astream(
            {'messages': [HumanMessage(content=user_message.content)]},
            thread_config,
            stream_mode="values",
            ):
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

    # # Shutdown RAG resources
    # try:
    #     shutdown_rag_resources()
    # except Exception as e:
    #     logger.warning(f"RAG shutdown encountered an error: {e}")

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

"""
Streamlit-Native Fiddler Chatbot
A Streamlit-based chat interface that uses the same LangGraph backend as the Chainlit version
This version works seamlessly in Streamlit Cloud without iframe or port issues
"""

import os
import sys
import json
import uuid
import logging
import traceback
from datetime import datetime
from dotenv import load_dotenv
from pydantic import SecretStr

import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_core.runnables.config import RunnableConfig
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver

# Import your existing modules
from fiddler_langgraph import FiddlerClient
from fiddler_langgraph.tracing.instrumentation import LangGraphInstrumentor, set_conversation_id

from utils.custom_logging import setup_logging
from utils.pretty_formatter import try_pretty_formatting
from agentic_tools.state_data_model import ChatbotState
from agentic_tools.rag import cassandra_search_function
from config import CONFIG_CHATBOT_NEW as config

load_dotenv()

# Set up logging
setup_logging(log_level="DEBUG")
logger = logging.getLogger(__name__)

# Configuration
FIDDLER_URL = config.get("FIDDLER_URL")
FIDDLER_API_KEY = os.getenv("FIDDLER_API_KEY")
FIDDLER_APP_ID = os.getenv("FIDDLER_APP_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def validate_environment():
    """Validate required environment variables"""
    missing_vars = []
    if not OPENAI_API_KEY:
        missing_vars.append("OPENAI_API_KEY")
    if not FIDDLER_API_KEY:
        missing_vars.append("FIDDLER_API_KEY")
    if not FIDDLER_APP_ID:
        missing_vars.append("FIDDLER_APP_ID")
    
    return missing_vars

@st.cache_resource
def initialize_fiddler_client():
    """Initialize Fiddler client with caching"""
    try:
        logger.info("Initializing Fiddler monitoring...")
        fdl_client = FiddlerClient(
            api_key=FIDDLER_API_KEY,
            application_id=FIDDLER_APP_ID,
            url=str(FIDDLER_URL),
            console_tracer=False,
        )
        
        # Instrument the application
        instrumentor = LangGraphInstrumentor(fdl_client)
        instrumentor.instrument()
        logger.info("✓ Fiddler monitoring initialized successfully")
        return fdl_client, instrumentor
    except Exception as e:
        logger.error(f"Failed to initialize Fiddler client: {e}")
        return None, None

@st.cache_resource
def load_system_instructions():
    """Load system instructions template with caching"""
    try:
        PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(PROJECT_ROOT, "src", "system_instructions.md"), "r") as f:
            return PromptTemplate.from_template(f.read().strip())
    except Exception as e:
        logger.error(f"Failed to load system instructions: {e}")
        return None

@st.cache_resource
def initialize_llm():
    """Initialize the language model with caching"""
    try:
        base_llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=SecretStr(OPENAI_API_KEY) if OPENAI_API_KEY else None,
            streaming=True,
        )
        
        # Define tools
        @tool
        def get_system_time() -> str:
            """Get the current system time"""
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        tools = [get_system_time, cassandra_search_function]
        llm = base_llm.bind_tools(tools)
        
        logger.info("✓ Language model initialized successfully")
        return llm, tools
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        return None, None

@st.cache_resource
def build_chatbot_graph():
    """Build the LangGraph workflow"""
    try:
        logger.info("Building LangGraph workflow...")
        
        def chatbot_node(state: ChatbotState):
            """Processes the conversation state to generate a response using the LLM."""
            all_messages_in_state = state["messages"]
            llm, _ = initialize_llm()
            
            if not llm:
                raise ValueError("LLM not initialized")
            
            response = llm.invoke(all_messages_in_state)
            logger.debug(f"CHATBOT_NODE: Debug - Response: \n\t{try_pretty_formatting(response.content)}")

            if hasattr(response, "tool_calls") and response.tool_calls and len(response.tool_calls) > 0:
                logger.debug('Tool calls detected - transferring to tool_execution node')
                return Command(update={"messages": [response]}, goto="tool_execution")
            else:
                logger.debug('No tool calls - ending conversation turn')
                return Command(update={"messages": [response]}, goto=END)
        
        def tool_execution_node(state: ChatbotState):
            """Custom tool node to execute tool calls"""
            ai_message = state["messages"][-1]
            tool_outputs = []
            
            _, tools = initialize_llm()
            tool_dict = {tool.name: tool for tool in tools}
            
            for tool_call in (ai_message.tool_calls) or []:
                tool_name = tool_call['name']
                if tool_name in tool_dict:
                    output = tool_dict[tool_name].invoke(tool_call['args'])
                    tool_outputs.append(
                        ToolMessage(
                            content=json.dumps(output),
                            name=tool_name,
                            tool_call_id=tool_call['id'],
                        )
                    )
            
            return Command(update={"messages": tool_outputs}, goto="chatbot")
        
        # Build the graph
        workflow_builder = StateGraph(ChatbotState)
        workflow_builder.add_node("chatbot", chatbot_node)
        workflow_builder.add_node("tool_execution", tool_execution_node)
        workflow_builder.add_edge(START, "chatbot")
        workflow_builder.add_edge("chatbot", END)
        
        checkpointer = MemorySaver()
        chatbot_graph = workflow_builder.compile(checkpointer=checkpointer)
        
        logger.info("✓ Workflow compiled successfully")
        return chatbot_graph
    
    except Exception as e:
        logger.error(f"Failed to build chatbot graph: {e}")
        return None

def initialize_session():
    """Initialize session state"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(datetime.now().strftime("%Y%m%d%H%M%S")) + '_' + str(uuid.uuid4())
        set_conversation_id(st.session_state.session_id)
    
    if "chatbot_graph" not in st.session_state:
        st.session_state.chatbot_graph = build_chatbot_graph()
    
    if "thread_config" not in st.session_state:
        st.session_state.thread_config = RunnableConfig(
            configurable={"thread_id": st.session_state.session_id}
        )

def render_sidebar():
    """Render the sidebar with system information"""
    with st.sidebar:
        st.subheader("🔧 System Status")
        
        # Environment validation
        missing_vars = validate_environment()
        if missing_vars:
            st.error("❌ Missing Environment Variables")
            for var in missing_vars:
                st.error(f"• {var}")
        else:
            st.success("✅ Environment OK")
        
        # Fiddler status
        fdl_client, _ = initialize_fiddler_client()
        if fdl_client:
            st.success("✅ Fiddler Monitoring")
        else:
            st.error("❌ Fiddler Monitoring")
        
        # LLM status
        llm, _ = initialize_llm()
        if llm:
            st.success("✅ Language Model")
        else:
            st.error("❌ Language Model")
        
        st.markdown("---")
        
        # Session info
        st.subheader("📊 Session Info")
        st.info(f"**Session ID:** `{st.session_state.get('session_id', 'Not set')}`")
        st.info(f"**Messages:** {len(st.session_state.get('messages', []))}")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.session_id = str(datetime.now().strftime("%Y%m%d%H%M%S")) + '_' + str(uuid.uuid4())
            set_conversation_id(st.session_state.session_id)
            st.rerun()

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Fiddler AI Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session
    initialize_session()
    
    # Header
    st.title("🤖 Fiddler AI Assistant")
    st.markdown("*Powered by LangGraph & Streamlit*")
    
    # Render sidebar
    render_sidebar()
    
    # Check for environment issues
    missing_vars = validate_environment()
    if missing_vars:
        st.error("❌ **Environment Setup Required**")
        st.write("Please set the following environment variables in Streamlit Cloud's secrets:")
        for var in missing_vars:
            st.code(f"{var} = 'your-{var.lower().replace('_', '-')}-here'")
        st.info("Go to your Streamlit Cloud app → Settings → Secrets to add these variables.")
        return
    
    # Check if chatbot graph is available
    if not st.session_state.chatbot_graph:
        st.error("❌ **Chatbot Initialization Failed**")
        st.write("There was an error initializing the chatbot. Please check the logs and try refreshing the page.")
        return
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about Fiddler AI..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Create state for the conversation
                    exec_state = ChatbotState(messages=[HumanMessage(content=prompt)])
                    
                    # Stream the response
                    response_placeholder = st.empty()
                    final_response = ""
                    
                    for event in st.session_state.chatbot_graph.stream(
                        exec_state, 
                        st.session_state.thread_config, 
                        stream_mode="values"
                    ):
                        messages = event.get("messages", [])
                        if messages:
                            last_message = messages[-1]
                            
                            if isinstance(last_message, AIMessage) and last_message.content:
                                final_response = str(last_message.content)
                                response_placeholder.markdown(final_response)
                            
                            elif isinstance(last_message, ToolMessage):
                                # Show tool usage
                                with st.expander(f"🔧 Tool Used: {last_message.name}", expanded=False):
                                    st.json(last_message.content)
                    
                    # Add assistant response to chat history
                    if final_response:
                        st.session_state.messages.append({"role": "assistant", "content": final_response})
                
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    logger.error(f"Error in conversation: {e}", exc_info=True)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main()
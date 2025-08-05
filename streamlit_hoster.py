"""
Streamlit-Chainlit Hybrid Host for Streamlit Cloud

This production-ready solution keeps Streamlit alive for health checks while
running Chainlit as a subprocess and embedding it via iframe.

Key Features:
- Automatic Chainlit startup
- Real-time health monitoring
- Clean error handling
- Professional UI with status indicators
- Restart capabilities

Author: Fiddler AI Team
Version: 1.0.0
"""

import os
import sys
import subprocess
import streamlit as st
# import streamlit.components.v1 as components  # Only needed for iframe approach
import time
import atexit
import socket
from pathlib import Path
from typing import Tuple, Optional

# ===== CONFIGURATION - UPDATE THESE FOR YOUR PROJECT =====
REQUIRED_ENV_VARS = ["OPENAI_API_KEY", "FIDDLER_API_KEY", "FIDDLER_APP_ID"]  # Your required env vars

# Legacy Chainlit configuration (kept for backward compatibility)
CHAINLIT_APP_PATH = "src/chatbot_chainlit.py"  # Path to your Chainlit application
CHAINLIT_PORT = 8000  # Port for Chainlit (8501 is reserved for Streamlit)

# ===== GLOBAL STATE =====
chainlit_process = None

def cleanup_chainlit():
    """Clean up Chainlit process on exit"""
    global chainlit_process
    if chainlit_process and chainlit_process.poll() is None:
        try:
            chainlit_process.terminate()
            chainlit_process.wait(timeout=5)
        except (subprocess.TimeoutExpired, ProcessLookupError, OSError):
            try:
                chainlit_process.kill()
            except (ProcessLookupError, OSError):
                pass

# Register cleanup on exit
atexit.register(cleanup_chainlit)

def validate_environment() -> Tuple[list, list, Optional[str]]:
    """
    Validate that the environment is properly configured
    
    Returns:
        Tuple of (errors, warnings, streamlit_version)
    """
    errors = []
    warnings = []
    streamlit_version = None
    
    # Check required environment variables
    missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing_vars:
        errors.append(f"Missing environment variables: {', '.join(missing_vars)}")
    
    # Check if required modules are available
    try:
        import streamlit as st
        streamlit_version = st.__version__
    except ImportError:
        errors.append("Streamlit is not installed")
    
    # Check for other dependencies using importlib
    import importlib.util
    
    required_packages = [
        ("langchain_core", "LangChain core"),
        ("langgraph", "LangGraph"),
        ("fiddler_langgraph", "Fiddler LangGraph client")
    ]
    
    for package_name, display_name in required_packages:
        if importlib.util.find_spec(package_name) is None:
            errors.append(f"{display_name} is not installed")
    
    # Check for chatbot source files
    required_files = [
        "src/system_instructions.md",
        "src/agentic_tools/state_data_model.py",
        "src/agentic_tools/rag.py",
        "config.py"
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            errors.append(f"Required file not found: {file_path}")
    
    return errors, warnings, streamlit_version

def start_chainlit_subprocess() -> Tuple[bool, str]:
    """
    Start Chainlit as a subprocess
    
    Returns:
        Tuple of (success, message)
    """
    global chainlit_process
    
    try:
        # Clean up any existing process
        cleanup_chainlit()
        
        # Prepare command to start Chainlit
        command = [
            sys.executable, "-m", "chainlit", "run", 
            CHAINLIT_APP_PATH,
            "--port", str(CHAINLIT_PORT),
            "--host", "0.0.0.0",
            "--headless"  # Prevent auto-opening browser
        ]
        
        # Start Chainlit subprocess
        chainlit_process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        return True, f"Chainlit started on port {CHAINLIT_PORT} with PID {chainlit_process.pid}"
        
    except Exception as e:
        return False, f"Failed to start Chainlit: {str(e)}"

def check_chainlit_health() -> Tuple[bool, str]:
    """
    Check if Chainlit is running and healthy
    
    Returns:
        Tuple of (is_healthy, status_message)
    """
    global chainlit_process
    
    if chainlit_process is None:
        return False, "Not started"
    
    # Check if process is still running
    if chainlit_process.poll() is not None:
        return False, f"Process exited with code {chainlit_process.returncode}"
    
    # Check if port is responding
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', CHAINLIT_PORT))
        sock.close()
        
        if result == 0:
            return True, "Running"
        else:
            return False, "Port not responding"
    except Exception as e:
        return False, f"Health check failed: {str(e)}"

def render_sidebar(errors: list, streamlit_version: Optional[str], chatbot_ready: bool, health_status: str):
    """Render the sidebar with status and controls"""
    with st.sidebar:
        st.subheader("🔧 System Status")
        
        # Environment status
        if errors:
            st.error("❌ Environment Issues")
            for error in errors:
                st.error(f"• {error}")
        else:
            st.success("✅ Environment OK")
            if streamlit_version:
                st.info(f"Streamlit v{streamlit_version}")
        
        # Chatbot status
        if chatbot_ready:
            st.success(f"✅ Chatbot: {health_status}")
        else:
            st.error(f"❌ Chatbot: {health_status}")
        
        # Session info
        if st.session_state.get('session_id'):
            st.info(f"**Session:** `{st.session_state.session_id[:8]}...`")
        
        if st.session_state.get('messages'):
            st.info(f"**Messages:** {len(st.session_state.messages)}")
        
        st.markdown("---")
        
        # Control buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Restart", use_container_width=True, disabled=bool(errors)):
                # Clear session state to restart chatbot
                for key in ['messages', 'session_id', 'chatbot_graph', 'thread_config']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        with col2:
            if st.button("🧪 Test", use_container_width=True):
                st.rerun()
        
        # Configuration info
        with st.expander("⚙️ Configuration"):
            st.code(f"""
Mode: Streamlit Native Chatbot
Port: 8501 (Streamlit)
Required Vars: {', '.join(REQUIRED_ENV_VARS)}
Backend: LangGraph + Fiddler
            """)

def render_error_state(errors: list):
    """Render the error state UI"""
    st.error("❌ **Environment Issues Detected**")
    st.write("Please resolve the following issues before proceeding:")
    for error in errors:
        st.error(f"• {error}")
    
    st.markdown("---")
    st.subheader("🛠️ Setup Instructions")
    st.markdown("""
    1. **Missing environment variables**: Set required variables in Streamlit Cloud's secrets
    2. **Missing dependencies**: Ensure all required packages are in `requirements.txt`
    3. **Missing source files**: Ensure all chatbot source files are present
    
    **Required Environment Variables:**
    ```
    OPENAI_API_KEY = "your-openai-api-key"
    FIDDLER_API_KEY = "your-fiddler-api-key"  
    FIDDLER_APP_ID = "your-fiddler-app-id"
    ```
    
    **Key Dependencies:**
    ```
    streamlit>=1.28.0
    langchain>=0.3.0
    langgraph>=0.5.0
    fiddler-langgraph
    openai>=1.0.0
    ```
    """)

def render_starting_state():
    """Render the starting/loading state UI"""
    st.warning("⚠️ **Chatbot Initializing**")
    st.write("The Fiddler AI Assistant is starting up. This may take a few moments...")
    
    with st.spinner("Initializing AI Assistant..."):
        # Show progress and automatically retry
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            progress_bar.progress(i + 1)
            if i < 30:
                status_text.text("Loading dependencies...")
            elif i < 60:
                status_text.text("Initializing Fiddler client...")
            elif i < 80:
                status_text.text("Building LangGraph workflow...")
            else:
                status_text.text("Almost ready...")
            time.sleep(0.03)
        
        st.success("🎉 Initialization complete! Refreshing...")
        time.sleep(1)
        st.rerun()

def render_running_state():
    """Render the main running state with Streamlit-native chatbot"""
    st.success("✅ **Fiddler AI Assistant is Ready**")
    
    # Import and run the Streamlit-native chatbot
    try:
        # Import the chatbot components we need
        from src import streamlit_chatbot
        
        # Initialize the chatbot session
        streamlit_chatbot.initialize_session()
        
        # Check for environment issues first
        missing_vars = streamlit_chatbot.validate_environment()
        if missing_vars:
            st.error("❌ **Environment Setup Required**")
            st.write("Please set the following environment variables in Streamlit Cloud's secrets:")
            for var in missing_vars:
                st.code(f"{var} = 'your-{var.lower().replace('_', '-')}-here'")
            st.info("Go to your Streamlit Cloud app → Settings → Secrets to add these variables.")
            return
        
        # Check if chatbot graph is available
        if not st.session_state.get('chatbot_graph'):
            st.error("❌ **Chatbot Initialization Failed**")
            st.write("There was an error initializing the chatbot. Please check the logs and try refreshing the page.")
            return
        
        # Display welcome message if no conversation started
        if not st.session_state.get('messages'):
            st.markdown("""
            ### 🤖 Welcome to Fiddler AI Assistant!
            
            I'm your intelligent companion for AI observability, monitoring, and model insights.
            
            I can help you with:
            - Fiddler platform questions
            - ML monitoring best practices  
            - Technical guidance and documentation
            - Model performance analysis
            
            **What would you like to explore today?**
            """)
        
        # Display chat messages
        for message in st.session_state.get('messages', []):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about Fiddler AI..."):
            # Add user message to chat history
            if 'messages' not in st.session_state:
                st.session_state.messages = []
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Import required classes
                        from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
                        
                        # Try to import ChatbotState with path adjustment
                        try:
                            from src.agentic_tools.state_data_model import ChatbotState
                        except ImportError:
                            import sys
                            sys.path.append('src')
                            from src.agentic_tools.state_data_model import ChatbotState
                        
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
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.error(f"Error in conversation: {e}", exc_info=True)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
    except ImportError as e:
        st.error(f"❌ **Import Error**: {str(e)}")
        st.write("Please ensure all required dependencies are installed.")
    except Exception as e:
        st.error(f"❌ **Chatbot Error**: {str(e)}")
        st.write("There was an error loading the chatbot. Please try refreshing the page.")
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; font-size: 14px;">
        <a href="?refresh={time.time()}" style="color: #FF6B6B;">Force refresh</a> | 
        Session: {st.session_state.get('session_id', 'Not initialized')[:8]}...
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main Streamlit application"""
    
    # Page configuration
    st.set_page_config(
        page_title="Fiddler AI Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state for chatbot
    if 'chatbot_initialized' not in st.session_state:
        st.session_state.chatbot_initialized = False
    
    # Check current status
    errors, warnings, streamlit_version = validate_environment()
    
    # Determine chatbot health
    chatbot_ready = False
    health_status = "Not initialized"
    
    if not errors:
        try:
            # Try to initialize the chatbot components
            from src import streamlit_chatbot
            streamlit_chatbot.initialize_session()
            
            if st.session_state.get('chatbot_graph'):
                chatbot_ready = True
                health_status = "Ready"
            else:
                health_status = "Initialization failed"
        except Exception as e:
            health_status = f"Error: {str(e)[:50]}..."
    else:
        health_status = "Environment issues"
    
    # Header
    st.title("🤖 Fiddler AI Assistant")
    st.markdown("*Powered by Streamlit & LangGraph*")
    
    # Render sidebar
    render_sidebar(errors, streamlit_version, chatbot_ready, health_status)
    
    # Main content area - render appropriate state
    if errors:
        render_error_state(errors)
    elif not chatbot_ready:
        render_starting_state()
    else:
        render_running_state()

if __name__ == "__main__":
    main()
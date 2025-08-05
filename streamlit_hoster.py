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
import streamlit.components.v1 as components
import time
import atexit
import socket
from pathlib import Path
from typing import Tuple, Optional

# ===== CONFIGURATION - UPDATE THESE FOR YOUR PROJECT =====
CHAINLIT_APP_PATH = "src/chatbot_chainlit.py"  # Path to your Chainlit application
CHAINLIT_PORT = 8000  # Port for Chainlit (8501 is reserved for Streamlit)
REQUIRED_ENV_VARS = ["OPENAI_API_KEY", "FIDDLER_API_KEY", "FIDDLER_APP_ID"]  # Your required env vars

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
        Tuple of (errors, warnings, chainlit_version)
    """
    errors = []
    warnings = []
    chainlit_version = None
    
    # Check if Chainlit app exists
    if not Path(CHAINLIT_APP_PATH).exists():
        errors.append(f"Chainlit app not found at: {CHAINLIT_APP_PATH}")
    
    # Check required environment variables
    missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing_vars:
        errors.append(f"Missing environment variables: {', '.join(missing_vars)}")
    
    # Check if chainlit is installed
    try:
        import chainlit
        chainlit_version = chainlit.__version__
    except ImportError:
        errors.append("Chainlit is not installed. Add 'chainlit' to your requirements.txt")
    
    return errors, warnings, chainlit_version

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

def render_sidebar(errors: list, chainlit_version: Optional[str], chainlit_healthy: bool, health_status: str):
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
            if chainlit_version:
                st.info(f"Chainlit v{chainlit_version}")
        
        # Chainlit status
        if chainlit_healthy:
            st.success(f"✅ Chainlit: {health_status}")
        else:
            st.error(f"❌ Chainlit: {health_status}")
        
        st.markdown("---")
        
        # Control buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Restart", use_container_width=True, disabled=bool(errors)):
                with st.spinner("Restarting Chainlit..."):
                    success, message = start_chainlit_subprocess()
                    if success:
                        st.session_state.chainlit_started = True
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(message)
        
        with col2:
            if st.button("🧪 Test", use_container_width=True):
                st.rerun()
        
        # Configuration info
        with st.expander("⚙️ Configuration"):
            st.code(f"""
App Path: {CHAINLIT_APP_PATH}
Chainlit Port: {CHAINLIT_PORT}
Streamlit Port: 8501
Required Vars: {', '.join(REQUIRED_ENV_VARS)}
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
    1. **Missing Chainlit app**: Ensure your Chainlit application exists at the specified path
    2. **Missing environment variables**: Set required variables in Streamlit Cloud's secrets
    3. **Missing dependencies**: Add `chainlit` to your `requirements.txt`
    
    Example `requirements.txt`:
    ```
    streamlit>=1.28.0
    chainlit>=1.0.0
    # Your other dependencies...
    ```
    """)

def render_starting_state():
    """Render the starting/loading state UI"""
    st.warning("⚠️ **Chainlit Starting Up**")
    st.write("Your Chainlit application is initializing. This may take a few moments...")
    
    with st.spinner("Starting Chainlit..."):
        # Try to start if not already attempted
        if not st.session_state.chainlit_started:
            success, message = start_chainlit_subprocess()
            if success:
                st.session_state.chainlit_started = True
                time.sleep(3)
                st.rerun()
            else:
                st.error(f"Failed to start Chainlit: {message}")
        else:
            # Wait and check again
            progress_bar = st.progress(0)
            for i in range(100):
                progress_bar.progress(i + 1)
                time.sleep(0.02)
            st.rerun()

def render_running_state():
    """Render the main running state with embedded Chainlit"""
    st.success("✅ **Fiddler AI Assistant is Ready**")
    
    # Embed Chainlit using iframe
    chainlit_url = f"http://localhost:{CHAINLIT_PORT}"
    
    # Create iframe HTML with professional styling
    iframe_html = f"""
    <iframe 
        src="{chainlit_url}" 
        width="100%" 
        height="700" 
        style="border: none; 
               border-radius: 8px; 
               box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
               background: white;"
        title="Fiddler AI Assistant">
    </iframe>
    """
    
    # Display the iframe
    components.html(iframe_html, height=720)
    
    # Footer with helpful links
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; font-size: 14px;">
        Having issues? 
        <a href="{chainlit_url}" target="_blank" style="color: #FF6B6B;">Open Chainlit directly</a> | 
        <a href="?refresh={time.time()}" style="color: #FF6B6B;">Force refresh</a>
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
    
    # Initialize session state
    if 'chainlit_started' not in st.session_state:
        st.session_state.chainlit_started = False
        st.session_state.startup_attempted = False
    
    # Auto-start Chainlit on first load
    if not st.session_state.startup_attempted:
        st.session_state.startup_attempted = True
        
        # Validate environment first
        errors, warnings, chainlit_version = validate_environment()
        
        if not errors:
            # Try to start Chainlit automatically
            success, message = start_chainlit_subprocess()
            if success:
                st.session_state.chainlit_started = True
                # Wait a moment for Chainlit to fully start
                time.sleep(3)
    
    # Check current status
    errors, warnings, chainlit_version = validate_environment()
    chainlit_healthy, health_status = check_chainlit_health()
    
    # Header
    st.title("🤖 Fiddler AI Assistant")
    st.markdown("*Powered by Chainlit & LangGraph*")
    
    # Render sidebar
    render_sidebar(errors, chainlit_version, chainlit_healthy, health_status)
    
    # Main content area - render appropriate state
    if errors:
        render_error_state(errors)
    elif not chainlit_healthy:
        render_starting_state()
    else:
        render_running_state()
    
    # Auto-refresh if Chainlit isn't healthy (and no errors)
    if not chainlit_healthy and not errors:
        time.sleep(5)
        st.rerun()

if __name__ == "__main__":
    main()
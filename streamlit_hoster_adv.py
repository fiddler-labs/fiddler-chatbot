"""
Streamlit Cloud Deployment Wrapper for Chainlit Application

This script provides multiple approaches to deploy a Chainlit application on Streamlit Cloud.
Choose the approach that works best for your deployment scenario.

Author: AI Assistant
Created for: Chainlit-on-Streamlit-Cloud deployment
"""

import os
import sys
import time
import subprocess
import threading
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# Configuration
CHAINLIT_APP_PATH = "src/chatbot_chainlit.py"  # Path to your Chainlit app
CHAINLIT_PORT = 8501  # Must match Streamlit Cloud's expected port
CHAINLIT_HOST = "0.0.0.0"

def approach_1_direct_chainlit():
    """
    Approach 1: Direct Chainlit Execution (RECOMMENDED)
    
    This approach directly runs Chainlit on port 8501, which is what Streamlit Cloud expects.
    This is the simplest and most reliable method.
    """
    st.title("🚀 Launching Fiddler Chainlit Chatbot...")
    
    # Validate Chainlit app exists
    if not Path(CHAINLIT_APP_PATH).exists():
        st.error(f"❌ Chainlit app not found at: {CHAINLIT_APP_PATH}")
        st.info("Please ensure your Chainlit app is in the correct location.")
        return
    
    st.success("✅ Chainlit app found!")
    st.info("🔄 Starting Chainlit server on port 8501...")
    
    # Show what command will be executed
    command = [
        sys.executable, "-m", "chainlit", "run", 
        CHAINLIT_APP_PATH,
        "--port", str(CHAINLIT_PORT),
        "--host", CHAINLIT_HOST,
        "--headless"  # Prevents auto-opening browser
    ]
    
    st.code(" ".join(command), language="bash")
    
    try:
        # Execute Chainlit directly
        # Note: This will replace the current Streamlit process
        st.warning("⚠️ About to launch Chainlit. The Streamlit interface will be replaced.")
        time.sleep(2)  # Give user time to read
        
        # Use exec to replace the current process
        os.execv(sys.executable, command)
        
    except Exception as e:
        st.error(f"❌ Failed to launch Chainlit: {e}")
        st.info("Please check the error logs and ensure all dependencies are installed.")

def approach_2_subprocess_monitor():
    """
    Approach 2: Subprocess with Monitoring
    
    This approach runs Chainlit as a subprocess and provides a Streamlit interface
    to monitor its status. Less reliable but provides more control.
    """
    st.title("🔧 Chainlit Subprocess Manager")
    
    # Initialize session state
    if 'chainlit_process' not in st.session_state:
        st.session_state.chainlit_process = None
        st.session_state.chainlit_status = "stopped"
        st.session_state.chainlit_logs = []
    
    # Status display
    status_color = {"running": "🟢", "stopped": "🔴", "starting": "🟡"}
    st.write(f"**Status:** {status_color.get(st.session_state.chainlit_status, '⚫')} {st.session_state.chainlit_status.title()}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶️ Start Chainlit", disabled=(st.session_state.chainlit_status == "running")):
            start_chainlit_subprocess()
    
    with col2:
        if st.button("⏹️ Stop Chainlit", disabled=(st.session_state.chainlit_status != "running")):
            stop_chainlit_subprocess()
    
    with col3:
        if st.button("🔄 Restart Chainlit"):
            stop_chainlit_subprocess()
            time.sleep(1)
            start_chainlit_subprocess()
    
    # Display logs
    if st.session_state.chainlit_logs:
        st.subheader("📋 Recent Logs")
        for log in st.session_state.chainlit_logs[-10:]:  # Show last 10 logs
            st.text(log)
    
    # Auto-refresh every 5 seconds
    time.sleep(5)
    st.rerun()

def start_chainlit_subprocess():
    """Start Chainlit as a subprocess"""
    try:
        if not Path(CHAINLIT_APP_PATH).exists():
            st.error(f"❌ Chainlit app not found at: {CHAINLIT_APP_PATH}")
            return
        
        st.session_state.chainlit_status = "starting"
        
        # Prepare command
        command = [
            sys.executable, "-m", "chainlit", "run", 
            CHAINLIT_APP_PATH,
            "--port", str(CHAINLIT_PORT),
            "--host", CHAINLIT_HOST,
            "--headless"
        ]
        
        # Start subprocess
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        st.session_state.chainlit_process = process
        st.session_state.chainlit_status = "running"
        st.session_state.chainlit_logs.append(f"[{time.strftime('%H:%M:%S')}] Chainlit started with PID: {process.pid}")
        
        # Start log monitoring thread
        threading.Thread(target=monitor_chainlit_logs, daemon=True).start()
        
        st.success("✅ Chainlit started successfully!")
        
    except Exception as e:
        st.session_state.chainlit_status = "stopped"
        st.error(f"❌ Failed to start Chainlit: {e}")

def stop_chainlit_subprocess():
    """Stop the Chainlit subprocess"""
    if st.session_state.chainlit_process:
        try:
            st.session_state.chainlit_process.terminate()
            st.session_state.chainlit_process.wait(timeout=10)
            st.session_state.chainlit_status = "stopped"
            st.session_state.chainlit_logs.append(f"[{time.strftime('%H:%M:%S')}] Chainlit stopped")
            st.info("🛑 Chainlit stopped")
        except Exception as e:
            st.error(f"❌ Error stopping Chainlit: {e}")
    else:
        st.warning("⚠️ No Chainlit process to stop")

def monitor_chainlit_logs():
    """Monitor Chainlit subprocess logs"""
    if st.session_state.chainlit_process:
        for line in iter(st.session_state.chainlit_process.stdout.readline, ''):
            if line:
                timestamp = time.strftime('%H:%M:%S')
                st.session_state.chainlit_logs.append(f"[{timestamp}] {line.strip()}")

def approach_3_iframe_embed():
    """
    Approach 3: iframe Embedding (EXPERIMENTAL)
    
    This approach runs Chainlit on a different port and embeds it in Streamlit via iframe.
    May have limitations with Streamlit Cloud's networking.
    """
    st.title("🖼️ Chainlit iframe Embedding")
    
    st.warning("⚠️ This approach is experimental and may not work on Streamlit Cloud due to port restrictions.")
    
    # Use a different port for Chainlit
    iframe_port = 8502
    
    # Start Chainlit on different port (simplified)
    chainlit_url = f"http://localhost:{iframe_port}"
    
    st.write(f"Attempting to embed Chainlit from: {chainlit_url}")
    
    # Embed iframe
    iframe_html = f"""
    <iframe 
        src="{chainlit_url}" 
        width="100%" 
        height="600" 
        style="border: 1px solid #ccc; border-radius: 5px;">
    </iframe>
    """
    
    components.html(iframe_html, height=620)
    
    st.info("💡 If the iframe is empty, the Chainlit server may not be running or accessible.")

def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="Chainlit-Streamlit Deployment",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 Chainlit on Streamlit Cloud Deployment")
    st.write("Choose your deployment approach:")
    
    # Sidebar for approach selection
    st.sidebar.title("Deployment Approaches")
    approach = st.sidebar.selectbox(
        "Select Approach:",
        [
            "1. Direct Chainlit (Recommended)",
            "2. Subprocess Monitor", 
            "3. iframe Embedding (Experimental)"
        ]
    )
    
    # Display approach information
    st.sidebar.markdown("---")
    if "Direct Chainlit" in approach:
        st.sidebar.success("✅ **Recommended**")
        st.sidebar.write("Directly runs Chainlit on port 8501. Most reliable for Streamlit Cloud.")
    elif "Subprocess" in approach:
        st.sidebar.warning("⚠️ **Advanced**")
        st.sidebar.write("Provides monitoring but may be less reliable.")
    elif "iframe" in approach:
        st.sidebar.error("🧪 **Experimental**")
        st.sidebar.write("May not work on Streamlit Cloud due to networking restrictions.")
    
    # Route to selected approach
    if "Direct Chainlit" in approach:
        approach_1_direct_chainlit()
    elif "Subprocess" in approach:
        approach_2_subprocess_monitor()
    elif "iframe" in approach:
        approach_3_iframe_embed()

if __name__ == "__main__":
    main()
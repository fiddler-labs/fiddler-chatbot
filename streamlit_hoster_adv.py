"""
Advanced Streamlit-Chainlit Host with Multiple Deployment Approaches

This file demonstrates alternative deployment strategies for educational purposes.
For production use, we recommend the main streamlit_hoster.py

Approaches included:
1. Direct Process Replacement (Original approach - causes health check issues)
2. Subprocess with Advanced Monitoring
3. iframe Embedding with Custom Ports

Author: Fiddler AI Team
Version: 1.0.0 (Reference Implementation)
"""

import os
import sys
import time
import subprocess
import threading
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import json
from datetime import datetime

# Configuration
CHAINLIT_APP_PATH = "src/chatbot_chainlit.py"
CHAINLIT_PORT = 8501  # For direct replacement
CHAINLIT_ALT_PORT = 8502  # For iframe approach
CHAINLIT_HOST = "0.0.0.0"

def approach_1_direct_replacement():
    """
    Approach 1: Direct Process Replacement
    
    WARNING: This causes health check failures on Streamlit Cloud!
    Included for educational purposes only.
    
    How it works:
    - Validates environment
    - Shows launch button
    - Uses os.execv() to replace Streamlit with Chainlit
    
    Issues:
    - Streamlit health checks fail after process replacement
    - No way to return to Streamlit interface
    """
    st.title("🚀 Direct Chainlit Launch (Legacy Approach)")
    
    st.warning("""
    ⚠️ **Known Issue**: This approach causes health check failures on Streamlit Cloud.
    
    Error: `Get "http://localhost:8501/healthz": connection refused`
    
    Use the main `streamlit_hoster.py` for production deployments.
    """)
    
    # Validate Chainlit app exists
    if not Path(CHAINLIT_APP_PATH).exists():
        st.error(f"❌ Chainlit app not found at: {CHAINLIT_APP_PATH}")
        return
    
    st.success("✅ Chainlit app found!")
    
    # Show launch command
    command = [
        sys.executable, "-m", "chainlit", "run", 
        CHAINLIT_APP_PATH,
        "--port", str(CHAINLIT_PORT),
        "--host", CHAINLIT_HOST,
        "--headless"
    ]
    
    st.code(" ".join(command), language="bash")
    
    if st.button("🚀 Launch Chainlit (Replace Streamlit)", type="primary"):
        st.info("Launching Chainlit...")
        time.sleep(2)
        
        try:
            # This replaces the current process - causes health check issues!
            os.execv(sys.executable, command)
        except Exception as e:
            st.error(f"Failed to launch: {e}")

def approach_2_advanced_subprocess():
    """
    Approach 2: Advanced Subprocess Management
    
    Features:
    - Real-time log streaming
    - Process management
    - Resource monitoring
    - Log persistence
    """
    st.title("🔧 Advanced Chainlit Process Manager")
    
    # Initialize advanced session state
    if 'process_logs' not in st.session_state:
        st.session_state.process_logs = []
        st.session_state.process_stats = {}
        st.session_state.log_level = "INFO"
    
    # Advanced controls
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("▶️ Start", disabled=st.session_state.get('chainlit_running', False)):
            start_with_monitoring()
    
    with col2:
        if st.button("⏹️ Stop", disabled=not st.session_state.get('chainlit_running', False)):
            stop_with_cleanup()
    
    with col3:
        if st.button("📊 Stats"):
            show_process_stats()
    
    with col4:
        log_level = st.selectbox("Log Level", ["DEBUG", "INFO", "WARNING", "ERROR"], 
                                index=1, label_visibility="collapsed")
        st.session_state.log_level = log_level
    
    # Process information
    if st.session_state.get('chainlit_process'):
        process = st.session_state.chainlit_process
        if process.poll() is None:
            st.success(f"✅ Running (PID: {process.pid})")
        else:
            st.error(f"❌ Exited (Code: {process.returncode})")
    
    # Advanced log viewer with filtering
    if st.session_state.process_logs:
        st.subheader("📋 Process Logs")
        
        # Log filters
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("Filter logs", placeholder="Search...")
        with col2:
            if st.button("Clear Logs"):
                st.session_state.process_logs = []
        
        # Display filtered logs
        filtered_logs = [log for log in st.session_state.process_logs 
                        if search_term.lower() in log.lower()]
        
        log_container = st.container()
        with log_container:
            for log in filtered_logs[-50:]:  # Show last 50 logs
                if "[ERROR]" in log:
                    st.error(log)
                elif "[WARNING]" in log:
                    st.warning(log)
                else:
                    st.text(log)

def approach_3_multi_port_iframe():
    """
    Approach 3: Multi-Port iframe Embedding
    
    Features:
    - Multiple Chainlit instances
    - Port management
    - Load balancing concepts
    """
    st.title("🖼️ Multi-Port Chainlit Deployment")
    
    st.info("""
    This approach demonstrates running multiple Chainlit instances on different ports.
    Useful for A/B testing or serving different models.
    """)
    
    # Port configuration
    ports = {
        "Primary": 8502,
        "Secondary": 8503,
        "Testing": 8504
    }
    
    # Instance selector
    selected_instance = st.selectbox("Select Instance:", list(ports.keys()))
    selected_port = ports[selected_instance]
    
    # Control buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(f"Start {selected_instance}"):
            start_chainlit_on_port(selected_port)
    
    with col2:
        if st.button(f"Stop {selected_instance}"):
            stop_chainlit_on_port(selected_port)
    
    with col3:
        if st.button("Stop All"):
            for port in ports.values():
                stop_chainlit_on_port(port)
    
    # Display status for all ports
    st.subheader("Instance Status")
    for name, port in ports.items():
        if check_port_status(port):
            st.success(f"✅ {name} (Port {port}): Running")
        else:
            st.error(f"❌ {name} (Port {port}): Stopped")
    
    # Embed selected instance
    if check_port_status(selected_port):
        st.subheader(f"Connected to {selected_instance} Instance")
        
        iframe_html = f"""
        <iframe 
            src="http://localhost:{selected_port}" 
            width="100%" 
            height="600" 
            style="border: 2px solid #ccc; border-radius: 8px;">
        </iframe>
        """
        
        components.html(iframe_html, height=620)
    else:
        st.warning(f"Start the {selected_instance} instance to see the interface")

# Helper functions for advanced approaches

def start_with_monitoring():
    """Start Chainlit with advanced monitoring"""
    try:
        command = [
            sys.executable, "-m", "chainlit", "run", 
            CHAINLIT_APP_PATH,
            "--port", "8502",
            "--host", "0.0.0.0",
            "--headless"
        ]
        
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        st.session_state.chainlit_process = process
        st.session_state.chainlit_running = True
        st.session_state.process_start_time = datetime.now()
        
        # Start monitoring thread
        monitor_thread = threading.Thread(
            target=monitor_process_output,
            args=(process,),
            daemon=True
        )
        monitor_thread.start()
        
        add_log(f"Process started with PID {process.pid}", "INFO")
        
    except Exception as e:
        add_log(f"Failed to start: {e}", "ERROR")
        st.session_state.chainlit_running = False

def stop_with_cleanup():
    """Stop Chainlit with proper cleanup"""
    if 'chainlit_process' in st.session_state:
        process = st.session_state.chainlit_process
        try:
            process.terminate()
            process.wait(timeout=5)
            add_log("Process terminated gracefully", "INFO")
        except subprocess.TimeoutExpired:
            process.kill()
            add_log("Process killed forcefully", "WARNING")
        except Exception as e:
            add_log(f"Error stopping process: {e}", "ERROR")
        
        st.session_state.chainlit_running = False

def monitor_process_output(process):
    """Monitor and log process output"""
    try:
        for line in iter(process.stdout.readline, ''):
            if line:
                add_log(line.strip(), "INFO")
    except Exception as e:
        add_log(f"Monitor error: {e}", "ERROR")

def add_log(message, level="INFO"):
    """Add timestamped log entry"""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    log_entry = f"[{timestamp}] [{level}] {message}"
    
    if 'process_logs' not in st.session_state:
        st.session_state.process_logs = []
    
    st.session_state.process_logs.append(log_entry)
    
    # Keep only last 1000 logs
    if len(st.session_state.process_logs) > 1000:
        st.session_state.process_logs = st.session_state.process_logs[-1000:]

def show_process_stats():
    """Show process statistics"""
    if 'chainlit_process' in st.session_state and st.session_state.chainlit_process:
        process = st.session_state.chainlit_process
        if process.poll() is None:
            try:
                # Get process info (platform-dependent)
                import psutil
                p = psutil.Process(process.pid)
                
                stats = {
                    "CPU %": p.cpu_percent(interval=1),
                    "Memory (MB)": p.memory_info().rss / 1024 / 1024,
                    "Threads": p.num_threads(),
                    "Status": p.status(),
                    "Create Time": datetime.fromtimestamp(p.create_time()).strftime("%Y-%m-%d %H:%M:%S")
                }
                
                st.json(stats)
            except ImportError:
                st.info("Install `psutil` for detailed process statistics")
            except Exception as e:
                st.error(f"Could not get stats: {e}")

def start_chainlit_on_port(port):
    """Start Chainlit on specific port"""
    # Implementation would be similar to start_with_monitoring
    # but with port parameter
    st.info(f"Starting Chainlit on port {port}...")
    # ... implementation ...

def stop_chainlit_on_port(port):
    """Stop Chainlit on specific port"""
    # Implementation would track processes by port
    st.info(f"Stopping Chainlit on port {port}...")
    # ... implementation ...

def check_port_status(port):
    """Check if port is in use"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

def main():
    """Main application with approach selector"""
    st.set_page_config(
        page_title="Chainlit Advanced Deployment",
        page_icon="🔬",
        layout="wide"
    )
    
    st.title("🔬 Chainlit Advanced Deployment Strategies")
    st.markdown("*Educational reference implementation*")
    
    # Approach selector
    approach = st.selectbox(
        "Select Deployment Approach:",
        [
            "1. Direct Process Replacement (Legacy)",
            "2. Advanced Subprocess Management",
            "3. Multi-Port iframe Deployment"
        ]
    )
    
    st.markdown("---")
    
    # Route to selected approach
    if "Direct Process" in approach:
        approach_1_direct_replacement()
    elif "Advanced Subprocess" in approach:
        approach_2_advanced_subprocess()
    elif "Multi-Port" in approach:
        approach_3_multi_port_iframe()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 12px;">
        For production use, see the main <code>streamlit_hoster.py</code> implementation.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
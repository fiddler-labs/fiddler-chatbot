"""
Fiddler AI Assistant - Comprehensive Streamlit-Chainlit Host
Production-ready solution with multiple deployment strategies for Streamlit Cloud

This consolidated solution provides three deployment approaches:
1. Hybrid Host with iframe Embedding (Recommended for cloud)
2. Advanced Subprocess Management (For monitoring & debugging)
3. Direct Process Replacement (Local development only)

Author: Fiddler AI Team
Version: 2.0.0 - Consolidated Edition
"""

import os
import sys
import subprocess
import streamlit as st
import streamlit.components.v1 as components
import time
import atexit
import socket
import threading
import json
from pathlib import Path
from typing import Tuple, Optional
from datetime import datetime

# ===== CONFIGURATION =====
REQUIRED_ENV_VARS = ["OPENAI_API_KEY", "FIDDLER_API_KEY", "FIDDLER_APP_ID"]
CHAINLIT_APP_PATH = "src/chatbot_chainlit.py"
CHAINLIT_PORT = 8000
CHAINLIT_HOST = "0.0.0.0"

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
    """Validate environment configuration"""
    errors = []
    warnings = []
    chainlit_version = None
    
    # Check Chainlit app exists
    if not Path(CHAINLIT_APP_PATH).exists():
        errors.append(f"Chainlit app not found at: {CHAINLIT_APP_PATH}")
    
    # Check required environment variables
    missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing_vars:
        errors.append(f"Missing environment variables: {', '.join(missing_vars)}")
    
    # Check dependencies
    try:
        import chainlit
        chainlit_version = chainlit.__version__
    except ImportError:
        errors.append("Chainlit is not installed. Add 'chainlit' to requirements.txt")
    
    # Check other dependencies
    import importlib.util
    required_packages = [
        ("langchain_core", "LangChain core"),
        ("langgraph", "LangGraph"),
        ("fiddler_langgraph", "Fiddler LangGraph client")
    ]
    
    for package_name, display_name in required_packages:
        if importlib.util.find_spec(package_name) is None:
            errors.append(f"{display_name} is not installed")
    
    # Check required source files
    required_files = [
        "src/system_instructions.md",
        "src/agentic_tools/state_data_model.py",
        "src/agentic_tools/rag.py",
        "config.py"
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            errors.append(f"Required file not found: {file_path}")
    
    return errors, warnings, chainlit_version

def start_chainlit_subprocess(port: int = CHAINLIT_PORT) -> Tuple[bool, str]:
    """Start Chainlit as subprocess"""
    global chainlit_process
    
    try:
        cleanup_chainlit()
        
        command = [
            sys.executable, "-m", "chainlit", "run", 
            CHAINLIT_APP_PATH,
            "--port", str(port),
            "--host", CHAINLIT_HOST,
            "--headless"
        ]
        
        chainlit_process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        return True, f"Chainlit started on port {port} with PID {chainlit_process.pid}"
        
    except Exception as e:
        return False, f"Failed to start Chainlit: {str(e)}"

def check_chainlit_health(port: int = CHAINLIT_PORT) -> Tuple[bool, str]:
    """Check Chainlit health"""
    global chainlit_process
    
    if chainlit_process is None:
        return False, "Not started"
    
    if chainlit_process.poll() is not None:
        return False, f"Process exited with code {chainlit_process.returncode}"
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            return True, "Running"
        else:
            return False, "Port not responding"
    except Exception as e:
        return False, f"Health check failed: {str(e)}"

def check_port_status(port: int) -> bool:
    """Check if port is active"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result == 0
    except:
        return False

def add_log(message: str, level: str = "INFO"):
    """Add timestamped log entry"""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    log_entry = f"[{timestamp}] [{level}] {message}"
    
    if 'process_logs' not in st.session_state:
        st.session_state.process_logs = []
    
    st.session_state.process_logs.append(log_entry)
    
    # Keep only last 1000 logs
    if len(st.session_state.process_logs) > 1000:
        st.session_state.process_logs = st.session_state.process_logs[-1000:]

def monitor_process_output(process):
    """Monitor and log process output"""
    try:
        for line in iter(process.stdout.readline, ''):
            if line:
                add_log(line.strip(), "INFO")
    except Exception as e:
        add_log(f"Monitor error: {e}", "ERROR")

# ===== DEPLOYMENT APPROACHES =====

def approach_1_hybrid_iframe():
    """
    Approach 1: Hybrid iframe Embedding (Recommended)
    Best for Streamlit Cloud deployment with health check compliance
    """
    st.title("🚀 Hybrid iframe Deployment (Recommended)")
    
    # Initialize session state
    if 'chainlit_started' not in st.session_state:
        st.session_state.chainlit_started = False
        st.session_state.startup_attempted = False
    
    # Auto-start on first load
    if not st.session_state.startup_attempted:
        st.session_state.startup_attempted = True
        errors, _, _ = validate_environment()
        
        if not errors:
            success, message = start_chainlit_subprocess()
            if success:
                st.session_state.chainlit_started = True
                time.sleep(3)
    
    # Check current status
    errors, warnings, chainlit_version = validate_environment()
    chainlit_healthy, health_status = check_chainlit_health()
    
    # Status display
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        if errors:
            st.error("❌ Environment Issues")
            for error in errors:
                st.error(f"• {error}")
        else:
            st.success("✅ Environment OK")
            if chainlit_version:
                st.info(f"Chainlit v{chainlit_version}")
    
    with col2:
        if chainlit_healthy:
            st.success(f"✅ Chainlit: {health_status}")
        else:
            st.error(f"❌ Chainlit: {health_status}")
    
    with col3:
        if st.button("🔄 Restart"):
            with st.spinner("Restarting..."):
                success, message = start_chainlit_subprocess()
                if success:
                    st.session_state.chainlit_started = True
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(message)
    
    # Main content
    if errors:
        st.error("❌ **Environment Setup Required**")
        st.markdown("""
        **Required Environment Variables:**
        ```
        OPENAI_API_KEY = "your-openai-api-key"
        FIDDLER_API_KEY = "your-fiddler-api-key"  
        FIDDLER_APP_ID = "your-fiddler-app-id"
        ```
        
        **Key Dependencies:**
        ```
        streamlit>=1.28.0
        chainlit>=1.0.0
        langchain>=0.3.0
        langgraph>=0.5.0
        fiddler-langgraph
        ```
        """)
        
    elif not chainlit_healthy:
        st.warning("⚠️ **Chainlit Starting Up**")
        with st.spinner("Initializing Chainlit..."):
            if not st.session_state.chainlit_started:
                success, message = start_chainlit_subprocess()
                if success:
                    st.session_state.chainlit_started = True
                    time.sleep(3)
                    st.rerun()
                else:
                    st.error(f"Failed to start: {message}")
            else:
                progress_bar = st.progress(0)
                for i in range(100):
                    progress_bar.progress(i + 1)
                    time.sleep(0.02)
                st.rerun()
    
    else:
        st.success("✅ **Fiddler AI Assistant is Ready**")
        
        # Determine deployment context
        is_cloud = os.getenv("STREAMLIT_SHARING_MODE") or "streamlit.app" in os.getenv("HOSTNAME", "")
        
        if is_cloud:
            # Cloud deployment - provide direct link
            st.info("🌐 **Running in Streamlit Cloud** - Access via direct link")
            
            current_url = st.get_option("browser.serverAddress") or "your-app-url"
            # For cloud, construct the external URL
            if "streamlit.app" in current_url:
                # Streamlit Cloud external URL construction
                chainlit_url = current_url.replace("8501", "8000")
            else:
                chainlit_url = f"https://{current_url.replace(':8501', ':8000').replace('http://', '').replace('https://', '')}"
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(f"""
                <a href="{chainlit_url}" target="_blank" style="
                    display: inline-block;
                    padding: 12px 24px;
                    background-color: #FF6B6B;
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: bold;
                    text-align: center;
                    width: 100%;
                    box-sizing: border-box;
                ">🚀 Open Fiddler AI Assistant</a>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("📋 Copy URL", use_container_width=True):
                    st.code(chainlit_url)
                    st.success("URL ready to copy!")
            
            st.markdown("**Direct URL:**")
            st.code(chainlit_url)
            
        else:
            # Local development - iframe embedding
            chainlit_url = f"http://localhost:{CHAINLIT_PORT}"
            st.info("🖥️ **Local Development** - Embedded interface")
            
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
            
            components.html(iframe_html, height=720)
    
    # Auto-refresh if needed
    if not chainlit_healthy and not errors and st.session_state.chainlit_started:
        time.sleep(5)
        st.rerun()

def approach_2_advanced_monitoring():
    """
    Approach 2: Advanced Subprocess Management
    Best for development, debugging, and monitoring
    """
    st.title("🔧 Advanced Process Management")
    
    # Initialize session state
    if 'process_logs' not in st.session_state:
        st.session_state.process_logs = []
        st.session_state.process_stats = {}
        st.session_state.log_level = "INFO"
    
    # Control panel
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("▶️ Start", disabled=st.session_state.get('advanced_running', False)):
            start_with_monitoring()
    
    with col2:
        if st.button("⏹️ Stop", disabled=not st.session_state.get('advanced_running', False)):
            stop_with_cleanup()
    
    with col3:
        if st.button("📊 Stats"):
            show_process_stats()
    
    with col4:
        log_level = st.selectbox("Log Level", ["DEBUG", "INFO", "WARNING", "ERROR"], 
                                index=1, label_visibility="collapsed")
        st.session_state.log_level = log_level
    
    # Process status
    if st.session_state.get('chainlit_process'):
        process = st.session_state.chainlit_process
        if process.poll() is None:
            st.success(f"✅ Running (PID: {process.pid})")
            
            # Embed if running
            chainlit_url = f"http://localhost:{CHAINLIT_PORT}"
            if check_port_status(CHAINLIT_PORT):
                st.subheader("📱 Live Interface")
                iframe_html = f"""
                <iframe 
                    src="{chainlit_url}" 
                    width="100%" 
                    height="600" 
                    style="border: 2px solid #4CAF50; border-radius: 8px;">
                </iframe>
                """
                components.html(iframe_html, height=620)
        else:
            st.error(f"❌ Exited (Code: {process.returncode})")
    
    # Advanced log viewer
    if st.session_state.process_logs:
        st.subheader("📋 Process Logs")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("Filter logs", placeholder="Search...")
        with col2:
            if st.button("Clear Logs"):
                st.session_state.process_logs = []
                st.rerun()
        
        # Display filtered logs
        filtered_logs = [log for log in st.session_state.process_logs 
                        if search_term.lower() in log.lower()]
        
        log_container = st.container()
        with log_container:
            for log in filtered_logs[-50:]:
                if "[ERROR]" in log:
                    st.error(log)
                elif "[WARNING]" in log:
                    st.warning(log)
                else:
                    st.text(log)

def approach_3_direct_replacement():
    """
    Approach 3: Direct Process Replacement
    WARNING: Causes health check failures on Streamlit Cloud
    Use only for local development
    """
    st.title("⚠️ Direct Process Replacement (Local Only)")
    
    st.warning("""
    **⚠️ WARNING**: This approach causes health check failures on Streamlit Cloud!
    
    Error: `Get "http://localhost:8501/healthz": connection refused`
    
    **Use only for local development where health checks are not required.**
    """)
    
    # Validate environment
    errors, _, chainlit_version = validate_environment()
    
    if errors:
        st.error("❌ Environment Issues:")
        for error in errors:
            st.error(f"• {error}")
        return
    
    st.success("✅ Environment validated")
    if chainlit_version:
        st.info(f"Chainlit v{chainlit_version}")
    
    # Show command that will be executed
    command = [
        sys.executable, "-m", "chainlit", "run", 
        CHAINLIT_APP_PATH,
        "--port", str(CHAINLIT_PORT),
        "--host", CHAINLIT_HOST,
        "--headless"
    ]
    
    st.subheader("🔧 Launch Command")
    st.code(" ".join(command), language="bash")
    
    # Launch button
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("🚀 Launch Chainlit", type="primary"):
            st.info("Launching Chainlit... This will replace the current Streamlit process.")
            time.sleep(2)
            
            try:
                # This replaces the current process
                os.execv(sys.executable, command)
            except Exception as e:
                st.error(f"Failed to launch: {e}")
    
    with col2:
        st.info("**Note**: After launching, you'll need to refresh your browser to return to Streamlit.")

# ===== HELPER FUNCTIONS =====

def start_with_monitoring():
    """Start Chainlit with advanced monitoring"""
    try:
        command = [
            sys.executable, "-m", "chainlit", "run", 
            CHAINLIT_APP_PATH,
            "--port", str(CHAINLIT_PORT),
            "--host", CHAINLIT_HOST,
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
        st.session_state.advanced_running = True
        st.session_state.process_start_time = datetime.now()
        
        # Start monitoring thread
        monitor_thread = threading.Thread(
            target=monitor_process_output,
            args=(process,),
            daemon=True
        )
        monitor_thread.start()
        
        add_log(f"Process started with PID {process.pid}", "INFO")
        st.success("Started successfully!")
        
    except Exception as e:
        add_log(f"Failed to start: {e}", "ERROR")
        st.session_state.advanced_running = False
        st.error(f"Failed to start: {e}")

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
        
        st.session_state.advanced_running = False
        st.success("Stopped successfully!")

def show_process_stats():
    """Show detailed process statistics"""
    if 'chainlit_process' in st.session_state and st.session_state.chainlit_process:
        process = st.session_state.chainlit_process
        if process.poll() is None:
            try:
                import psutil
                p = psutil.Process(process.pid)
                
                stats = {
                    "PID": process.pid,
                    "CPU %": round(p.cpu_percent(interval=1), 2),
                    "Memory (MB)": round(p.memory_info().rss / 1024 / 1024, 2),
                    "Threads": p.num_threads(),
                    "Status": p.status(),
                    "Started": datetime.fromtimestamp(p.create_time()).strftime("%Y-%m-%d %H:%M:%S"),
                    "Command": " ".join(p.cmdline())
                }
                
                st.json(stats)
            except ImportError:
                st.info("Install `psutil` for detailed process statistics: `pip install psutil`")
            except Exception as e:
                st.error(f"Could not get stats: {e}")
        else:
            st.error("Process is not running")
    else:
        st.warning("No process to monitor")

def render_sidebar():
    """Render sidebar with configuration and status"""
    with st.sidebar:
        st.subheader("⚙️ Configuration")
        
        # Environment variables status
        st.markdown("**Environment Variables:**")
        for var in REQUIRED_ENV_VARS:
            if os.getenv(var):
                st.success(f"✅ {var}")
            else:
                st.error(f"❌ {var}")
        
        st.markdown("---")
        
        # File paths
        st.markdown("**File Paths:**")
        st.code(f"App: {CHAINLIT_APP_PATH}")
        st.code(f"Port: {CHAINLIT_PORT}")
        st.code(f"Host: {CHAINLIT_HOST}")
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("**Quick Actions:**")
        if st.button("🔄 Force Restart", use_container_width=True):
            cleanup_chainlit()
            st.rerun()
        
        if st.button("🧹 Clear Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

def main():
    """Main application with approach selector"""
    
    # Page configuration
    st.set_page_config(
        page_title="Fiddler AI Assistant - Deployment Hub",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("🤖 Fiddler AI Assistant - Deployment Hub")
    st.markdown("*Production-ready Streamlit-Chainlit integration with multiple deployment strategies*")
    
    # Render sidebar
    render_sidebar()
    
    # Deployment approach selector
    st.subheader("🚀 Select Deployment Approach")
    
    approach = st.selectbox(
        "Choose the deployment strategy that best fits your needs:",
        [
            "1. 🏆 Hybrid iframe (Recommended for Streamlit Cloud)",
            "2. 🔧 Advanced Monitoring (Development & Debugging)", 
            "3. ⚠️ Direct Replacement (Local Development Only)"
        ],
        help="Each approach has different benefits and use cases. See documentation for details."
    )
    
    st.markdown("---")
    
    # Route to selected approach
    if "Hybrid iframe" in approach:
        approach_1_hybrid_iframe()
    elif "Advanced Monitoring" in approach:
        approach_2_advanced_monitoring()
    elif "Direct Replacement" in approach:
        approach_3_direct_replacement()
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; font-size: 14px;">
        Fiddler AI Assistant v2.0.0 | 
        <a href="?refresh={time.time()}" style="color: #FF6B6B;">Force Refresh</a> |
        Session: {datetime.now().strftime('%H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
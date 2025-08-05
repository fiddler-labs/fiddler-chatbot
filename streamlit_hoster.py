"""
Simple Streamlit-to-Chainlit Launcher for Streamlit Cloud

This is the RECOMMENDED approach: directly launch Chainlit on port 8501.
This script will replace the Streamlit process with Chainlit, which is exactly
what Streamlit Cloud expects.

Usage: Deploy this as your main app.py on Streamlit Cloud
"""

import os
import sys
import subprocess
import streamlit as st
from pathlib import Path
import time

# Configuration - UPDATE THESE PATHS FOR YOUR PROJECT
CHAINLIT_APP_PATH = "src/chatbot_chainlit.py"  # Path to your Chainlit application
REQUIRED_ENV_VARS = ["OPENAI_API_KEY", "FIDDLER_API_KEY", "FIDDLER_APP_ID"]  # Add your required env vars

def validate_environment():
    """Validate that the environment is properly configured"""
    errors = []
    warnings = []
    
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
        st.success(f"✅ Chainlit {chainlit.__version__} is installed")
    except ImportError:
        errors.append("Chainlit is not installed. Add 'chainlit' to your requirements.txt")
    
    return errors, warnings

def show_pre_launch_info():
    """Display information before launching Chainlit"""
    st.title("🚀 Fiddler Chainlit Chatbot Launcher")
    
    st.markdown("""
    ### About This Deployment
    
    This Streamlit app serves as a launcher for your Chainlit application. When you click "Launch Chainlit" below, 
    this Streamlit interface will be replaced by your Chainlit chatbot running on the same port (8501).
    
    **What happens next:**
    1. The current Streamlit process will be terminated
    2. Chainlit will start on port 8501 (the same port Streamlit Cloud expects)
    3. Your chatbot will be available at the same URL as this page
    """)
    
    # Environment validation
    st.subheader("🔍 Environment Check")
    errors, warnings = validate_environment()
    
    if errors:
        st.error("❌ Environment validation failed:")
        for error in errors:
            st.error(f"• {error}")
        st.stop()
    
    if warnings:
        st.warning("⚠️ Warnings:")
        for warning in warnings:
            st.warning(f"• {warning}")
    
    if not errors:
        st.success("✅ Environment validation passed!")
    
    # Show configuration
    st.subheader("⚙️ Configuration")
    st.info(f"**Chainlit App:** `{CHAINLIT_APP_PATH}`")
    st.info(f"**Port:** `8501` (Streamlit Cloud default)")
    st.info(f"**Host:** `0.0.0.0` (allow external connections)")
    
    # Show the command that will be executed
    command = [
        sys.executable, "-m", "chainlit", "run", 
        CHAINLIT_APP_PATH,
        "--port", "8501",
        "--host", "0.0.0.0", 
        "--headless"
    ]
    
    st.subheader("🛠️ Launch Command")
    st.code(" ".join(command), language="bash")
    
    return True

def launch_chainlit():
    """Launch Chainlit and replace the current Streamlit process"""
    
    # Final validation
    if not Path(CHAINLIT_APP_PATH).exists():
        st.error(f"❌ Cannot launch: {CHAINLIT_APP_PATH} not found")
        return False
    
    try:
        # Show launch sequence
        st.success("🚀 Launching Chainlit...")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simulate progress for user feedback
        for i in range(100):
            progress_bar.progress(i + 1)
            if i < 30:
                status_text.text("Preparing Chainlit environment...")
            elif i < 60:
                status_text.text("Loading your chatbot configuration...")
            elif i < 90:
                status_text.text("Starting Chainlit server...")
            else:
                status_text.text("Transferring control to Chainlit...")
            time.sleep(0.02)  # Small delay for visual effect
        
        st.success("✅ Environment ready! Launching Chainlit now...")
        time.sleep(1)
        
        # Prepare the command to launch Chainlit
        command = [
            sys.executable, "-m", "chainlit", "run", 
            CHAINLIT_APP_PATH,
            "--port", "8501",
            "--host", "0.0.0.0",
            "--headless"  # Prevent auto-opening browser
        ]
        
        # Replace current process with Chainlit
        # This is the key: we're not running a subprocess, we're replacing this process
        os.execv(sys.executable, command)
        
    except Exception as e:
        st.error(f"❌ Failed to launch Chainlit: {str(e)}")
        st.error("Please check the error details above and your configuration.")
        return False

def main():
    """Main application"""
    
    # Page configuration
    st.set_page_config(
        page_title="Chainlit Launcher",
        page_icon="🚀",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Check if we should auto-launch (useful for direct deployment)
    auto_launch = st.query_params.get("auto_launch", "false").lower() == "true"
    
    if auto_launch:
        st.write("🔄 Auto-launching Chainlit...")
        launch_chainlit()
    else:
        # Show the pre-launch interface
        if show_pre_launch_info():
            
            st.markdown("---")
            
            # Large, prominent launch button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Launch Chainlit Chatbot", 
                           type="primary", 
                           use_container_width=True,
                           help="Click to replace this interface with your Chainlit chatbot"):
                    launch_chainlit()
            
            # Additional options
            st.markdown("---")
            st.subheader("🔧 Advanced Options")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🧪 Test Environment", use_container_width=True):
                    st.info("Re-running environment validation...")
                    validate_environment()
                    st.experimental_rerun()
            
            with col2:
                if st.button("📋 View Logs", use_container_width=True):
                    st.info("For detailed logs, check the Streamlit Cloud logs after launching Chainlit.")
            
            # Help section
            with st.expander("❓ Need Help?"):
                st.markdown("""
                **Common Issues:**
                
                1. **Environment Variables Missing**: Make sure all required environment variables are set in Streamlit Cloud's secrets management.
                
                2. **Chainlit App Not Found**: Ensure your Chainlit app is at the correct path specified above.
                
                3. **Dependencies Missing**: Make sure `chainlit` and all your app dependencies are listed in `requirements.txt`.
                
                4. **Port Issues**: This launcher automatically uses port 8501, which is what Streamlit Cloud expects.
                
                **For more help, check the deployment guide or contact support.**
                """)

if __name__ == "__main__":
    main()
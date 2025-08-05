# Deploying Chainlit on Streamlit Cloud - Complete Guide

This guide provides a comprehensive solution to deploy your Chainlit application on Streamlit Cloud, overcoming platform limitations and health check issues.

## 🎯 Problem Statement

Streamlit Cloud expects applications to:
- Run via `streamlit run app.py` on port 8501
- Respond to health checks at `/healthz`
- Keep the Streamlit process alive

Chainlit applications typically:
- Run via `chainlit run app.py` on port 8000
- Don't provide Streamlit health check endpoints
- Replace the parent process when launched

## 💡 Solution Overview

We've developed a **hybrid hosting approach** that keeps Streamlit alive for health checks while running Chainlit as a subprocess and embedding it seamlessly via iframe.

## ✅ Key Benefits

- **Health checks pass** - Streamlit stays alive and responsive
- **Seamless integration** - Chainlit appears embedded in Streamlit
- **Auto-start capability** - Chainlit launches automatically
- **Monitoring & control** - Real-time status and restart options
- **Clean user experience** - Professional interface with error handling

## 🚀 Quick Start

### Step 1: File Structure
```
your-project/
├── streamlit_hoster.py       # Main hybrid host app
├── src/
│   └── chatbot_chainlit.py  # Your existing Chainlit app
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── requirements.txt         # All dependencies
└── docs/
    └── feature-streamlit_chainlit_hosting.md  # This guide
```

### Step 2: Configure the Host App

Update these settings in `streamlit_hoster.py`:

```python
# Path to your Chainlit application
CHAINLIT_APP_PATH = "src/chatbot_chainlit.py"

# Required environment variables
REQUIRED_ENV_VARS = ["OPENAI_API_KEY", "FIDDLER_API_KEY", "FIDDLER_APP_ID"]

# Port configuration (don't change unless necessary)
CHAINLIT_PORT = 8000  # Chainlit runs here
# Streamlit automatically uses 8501
```

### Step 3: Update Dependencies

Add to your `requirements.txt`:
```txt
# Core frameworks
streamlit>=1.28.0
chainlit>=1.0.0

# Your existing Chainlit dependencies...
```

### Step 4: Set Environment Variables

In Streamlit Cloud → App Settings → Secrets:
```toml
OPENAI_API_KEY = "your-openai-key"
FIDDLER_API_KEY = "your-fiddler-key"
FIDDLER_APP_ID = "your-fiddler-app-id"
# Add other required variables...
```

### Step 5: Deploy

1. **Rename the host app**: `mv streamlit_hoster.py app.py`
2. **Push to GitHub**
3. **Deploy on Streamlit Cloud** pointing to `app.py`
4. **Wait for startup** (1-2 minutes for full initialization)

## 🎮 How It Works

1. **Streamlit starts** and validates the environment
2. **Chainlit auto-launches** as a subprocess on port 8000
3. **Health monitoring** checks Chainlit status continuously
4. **iframe embedding** displays Chainlit within Streamlit
5. **Users interact** with your chatbot seamlessly

## 🔍 Features

### Real-Time Status Monitoring
- Environment validation
- Chainlit process health
- Automatic error detection
- Visual status indicators

### Control Panel (Sidebar)
- **System Status**: Live health indicators
- **Restart Button**: Quick recovery from issues
- **Test Button**: Re-validate environment
- **Configuration Info**: View current settings

### Error Handling
- Clear error messages
- Setup instructions when issues detected
- Auto-retry logic for startup
- Fallback direct link to Chainlit

### Professional UI
- Clean, modern interface
- Responsive design
- Loading states
- Success/error feedback

## 🚨 Troubleshooting

### Common Issues & Solutions

#### 1. Health Check Errors
**Error**: `connection refused on port 8501`

**Solution**: Use the hybrid host approach (current solution) instead of direct replacement.

#### 2. Chainlit Won't Start
**Symptoms**: Status shows "Not started" or "Process exited"

**Solutions**:
- Check sidebar for specific error messages
- Verify `CHAINLIT_APP_PATH` is correct
- Ensure all environment variables are set
- Check Streamlit Cloud logs for details

#### 3. iframe Shows Empty
**Symptoms**: Blank space where Chainlit should appear

**Solutions**:
- Wait 1-2 minutes for full startup
- Click "Open Chainlit directly" link
- Use the Restart button in sidebar
- Check if Chainlit has startup errors

#### 4. Environment Issues
**Symptoms**: Red error messages on startup

**Solutions**:
- Verify all dependencies in `requirements.txt`
- Set all required environment variables
- Ensure Chainlit app exists at specified path

### Debug Commands

Test locally before deploying:
```bash
# Test the hybrid host
streamlit run streamlit_hoster.py

# Test Chainlit standalone
chainlit run src/chatbot_chainlit.py --port 8000

# Check dependencies
pip list | grep -E "streamlit|chainlit"
```

## 🔧 Configuration Files

### `.streamlit/config.toml`
```toml
[server]
port = 8501
address = "0.0.0.0"
enableCORS = true
headless = true

[client]
showErrorDetails = "full"
toolbarMode = "minimal"

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

### Complete `requirements.txt` Example
```txt
# Core frameworks
streamlit>=1.28.0
chainlit>=1.0.0

# LangChain ecosystem
langchain>=0.1.0
langchain-openai>=0.1.0
langchain-core>=0.1.0
langchain-community>=0.0.20
langgraph>=0.1.0

# AI/ML
openai>=1.0.0

# Database
cassandra-driver>=3.25.0

# Utilities
python-dotenv>=1.0.0
pydantic>=2.0.0
pandas>=2.0.0
numpy>=1.24.0
requests>=2.28.0
typing-extensions>=4.0.0
```

## 🎯 Advanced Usage

### Auto-Refresh Configuration
The app automatically refreshes every 30 seconds if Chainlit isn't healthy. To disable:
```python
# In streamlit_hoster.py, comment out:
# if not chainlit_healthy and not errors:
#     time.sleep(5)
#     st.rerun()
```

### Custom Styling
Modify the iframe styling in the app:
```python
iframe_html = f"""
<iframe 
    src="{chainlit_url}" 
    width="100%" 
    height="700" 
    style="border: none; 
           border-radius: 8px; 
           box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
           /* Add custom styles here */"
    title="Your Custom Title">
</iframe>
"""
```

### Multiple Chainlit Apps
To support multiple apps, modify the configuration:
```python
CHAINLIT_APPS = {
    "default": "src/chatbot_chainlit.py",
    "assistant": "src/assistant_chainlit.py",
    "support": "src/support_bot.py"
}

# Add selector in UI
selected_app = st.selectbox("Choose App:", list(CHAINLIT_APPS.keys()))
CHAINLIT_APP_PATH = CHAINLIT_APPS[selected_app]
```

## 📊 Success Indicators

✅ **Deployment is successful when:**
- Streamlit page loads without errors
- Sidebar shows "✅ Environment OK"
- Status shows "✅ Chainlit: Running"
- Your chatbot interface appears in the main area
- You can interact with the chatbot normally
- No health check errors in Streamlit Cloud logs

## 🆘 Getting Help

1. **Check this guide** for solutions
2. **Review Streamlit Cloud logs**:
   - Go to your app dashboard
   - Click "Manage app" → "Logs"
   - Look for error patterns
3. **Test locally** to isolate issues
4. **Verify dependencies** are all listed
5. **Check environment variables** are set correctly

## 📚 Additional Resources

- [Chainlit Documentation](https://docs.chainlit.io/)
- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Chainlit Deployment Guide](https://docs.chainlit.io/deployment)
- [Streamlit Health Checks](https://docs.streamlit.io/knowledge-base/deploy/health-checks)

---

**Key Insight**: The hybrid approach solves the health check issue by keeping Streamlit alive while running Chainlit as a managed subprocess. This satisfies Streamlit Cloud's requirements while providing the full Chainlit experience.
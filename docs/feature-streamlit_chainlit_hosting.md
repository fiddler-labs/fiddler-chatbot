# Deploying Chainlit on Streamlit Cloud - Complete Guide

This guide provides multiple approaches to deploy your Chainlit application on Streamlit Cloud, bypassing the platform's native limitations.

## 🎯 Problem Statement

Streamlit Cloud expects applications to run via `streamlit run app.py` on port 8501, but Chainlit applications run via `chainlit run app.py` typically on port 8000. This creates a deployment incompatibility.

## 💡 Solution Overview

We create a Streamlit wrapper application (`app.py`) that launches your Chainlit application on the correct port, essentially "tricking" Streamlit Cloud into serving your Chainlit app.

## 🚀 Quick Start (Recommended Approach)

### Step 1: File Structure
```
your-project/
├── app.py                     # Use app_simple.py (renamed)
├── src/
│   └── chatbot_chainlit.py   # Your existing Chainlit app
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── requirements.txt          # All dependencies
└── DEPLOYMENT_GUIDE.md       # This file
```

### Step 4: Deploy to Streamlit Cloud
1. **Push to GitHub** with the new `app.py` as your main file
2. **Deploy on Streamlit Cloud** pointing to `app.py`
3. **Set environment variables** in Streamlit Cloud's secrets management
4. **Launch**: Visit your app URL and click "Launch Chainlit Chatbot"

## 📋 Detailed Approaches

### Approach 1: Direct Replacement (RECOMMENDED)
**File**: `app_simple.py` → `app.py`

**How it works**:
- Streamlit Cloud launches the wrapper app
- User clicks "Launch Chainlit" 
- The wrapper terminates itself and starts Chainlit on port 8501
- Chainlit takes over the same URL/port

**Pros**:
- ✅ Most reliable
- ✅ Clean user experience
- ✅ No port conflicts
- ✅ Uses the same URL

**Cons**:
- ⚠️ No way to return to Streamlit interface
- ⚠️ Manual launch step required

### Approach 2: Subprocess Management
**File**: `app.py` (full version with approach selection)

**How it works**:
- Runs Chainlit as a subprocess
- Provides Streamlit interface to monitor/control Chainlit
- Both run simultaneously

**Pros**:
- ✅ Can monitor Chainlit status
- ✅ Can restart Chainlit if needed
- ✅ Streamlit interface remains available

**Cons**:
- ⚠️ More complex
- ⚠️ Resource overhead
- ⚠️ Potential port conflicts

### Approach 3: iframe Embedding (EXPERIMENTAL)
**File**: `app.py` (full version)

**How it works**:
- Runs Chainlit on a different port
- Embeds Chainlit in Streamlit via iframe

**Pros**:
- ✅ Both interfaces available
- ✅ Seamless integration

**Cons**:
- ❌ May not work on Streamlit Cloud (networking restrictions)
- ❌ Complex networking setup
- ❌ Not recommended for production

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
```

### `requirements.txt` (Essential additions)
```txt
chainlit>=1.0.0
streamlit>=1.28.0
# Add your existing dependencies below
```

## 🔐 Environment Variables Setup

In Streamlit Cloud's App Settings → Secrets:

```toml
# Add your environment variables here
OPENAI_API_KEY = "your-openai-key"
FIDDLER_API_KEY = "your-fiddler-key"
FIDDLER_APP_ID = "your-fiddler-app-id"

# Add any other environment variables your Chainlit app needs
```

## 🚨 Troubleshooting

### Common Issues

1. **"Chainlit app not found"**
   - Verify the path in `CHAINLIT_APP_PATH` is correct
   - Ensure your Chainlit file is committed to your repository

2. **"Missing environment variables"**
   - Set all required environment variables in Streamlit Cloud's secrets
   - Update `REQUIRED_ENV_VARS` list in `app.py`

3. **"Import error: No module named 'chainlit'"**
   - Add `chainlit` to your `requirements.txt`
   - Ensure the version is compatible with your code

4. **"Port already in use"**
   - Use Approach 1 (Direct Replacement) instead of subprocess approaches
   - Ensure no other services are running on port 8501

5. **"App doesn't launch automatically"**
   - Click the "Launch Chainlit Chatbot" button in the Streamlit interface
   - Or use auto-launch: add `?auto_launch=true` to your URL

### Debug Steps

1. **Check Streamlit Cloud logs**:
   - Go to your app in Streamlit Cloud
   - Click "Manage app" → "Logs"
   - Look for error messages during startup

2. **Test locally first**:
   ```bash
   # Test the wrapper
   streamlit run app.py
   
   # Test Chainlit directly
   chainlit run src/chatbot_chainlit.py --port 8501
   ```

3. **Validate environment**:
   - Use the "Test Environment" button in the app
   - Check that all dependencies are installed

## 🎮 Advanced Usage

### Auto-Launch Mode
Add `?auto_launch=true` to your Streamlit Cloud URL to automatically launch Chainlit without user interaction:
```
https://your-app.streamlit.app/?auto_launch=true
```

### Custom Port Configuration
If you need to use a different port (advanced scenarios):
```python
# In app.py, modify:
CHAINLIT_PORT = 8502  # Or your preferred port
```

### Multiple Chainlit Apps
To support multiple Chainlit applications:
```python
# In app.py, add:
CHAINLIT_APPS = {
    "Chatbot": "src/chatbot_chainlit.py",
    "Assistant": "src/assistant_chainlit.py"
}
```

## 📚 Additional Resources

- [Chainlit Documentation](https://docs.chainlit.io/)
- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Chainlit Deployment Guide](https://docs.chainlit.io/deployment)

## 🔄 Migration from Existing Deployment

If you already have a working Chainlit app and want to deploy it on Streamlit Cloud:

1. **Backup your current deployment**
2. **Copy your Chainlit app** to the correct path structure
3. **Use `app_simple.py`** as your new `app.py`
4. **Update configuration** with your specific paths and environment variables
5. **Test locally** before deploying
6. **Deploy to Streamlit Cloud** and test the launch process

## 🤝 Support

If you encounter issues:

1. **Check this guide** for common solutions
2. **Review Streamlit Cloud logs** for specific error messages
3. **Test locally** to isolate the issue
4. **Verify all dependencies** are in `requirements.txt`
5. **Ensure environment variables** are properly set

---

**Success Indicator**: When working correctly, you should be able to visit your Streamlit Cloud URL, see the launcher interface, click "Launch Chainlit Chatbot", and have your Chainlit application appear at the same URL.
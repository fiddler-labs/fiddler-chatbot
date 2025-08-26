# Chainlit Migration

This document explains the migration of the Fiddler Agentic Chatbot from CLI to Chainlit interface.

## Overview

The chatbot has been extended to support Chainlit, a powerful UI framework for conversational AI applications. The Chainlit interface provides:

- A web-based chat interface - `http://localhost:8000`
- Session Tracking - Each conversation gets a unique session ID displayed in the welcome message.
- Tool Execution Display - When tools are called, they appear as collapsible steps in the UI.
- Streaming Responses - Responses stream token by token for better user experience.
- Error Handling - Errors are displayed gracefully in the chat interface.

## Key Changes from CLI version

- Decorator-Based Structure - The Chainlit version uses decorators to handle chat lifecycle:
  - `@cl.on_chat_start`: Initializes the chat session
  - `@cl.on_message`: Handles incoming messages
  - `@cl.on_chat_end`: Cleanup on session end

- Async/Await Pattern - All Chainlit handlers are async functions for better performance and streaming support.

- Session Management - Each chat session stores:
  - LLM instance
  - LangGraph workflow
  - Session ID for tracking

- Streaming Support - The implementation uses `astream` for real-time response streaming to the UI.

- Tool Visualization - Tool executions are displayed as steps in the UI for transparency.

---

## Files Created/Modified

- `src/chatbot_chainlit.py` : Main Chatbot implementation file containing Chainlit decorators for chat lifecycle management

- `.chainlit/config.toml` : Configuration file for Chainlit with:
  - Project metadata (name, description)
  - Feature toggles (file uploads, multimodal support)
  - UI customization options
  - Security settings

- `docs/chainlit_migration.md` : Comprehensive migration guide covering:
  - Architecture overview
  - Key changes from CLI version
  - Running instructions
  - Feature comparison

---

## Development and Debugging Checklist

Run with auto-reload enabled during development:

```bash
chainlit run src/chatbot_agentic.py -w
```

When ready to test:

1. Environment variables loaded (check `.env` file)
2. Dependencies installed (`uv pip install -e .`)
3. Cassandra connection available (check `src/agentic_tools/rag.py`)
4. Fiddler monitoring accessible (check `src/chatbot_chainlit.py`)
5. Port 8000 available (check `src/chatbot_chainlit.py`)

---

## Benefits

- **Tool transparency**: Visual tool execution steps
- **Multi-user support**: Built-in session isolation
- **Future-ready**: Easy to add file uploads, auth, etc.

## Next Steps (Potential enhancements)

- Add file upload support for documents
- Implement chat history persistence
- Add user authentication (e.g. API key)
- Custom UI branding
- Export conversation history
- Add a chat history feature

## Customization

See the [Chainlit documentation](https://docs.chainlit.io) for customization options:

- Themes
- Logos
- Authentication
- Custom UI elements

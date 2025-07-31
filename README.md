# Fiddler Chatbot

A RAG-based (Retrieval-Augmented Generation) chatbot application designed to answer questions about Fiddler AI's product documentation. The chatbot uses vector similarity search to retrieve relevant documentation snippets and generates contextual responses using OpenAI's GPT models.

## 🏗️ Project Status

> **Note**: This repository is currently under active development on a branch. Several sections are marked as WIP (Work in Progress) and will be updated post-cleanup.

## 🔍 Overview

The Fiddler Chatbot is built to provide intelligent, context-aware responses about Fiddler AI's platform and documentation. Key features include:

- **RAG Architecture**: Combines retrieval and generation for accurate, source-based responses
- **Vector Search**: Uses DataStax Cassandra for efficient similarity search
- **Real-time Monitoring**: Integrates with Fiddler platform for response quality tracking
- **Safety Guardrails**: Implements faithfulness and safety scoring
- **Monitoring Integration**: Fiddler LangGraph SDK
- **Interaction Interface**: CLI-based (Chainlit integration planned for later)

## 🚀 Installation

### Prerequisites

- Python 3.11+
- OpenAI API key
- DataStax Astra DB account and credentials
- Fiddler AI platform access (optional, for monitoring)
- Fiddler LangGraph (for agentic monitoring)

   ```bash
   uv pip install -i https://test.pypi.org/simple/ fiddler-langgraph --prerelease=allow
   ```

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/fiddler-labs/fiddler-chatbot.git
   cd fiddler-chatbot
   ```

2. **Install dependencies**

   ```bash
   # Using uv (recommended)
   uv sync

   # Or using pip / uv pip
   uv pip install .
   ```

3. **Environment Configuration**

   Create a `.env` file with required API keys by copying the `.env.template` file.
   Test the env by running the following command:

   ```bash
   uv run src/utils/test_agentic_env.py
   ```

4. **Run the new agentic application**

   ```bash
   uv run src/chatbot_agentic.py "hello" "what is the current time?" "quit"
   ```

5. **Running the older Streamlit Application**
   The application will be available at `http://localhost:8501`

   ```bash
   streamlit run chatbot.py
   ```

---

## Fiddler Agentic Monitoring Integration

The agentic chatbot application is fully integrated with Fiddler monitoring from the foundation phase:

- **Application Name**: "Agentic Documentation Chatbot - APP1"
- **Platform**: Fiddler Cloud Pre-production (`preprod.cloud.fiddler.ai`)
- **Monitoring Components**:
  - LangGraph workflow execution spans
  - ChatOpenAI LLM invocation tracking
  - Chatbot node execution monitoring
- **Session Tracking**: UUID-based conversation tracking with context preservation
- **Real-time Visibility**: All interactions visible in Fiddler web UI dashboard

### Expected Web UI Behavior

Based on current implementation, developers should expect to see:

- Three primary span types: `LangGraph`, `ChatOpenAI`, and `chatbot`
- Session IDs in shortened UUID format (e.g., `bf246607`, `b6a4fa2`, `528d3fe`)
- Event ingestion counts per span
- Agent classification showing named agents and unknown agents
- Real-time span status (Active/Inactive)

### Spans and Traces in Fiddler Web UI

Based on the monitoring dashboard, the following span types are automatically generated:

#### 1. **chatbot** Span

- **Purpose**: Tracks the main chatbot node execution
- **Session ID Format**: `528d3fe` (shortened UUID)
- **Represents**: The core chatbot logic flow

#### 2. **ChatOpenAI** Span

- **Purpose**: Tracks OpenAI API calls and responses
- **Session ID Format**: `b6a4fa2` (shortened UUID)
- **Represents**: LLM invocations and responses

#### 3. **LangGraph** Span

- **Purpose**: Tracks the overall LangGraph workflow execution
- **Session ID Format**: `bf246607` (shortened UUID)
- **Represents**: State transitions and graph execution

---

## Legacy Monitoring

The legacy chatbot application also integrates with Fiddler AI's platform for:

- **Response Quality**: Faithfulness scoring against source documents
- **Safety Monitoring**: Jailbreak attempt detection
- **Performance Metrics**: Response latency and token usage
- **User Feedback**: Like/dislike ratings and comments

---

### Development Methodology for Risk Mitigation

This project follows an iterative, verification-driven approach, emphasizing small, testable increments with validation at each stage,
avoiding large-scale development without proper testing.

- Each phase must be fully functional before proceeding
- All features must be tested and verified
- **Testing**: Mandatory verification at each major development milestone
- **Integration Issues**: Continuous integration testing with green-streamlit
- **Monitoring Failures**: Early integration of Fiddler monitoring to identify issues
- **Platform Compatibility**: Regular validation of Fiddler LangGraph SDK compatibility
- **Data Visibility**: Continuous monitoring of data flow to Fiddler platform

---

## 📄 License

This is a private internal tool for Fiddler AI use only. Not licensed for external use or distribution.

---

> **Note**: This README is actively being updated. Please check back for the latest information as we continue to improve the documentation and codebase structure.

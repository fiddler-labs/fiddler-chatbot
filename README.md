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
- **Interactive UI**: Streamlit-based web interface with feedback collection

## 🏛️ Architecture

**WIP** - Detailed architecture diagram and component relationships will be added here.

### Core Components

**WIP** - Detailed lay out will be added here.

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
   git clone <repository-url>
   cd fiddler-chatbot
   ```

2. **Install dependencies**

   ```bash
   # Using uv (recommended)
   uv sync

   # Or using pip
   pip install -e .
   ```

3. **Environment Configuration**

    **WIP** - Detailed environment setup instructions will be added here.

    Create a `.env` file with required API keys:

   ```bash
   OPENAI_API_KEY=your_openai_api_key
   ASTRA_DB_APPLICATION_TOKEN=your_datastax_token
   FIDDLER_API_TOKEN=your_fiddler_token  # Optional
   ```

4. **Database Setup**

   **WIP** - Detailed database setup and schema creation instructions.

## 🔧 Local Development

### Running the Application

```bash
# Start the Streamlit application
streamlit run chatbot.py
```

The application will be available at `http://localhost:8501`

### Development Workflow

**WIP** - Development best practices, testing procedures, and contribution guidelines.

## 📊 Usage

### Basic Chat Interface

1. Open the Streamlit application in your browser
2. Enter your question about Fiddler documentation
3. Review the generated response with source citations
4. Provide feedback using thumbs up/down buttons
5. Add comments for additional context

### Advanced Features

**WIP** - Advanced usage patterns, API integration, and customization options.

## 📁 Project Structure

```bash-tree
fiddler-chatbot/
** WIP **
```

## 📊 Monitoring

The application integrates with Fiddler AI's platform for:

- **Response Quality**: Faithfulness scoring against source documents
- **Safety Monitoring**: Jailbreak attempt detection
- **Performance Metrics**: Response latency and token usage
- **User Feedback**: Like/dislike ratings and comments

**WIP** - Detailed monitoring setup and dashboard configuration.

## 🔧 Troubleshooting

### Common Issues **WIP**

- Comprehensive troubleshooting guide.
  - Database Connection Issues ( WIP )
  - OpenAI API Issues ( WIP )
  - Vector Search Problems ( WIP )

## 📄 License

This is a private internal tool for Fiddler AI use only. Not licensed for external use or distribution.

---

> **Note**: This README is actively being updated. Please check back for the latest information as we continue to improve the documentation and codebase structure.

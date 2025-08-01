# Fiddler Chatbot System Architecture Overview

This document provides a comprehensive view of the entire Fiddler Chatbot system, including both implementations and all supporting components.

## High-Level System Architecture

```mermaid
graph TB
    subgraph "Data Pipeline"
        A[Data Sources<br/>Repos, RSS, Docs] --> B[data_generation.py<br/>Corpus Processing]
        B --> C[CSV Corpus<br/>vector_index_feed_*.csv]
        C --> D[vector_index_mgmt.py<br/>Index Management]
    end
    
    subgraph "Storage Layer"
        D --> E[(Cassandra DB<br/>fiddlerai keyspace)]
        E --> F[Vector Store<br/>fiddler_doc_snippets_openai]
        E --> G[Ledger<br/>fiddler_chatbot_ledger]
        E --> H[History<br/>fiddler_chatbot_history]
    end
    
    subgraph "Application Layer"
        I[chatbot.py<br/>Streamlit Web UI] 
        J[chatbot_agentic.py<br/>LangGraph CLI]
    end
    
    subgraph "External Services"
        K[OpenAI API<br/>LLM & Embeddings]
        L[Fiddler Platform<br/>Monitoring & Guardrails]
    end
    
    F --> I
    F --> J
    G --> I
    
    I --> K
    J --> K
    I --> L
    J --> L
    
    style A fill:#e1f5fe
    style E fill:#c8e6c9
    style I fill:#ffecb3
    style J fill:#ffecb3
    style K fill:#f3e5f5
    style L fill:#f3e5f5
```

## Comparison of Chatbot Implementations

```mermaid
graph LR
    subgraph "Streamlit Implementation (chatbot.py)"
        A1[Web UI Interface]
        A2[ConversationalRetrievalChain]
        A3[Session State Management]
        A4[Real-time Streaming]
        A5[Guardrail Integration]
        A6[User Feedback System]
    end
    
    subgraph "LangGraph Implementation (chatbot_agentic.py)"
        B1[CLI Interface]
        B2[StateGraph Workflow]
        B3[Node-based Architecture]
        B4[Tool Integration]
        B5[Auto-instrumentation]
        B6[Thread-based Sessions]
    end
    
    subgraph "Shared Components"
        C1[Cassandra Vector Store]
        C2[OpenAI Models]
        C3[System Instructions]
        C4[RAG Pipeline]
    end
    
    A2 --> C1
    B2 --> C1
    A2 --> C2
    B2 --> C2
    A2 --> C3
    B2 --> C3
    A2 --> C4
    B2 --> C4
    
    style A1 fill:#e1f5fe
    style B1 fill:#fff3e0
    style C1 fill:#c8e6c9
```

## Key Differences

| Feature | Streamlit (chatbot.py) | LangGraph (chatbot_agentic.py) |
|---------|------------------------|--------------------------------|
| **Interface** | Web UI (Streamlit) | CLI |
| **Architecture** | Traditional chain-based | Graph-based with nodes |
| **LLM Model** | gpt-4-turbo | gpt-4o-mini |
| **Temperature** | 0 (deterministic) | 0.7 (creative) |
| **Monitoring** | Manual event publishing | Auto-instrumentation |
| **Session Management** | Streamlit session state | Thread-based config |
| **RAG Integration** | ConversationalRetrievalChain | Tool-based approach |
| **Guardrails** | Pre/post safety checks | Tool-based validation |
| **Feedback** | Built-in UI buttons | Not implemented |
| **Streaming** | StreamHandler callback | Console output |

## Data Flow Patterns

### Streamlit Flow

```mermaid
sequenceDiagram
    User->>Streamlit UI: Enter query
    Streamlit UI->>Guardrails: Safety check
    Guardrails->>RAG Chain: Process query
    RAG Chain->>Cassandra: Vector search
    Cassandra->>LLM: Retrieved docs
    LLM->>Streamlit UI: Stream response
    Streamlit UI->>Guardrails: Faithfulness check
    Streamlit UI->>User: Display result
    User->>Streamlit UI: Feedback
    Streamlit UI->>Cassandra: Store feedback
```

### LangGraph Flow

```mermaid
sequenceDiagram
    User->>CLI: Enter message
    CLI->>Human Node: Process input
    Human Node->>Force RAG Node: Generate tool call
    Force RAG Node->>RAG Tool: Execute retrieval
    RAG Tool->>Cassandra: Vector search
    Cassandra->>Chatbot Node: Retrieved docs
    Chatbot Node->>LLM: Generate response
    LLM->>CLI: Display response
    CLI->>Fiddler: Auto-instrument spans
```

# Fiddler Monitoring Architecture Diagrams

## Code to Web UI Mapping - LangGraph Implementation

```mermaid
graph TB
    subgraph "Python Code Implementation (chatbot_agentic.py)"
        A["`**chatbot_agentic.py**
        CLI Application with LangGraph`"]
        B["`**chatbot_node()**
        LLM Response Generation`"]
        C["`**llm.invoke()**
        ChatOpenAI gpt-4o-mini`"]
        D["`**chatbot_graph.stream()**
        LangGraph Workflow Execution`"]
        E["`**set_conversation_id()**
        Thread-based Session Management`"]
        F["`**set_llm_context()**
        Unified Context for Monitoring`"]
        G["`**LangGraphInstrumentor**
        Fiddler Integration`"]
    end
    
    subgraph "Fiddler Web UI Dashboard"
        H["`**Application**
        Agentic Documentation Chatbot - APP1`"]
        I["`**chatbot Span**
        Node Execution Tracking`"]
        J["`**ChatOpenAI Span**
        LLM Invocation Tracking`"]
        K["`**LangGraph Span**
        Workflow Execution Tracking`"]
        L["`**RAG Retrieval Span**
        Vector Search Tracking`"]
        M["`**Tool Execution Span**
        Tool Call Tracking`"]
    end
    
    A --> H
    B --> I
    C --> J
    D --> K
    F --> L
    G --> M
    
    style A fill:#e1f5fe
    style H fill:#c8e6c9
    style I fill:#ffecb3
    style J fill:#ffecb3
    style K fill:#ffecb3
```

## Code to Web UI Mapping - Streamlit Implementation

```mermaid
graph TB
    subgraph "Python Code Implementation (chatbot.py)"
        A["`**chatbot.py**
        Streamlit Web Application`"]
        B["`**main()**
        UI Orchestration`"]
        C["`**ChatOpenAI**
        gpt-4-turbo with Streaming`"]
        D["`**ConversationalRetrievalChain**
        RAG Pipeline`"]
        E["`**publish_and_store()**
        Event Publishing to Fiddler`"]
        F["`**Guardrails**
        Safety & Faithfulness Checks`"]
    end
    
    subgraph "Fiddler Platform Monitoring"
        G["`**Project**
        fiddler_chatbot_v3`"]
        H["`**Model**
        fiddler_rag_chatbot`"]
        I["`**Event Tracking**
        Row-based Event Publishing`"]
        J["`**Metrics**
        Token Counts & Latency`"]
        K["`**Feedback**
        User Ratings & Comments`"]
    end
    
    A --> G
    B --> H
    E --> I
    E --> J
    F --> K
    
    style A fill:#e1f5fe
    style G fill:#c8e6c9
    style I fill:#ffecb3
```

## Session Flow Architecture - LangGraph Implementation

```mermaid
sequenceDiagram
    participant User as User Input
    participant App as chatbot_agentic.py
    participant LG as LangGraph
    participant HN as human_node
    participant FRT as force_rag_tool_call_node
    participant RAG as rag_retrieval ToolNode
    participant CB as chatbot_node
    participant OpenAI as ChatOpenAI
    participant Cass as Cassandra
    participant Fiddler as Fiddler Platform
    
    User->>App: CLI Input or Automated Message
    App->>App: Generate thread_id: datetime + uuid4()
    App->>LG: set_conversation_id(session_id)
    
    App->>LG: chatbot_graph.stream(state, thread_config)
    LG->>HN: Execute human_node
    HN-->>LG: HumanMessage
    
    LG->>FRT: force_rag_tool_call_node
    FRT-->>LG: AIMessage with tool_call
    
    LG->>RAG: Execute rag_retrieval
    RAG->>Cass: similarity_search(query, k=6)
    Cass-->>RAG: Retrieved documents
    RAG-->>LG: ToolMessage with documents
    
    LG->>CB: chatbot_node(state)
    CB->>CB: Build context from messages + tool outputs
    CB->>CB: set_llm_context() for monitoring
    CB->>OpenAI: llm.invoke(messages + system_prompt)
    OpenAI-->>CB: AI Response
    CB-->>LG: AIMessage
    
    LG->>Fiddler: Auto-instrumented spans
    Fiddler-->>User: Display response
    
    App->>User: "🤖 Assistant: [Response]"
```

## Web UI Components Breakdown

```mermaid
graph LR
    subgraph "Fiddler Web UI Structure"
        A["`**Main Dashboard**
        Agentic Documentation Chatbot - APP1`"]
        
        subgraph "Navigation Tabs"
            B["`**Agents Tab**
            Agent Management`"]
            C["`**Enrichments Tab**
            Data Processing`"]
        end
        
        subgraph "Spans Section"
            D["`**Time Range**
            Last 7 days: Jul 4-10, 2025`"]
            E["`**Span Status**
            Active (3) | Inactive (0)`"]
            F["`**Search Bar**
            Search spans...`"]
        end
        
        subgraph "Span Details"
            G["`**chatbot**
            528d3fe | Events: 5`"]
            H["`**ChatOpenAI**
            b1ad4fa2 | Events: 5`"]
            I["`**LangGraph**
            bf246607 | Events: 5`"]
        end
        
        subgraph "Agent Classification"
            J["`**Named Agent**
            chatbot (4f7d5200)`"]
            K["`**Unknown Agent**
            <UNKNOWN_AGENT> (8552e276)`"]
        end
    end
    
    A --> B
    A --> C
    A --> D
    A --> E
    A --> F
    A --> G
    A --> H
    A --> I
    B --> J
    B --> K
    
    style A fill:#1976d2,color:#fff
    style B fill:#388e3c,color:#fff
    style C fill:#388e3c,color:#fff
    style G fill:#ff9800,color:#fff
    style H fill:#ff9800,color:#fff
    style I fill:#ff9800,color:#fff
```

## Data Flow Architecture

```mermaid
flowchart TD
    subgraph "Application Layer"
        A["`**User Input**
        CLI Interface / Automated Args`"]
        B["`**Thread Config**
        Session ID: datetime + uuid4()`"]
        C["`**State Management**
        ChatbotState with Messages`"]
    end
    
    subgraph "LangGraph Workflow"
        D["`**StateGraph Builder**
        workflow_builder.compile()`"]
        E["`**Node Chain**
        human→force_rag→retrieval→chatbot`"]
        F["`**Conditional Edges**
        tools_condition`"]
        G["`**Memory Checkpointer**
        MemorySaver`"]
    end
    
    subgraph "RAG System"
        H["`**Retrieval Tool**
        make_cassandra_rag_retriever_tool()`"]
        I["`**Vector Search**
        CassandraVectorStore`"]
        J["`**OpenAI Embeddings**
        text-embedding-3-large`"]
    end
    
    subgraph "Fiddler Instrumentation"
        K["`**LangGraphInstrumentor**
        Auto-instrumentation`"]
        L["`**Context Tracking**
        set_llm_context()`"]
        M["`**Conversation ID**
        set_conversation_id()`"]
    end
    
    subgraph "External Services"
        N["`**Cassandra DB**
        fiddler_doc_snippets_openai`"]
        O["`**OpenAI API**
        gpt-4o-mini`"]
        P["`**Fiddler Platform**
        preprod.cloud.fiddler.ai`"]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    D --> G
    
    E --> H
    H --> I
    I --> J
    I --> N
    
    K --> L
    L --> M
    D --> K
    
    E --> O
    K --> P
    
    style A fill:#e3f2fd
    style H fill:#fff3e0
    style K fill:#e8f5e8
    style N fill:#fce4ec
```

## Environment Configuration Mapping

```mermaid
graph TB
    subgraph "Environment Variables"
        A["`**FIDDLER_API_KEY**
        Authentication for both chatbots`"]
        B["`**FIDDLER_APP_ID**
        Application ID for LangGraph`"]
        C["`**OPENAI_API_KEY**
        LLM & Embeddings Access`"]
        D["`**ASTRA_DB_APPLICATION_TOKEN**
        Cassandra Authentication`"]
    end
    
    subgraph "LangGraph Configuration (chatbot_agentic.py)"
        E["`**FiddlerClient**
        API Key + App ID + URL`"]
        F["`**ChatOpenAI**
        gpt-4o-mini, temp=0.7`"]
        G["`**Platform URL**
        preprod.cloud.fiddler.ai`"]
    end
    
    subgraph "Streamlit Configuration (chatbot.py)"
        H["`**Fiddler Project**
        fiddler_chatbot_v3`"]
        I["`**Fiddler Model**
        fiddler_rag_chatbot`"]
        J["`**ChatOpenAI**
        gpt-4-turbo, temp=0`"]
        K["`**Platform URL**
        demo.fiddler.ai`"]
    end
    
    subgraph "Shared Configuration"
        L["`**Cassandra Keyspace**
        fiddlerai`"]
        M["`**Vector Table**
        fiddler_doc_snippets_openai`"]
        N["`**Embedding Model**
        text-embedding-3-large`"]
    end
    
    A --> E
    A --> H
    B --> E
    C --> F
    C --> J
    D --> L
    
    E --> G
    H --> K
    L --> M
    
    style A fill:#ffebee
    style B fill:#ffebee
    style C fill:#ffebee
    style D fill:#ffebee
    style E fill:#e0f2f1
    style H fill:#e0f2f1
    style L fill:#e8eaf6
```

---

*These diagrams illustrate the complete flow from code implementation to Web UI visualization in the Fiddler monitoring system.*

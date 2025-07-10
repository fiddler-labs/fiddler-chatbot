# Fiddler Monitoring Architecture Diagrams

## Code to Web UI Mapping

```mermaid
graph TB
    subgraph "Python Code Implementation"
        A["`**chatbot_agentic.py**
        Main Application`"]
        B["`**chatbot_node()**
        Function Execution`"]
        C["`**llm.invoke()**
        OpenAI API Call`"]
        D["`**app.invoke()**
        LangGraph Workflow`"]
        E["`**set_conversation_id()**
        Session Management`"]
        F["`**set_llm_context()**
        Context Tracking`"]
    end
    
    subgraph "Fiddler Web UI Dashboard"
        G["`**Application**
        Agentic Documentation Chatbot - APP1`"]
        H["`**chatbot Span**
        47d5200 | Events: 5`"]
        I["`**ChatOpenAI Span**
        b1ad4fa2 | Events: 5`"]
        J["`**LangGraph Span**
        bf246607 | Events: 5`"]
        K["`**Agents Tab**
        Named & Unknown Agents`"]
        L["`**Enrichments Tab**
        Data Processing Metrics`"]
    end
    
    A --> G
    B --> H
    C --> I
    D --> J
    E --> K
    F --> L
    
    style A fill:#e1f5fe
    style G fill:#c8e6c9
    style H fill:#ffecb3
    style I fill:#ffecb3
    style J fill:#ffecb3
```

## Session Flow Architecture

```mermaid
sequenceDiagram
    participant User as User Input
    participant App as Chatbot App
    participant LG as LangGraph
    participant CB as Chatbot Node
    participant OpenAI as ChatOpenAI
    participant Fiddler as Fiddler Platform
    participant UI as Web UI Dashboard
    
    User->>App: "Hello, how are you?"
    App->>App: Generate session_id: uuid4()
    App->>LG: set_conversation_id(session_id)
    
    App->>LG: app.invoke({"messages": [HumanMessage]})
    LG->>Fiddler: Create LangGraph Span (bf246607)
    LG->>UI: Display LangGraph Span
    
    LG->>CB: chatbot_node(state)
    CB->>Fiddler: Create chatbot Span (47d5200)
    CB->>UI: Display chatbot Span
    
    CB->>OpenAI: llm.invoke(messages)
    OpenAI->>Fiddler: Create ChatOpenAI Span (b1ad4fa2)
    OpenAI->>UI: Display ChatOpenAI Span
    
    OpenAI-->>CB: AI Response
    CB-->>LG: Updated State
    LG-->>App: Final Response
    
    Fiddler->>UI: Update Event Counts (5 events each)
    UI->>UI: Show Active/Inactive Status
    
    App->>User: "I'm doing well, thank you!"
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
        CLI Interface`"]
        B["`**Session Creation**
        UUID Generation`"]
        C["`**State Management**
        ChatbotState`"]
    end
    
    subgraph "LangGraph Workflow"
        D["`**Workflow Compilation**
        app = workflow.compile()`"]
        E["`**Node Execution**
        chatbot_node()`"]
        F["`**LLM Invocation**
        llm.invoke()`"]
    end
    
    subgraph "Fiddler Instrumentation"
        G["`**LangGraphInstrumentor**
        instrumentor.instrument()`"]
        H["`**Span Creation**
        Auto-generated spans`"]
        I["`**Event Ingestion**
        Real-time streaming`"]
    end
    
    subgraph "Fiddler Platform"
        J["`**Data Processing**
        Event aggregation`"]
        K["`**Storage**
        Span persistence`"]
        L["`**Analytics**
        Performance metrics`"]
    end
    
    subgraph "Web UI Dashboard"
        M["`**Real-time Display**
        Live span updates`"]
        N["`**Agent Classification**
        Named/Unknown agents`"]
        O["`**Event Counts**
        Ingestion metrics`"]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    
    G --> H
    H --> I
    D --> G
    E --> G
    F --> G
    
    I --> J
    J --> K
    K --> L
    
    L --> M
    L --> N
    L --> O
    
    style A fill:#e3f2fd
    style G fill:#fff3e0
    style J fill:#e8f5e8
    style M fill:#fce4ec
```

## Environment Configuration Mapping

```mermaid
graph TB
    subgraph "Environment Variables"
        A["`**FIDDLER_API_KEY**
        Authentication`"]
        B["`**FIDDLER_APP_ID**
        Application Identity`"]
        C["`**OPENAI_API_KEY**
        LLM Access`"]
    end
    
    subgraph "Application Configuration"
        D["`**FiddlerClient**
        Client initialization`"]
        E["`**Application Name**
        'Agentic Documentation Chatbot - APP1'`"]
        F["`**Platform URL**
        preprod.cloud.fiddler.ai`"]
    end
    
    subgraph "Web UI Display"
        G["`**Dashboard Title**
        Shows application name`"]
        H["`**Span Organization**
        Groups by application`"]
        I["`**Session Tracking**
        UUID-based identification`"]
    end
    
    A --> D
    B --> D
    C --> D
    
    D --> E
    D --> F
    
    E --> G
    E --> H
    F --> I
    
    style A fill:#ffebee
    style B fill:#ffebee
    style C fill:#ffebee
    style D fill:#e0f2f1
    style E fill:#e0f2f1
    style F fill:#e0f2f1
    style G fill:#e8eaf6
    style H fill:#e8eaf6
    style I fill:#e8eaf6
```

---

*These diagrams illustrate the complete flow from code implementation to Web UI visualization in the Fiddler monitoring system.* 
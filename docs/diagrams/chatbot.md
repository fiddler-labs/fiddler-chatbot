# Fiddler Chatbot Diagrams

## Fiddler Chatbot System Architecture

```mermaid
graph TB
    A[User Input] --> B[Streamlit UI]
    B --> C{Safety Check}
    C -->|Pass| D[RAG Pipeline]
    C -->|Fail| E[Reject Query]
    
    D --> F[Question Generator]
    F --> G[Vector Search]
    G --> H[Retrieve Documents]
    H --> I[LLM Processing]
    I --> J[Generate Response]
    
    J --> K{Faithfulness Check}
    K --> L[Display Response]
    
    L --> M[User Feedback]
    M --> N[Store Feedback]
    
    subgraph "Data Storage"
        O[(Cassandra DB)]
        P[(Fiddler Platform)]
    end
    
    G -.-> O
    N --> O
    J --> P
    K --> P
    
style A fill:#f9f,stroke:#333,stroke-width:2px
style O fill:#bbf,stroke:#333,stroke-width:2px
style P fill:#bbf,stroke:#333,stroke-width:2px
```

---

## System Components

```mermaid
graph LR
    subgraph "RAG Stack Components"
        A[OpenAI Embeddings<br/>text-embedding-3-large] --> B[Vector Store<br/>Cassandra]
        C[LangChain Framework] --> D[ConversationalRetrievalChain]
        D --> E[Question Generator<br/>LLMChain]
        D --> F[Document Chain<br/>load_qa_chain]
        D --> G[Memory<br/>ConversationSummaryBufferMemory]
        H[ChatOpenAI<br/>gpt-4-turbo] --> E
        H --> F
        H --> G
        B --> I[Retriever<br/>k=3 documents]
        I --> D
    end
    
style A fill:#f96,stroke:#333,stroke-width:2px
style H fill:#6f9,stroke:#333,stroke-width:2px
style C fill:#96f,stroke:#333,stroke-width:2px
```

---

## Sequence Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Streamlit UI
    participant SG as Safety Guardrail
    participant QG as Question Generator
    participant VS as Vector Store
    participant LLM as LLM (GPT-4)
    participant FG as Faithfulness Guardrail
    participant DB as Cassandra DB
    participant FP as Fiddler Platform
    
    U->>UI: Enter question
    UI->>SG: Check for jailbreak
    SG-->>UI: Safety score
    
    alt Jailbreak detected
        UI->>U: Reject query
        UI->>DB: Store rejected query
        UI->>FP: Publish event
    else Safe query
        UI->>QG: Generate search query
        QG->>VS: Search similar docs
        VS-->>QG: Top 3 documents
        QG->>LLM: Generate response
        LLM-->>UI: Stream response
        UI->>FG: Check faithfulness
        FG-->>UI: Faithfulness score
        UI->>DB: Store conversation
        UI->>FP: Publish metrics
        UI->>U: Display response
    end
    
    U->>UI: Provide feedback
    UI->>DB: Update feedback
```

---

## Session State Managment : Attributes

```mermaid
graph LR
    A[st.session_state]
    A --> B[UUID<br/>Unique conversation ID]
    A --> C[SESSION_ID<br/>User session tracking]
    A --> D[MEMORY<br/>Conversation history]
    A --> E[messages<br/>Chat display history]
    A --> F[ANSWER<br/>Latest response]
    A --> G[COMMENT<br/>User feedback text]
    A --> H[THUMB_UP/DOWN<br/>Feedback buttons]
    A --> I[DB_CONN<br/>Cassandra connection]
style A fill:#f9f,stroke:#333,stroke-width:2px
```

---

## Data Flow

```mermaid
graph TB
    J[Initialize Session] --> K{Check State}
    K -->|Missing| L[Create New]
    K -->|Exists| M[Use Existing]
    L --> N[Store in session_state]
    M --> N
style J fill:#9f9,stroke:#333,stroke-width:2px
    
```

---

## Areas of Responsibility

```mermaid
graph LR
        A[main<br/>Entry point & UI orchestration]
        
        B[get_safety_guardrail_results<br/>Jailbreak detection]
        C[get_faithfulness_guardrail_results<br/>Response validation]
        
        D[publish_and_store<br/>Data persistence & monitoring]
        
        E[store_feedback<br/>User feedback handling]
        F[store_comment<br/>Comment storage]
        G[erase_history<br/>Session cleanup]
        
        H[StreamHandler<br/>Real-time response streaming]
    
    A --> B
    A --> C
    A --> D
    A --> E
    A --> F
    A --> G
    A --> H
    
    subgraph "External Services"
        I[Fiddler API<br/>Guardrails & Monitoring]
        J[OpenAI API<br/>LLM & Embeddings]
        K[Cassandra<br/>Vector Store & Ledger]
    end
    
    B --> I
    C --> I
    D --> I
    D --> K
    E --> K
    F --> K
    
style A fill:#f96,stroke:#333,stroke-width:2px
style I fill:#bbf,stroke:#333,stroke-width:2px
style J fill:#bbf,stroke:#333,stroke-width:2px
style K fill:#bbf,stroke:#333,stroke-width:2px
``

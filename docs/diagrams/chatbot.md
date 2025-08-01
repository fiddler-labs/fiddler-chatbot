# Fiddler Chatbot Diagrams

**Note**: This document describes the Streamlit-based chatbot implementation (`chatbot.py`). For the newer LangGraph-based implementation, see `chatbot_agentic.md`.

## Fiddler Chatbot System Architecture (Streamlit Version)

```mermaid
graph TB
    A[User Input] --> B[Streamlit UI<br/>chatbot.py]
    B --> C{Jailbreak Detection<br/>get_safety_guardrail_results}
    C -->|Pass| D[RAG Pipeline]
    C -->|Fail| E[Reject Query<br/>Set prompt='Rejected']
    
    D --> F[Question Generator<br/>LLMChain]
    F --> G[Vector Search<br/>Cassandra]
    G --> H[Retrieve Documents<br/>k=6]
    H --> I[LLM Processing<br/>ChatOpenAI]
    I --> J[Generate Response<br/>ConversationalRetrievalChain]
    
    J --> K{Faithfulness Check<br/>get_faithfulness_guardrail_results}
    K --> L[Display Response<br/>StreamHandler]
    
    L --> M[User Feedback<br/>👍 👎]
    M --> N[Store Feedback<br/>store_feedback]
    
    subgraph "Data Storage"
        O[(Cassandra DB<br/>fiddler_chatbot_ledger)]
        P[(Fiddler Platform<br/>fiddler_chatbot_v3)]
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
        A[OpenAI Embeddings<br/>text-embedding-3-large<br/>dimensions=1536] --> B[Vector Store<br/>Cassandra<br/>fiddler_doc_snippets_openai]
        C[LangChain Framework] --> D[ConversationalRetrievalChain]
        D --> E[Question Generator<br/>LLMChain<br/>CONDENSE_QUESTION_PROMPT]
        D --> F[Document Chain<br/>load_qa_chain<br/>QA_CHAIN_PROMPT]
        D --> G[Memory<br/>ConversationSummaryBufferMemory<br/>max_token_limit=50]
        H[ChatOpenAI<br/>gpt-4-turbo<br/>temperature=0] --> E
        H --> F
        H --> G
        B --> I[Retriever<br/>k=6 documents<br/>as_retriever()]
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

## Session State Management : Attributes

```mermaid
graph LR
    A[st.session_state]
    A --> B[uuid<br/>Unique conversation ID]
    A --> C[session_id<br/>User session tracking]
    A --> D[memory<br/>ConversationSummaryBufferMemory]
    A --> E[messages<br/>Chat display history]
    A --> F[answer<br/>Latest response]
    A --> G[comment<br/>User feedback text]
    A --> H[thumbs_up_button<br/>thumbs_down_button]
    A --> I[db_conn<br/>Cassandra cluster connection]
    A --> J[qa<br/>ConversationalRetrievalChain]
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
```

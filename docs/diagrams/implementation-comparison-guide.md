# Implementation Comparison Guide

This guide provides a detailed comparison between the Streamlit and LangGraph implementations of the Fiddler Chatbot.

## LangGraph Workflow Generation

The `chatbot_agentic.py` implementation automatically generates a visual representation of its workflow graph when executed. This diagram is saved as `workflow_graph.png` in the project root.

```mermaid
graph LR
    A[build_chatbot_graph()] --> B[StateGraph(ChatbotState)]
    B --> C[Add Nodes]
    C --> D[Add Edges]
    D --> E[workflow_builder.compile()]
    E --> F[visualize_chatbot_graph()]
    F --> G[chatbot_graph.get_graph().draw_mermaid_png()]
    G --> H[workflow_graph.png]
    
    style A fill:#e1f5fe
    style E fill:#c8e6c9
    style H fill:#fff3e0
```

## Architecture Comparison

```mermaid
graph TB
    subgraph "Streamlit Architecture (chatbot.py)"
        A1[Web Browser] --> A2[Streamlit Server]
        A2 --> A3[Session State Manager]
        A3 --> A4[ConversationalRetrievalChain]
        A4 --> A5[LangChain Components]
        A5 --> A6[Memory Buffer]
        A5 --> A7[Question Generator]
        A5 --> A8[Document Chain]
    end
    
    subgraph "LangGraph Architecture (chatbot_agentic.py)"
        B1[CLI Terminal] --> B2[Python Process]
        B2 --> B3[StateGraph Engine]
        B3 --> B4[Node System]
        B4 --> B5[Human Node]
        B4 --> B6[RAG Tool Node]
        B4 --> B7[Chatbot Node]
        B3 --> B8[Checkpointer]
    end
    
    style A1 fill:#e1f5fe
    style B1 fill:#fff3e0
```

## Feature Mapping

```mermaid
graph LR
    subgraph "Streamlit Features"
        S1[Web UI]
        S2[Real-time Streaming]
        S3[Session Persistence]
        S4[User Feedback UI]
        S5[Guardrail Checks]
        S6[Event Publishing]
    end
    
    subgraph "Equivalent in LangGraph"
        L1[CLI Interface]
        L2[Console Output]
        L3[Thread Config]
        L4[Not Implemented]
        L5[Tool-based Checks]
        L6[Auto-instrumentation]
    end
    
    S1 -.->|maps to| L1
    S2 -.->|maps to| L2
    S3 -.->|maps to| L3
    S4 -.->|no equivalent| L4
    S5 -.->|different approach| L5
    S6 -.->|automated| L6
```

## Migration Considerations

```mermaid
graph TD
    A[Current Streamlit App] --> B{Migration Goal?}
    B -->|API Service| C[Use LangGraph]
    B -->|Web Interface| D[Keep Streamlit]
    B -->|Both| E[Hybrid Approach]
    
    C --> F[Benefits:<br/>- Stateless<br/>- Auto-monitoring<br/>- Tool ecosystem]
    D --> G[Benefits:<br/>- User-friendly<br/>- Feedback system<br/>- Visual guardrails]
    E --> H[Shared Backend:<br/>- Common RAG<br/>- Unified config<br/>- Consistent prompts]
```

## Configuration Differences

```mermaid
graph LR
    subgraph "Environment Variables"
        E1[OPENAI_API_KEY]
        E2[FIDDLER_API_KEY]
        E3[ASTRA_DB_APPLICATION_TOKEN]
        E4[FIDDLER_APP_ID]
    end
    
    subgraph "Streamlit Uses"
        S[chatbot.py]
        E1 --> S
        E2 --> S
        E3 --> S
    end
    
    subgraph "LangGraph Uses"
        L[chatbot_agentic.py]
        E1 --> L
        E2 --> L
        E3 --> L
        E4 --> L
    end
    
    style E4 fill:#fff3e0
```

## Future Convergence Path

```mermaid
graph TD
    A[Current State:<br/>Two Implementations] --> B[Phase 1:<br/>Shared Components]
    B --> C[Phase 2:<br/>Unified Backend]
    C --> D[Phase 3:<br/>API Gateway]
    D --> E[Future State:<br/>Single Backend,<br/>Multiple Frontends]
    
    B --> F[Extract common:<br/>- RAG logic<br/>- Guardrails<br/>- Prompts]
    C --> G[Create service:<br/>- REST API<br/>- WebSocket<br/>- GraphQL]
    D --> H[Frontend options:<br/>- Streamlit UI<br/>- CLI client<br/>- SDK]
    
    style A fill:#ffebee
    style E fill:#c8e6c9
```

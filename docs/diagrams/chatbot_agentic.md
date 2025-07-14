# Chatbot Agentic

## Flow

```mermaid
graph TD
    A[START] --> B[human]
    B --> C[rag_retrieval]
    C --> D[chatbot]
    D --> E[continue]
    E --> B
    B --> F[END]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e8f5e8
    style D fill:#fff3e0
    style E fill:#fce4ec
    style F fill:#ffebee
```

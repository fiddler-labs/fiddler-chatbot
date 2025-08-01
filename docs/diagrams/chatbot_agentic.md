# Chatbot Agentic - LangGraph Implementation

## Current Architecture Overview

The agentic chatbot uses LangGraph to create a stateful conversation flow with integrated RAG (Retrieval-Augmented Generation) capabilities and Fiddler monitoring.

## Main Workflow Flow

```mermaid
graph TD
    A[START] --> B[human_node<br/>User Input]
    B --> C[force_rag_tool_call_node<br/>Generate Tool Call]
    C --> D[rag_retrieval<br/>ToolNode]
    D --> E[chatbot_node<br/>LLM Processing]
    E --> F{tools_condition}
    F -->|Tool Needed| G[tools<br/>ToolNode]
    G --> E
    F -->|No Tools| B
    E --> H[END]
    B --> H
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#fff3e0
    style D fill:#e8f5e8
    style E fill:#ffecb3
    style F fill:#fce4ec
    style G fill:#e8f5e8
    style H fill:#ffebee
```

## Node Descriptions

- **human_node**: Handles user input (CLI or automated messages)
- **force_rag_tool_call_node**: Creates AIMessage with RAG tool call for retrieval
- **rag_retrieval**: ToolNode that executes Cassandra vector search
- **chatbot_node**: Processes conversation state and generates LLM response
- **tools**: Additional tools like get_system_time
- **tools_condition**: Conditional edge that checks if tools are needed

## State Management

```mermaid
graph LR
    A[ChatbotState] --> B[messages<br/>Annotated[Sequence[BaseMessage], add_messages]]
    
    C[Message Types] --> D[HumanMessage]
    C --> E[AIMessage]
    C --> F[ToolMessage]
    C --> G[SystemMessage]
    
    style A fill:#e1f5fe
    style B fill:#fff3e0
```

## Key Components

```mermaid
graph TB
    A[chatbot_agentic.py<br/>Main Application] --> B[LangGraph Setup]
    B --> C[StateGraph Builder]
    B --> D[Memory Saver<br/>Checkpointer]
    B --> E[Tool Binding]
    
    A --> F[Fiddler Integration]
    F --> G[FiddlerClient]
    F --> H[LangGraphInstrumentor]
    F --> I[Conversation Tracking]
    
    A --> J[RAG System]
    J --> K[Cassandra Vector Store]
    J --> L[OpenAI Embeddings]
    J --> M[Retrieval Tool]
    
    style A fill:#f3e5f5
    style F fill:#e8f5e8
    style J fill:#fff3e0
```

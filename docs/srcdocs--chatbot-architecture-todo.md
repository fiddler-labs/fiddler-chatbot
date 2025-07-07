# Fiddler Chatbot Architecture Documentation

The Fiddler Chatbot is a sophisticated RAG (Retrieval-Augmented Generation) application built with Streamlit that provides intelligent Q&A capabilities for Fiddler AI's product documentation. This document provides a comprehensive walkthrough of the system architecture, components, and data flow.

## System Architecture

The chatbot follows a modern RAG architecture pattern with several key enhancements:

- **Safety Guardrails**: Pre-flight checks for jailbreak attempts
- **Faithfulness Validation**: Post-generation validation of responses
- **Conversation Memory**: Maintains context across interactions
- **Real-time Streaming**: Progressive response display
- **Comprehensive Monitoring**: Full observability via Fiddler platform

### Core Technologies

- **UI Framework**: Streamlit
- **LLM Framework**: LangChain
- **LLM Provider**: OpenAI (GPT-4-turbo)
- **Embeddings**: OpenAI text-embedding-3-large
- **Vector Database**: DataStax Cassandra
- **Monitoring**: Fiddler AI Platform

### Session State Management

Streamlit's session state maintains conversation context:

- `UUID`: Unique identifier for each conversation turn
- `SESSION_ID`: Tracks the entire user session
- `MEMORY`: LangChain conversation memory
- `messages`: Chat history for UI display
- `DB_CONN`: Persistent database connection
- `ANSWER`: Latest generated response
- `THUMB_UP/DOWN`: Feedback button states
- `COMMENT`: User feedback text

## Data Flow

### User Query Processing

1. **Input Reception**: User enters query via Streamlit chat input
2. **Safety Check**: Query sent to Fiddler's safety guardrail API
3. **Jailbreak Detection**: If score > 0.5, query is rejected
4. **Query Conditioning**: LangChain reformulates query based on chat history

### RAG Pipeline

1. **Vector Search**: Query embedded and searched against Cassandra
2. **Document Retrieval**: Top 3 most relevant documents retrieved
3. **Context Building**: Documents formatted with system instructions
4. **Response Generation**: GPT-4 generates response with streaming
5. **Faithfulness Check**: Response validated against source documents

### Data Persistence

Every interaction is persisted in two systems:

- **Cassandra Ledger**
  - Stores complete conversation records
  - Includes source documents, tokens, duration
  - Enables feedback updates

- **Fiddler Platform**
  - Publishes events for monitoring
  - Tracks model performance metrics
  - Enables ML observability

## Guardrail Systems

### Safety Guardrail

- **Endpoint**: `/v3/guardrails/ftl-safety`
- **Purpose**: Detect jailbreak attempts
  - Checks if someone's trying to make the chatbot misbehave
- **Threshold**: Score > 0.5 triggers rejection

### Faithfulness Guardrail

- **Endpoint**: `/v3/guardrails/ftl-response-faithfulness`
- **Input**: Response + concatenated source documents
- **Purpose**: Validate response accuracy
  - Compares the generated response against source documents
  - Ensures the chatbot isn't making things up
  - Provides a confidence score


## Feedback System

The chatbot includes a comprehensive feedback mechanism:

1. **Binary Feedback**: Thumbs up/down buttons
2. **Text Comments**: Expandable comment field
3. **Persistence**: Updates stored in Cassandra
4. **Analytics**: Feedback tracked in Fiddler platform

---

## Analysis Report: Fiddler Chatbot Code Review

As we plan to make this more agentic, consider these architectural patterns:

1. **Modular Guardrails**: The guardrail system is already separate from the main logic
2. **Flexible Memory**: The conversation memory can be extended for more complex interactions
3. **Pluggable Retrieval**: The vector search is abstracted through LangChain
4. **Observable by Design**: Every action is already instrumented for monitoring

### 1. Critical Error Handling Deficiencies

The application has significant gaps in error handling that could lead to terminal failures:

- **Unhandled API Failures**: Calls to external services (OpenAI, Fiddler guardrails) have no try-except blocks, meaning any API failure will crash the entire application
  ```python
  # Example of problematic code:
  guardrail_response_safety = requests.request(
      "POST", url_safety, headers=headers, data=payload, timeout=REQUESTS_TIMEOUT
  )
  # No error handling if the request fails
  ```

- **Missing Fallback Mechanisms**: When guardrails or database operations fail, there's no graceful degradation path

- **Global Variable Reliance**: The code uses global variables like `FAITHFULNESS_SCORE` and `JAILBREAK_SCORE` without proper initialization in all code paths

### 2. SQL Injection Vulnerabilities

Multiple instances of SQL injection vulnerabilities exist in database operations:

```python
# Vulnerable to SQL injection:
astra_session.execute(
    "UPDATE fiddlerai.fiddler_chatbot_ledger "
    f"SET feedback = {feedback}, feedback2 = '{feedback2}' "
    f"WHERE row_id = '{uuid}'"
)

# Also vulnerable:
astra_session.execute(
    "UPDATE fiddlerai.fiddler_chatbot_ledger "
    f"SET comment = '{comment}' "
    f"WHERE row_id = '{uuid}'"
)
```

The code uses string interpolation instead of parameterized queries, which is a serious security risk. While there's some sanitization with `replace("'", "''")`, this is insufficient and inconsistently applied.

### 3. Poor Database Connection Management

Database connections are not properly managed:

- **No Connection Pooling**: The application creates a single connection at startup and reuses it for all operations
- **No Connection Error Handling**: No retry logic or reconnection strategy if the database connection is lost
- **No Connection Closing**: Connections are never explicitly closed, potentially leading to resource leaks

### 4. Brittle Data Structure Assumptions

The code makes rigid assumptions about data structures that could lead to failures:

```python
# Assumes exactly 3 source documents will always be available
source_doc0 = source_docs_list[0].replace("'", "''")
source_doc1 = source_docs_list[1].replace("'", "''")
source_doc2 = source_docs_list[2].replace("'", "''")
```

This will crash if fewer than 3 documents are returned from the vector search.

### 5. Global State Management Issues

The application relies heavily on Streamlit's session state for critical functionality:

- **Implicit State Dependencies**: Functions assume state variables exist without validation
- **No State Validation**: No checks to ensure state is in a consistent state before operations
- **No Error Recovery**: If session state becomes corrupted, there's no mechanism to reset it

### 6. Lack of Modular Design

The code violates single responsibility principle:

- **Monolithic Functions**: Functions like `publish_and_store` handle multiple concerns (data transformation, database storage, API calls)
- **Tight Coupling**: UI logic, business logic, and data access are intertwined
- **No Abstraction Layers**: Direct API calls and database operations are mixed with application logic

### 7. Configuration Management Problems

Configuration is scattered throughout the code:

- **Hardcoded Values**: URLs, table names, and other configuration values are hardcoded
- **Inconsistent Environment Variable Handling**: Some variables are checked immediately, others only when used
- **Duplicate Configuration**: The same values are defined multiple times (e.g., `OPENAI_API_KEY`)

### 8. Lack of Logging and Monitoring

While the application uses a logger, it's underutilized:

- **Minimal Error Logging**: Most operations don't log errors or important events
- **No Structured Logging**: Log messages lack context needed for debugging
- **No Performance Monitoring**: No systematic tracking of response times or error rates

### 9. Code Duplication

Several patterns are repeated throughout the code:

- **Repeated String Escaping**: The `replace("'", "''")` pattern is duplicated multiple times
- **Similar Database Operations**: Database query patterns are repeated without abstraction
- **Redundant State Checks**: Similar session state checks are scattered throughout

### 10. Minor Issues and Style Concerns

- **Inconsistent Naming**: Mix of snake_case and camelCase in variable names
- **Magic Numbers**: Hardcoded values like `0.5` for threshold checks
- **Commented Code**: Commented code fragments that should be removed
- **Limited Documentation**: Some functions lack comprehensive docstrings

## Recommendations

1. **Implement Comprehensive Error Handling**:
   - Add try-except blocks around all external API calls
   - Create fallback mechanisms for when guardrails fail
   - Log all errors with appropriate context

2. **Fix SQL Injection Vulnerabilities**:
   - Use parameterized queries for all database operations
   - Create a database access layer to encapsulate and standardize queries

3. **Improve Database Connection Management**:
   - Implement connection pooling
   - Add reconnection logic for failed connections
   - Properly close connections when not needed

4. **Make Data Structure Handling Robust**:
   - Add validation for all data structures
   - Handle edge cases (e.g., fewer than expected documents)
   - Use defensive programming techniques

5. **Refactor to a More Modular Design**:
   - Separate UI, business logic, and data access into distinct modules
   - Create service classes for external API interactions
   - Implement proper dependency injection

6. **Centralize Configuration Management**:
   - Move all configuration to a dedicated config module
   - Use environment variables consistently with proper validation
   - Create a configuration validation system

7. **Enhance Logging and Monitoring**:
   - Add structured logging throughout the application
   - Log all significant events and errors
   - Implement performance monitoring

8. **Eliminate Code Duplication**:
   - Create utility functions for common operations
   - Implement a proper data access layer
   - Use consistent patterns across the codebase

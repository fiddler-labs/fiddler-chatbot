# Vector Index to Cassandra Loader

This document provides a comprehensive overview of `src/loader_cassandra_vector_index.py` which is responsible for creating and managing vector indices in DataStax Cassandra for the Fiddler chatbot's RAG (Retrieval-Augmented Generation) system.

```mermaid
graph LR
    A[CSV file] --> B[Pandas DataFrame] --> C[LangChain Documents] --> D[OpenAI Embeddings] --> E[Cassandra Vector Store] --> F[used by chatbot.py for RAG]
```

Database: DataStax Astra (Cassandra as a Service)
Keyspace: `fiddlerai`
Main Table: `fiddler_doc_snippets_openai`
Embedding Model: `text-embedding-3-large` (1536 dimensions)
Input Data: `documentation_data/vector_index_feed_v25.10.csv`

---

### Section 1: Database Connection Setup ( Code Lines 1-27)
**Purpose**: Establishes connection to DataStax Cassandra
- Loads secure connect bundle from `datastax_auth/secure-connect-fiddlerai.zip`
- Uses token-based authentication
- Sets keyspace to `fiddlerai`

### Section 2: LLM and Embedding Configuration (Lines 29-42)
**Purpose**: Sets up OpenAI models for embeddings
- Configures OpenAI LLM with temperature=0
- Sets up text-embedding-3-large model with 1536 dimensions
- Prints confirmation of model setup

### Section 3: Data Loading and Vector Store Population (Lines 44-85)
**Purpose**: Main workflow for loading documentation into vector store
- Loads pre-chunked documentation from CSV
- Clears existing table data (TRUNCATE)
- Uses DataFrameLoader to load documents
- Initializes Cassandra vector store
- Adds documents to vector store (creates embeddings)
- Includes a quick test function to verify functionality

### Section 4: Table Structure Inspection (Lines 90-149)
**Purpose**: Utility code for inspecting Cassandra table structure
- Queries system schema for table information
- Shows column definitions
- Displays approximate row count
- Shows sample data with vector dimensions
- Uses named_tuple_factory for proper row handling

### Section 5: Data Verification Queries (Lines 151-171)
**Purpose**: Additional verification of indexed data
- Executes SELECT queries to view data
- Handles different cassIO versions
- Displays row details including vectors and metadata

### Section 6: Data Export to CSV (Lines 173-196)
**Purpose**: Exports vector store data to CSV for backup/analysis
- Queries all data from the table
- Converts to pandas DataFrame
- Saves to CSV file

### Section 7: Chatbot History Table Creation (Lines 198-236)
**Purpose**: Creates a table for storing chatbot interaction history
- Defines schema for `fiddler_chatbot_history` table
- Includes columns for questions, responses, feedback, and vectors
- Currently missing table configuration options (commented out)

### Section 8: OpenAI Embedding Test (Lines 238-243)
**Purpose**: Direct test of OpenAI embedding API
- Tests embedding generation with sample text
- **Note**: Contains linter error - uses deprecated API # todo
    - Line 240: `"Embedding" is not a known attribute of module "openai"` - Using deprecated API

### Section 9: Duplicate Table Inspection (Lines 245-305)
**Purpose**: Duplicate of Section 4 (likely from different notebook cells)
- Repeats the same table structure inspection code

### Section 10: Squad Table Query (Lines 307-325)
**Purpose**: Queries and processes data from 'squad' table
- Sets pandas factory for row processing
- Queries squad table
- Converts 'answers' column to string
- **Note**: Contains linter error on default_fetch_size
- Line 315: `Cannot assign to attribute "default_fetch_size"` - Incorrect attribute assignment

---
## Cassandra Vector Loader Cleanup Initiative 

This cleanup initiative aims to transform the Fiddler chatbot's vector indexing system from a manual, notebook-based process into an automated, production-ready application.
We plan to refactor `loader_cassandra_vector_index.py` from a monolithic notebook-conversion into a well-structured, modular Python application while preserving all existing functionality.


### Critical Issues

- Data Loss Risk: The script truncates the entire vector store table before reloading rename . the older table to a timestamped data 
- Duplicate Code: Sections 4 and 9 contain identical functionality
- No Error Handling: No try-catch blocks for database operations

### Immediate Actions Needed

- Add configuration management (config file or class)
- Implement proper error handling

- Automation Considerations
  - Dry-run option
  - Add tqdm progress tracking for large datasets
  - Implement retry logic for failed operations

### Key themes of issues

- **No modularity** - 329 lines of procedural code
- **Data loss risk** - Truncates entire table on each run
- **Hardcoded configurations** - Paths, credentials, table names
- **No error handling** - Database operations can fail silently
- **Deprecated APIs** - Using old OpenAI embedding API
- **Duplicate code** - Table inspection code appears twice
- **Manual process** - Requires running notebook cells in specific order
- **No progress tracking** - Silent operation on large datasets
- **No rollback** - Destructive operations without safety nets

### Key improvments needed

- **Safety**: Dry-run mode, confirmation prompts, transaction support
- **Observability**: Logging, progress bars, metrics
- **Maintainability**: Clear module boundaries, unit testable
- **Flexibility**: Configurable for different environments

## Design Principles

- **Preserve All Code**: No functionality will be deleted, only reorganized
- **Clear Separation of Concerns**: Each module handles one specific aspect
- **Production-Ready**: Add proper error handling, logging, and CLI support

### Modularization Plan

- Database Connection Module: Handle all Cassandra connection logic
- Vector Store Manager: Encapsulate vector store operations
- Data Loader: Handle CSV loading and document preparation
- Table Management: Create, inspect, and manage tables
- Utilities: Query helpers, data export functions


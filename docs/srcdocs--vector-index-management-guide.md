# Vector Index Management Guide

## Overview

The `vector_index_mgmt.py` file is a comprehensive tool for managing vector embeddings in DataStax Cassandra for the Fiddler chatbot's RAG (Retrieval-Augmented Generation) system. It handles the complete pipeline from loading documentation data to creating and maintaining vector indices that power the chatbot's knowledge base.

## System Architecture

```mermaid
graph LR
    A[CSV file] --> B[Pandas DataFrame] --> C[LangChain Documents] --> D[OpenAI Embeddings] --> E[Cassandra Vector Store] --> F[used by chatbot.py for RAG]
```

## Core Purpose

This tool enables you to:

- Load documentation data from CSV files into a vector database
- Create embeddings using OpenAI's models
- Store and manage vector indices in DataStax Cassandra
- Maintain and inspect the vector store
- Perform health checks and data exports

## Prerequisites

### Environment Variables Required

- `ASTRA_DB_APPLICATION_TOKEN`: Your DataStax Astra DB token
- `OPENAI_API_KEY`: Your OpenAI API key for embeddings

### Files Required

- `datastax_auth/secure-connect-fiddlerai.zip`: DataStax secure connection bundle
- CSV file with documentation data (default: `./local_assets/vector_index_feed_<LATEST_DATE>.csv`)

## Configuration

The system uses a centralized configuration in the `CONFIG` dictionary:

```python
CONFIG = {
    "keyspace": "fiddlerai",
    "llm_provider": "openai",
    "embedding_model": "text-embedding-3-large",
    "embedding_dimensions": 1536,
    # ... more configuration options
}
```

## Usage Modes

### 1. Basic Usage (Safe Mode)

```bash
python src/vector_index_mgmt.py
```

**What it does:**

- Loads data from the default CSV file
- Validates the data structure
- Creates embeddings using OpenAI
- Appends to existing vector store (no data loss)
- Performs maintenance operations
- Creates test queries to verify functionality

**Best for:** Regular updates, adding new documentation

### 2. Replace Mode (Destructive)

```bash
python src/vector_index_mgmt.py --truncate
```

**What it does:**

- Creates a backup of existing data with timestamp
- Replaces all existing vector data with new data
- Performs complete re-indexing
- Runs verification tests

**Best for:** Complete refresh, fixing data corruption, major updates

**⚠️ WARNING:** This mode will replace all existing data. A backup is created automatically.

### 3. Skip Maintenance Mode

```bash
python src/vector_index_mgmt.py --skip-maintenance
```

**What it does:**

- Performs only the core vector loading operation
- Skips optional operations like table inspection, exports, etc.
- Faster execution for production scenarios

**Best for:** Production deployments, automated scripts

### 4. Health Check Only

```bash
python src/vector_index_mgmt.py --health-check
```

**What it does:**

- Performs comprehensive system health checks
- Validates database connectivity
- Checks table structure and data integrity
- Tests vector search functionality
- Reports overall system health

**Best for:** Monitoring, troubleshooting, system verification

## Detailed Operations

### Core Operations

#### 1. Data Validation

- Checks CSV file existence and structure
- Validates required 'text' column
- Identifies null, empty, or problematic entries
- Reports data quality statistics

#### 2. Vector Embedding

- Uses OpenAI's `text-embedding-3-large` model
- Processes documents in configurable batches (default: 100)
- Handles rate limiting and token limits automatically
- Supports retry logic for failed embeddings

#### 3. Database Operations

- Creates staging tables for safe operations
- Implements atomic operations with rollback capability
- Manages backup creation and restoration
- Handles connection pooling and retry logic

## Error Handling and Safety

### Built-in Safety Features

- **Staging Tables:** All operations use temporary staging tables first
- **Automatic Backups:** Destructive operations create timestamped backups
- **Validation:** Multiple validation layers prevent corrupt data
- **Retry Logic:** Automatic retry for transient failures
- **Rollback:** Failed operations can be rolled back

### Common Error Scenarios

1. **Missing Environment Variables:** Clear error messages guide setup
2. **Network Issues:** Automatic retry with exponential backoff
3. **Token Limits:** Dynamic batch size adjustment
4. **Data Corruption:** Validation prevents invalid data insertion

## Performance Considerations

### Batch Processing

- Documents processed in configurable batches (default: 100)
- Automatic adjustment for token limits
- Progress reporting for large datasets

### Resource Management

- Connection pooling for database efficiency
- Memory-efficient streaming for large files
- Automatic cleanup of temporary resources

### Scaling

- Chunked operations for large datasets (default: 1000 rows)
- Timeout handling for long-running operations
- Memory usage optimization

## Integration with Chatbot

The vector store created by this tool is directly used by `chatbot.py`:

1. **Vector Store Creation:** This tool creates the indexed knowledge base
2. **RAG Pipeline:** `chatbot.py` queries this vector store for relevant documents
3. **Response Generation:** Retrieved documents provide context for LLM responses

## Best Practices: Production Deployments

1. **Test first** with `--skip-maintenance` flag
2. **Use replace mode** only when necessary
3. **Monitor logs** for performance and errors
4. **Monitor health** regularly: `python src/vector_index_mgmt.py --health-check`

## Command Reference

```bash
# Basic usage (safe, appends data)
python src/vector_index_mgmt.py

# Replace all data (with backup)
python src/vector_index_mgmt.py --truncate

# Skip optional maintenance operations
python src/vector_index_mgmt.py --skip-maintenance

# Health check only
python src/vector_index_mgmt.py --health-check
```

## Output Files

The tool creates several output files:

- **Backup tables:** `{table_name}_backup_{timestamp}` (when using --truncate)
- **Export files:** `{table_name}_output_pandas.csv`
- **Log files:** Detailed operation logs in the console

## Next Steps

After successfully running this tool:

1. **Verify the vector store** with health checks
2. **Test the chatbot** to ensure responses use new data
3. **Monitor performance** for any degradation
4. **Document changes** for team knowledge

For more information about the chatbot and how to use it, see the related documentation in the `docs/` folder

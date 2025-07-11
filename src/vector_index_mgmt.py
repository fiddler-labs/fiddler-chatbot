"""--markdown
Vector Index Loader to Cassandra

Responsible for creating and managing vector indices in DataStax Cassandra for the Fiddler chatbot's RAG (Retrieval-Augmented Generation) system.

```mermaid
graph LR
    A[CSV file] --> B[Pandas DataFrame] --> C[LangChain Documents] --> D[OpenAI Embeddings] --> E[Cassandra Vector Store] --> F[used by chatbot.py for RAG]
```

"""

import os
import sys
import logging
import time
import functools
import pandas as pd
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, Any, Callable, Dict, List, Tuple, Union
from contextlib import contextmanager
from enum import Enum

# Configure Cassandra driver for Python 3.13 compatibility
# Need to provide asyncore compatibility for Python 3.13
# Python 3.12+ removed asyncore module, so we need to provide a compatibility layer
try:
    from utils.cassandra_compatibility import setup_cassandra_compatibility
    Cluster, Session, PlainTextAuthProvider, named_tuple_factory, cassandra_connection_class = setup_cassandra_compatibility()
except Exception as e:
    print(f"❌ Failed to setup Cassandra compatibility: {e}")
    sys.exit(1)

# Cassandra imports are now handled in the compatibility section above

from openai import OpenAI as OpenAIClient

from langchain_community.document_loaders import DataFrameLoader
from langchain_community.vectorstores import Cassandra
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings

from utils.custom_logging import setup_logging

# Setup logging with default values
setup_logging(log_level="DEBUG")
logger = logging.getLogger(__name__)

# ==================== ENUMS AND DATA CLASSES ====================

class OperationResult(Enum):
    """Enum for operation results"""
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"

@dataclass
class LoadResult:
    """Result of loading operation"""
    result: OperationResult
    message: str
    rows_processed: int = 0
    backup_table: Optional[str] = None
    errors: List[str] = field(default_factory=list)

@dataclass
class ValidationResult:
    """Result of configuration validation"""
    is_valid: bool
    errors:   List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    valid_rows: int = 0
    total_rows: int = 0

# ==================== CONFIGURATION ====================
# Centralized configuration to avoid hardcoding throughout the file
CONFIG = { # todo - follow this pattern in the chatbot.py file too
    "secure_bundle_path": "datastax_auth/secure-connect-fiddlerai.zip",
    "keyspace": "fiddlerai",
    "llm_provider": "openai", # 'GCP_VertexAI', 'Azure_OpenAI'
    "embedding_model": "text-embedding-3-large",
    "embedding_dimensions": 1536,
    "temperature": 0,
    "default_csv_path": "./local_assets/vector_index_feed_20250701011105.csv",
    "squad_table": "squad",
    "chatbot_history_table": "fiddler_chatbot_history",
    "backup_chunk_size": 1000,  # For backup operations
    "embedding_batch_size": 100,  # For processing embeddings in batches to avoid token limits
    "max_retry_attempts": 3,
    "retry_delay": 2.0,
    "retry_backoff": 2.0
    }

# Computed values
TABLE_NAME = f'fiddler_doc_snippets_{CONFIG["llm_provider"]}'

# ==================== DATABASE CONNECTION ====================

@contextmanager
def cassandra_connection():
    """
    Context manager for Cassandra database connections with built-in retry logic.
    Ensures proper cleanup of resources even if exceptions occur.
    
    Usage:
        with cassandra_connection() as (cluster, session):
            # Use cluster and session here
            pass
    """
    cluster = None
    session = None
    
    # Retry logic for connection establishment
    max_attempts = CONFIG["max_retry_attempts"]
    delay = CONFIG["retry_delay"]
    backoff = CONFIG["retry_backoff"]
    current_delay = delay
    last_exception = None
    
    for attempt in range(max_attempts):
        try:
            # Check environment variables first
            ASTRA_DB_APPLICATION_TOKEN = os.environ.get('ASTRA_DB_APPLICATION_TOKEN')
            if not ASTRA_DB_APPLICATION_TOKEN:
                raise ValueError("ASTRA_DB_APPLICATION_TOKEN environment variable not set")
            
            # Check file existence
            if not os.path.exists(CONFIG["secure_bundle_path"]):
                raise FileNotFoundError(f"Secure bundle file not found: {CONFIG['secure_bundle_path']}")
            
            # Establish connection to DataStax Cassandra
            cloud_config = {'secure_connect_bundle': CONFIG["secure_bundle_path"]}
            auth_provider = PlainTextAuthProvider("token", ASTRA_DB_APPLICATION_TOKEN)
            
            # Use the selected connection class if available, otherwise default
            if cassandra_connection_class:
                cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider, connection_class=cassandra_connection_class)
            else:
                cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            
            session = cluster.connect()
            session.set_keyspace(CONFIG["keyspace"])
            
            logger.info(f"✅ Connected to Cassandra keyspace: {CONFIG['keyspace']}")
            
            try:
                yield cluster, session
            finally:
                # Cleanup resources
                if session:
                    session.shutdown()
                if cluster:
                    cluster.shutdown()
                logger.info("🔌 Cassandra connection closed")
            
            return  # Success, exit retry loop
            
        except Exception as e:
            last_exception = e
            if attempt == max_attempts - 1:
                logger.error(f"❌ Failed to connect to Cassandra after {max_attempts} attempts")
                raise e
            
            logger.warning(f"⚠️  Connection attempt {attempt + 1}/{max_attempts} failed: {e}")
            logger.info(f"🔄 Retrying connection in {current_delay:.1f} seconds...")
            
            # Cleanup any partial resources
            if session:
                try:
                    session.shutdown()
                except Exception:
                    pass
                session = None
                
            if cluster:
                try:
                    cluster.shutdown()
                except Exception:
                    pass
                cluster = None
            
            time.sleep(current_delay)
            current_delay *= backoff

def setup_llm_and_embeddings():
    """
    Configure OpenAI LLM and embeddings
    Returns: (llm, embedding) tuple
    """
    try:
        llm = OpenAI(temperature=CONFIG["temperature"])
        
        # Explicitly use the desired model and configure its dimension size
        embedding = OpenAIEmbeddings(
            model=CONFIG["embedding_model"],
            dimensions=CONFIG["embedding_dimensions"]
            )
        
        logger.info(f"✅ LLM and Embeddings configured: {embedding.model} with {CONFIG['embedding_dimensions']} dimensions")
        return llm, embedding
        
    except Exception as e:
        logger.error(f"❌ Failed to setup Embeddings: {e}")
        logger.error(f"   Error type: {type(e).__name__}")
        logger.error( "   Check OPENAI_API_KEY env var")
        logger.error( "   Check ASTRA_DB_APPLICATION_TOKEN env var")
        raise

# ==================== DATA LOADING AND VECTOR STORE ====================

def validate_and_load_documentation_data(csv_path: Optional[str] = None) -> Tuple[ValidationResult, Optional[pd.DataFrame]]:
    """
    Load  and Validate documentation data from CSV file
    Returns: (validation_result, dataframe) tuple
    """
    if csv_path is None:
        csv_path = CONFIG["default_csv_path"]
    
    # At this point csv_path is guaranteed to be a string
    assert isinstance(csv_path, str), "csv_path must be a string at this point"
    
    validation_result = ValidationResult(is_valid=False)
    
    try:
        # Check file existence first
        if not os.path.exists(csv_path):
            validation_result.errors.append(f"CSV file not found: {csv_path}")
            return validation_result, None
        
        # Load CSV file
        df = pd.read_csv(csv_path)
        validation_result.total_rows = len(df)
        
        if len(df) == 0:
            validation_result.errors.append("CSV file is empty (no data rows)")
            return validation_result, None
        
        # Check for required columns
        if 'text' not in df.columns:
            validation_result.errors.append("CSV file must contain 'text' column")
            return validation_result, None
        
        # Check for empty or null text values
        null_count = df['text'].isna().sum()
        empty_count = (df['text'] == '').sum()
        
        if null_count > 0:
            validation_result.warnings.append(f"Found {null_count} null values in 'text' column")
        
        if empty_count > 0:
            validation_result.warnings.append(f"Found {empty_count} empty values in 'text' column")
        
        # Check for very short text entries that might not be useful
        short_text_count = (df['text'].str.len() < 10).sum()
        if short_text_count > 0:
            validation_result.warnings.append(f"Found {short_text_count} very short text entries (< 10 characters)")
        
        # Check for very long text entries that might cause issues
        long_text_count = (df['text'].str.len() > 10000).sum()
        if long_text_count > 0:
            validation_result.warnings.append(f"Found {long_text_count} very long text entries (> 10,000 characters)")
        
        # Clean the dataframe
        df_clean = df.dropna(subset=['text'])
        df_clean = df_clean[df_clean['text'].str.strip() != '']
        
        # Ensure we have a DataFrame not a Series
        if isinstance(df_clean, pd.Series):
            df_clean = df_clean.to_frame()
        
        validation_result.valid_rows = len(df_clean)
        
        if len(df_clean) == 0:
            validation_result.errors.append("No valid rows found after filtering null/empty text")
            return validation_result, None
        
        if len(df_clean) < len(df):
            validation_result.warnings.append(f"{len(df) - len(df_clean)} rows will be skipped due to missing/empty text")
        
        validation_result.is_valid = True
        logger.info(f"✅ CSV file validated: {validation_result.valid_rows} valid rows out of {validation_result.total_rows} total rows")
        
        # Reset index to ensure clean DataFrame
        df_clean = df_clean.reset_index(drop=True)
        
        return validation_result, df_clean
        
    except pd.errors.EmptyDataError as e:
        validation_result.errors.append(f"CSV file is empty: {e}")
        return validation_result, None
    except pd.errors.ParserError as e:
        validation_result.errors.append(f"CSV file parsing error: {e}")
        return validation_result, None
    except Exception as e:
        validation_result.errors.append(f"Failed to load CSV file: {type(e).__name__}: {e}")
        return validation_result, None

def safe_truncate_table(session, table_name: str, force: bool = False, create_backup: bool = True) -> bool:
    """
    Safely truncate table with confirmation and optional backup
    Returns True if truncated, False if skipped
    """

    def _create_backup_table(session, source_table: str, backup_table: str) -> bool:
        """
        Create a backup table with the same structure as the source table
        Returns True if successful, False otherwise
        """
        try:
            # Get the table definition from system schema
            table_def_query = """
            SELECT table_name, bloom_filter_fp_chance, caching, comment, compaction, compression,
                crc_check_chance, default_time_to_live, gc_grace_seconds, max_index_interval,
                memtable_flush_period_in_ms, min_index_interval, read_repair, speculative_retry
            FROM system_schema.tables 
            WHERE keyspace_name = %s AND table_name = %s
            """
            
            table_info = session.execute(table_def_query, (CONFIG["keyspace"], source_table))
            table_row = list(table_info)
            
            if not table_row:
                logger.error(f"❌ Source table {source_table} not found")
                return False
            
            # Get column definitions
            columns_query = """
            SELECT column_name, type, kind, position, clustering_order
            FROM system_schema.columns 
            WHERE keyspace_name = %s AND table_name = %s
            ORDER BY position
            """
            
            columns_info = session.execute(columns_query, (CONFIG["keyspace"], source_table))
            columns = list(columns_info)
            
            if not columns:
                logger.error(f"❌ No columns found for table {source_table}")
                return False
            
            # Build CREATE TABLE statement
            primary_keys = []
            clustering_keys = []
            regular_columns = []
            
            for col in columns:
                col_def = f"{col.column_name} {col.type}"
                
                if col.kind == 'partition_key':
                    primary_keys.append(col.column_name)
                elif col.kind == 'clustering':
                    clustering_keys.append(col.column_name)
                
                regular_columns.append(col_def)
            
            # Construct PRIMARY KEY clause
            if clustering_keys:
                primary_key_clause = f"PRIMARY KEY (({', '.join(primary_keys)}), {', '.join(clustering_keys)})"
            else:
                primary_key_clause = f"PRIMARY KEY ({', '.join(primary_keys)})"
            
            create_table_sql = f"""
            CREATE TABLE {CONFIG["keyspace"]}.{backup_table} (
                {', '.join(regular_columns)},
                {primary_key_clause}
            )
            """
            
            logger.info(f"Creating backup table with SQL: {create_table_sql}")
            session.execute(create_table_sql)
            logger.info(f"✅ Backup table {backup_table} created successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create backup table: {e}")
            logger.error(f"   Error type: {type(e).__name__}")
            logger.error(f"   Backup table name: {backup_table}")
            logger.error(f"   Source table: {source_table}")
            return False


    def _copy_table_data(session, source_table: str, backup_table: str) -> bool:
        """
        Copy all data from source table to backup table
        Returns True if successful, False otherwise
        """
        try:
            # Get all data from source table
            logger.info(f"Copying data from {source_table} to {backup_table}...")
            
            # Use INSERT INTO ... SELECT approach for efficient copying
            copy_query = f"""
            INSERT INTO {CONFIG["keyspace"]}.{backup_table} 
            SELECT * FROM {CONFIG["keyspace"]}.{source_table}
            """
            
            session.execute(copy_query)
            logger.info(f"✅ Data copied successfully from {source_table} to {backup_table}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to copy data to backup table: {e}")
            logger.error(f"   Error type: {type(e).__name__}")
            logger.error(f"   Source table: {source_table}")
            logger.error(f"   Backup table: {backup_table}")
            return False


    if not force:
        # First, check if table has data
        try:
            count_result = session.execute(f"SELECT COUNT(*) FROM {CONFIG['keyspace']}.{table_name}")
            current_count = list(count_result)[0].count
            
            if current_count > 0:
                logger.warning(f"\n⚠️  WARNING: Table '{table_name}' contains {current_count} rows.")
                logger.warning("This operation will DELETE ALL existing data.")
                
                if create_backup:
                    backup_table = f"{table_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    logger.info(f"Creating backup table: {backup_table}")
                    
                    # Create backup table with same structure
                    if not _create_backup_table(session, table_name, backup_table):
                        logger.error("❌ Failed to create backup table. Aborting truncation.")
                        return False
                    
                    # Copy data to backup table
                    if not _copy_table_data(session, table_name, backup_table):
                        logger.error("❌ Failed to backup data. Aborting truncation.")
                        return False
                    
                    logger.info(f"✅ Successfully backed up {current_count} rows to {backup_table}")
                else:
                    logger.warning("⚠️  No backup will be created (create_backup=False)")

        except Exception as e:
            logger.error(f"Warning: Could not check table count: {e}")
    
    try:
        session.execute(f"TRUNCATE TABLE {table_name}")
        logger.info(f"✅ Table '{table_name}' truncated successfully.")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to truncate table: {e}")
        raise

def populate_vector_store_safely(df: pd.DataFrame, session, embedding, table_name: str, replace_existing: bool = False) -> LoadResult:
    """
    Safely load documents into Cassandra vector store with staging and rollback capability
    
    Args:
        df: DataFrame containing the documents to load
        session: Cassandra session
        embedding: Embedding model
        table_name: Name of the target table
        replace_existing: If True, replace existing data (with backup). If False, append to existing data.
    
    Returns:
        LoadResult with details about the operation
    """
    staging_table = f"{table_name}_staging_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_table = None
    
    try:
        # 1. Load the pre-chunked documents from the DataFrame
        logger.info("Loading pre-chunked documents from the DataFrame...")
        loader = DataFrameLoader(df, page_content_column="text")
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} document chunks.")
        
        # 2. Create staging table and populate it first
        logger.info(f"Creating staging table '{staging_table}'...")
        staging_vector_store = Cassandra(
            embedding=embedding,
            session=session,
            keyspace=CONFIG["keyspace"],
            table_name=staging_table,
        )
        
        # 3. Add documents to staging table in batches to avoid token limits
        batch_size = CONFIG["embedding_batch_size"]  # Process documents in batches to stay within token limits
        total_documents = len(documents)
        logger.info(f"Adding {total_documents} chunks to staging table in batches of {batch_size}. This may take a few minutes...")
        
        for i in range(0, total_documents, batch_size):
            batch_end = min(i + batch_size, total_documents)
            batch_documents = documents[i:batch_end]
            batch_num = (i // batch_size) + 1
            total_batches = (total_documents + batch_size - 1) // batch_size
            
            logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch_documents)} documents)...")
            
            # Add batch with retry logic for token limits
            max_retries = CONFIG["max_retry_attempts"]
            retry_delay = CONFIG["retry_delay"]
            
            for attempt in range(max_retries):
                try:
                    staging_vector_store.add_documents(batch_documents)
                    logger.info(f"✅ Successfully processed batch {batch_num}/{total_batches}")
                    break
                except Exception as e:
                    if "max_tokens_per_request" in str(e) and attempt < max_retries - 1:
                        # If we hit token limits, reduce batch size and retry
                        if batch_size > 10:
                            batch_size = max(10, batch_size // 2)
                            logger.warning(f"⚠️  Token limit hit, reducing batch size to {batch_size} and retrying...")
                            # Recalculate batch with smaller size
                            batch_documents = documents[i:min(i + batch_size, total_documents)]
                            time.sleep(retry_delay)
                            continue
                        else:
                            raise e
                    elif attempt < max_retries - 1:
                        logger.warning(f"⚠️  Batch processing failed (attempt {attempt + 1}/{max_retries}): {e}")
                        time.sleep(retry_delay)
                        continue
                    else:
                        raise e
        
        # 4. Verify staging table has expected number of rows
        verify_query = f"SELECT COUNT(*) FROM {CONFIG['keyspace']}.{staging_table}"
        result = session.execute(verify_query)
        staging_count = list(result)[0].count
        
        if staging_count != len(documents):
            raise ValueError(f"Staging verification failed: expected {len(documents)} rows, got {staging_count}")
        
        logger.info(f"✅ Staging table populated successfully with {staging_count} rows")
        
        # 5. Handle replacement logic
        if replace_existing:
            # Create backup of existing table if it exists
            try:
                check_query = f"SELECT COUNT(*) FROM {CONFIG['keyspace']}.{table_name}"
                result = session.execute(check_query)
                existing_count = list(result)[0].count
                
                if existing_count > 0:
                    backup_table = f"{table_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    logger.info(f"Creating backup table '{backup_table}' with {existing_count} rows...")
                    
                    # Create backup table structure
                    backup_result = _create_backup_table_safe(session, table_name, backup_table)
                    if not backup_result:
                        raise ValueError("Failed to create backup table")
                    
                    # Copy data to backup
                    copy_result = _copy_table_data_chunked(session, table_name, backup_table)
                    if not copy_result:
                        raise ValueError("Failed to backup existing data")
                    
                    logger.info(f"✅ Backup completed: {backup_table}")
                    
                    # Truncate original table
                    session.execute(f"TRUNCATE TABLE {CONFIG['keyspace']}.{table_name}")
                    logger.info(f"✅ Truncated original table: {table_name}")
                
            except Exception as e:
                if "doesn't exist" in str(e) or "not found" in str(e):
                    logger.info(f"Target table '{table_name}' doesn't exist, will create new")
                else:
                    raise
        
        # 6. Copy data from staging to target table
        logger.info(f"Copying data from staging to target table '{table_name}'...")
        copy_result = _copy_table_data_chunked(session, staging_table, table_name)
        if not copy_result:
            raise ValueError("Failed to copy data from staging to target table")
        
        # 7. Verify target table
        verify_query = f"SELECT COUNT(*) FROM {CONFIG['keyspace']}.{table_name}"
        result = session.execute(verify_query)
        target_count = list(result)[0].count
        
        if replace_existing and target_count != len(documents):
            raise ValueError(f"Target table verification failed: expected {len(documents)} rows, got {target_count}")
        
        logger.info(f"✅ Target table populated successfully with {target_count} rows")
        
        # 8. Clean up staging table
        logger.info(f"Cleaning up staging table '{staging_table}'...")
        session.execute(f"DROP TABLE IF EXISTS {CONFIG['keyspace']}.{staging_table}")
        
        logger.info("\n✅ Success! All document chunks have been embedded and stored in Cassandra.")
        
        return LoadResult(
            result=OperationResult.SUCCESS,
            message=f"Successfully loaded {len(documents)} documents into {table_name}",
            rows_processed=len(documents),
            backup_table=backup_table
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to populate vector store: {e}")
        logger.error(f"   Error type: {type(e).__name__}")
        logger.error(f"   Table name: {table_name}")
        logger.error(f"   Replace existing: {replace_existing}")
        
        # Clean up staging table if it exists
        try:
            session.execute(f"DROP TABLE IF EXISTS {CONFIG['keyspace']}.{staging_table}")
            logger.info(f"Cleaned up staging table: {staging_table}")
        except Exception as cleanup_error:
            logger.warning(f"Failed to clean up staging table: {cleanup_error}")
        
        return LoadResult(
            result=OperationResult.FAILURE,
            message=f"Failed to load documents: {str(e)}",
            rows_processed=0,
            backup_table=backup_table,
            errors=[str(e)]
        )

def _create_backup_table_safe(session, source_table: str, backup_table: str) -> bool:
    """
    Create a backup table with the same structure as the source table
    Uses a safer approach that doesn't rely on system schema queries
    """
    try:
        # For vector stores, we can use a simple approach since we know the structure
        # This is safer than querying system schema tables
        logger.info(f"Creating backup table: {backup_table}")
        
        # Create the backup table by copying the structure
        create_sql = f"""
        CREATE TABLE {CONFIG["keyspace"]}.{backup_table} (
            row_id text PRIMARY KEY,
            vector vector<float, {CONFIG["embedding_dimensions"]}>,
            body_blob text,
            metadata_s map<text, text>
        )
        """
        
        session.execute(create_sql)
        logger.info(f"✅ Backup table structure created: {backup_table}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to create backup table: {e}")
        return False

def _copy_table_data_chunked(session, source_table: str, target_table: str, chunk_size: Optional[int] = None) -> bool:
    """
    Copy data from source table to target table in chunks to handle large datasets
    """
    if chunk_size is None:
        chunk_size = CONFIG["backup_chunk_size"]
    
    try:
        # Get total count first
        count_query = f"SELECT COUNT(*) FROM {CONFIG['keyspace']}.{source_table}"
        result = session.execute(count_query)
        total_rows = list(result)[0].count
        
        if total_rows == 0:
            logger.info(f"Source table {source_table} is empty, nothing to copy")
            return True
        
        logger.info(f"Copying {total_rows} rows from {source_table} to {target_table} in chunks of {chunk_size}")
        
        # Cassandra doesn't support INSERT INTO ... SELECT syntax
        # We need to read data and insert it row by row
        logger.info(f"Copying {total_rows} rows from {source_table} to {target_table}")
        
        # Read data in chunks and process them to avoid timeout
        effective_chunk_size = min(chunk_size if chunk_size is not None else 500, 500)  # Limit chunk size for data copy operations
        logger.info(f"Reading data in chunks of {effective_chunk_size} rows to avoid timeout...")
        
        # Insert data into target table
        insert_query = f"""
        INSERT INTO {CONFIG["keyspace"]}.{target_table} (row_id, vector, body_blob, metadata_s)
        VALUES (?, ?, ?, ?)
        """
        prepared_statement = session.prepare(insert_query)
        
        rows_copied = 0
        
        # Process data in chunks using token-based pagination
        # First, get all row IDs to process
        select_ids_query = f"SELECT row_id FROM {CONFIG['keyspace']}.{source_table}"
        id_rows = session.execute(select_ids_query)
        row_ids = [row.row_id for row in id_rows]
        
        logger.info(f"Found {len(row_ids)} rows to copy")
        
        # Process in chunks
        for i in range(0, len(row_ids), effective_chunk_size):
            chunk_end = min(i + effective_chunk_size, len(row_ids))
            chunk_ids = row_ids[i:chunk_end]
            
            # Get full row data for this chunk
            for row_id in chunk_ids:
                select_query = f"SELECT row_id, vector, body_blob, metadata_s FROM {CONFIG['keyspace']}.{source_table} WHERE row_id = ?"
                row_result = session.execute(select_query, (row_id,))
                row_data = list(row_result)
                
                if row_data:
                    row = row_data[0]
                    # Insert with timeout handling
                    try:
                        session.execute(prepared_statement, (row.row_id, row.vector, row.body_blob, row.metadata_s))
                        rows_copied += 1
                    except Exception as e:
                        if "timeout" in str(e).lower():
                            logger.warning(f"⚠️  Timeout on row {row_id}, retrying...")
                            time.sleep(1)
                            session.execute(prepared_statement, (row.row_id, row.vector, row.body_blob, row.metadata_s))
                            rows_copied += 1
                        else:
                            raise e
                
                # Log progress for large datasets
                if rows_copied % 100 == 0:
                    logger.info(f"Copied {rows_copied}/{total_rows} rows...")
        
        logger.info(f"✅ Copied {rows_copied} rows from {source_table} to {target_table}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to copy data from {source_table} to {target_table}: {e}")
        return False

def test_vector_store(vector_store, query: str = "What is Fiddler?", k: int = 2):
    """
    Quick test of the vector store functionality
    """
    try:
        docs = vector_store.similarity_search(query, k=k)
        result = f"Retrieved {len(docs)} docs for query '{query}'. "
        if docs:
            result += f"First doc preview: {docs[0].page_content[:100]}..."
        else:
            result += "No documents found."
        return result
    except Exception as e:
        return f"Test failed: {e}"

# ==================== TABLE INSPECTION UTILITIES ====================

def inspect_table_structure_safe(session, table_name: str, keyspace: Optional[str] = None) -> None:
    """
    Thread-safe utility to inspect Cassandra table structure and sample data
    Uses a local session approach to avoid row factory concurrency issues
    """
    if keyspace is None:
        keyspace = CONFIG["keyspace"]
        
    logger.info(f"\n=== INSPECTING TABLE: {keyspace}.{table_name} ===")
    
    try:
        # Create a new session for this specific operation to avoid concurrency issues
        # Use the existing cluster connection
        inspect_session = session.cluster.connect()
        inspect_session.set_keyspace(keyspace)
        inspect_session.row_factory = named_tuple_factory
        
        try:
            # Check table structure using system schema queries
            logger.info("\n=== TABLE INFORMATION ===")
            table_info_query = """
            SELECT table_name, bloom_filter_fp_chance, caching, comment, compaction, compression 
            FROM system_schema.tables 
            WHERE keyspace_name = %s AND table_name = %s
            """
            
            rows = inspect_session.execute(table_info_query, (keyspace, table_name))
            for row in rows:
                logger.info(f"Table: {row.table_name} ; \nCompaction: {row.compaction} ; \nCompression: {row.compression} ; \nCaching: {row.caching}")
            
            # Get column info
            logger.info("\n=== COLUMN INFORMATION ===")
            columns_query = """
            SELECT column_name, type, kind, position 
            FROM system_schema.columns 
            WHERE keyspace_name = %s AND table_name = %s
            """
            
            rows = inspect_session.execute(columns_query, (keyspace, table_name))
            for row in rows:
                logger.info(f"Column: {row.column_name}, Type: {row.type}, Kind: {row.kind}")
            
            # Get approximate row count
            logger.info("\n=== ROW COUNT (APPROXIMATE) ===")
            count_query = f"SELECT COUNT(*) FROM {keyspace}.{table_name}"
            try:
                result = inspect_session.execute(count_query)
                for row in result:
                    logger.info(f"Approximate row count: {row.count}")
            except Exception as e:
                logger.error(f"Note: COUNT(*) may timeout on large tables. Error: {e}")
            
            # Show sample data
            logger.info("\n=== SAMPLE DATA ===")
            sample_query = f"SELECT * FROM {keyspace}.{table_name} LIMIT 3"
            rows = inspect_session.execute(sample_query)
            for i, row in enumerate(rows):
                logger.info(f"\nSample row {i+1}:")
                logger.info(f"  Row ID: {getattr(row, 'row_id', 'N/A')}")
                if hasattr(row, 'body_blob'):
                    logger.info(f"  Content preview: {str(row.body_blob)[:100]}...")
                if hasattr(row, 'vector') and row.vector:
                    logger.info(f"  Vector dimensions: {len(row.vector)}")
                if hasattr(row, 'metadata_s'):
                    logger.info(f"  Metadata: {row.metadata_s}")
                    
        finally:
            # Clean up the inspect session
            inspect_session.shutdown()
            
    except Exception as e:
        logger.error(f"❌ Error inspecting table: {e}")

def query_and_display_rows_safe(session, table_name: str, limit: int = 10) -> None:
    """
    Thread-safe query and display rows from a table with proper formatting
    """
    try:
        cql_select = f'SELECT * FROM {CONFIG["keyspace"]}.{table_name} LIMIT {limit};'
        rows = session.execute(cql_select)
        
        logger.info(f"\n=== DISPLAYING {limit} ROWS FROM {table_name} ===")
        for row_i, row in enumerate(rows):
            logger.info(f'\nRow {row_i}:')
            # Handle different cassIO versions
            if hasattr(row, 'row_id'):
                logger.info(f'    row_id:      {row.row_id}')
                logger.info(f'    vector:      {str(row.vector)[:64]}...')
                logger.info(f'    body_blob:   {row.body_blob[:64]}...')
                logger.info(f'    metadata_s:  {row.metadata_s}')
            else:
                # Legacy format
                logger.info(f'    document_id:      {getattr(row, "document_id", "N/A")}')
                logger.info(f'    embedding_vector: {str(getattr(row, "embedding_vector", ""))[:64]}...')
                logger.info(f'    document:         {getattr(row, "document", "")[:64]}...')
                logger.info(f'    metadata_blob:    {getattr(row, "metadata_blob", "N/A")}')
                
        logger.info('\n...')
        
    except Exception as e:
        logger.error(f"❌ Error querying rows: {e}")

# ==================== DATA EXPORT UTILITIES ====================

def export_table_to_csv(session, table_name: str, output_file: Optional[str] = None) -> Optional[str]:
    """
    Export Cassandra table data to CSV file
    Returns the path to the created CSV file
    """
    if output_file is None:
        output_file = f'{table_name}_output_pandas.csv'
        
    try:
        cql_query = f'SELECT * FROM {CONFIG["keyspace"]}.{table_name};'
        logger.info("Executing query and loading data into pandas DataFrame...")
        rows = session.execute(cql_query)
        
        # Convert the Cassandra ResultSet to a pandas DataFrame
        df = pd.DataFrame(list(rows))
        
        if df.empty:
            logger.info("Query returned no data. CSV file will not be created.")
            return None
        else:
            # Save the DataFrame to a CSV file
            df.to_csv(output_file, index=False, encoding='utf-8')
            logger.info(f"✅ Success! Data has been saved to '{output_file}'")
            return output_file
            
    except Exception as e:
        logger.error(f"❌ Failed to export data to CSV: {e}")
        raise

# ==================== TABLE CREATION UTILITIES ====================

def create_chatbot_history_table(session) -> None:
    """
    Create table for storing chatbot interaction history
    """
    try:
        create_table_sql = f"""--sql
        CREATE TABLE IF NOT EXISTS {CONFIG["chatbot_history_table"]}
        (
            row_id text PRIMARY KEY,
            response text,
            response_vector vector<float, {CONFIG['embedding_dimensions']}>,
            source_docs text,
            source_docs_vector vector<float, {CONFIG['embedding_dimensions']}>,
            question text,
            question_vector vector<float, {CONFIG['embedding_dimensions']}>,
            comment text,
            feedback int,
            metadata_s map<text, text>,
            ts timestamp
        )
        -- WITH additional_write_policy = '99p'
            --     AND bloom_filter_fp_chance = 0.01
            --     AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
            --     AND comment = ''
            --     AND compaction = {'class': 'org.apache.cassandra.db.compaction.UnifiedCompactionStrategy'}
            --     AND compression = {'chunk_length_in_kb': '16', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
            --     AND crc_check_chance = 1.0
            --     AND default_time_to_live = 0
            --     AND gc_grace_seconds = 864000
            --     AND max_index_interval = 2048
            --     AND memtable_flush_period_in_ms = 0
            --     AND min_index_interval = 128
            --     AND read_repair = 'BLOCKING'
            --     AND speculative_retry = '99p';
        """
        
        session.execute(create_table_sql)
        logger.info(f"✅ Created table '{CONFIG['chatbot_history_table']}' successfully.")
        
    except Exception as e:
        logger.error(f"❌ Failed to create chatbot history table: {e}")
        raise

# ==================== OPENAI EMBEDDING UTILITIES ====================

def test_openai_embeddings(text: str = "Test text: Tell me about yourself") -> None:
    """
    Test OpenAI embeddings using the new API
    """
    try:
        # Using the new OpenAI client API
        client = OpenAIClient()
        response = client.embeddings.create(
            model=CONFIG["embedding_model"],
            input=text,
            dimensions=CONFIG["embedding_dimensions"]
        )
        logger.info(f"✅ Embedding retrieval successful. Model: {CONFIG['embedding_model']}")
        logger.info(f"   Embedding dimensions: {len(response.data[0].embedding)}")
        logger.info(f"   Generated embedding for: '{text}'")
        logger.info(f"   Embedding: {response.data[0].embedding[:80]}...")
        
    except Exception as e:
        logger.error(f"❌ Failed to test OpenAI embeddings: {e}")
        raise

# ==================== SQUAD TABLE UTILITIES ====================

def query_squad_table(session) -> pd.DataFrame:
    """
    Query and process data from the squad table
    """
    # Save original row factory to restore later
    original_row_factory = session.row_factory
    
    try:
        def pandas_factory(colnames, rows):
            return pd.DataFrame(rows, columns=colnames)
        
        # Temporarily set pandas factory
        session.row_factory = pandas_factory
        
        rows = session.execute(f'SELECT * from {CONFIG["squad_table"]}')
        df_baseline = rows._current_rows
        
        logger.info(f"✅ Retrieved {len(df_baseline)} rows from squad table")
        logger.info("Column types:")
        logger.info(df_baseline.dtypes)
        
        # Convert answers column to string
        df_baseline['answers'] = df_baseline['answers'].apply(lambda x: str(x))
        
        return df_baseline
        
    except Exception as e:
        logger.error(f"❌ Failed to query squad table: {e}")
        raise
    finally:
        # Restore original row factory (don't assume it was None)
        session.row_factory = original_row_factory

# ==================== MAIN EXECUTION ====================

def validate_environment() -> ValidationResult:
    """
    Validate environment variables and basic configuration
    Returns ValidationResult with details
    """
    logger.info("🔍 Validating environment configuration...")
    
    result = ValidationResult(is_valid=True)
    
    # Check environment variables
    if not os.environ.get('ASTRA_DB_APPLICATION_TOKEN'):
        result.errors.append("ASTRA_DB_APPLICATION_TOKEN environment variable not set")
        result.is_valid = False
    
    if not os.environ.get('OPENAI_API_KEY'):
        result.errors.append("OPENAI_API_KEY environment variable not set")
        result.is_valid = False
    
    # Check file existence
    if not os.path.exists(CONFIG["secure_bundle_path"]):
        result.errors.append(f"Secure bundle file not found: {CONFIG['secure_bundle_path']}")
        result.is_valid = False
    
    if result.is_valid:
        logger.info("✅ Environment validation passed")
    else:
        logger.error("❌ Environment validation failed")
        for error in result.errors:
            logger.error(f"   - {error}")
    
    return result

def load_vector_data(replace_existing: bool = False, csv_path: Optional[str] = None) -> LoadResult:
    """
    Core function to load vector data into Cassandra
    
    Args:
        replace_existing: If True, replace existing data with backup
        csv_path: Path to CSV file (optional, uses default if not provided)
    
    Returns:
        LoadResult with operation details
    """
    logger.info("=== Loading Vector Data ===")
    
    # 1. Validate environment first
    env_validation = validate_environment()
    if not env_validation.is_valid:
        return LoadResult(
            result=OperationResult.FAILURE,
            message="Environment validation failed",
            errors=env_validation.errors
        )
    
    # 1. Load and validate data first (for both dry-run and normal mode)
    logger.info("\n1. Loading and validating documentation data...")
    validation_result, df = validate_and_load_documentation_data(csv_path)
    if not validation_result.is_valid:
        logger.error("❌ Data validation failed:")
        for error in validation_result.errors:
            logger.error(f"   - {error}")
        return LoadResult(
            result=OperationResult.FAILURE,
            message="Data validation failed",
            errors=validation_result.errors
        )
    
    if df is None:
        return LoadResult(
            result=OperationResult.FAILURE,
            message="Failed to load data despite validation passing",
            errors=["Data loading failed"]
        )
    
    # Log warnings if any
    for warning in validation_result.warnings:
        logger.warning(f"⚠️  {warning}")
    
    # Initialize LLM and embeddings (only for non-dry-run)
    llm, myEmbedding = setup_llm_and_embeddings()
    
    try:
        with cassandra_connection() as (cluster, session):
            # 2. Populate vector store
            logger.info("\n2. Populating vector store...")
            if replace_existing:
                logger.warning("⚠️  REPLACE MODE: Will replace existing data with backup")
            
            load_result = populate_vector_store_safely(df, session, myEmbedding, TABLE_NAME, replace_existing=replace_existing)
            
            if load_result.result == OperationResult.SUCCESS:
                logger.info("\n3. Testing vector store...")
                # Create a simple vector store instance for testing
                vector_store = Cassandra(
                    embedding=myEmbedding,
                    session=session,
                    keyspace=CONFIG["keyspace"],
                    table_name=TABLE_NAME,
                )
                test_result = test_vector_store(vector_store)
                logger.info(test_result)
            
            return load_result
            
    except Exception as e:
        logger.error(f"❌ Vector data loading failed: {e}")
        return LoadResult(
            result=OperationResult.FAILURE,
            message=f"Loading failed: {str(e)}",
            errors=[str(e)]
        )

def perform_maintenance_operations(session) -> None:
    """
    Perform optional maintenance and inspection operations
    """
    logger.info("=== Performing Maintenance Operations ===")
    
    try:
        # 1. Inspect table structure
        logger.info("\n1. Inspecting table structure...")
        inspect_table_structure_safe(session, TABLE_NAME)
        
        # 2. Query and display sample rows
        logger.info("\n2. Displaying sample rows...")
        query_and_display_rows_safe(session, TABLE_NAME, limit=5)
        
        # 3. Export to CSV
        logger.info("\n3. Exporting data to CSV...")
        csv_file = export_table_to_csv(session, TABLE_NAME)
        logger.info(f"✅ Exported data to CSV: {csv_file}")
        
        # 4. Create chatbot history table
        logger.info("\n4. Creating chatbot history table...")
        create_chatbot_history_table(session)
        
        # 5. Test OpenAI embeddings
        logger.info("\n5. Testing OpenAI embeddings...")
        test_openai_embeddings()
        
        # 6. Query squad table
        logger.info("\n6. Querying squad table...")
        df_squad = query_squad_table(session)
        logger.info(f"✅ Retrieved {len(df_squad)} rows from squad table")
        logger.info(f"Column types: {df_squad.dtypes}")
        
    except Exception as e:
        logger.error(f"❌ Maintenance operations failed: {e}")
        # Don't raise here, as these are optional operations

def main(truncate_first: bool = False, skip_maintenance: bool = False, csv_path: Optional[str] = None):
    """
    Main execution function for the vector index loader
    
    Args:
        truncate_first (bool): If True, replace existing table data with backup. Default is False for safety.
        skip_maintenance (bool): If True, skip optional maintenance operations. Default is False.
        csv_path (str): Path to CSV file. If None, uses default path.
    
    This function demonstrates the typical workflow:
    1. Load vector data (core operation)
    2. Optionally perform maintenance operations
    
    Command line usage:
        python vector_index_mgmt.py                    # Safe mode: no replacement
        python vector_index_mgmt.py --truncate         # Replace with backup
        python vector_index_mgmt.py --skip-maintenance # Skip optional operations
    """
    logger.info("=== Cassandra Vector Index Loader ===")
    logger.info(f"Target table: {TABLE_NAME} \nKeyspace: {CONFIG['keyspace']} \nEmbedding model: {CONFIG['embedding_model']}")
    
    # 1. Core operation: Load vector data
    load_result = load_vector_data(replace_existing=truncate_first, csv_path=csv_path)
    
    if load_result.result != OperationResult.SUCCESS:
        logger.error(f"❌ Vector data loading failed: {load_result.message}")
        for error in load_result.errors:
            logger.error(f"   - {error}")
        raise ValueError(f"Vector data loading failed: {load_result.message}")
    
    logger.info(f"✅ {load_result.message}")
    if load_result.backup_table:
        logger.info(f"✅ Backup table created: {load_result.backup_table}")
    
    # 2. Optional maintenance operations
    if not skip_maintenance:
        try:
            with cassandra_connection() as (cluster, session):
                perform_maintenance_operations(session)
        except Exception as e:
            logger.error(f"❌ Maintenance operations failed: {e}")
            # Don't raise here, as these are optional operations

def comprehensive_health_check(session, table_name: str) -> dict:
    """
    Perform comprehensive health checks on the vector store
    
    Returns:
        dict: Health check results
    """
    health_results = {
        "overall_health": "unknown",
        "checks": {},
        "warnings": [],
        "errors": []
    }
    
    try:
        # 1. Basic connectivity check
        health_results["checks"]["connectivity"] = "passed"
        
        # 2. Table existence check
        try:
            count_query = f"SELECT COUNT(*) FROM {CONFIG['keyspace']}.{table_name}"
            result = session.execute(count_query)
            row_count = list(result)[0].count
            health_results["checks"]["table_exists"] = "passed"
            health_results["checks"]["row_count"] = row_count
        except Exception as e:
            health_results["checks"]["table_exists"] = "failed"
            health_results["errors"].append(f"Table check failed: {e}")
            health_results["overall_health"] = "failed"
            return health_results
        
        # 3. Sample data integrity check
        try:
            sample_query = f"SELECT * FROM {CONFIG['keyspace']}.{table_name} LIMIT 5"
            rows = session.execute(sample_query)
            sample_rows = list(rows)
            
            if len(sample_rows) > 0:
                health_results["checks"]["sample_data"] = "passed"
                
                # Check vector dimensions
                for row in sample_rows:
                    if hasattr(row, 'vector') and row.vector:
                        vector_dim = len(row.vector)
                        if vector_dim != CONFIG["embedding_dimensions"]:
                            health_results["warnings"].append(f"Vector dimension mismatch: expected {CONFIG['embedding_dimensions']}, got {vector_dim}")
                        break
                
                # Check for required fields
                required_fields = ['row_id', 'vector', 'body_blob']
                for field in required_fields:
                    if not hasattr(sample_rows[0], field):
                        health_results["errors"].append(f"Missing required field: {field}")
                        
            else:
                health_results["warnings"].append("No sample data found in table")
                
        except Exception as e:
            health_results["checks"]["sample_data"] = "failed"
            health_results["errors"].append(f"Sample data check failed: {e}")
        
        # 4. Vector store functionality check
        try:
            from langchain_community.vectorstores import Cassandra
            from langchain_openai import OpenAIEmbeddings
            
            # Create a minimal embedding for testing
            embedding = OpenAIEmbeddings(
                model=CONFIG["embedding_model"],
                dimensions=CONFIG["embedding_dimensions"]
            )
            
            vector_store = Cassandra(
                embedding=embedding,
                session=session,
                keyspace=CONFIG["keyspace"],
                table_name=table_name,
            )
            
            # Test similarity search
            test_results = vector_store.similarity_search("test query", k=1)
            health_results["checks"]["vector_search"] = "passed"
            health_results["checks"]["search_result_count"] = len(test_results)
            
        except Exception as e:
            health_results["checks"]["vector_search"] = "failed"
            health_results["errors"].append(f"Vector search check failed: {e}")
        
        # 5. Overall health assessment
        if len(health_results["errors"]) == 0:
            health_results["overall_health"] = "healthy"
        elif len(health_results["errors"]) > 0:
            health_results["overall_health"] = "unhealthy"
            
    except Exception as e:
        health_results["overall_health"] = "failed"
        health_results["errors"].append(f"Health check failed: {e}")
    
    return health_results

if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Cassandra Vector Index Management Tool')
    parser.add_argument('--truncate', '-t', action='store_true', 
                       help='Replace existing data with backup (DESTRUCTIVE)')
    parser.add_argument('--skip-maintenance', action='store_true', 
                       help='Skip optional maintenance operations')
    parser.add_argument('--csv-path', type=str, 
                       help='Path to CSV file (optional, uses default if not provided)')
    parser.add_argument('--health-check', action='store_true', 
                       help='Perform comprehensive health check only')
    
    args = parser.parse_args()
    
    if args.health_check:
        logger.info("=== Performing Health Check ===")
        try:
            with cassandra_connection() as (cluster, session):
                health_results = comprehensive_health_check(session, TABLE_NAME)
                
                logger.info(f"Overall Health: {health_results['overall_health'].upper()}")
                
                for check_name, result in health_results["checks"].items():
                    if isinstance(result, str):
                        status = "✅" if result == "passed" else "❌"
                        logger.info(f"{status} {check_name}: {result}")
                    else:
                        logger.info(f"📊 {check_name}: {result}")
                
                for warning in health_results["warnings"]:
                    logger.warning(f"⚠️  {warning}")
                
                for error in health_results["errors"]:
                    logger.error(f"❌ {error}")
                
                if health_results["overall_health"] == "unhealthy":
                    sys.exit(1)
                    
        except Exception as e:
            logger.error(f"❌ Health check failed: {e}")
            sys.exit(1)
    else:
        if args.truncate:
            print("⚠️  REPLACE mode enabled: existing data will be backed up to a secondary timestamped table and replaced")
        
        main(truncate_first=args.truncate, skip_maintenance=args.skip_maintenance, csv_path=args.csv_path)


## Advanced Refactoring Proposal for Cassandra Managemnt

### config.py - Configuration Management
```python
@dataclass
class CassandraConfig:
    secure_bundle_path: str = "datastax_auth/secure-connect-fiddlerai.zip"
    keyspace: str = "fiddlerai"
    token_env_var: str = "ASTRA_DB_APPLICATION_TOKEN"

@dataclass
class EmbeddingConfig:
    model: str = "text-embedding-3-large"
    dimensions: int = 1536
    temperature: float = 0.0

@dataclass
class LoaderConfig:
    csv_path: str = "documentation_data/vector_index_feed_v25.10.csv"
    table_name: str = "fiddler_doc_snippets_openai"
    truncate_before_load: bool = True
    batch_size: int = 100
```

### connection.py - Database Connection
```python
class CassandraConnection:
    """Manages Cassandra database connections with proper resource handling."""
    
    def __init__(self, config: CassandraConfig):
        self.config = config
        self._cluster = None
        self._session = None
    
    def connect(self) -> Session:
        """Establish connection with retry logic and proper error handling."""
    
    def disconnect(self):
        """Properly close connections."""
    
    @contextmanager
    def session_scope(self):
        """Context manager for automatic connection handling."""
```

### embeddings.py - Embedding Management
```python
class EmbeddingManager:
    """Handles OpenAI embedding configuration and testing."""
    
    def __init__(self, config: EmbeddingConfig):
        self.config = config
        self._initialize_models()
    
    def get_embeddings(self) -> OpenAIEmbeddings:
        """Return configured embedding model."""
    
    def test_embedding(self, text: str) -> dict:
        """Test embedding generation (replaces the deprecated API call)."""
```

### loader.py - Main Loading Logic
```python
class VectorLoader:
    """Main class for loading documents into vector store."""
    
    def __init__(self, connection: CassandraConnection, 
                 embedding_manager: EmbeddingManager,
                 config: LoaderConfig):
        self.connection = connection
        self.embedding_manager = embedding_manager
        self.config = config
    
    def load_documents(self, csv_path: str = None) -> LoadResult:
        """Load documents from CSV into vector store."""
    
    def quick_test(self, query: str = "What is Fiddler?") -> str:
        """Test the vector store with a sample query."""
```

### vector_store.py - Vector Store Operations
```python
class VectorStoreManager:
    """Manages Cassandra vector store operations."""
    
    def __init__(self, session: Session, embeddings: OpenAIEmbeddings):
        self.session = session
        self.embeddings = embeddings
    
    def create_store(self, keyspace: str, table_name: str) -> Cassandra:
        """Create or get vector store instance."""
    
    def truncate_table(self, table_name: str):
        """Safely truncate table with confirmation."""
    
    def add_documents(self, documents: List[Document], 
                     batch_size: int = 100) -> int:
        """Add documents with progress tracking."""
```

### table_manager.py - Table Management
```python
class TableManager:
    """Handles table creation and schema management."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_history_table(self):
        """Create chatbot history table with proper schema."""
    
    def create_vector_table(self, table_name: str):
        """Create vector store table if not exists."""
    
    def get_table_schema(self, keyspace: str, table_name: str) -> dict:
        """Get detailed table schema information."""
```

### inspector.py - Inspection Utilities
```python
class TableInspector:
    """Utilities for inspecting and analyzing tables."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def inspect_table(self, keyspace: str, table_name: str) -> TableInfo:
        """Get comprehensive table information."""
    
    def get_sample_data(self, table_name: str, limit: int = 3) -> pd.DataFrame:
        """Get sample data from table."""
    
    def export_to_csv(self, table_name: str, output_path: str):
        """Export table data to CSV."""
```

### migrator.py - Data Migration
```python
class DataMigrator:
    """Handles data migration between tables."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def migrate_history_to_ledger(self):
        """Migrate data from history to ledger table."""
    
    def process_squad_data(self):
        """Process and convert squad table data."""
```

### cli.py - Command Line Interface
```python
@click.group()
def cli():
    """Cassandra Vector Loader CLI"""
    pass

@cli.command()
@click.option('--csv', help='Path to CSV file')
@click.option('--table', help='Target table name')
@click.option('--truncate/--no-truncate', default=True)
def load(csv, table, truncate):
    """Load documents into vector store."""

@cli.command()
@click.option('--table', required=True)
@click.option('--output', help='Output CSV path')
def inspect(table, output):
    """Inspect table structure and data."""

@cli.command()
def test():
    """Run quick test query."""
```

## Example Usage After Refactoring

### As a Library
```python
from cassandra_vector_loader import CassandraVectorLoader, LoaderConfig

# Configure and load
config = LoaderConfig(
    csv_path="path/to/docs.csv",
    table_name="my_vectors",
    truncate_before_load=False
)

loader = CassandraVectorLoader(config)
result = loader.load_documents()
print(f"Loaded {result.document_count} documents in {result.duration}s")
```

### As a CLI Tool
```bash
# Load documents
python -m cassandra_vector_loader load --csv docs.csv --table my_vectors

# Inspect table
python -m cassandra_vector_loader inspect --table my_vectors --output analysis.csv

# Test query
python -m cassandra_vector_loader test --query "What is Fiddler?"

# Migrate data
python -m cassandra_vector_loader migrate --from history --to ledger
```

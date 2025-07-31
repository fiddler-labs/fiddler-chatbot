CONFIG_DATA_GENERATION = {
    "FIDDLER_MAIN_REPO_URL": "https://github.com/fiddler-labs/fiddler.git",
    "FIDDLER_EXAMPLES_REPO_URL": "https://github.com/fiddler-labs/fiddler-examples.git",
    "FIDDLER_WEBSITE_BLOG_URL": "https://www.fiddler.ai/blog/",
    "FIDDLER_WEBSITE_RESOURCES_URL": "https://www.fiddler.ai/resources/",

    # GeneralText splitting configuration
    "RECURSIVE_SPLITTER_CHUNK_SIZE": 3000,
    "RECURSIVE_SPLITTER_CHUNK_OVERLAP": 600,
    
    # MarkdownHeaderTextSplitter configuration
    "USE_MARKDOWN_HEADER_SPLITTER": True,  # Enable markdown header-based splitting
    "MARKDOWN_STRIP_HEADERS": False,  # Keep headers for better context
    "MARKDOWN_RETURN_EACH_LINE": False,  # Aggregate lines by headers
    "MARKDOWN_HEADERS_TO_SPLIT_ON": [
        ("#", "Header 1"),
        # ("##", "Header 2"), 
        # ("###", "Header 3"),
        # ("####", "Header 4")
        ],
        
    "KEEP_REPOS": True,
    "KEEP_CSV_FILES": True,

    # Notebook conversion method configuration
    "NOTEBOOK_CONVERSION_METHOD": "native_regex", # Options: 'jupyter_nbconvert' or 'native_regex'

    # Markdown flattening method configuration
    "MARKDOWN_FLATTENING_METHOD": "individual", # Options: 'individual' or 'concatenated'
    }

CONFIG_VECTOR_INDEX_MGMT = {
    "secure_bundle_path": "datastax_auth/secure-connect-fiddlerai.zip",
    "keyspace": "fiddlerai",
    "TABLE_NAME": "fiddler_doc_snippets_openai",
    "embedding_model": "text-embedding-3-large",
    "embedding_dimensions": 1536,
    "temperature": 0,
    "squad_table": "squad",
    "chatbot_history_table": "fiddler_chatbot_history",
    "embedding_batch_size": 100,  # For processing embeddings in batches to avoid token limits
    "max_retry_attempts": 3,
    "retry_delay": 2.0,
    "retry_backoff": 2.0
    }

CONFIG_CHATBOT_OLD = {
    "PROJECT_NAME": "fiddler_chatbot_v3",
    "MODEL_NAME": "fiddler_rag_chatbot",
    "URL": "https://demo.fiddler.ai",
    
    "ASTRA_DB_SECURE_BUNDLE_PATH": "datastax_auth/secure-connect-fiddlerai.zip",
    "ASTRA_DB_KEYSPACE": "fiddlerai",
    "ASTRA_DB_TABLE_NAME": "fiddler_doc_snippets_openai",
    "ASTRA_DB_LEDGER_TABLE_NAME": "fiddler_chatbot_ledger",
    
    "TOP_K_RETRIEVAL": 6,
    
    "OPENAI_EMBEDDING_MODEL": "text-embedding-3-large",
    "OPENAI_LLM_MODEL": "gpt-4-turbo",
    
    "GR__FAITHFULNESS_SCORE": 0.0,
    "GR__JAILBREAK_SCORE": 0.0,
    "GR__SAFETY_LATENCY": 0.0,
    "GR__REQUESTS_TIMEOUT": 60
    }

CONFIG_CHATBOT_NEW = {
    "FIDDLER_URL": "https://preprod.cloud.fiddler.ai",

    "GR__FAITHFULNESS_SCORE": 0.0,
    "GR__JAILBREAK_SCORE": 0.0,
    "GR__SAFETY_LATENCY": 0.0,
    "GR__REQUESTS_TIMEOUT": 60,

    "TOP_K_RETRIEVAL": 6,
    }

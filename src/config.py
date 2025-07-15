CONFIG_CHATBOT_OLD = {
    "PROJECT_NAME": "fiddler_chatbot_v3",
    "MODEL_NAME": "fiddler_rag_chatbot",
    "URL": "https://preprod.cloud.fiddler.ai",
    "ORG_NAME": "preprod",
    
    "ASTRA_DB_SECURE_BUNDLE_PATH": "datastax_auth/secure-connect-fiddlerai.zip",
    "ASTRA_DB_KEYSPACE": "fiddlerai",
    "ASTRA_DB_TABLE_NAME": "fiddler_doc_snippets_openai",
    "ASTRA_DB_LEDGER_TABLE_NAME": "fiddler_chatbot_ledger",
    
    "OPENAI_EMBEDDING_MODEL": "text-embedding-3-large",
    "OPENAI_LLM_MODEL": "gpt-4-turbo",
    
    "GR__FAITHFULNESS_SCORE": 0.0,
    "GR__JAILBREAK_SCORE": 0.0,
    "GR__SAFETY_LATENCY": 0.0,
    "GR__REQUESTS_TIMEOUT": 30
}

CONFIG_CHATBOT_NEW = {
    "FIDDLER_URL": "https://preprod.cloud.fiddler.ai",

    "GR__FAITHFULNESS_SCORE": 0.0,
    "GR__JAILBREAK_SCORE": 0.0,
    "GR__SAFETY_LATENCY": 0.0,
    "GR__REQUESTS_TIMEOUT": 30
}

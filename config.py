CONFIG_CHATBOT_OLD = {
    "PROJECT_NAME": "fiddler_chatbot_v3",
    "MODEL_NAME": "fiddler_rag_chatbot",
    "URL": "https://preprod.fiddler.ai",
    "ORG_NAME": "preprod",
    
    "ASTRA_DB_SECURE_BUNDLE_PATH": "datastax_auth/secure-connect-fiddlerai.zip",
    "ASTRA_DB_KEYSPACE": "fiddlerai",
    "ASTRA_DB_TABLE_NAME": "fiddler_doc_snippets_openai",
    "ASTRA_DB_LEDGER_TABLE_NAME": "fiddler_chatbot_ledger",
    
    "OPENAI_EMBEDDING_MODEL": "text-embedding-3-large",
    "OPENAI_LLM_MODEL": "gpt-4-turbo",
    
    "FAITHFULNESS_SCORE": 0.0,
    "JAILBREAK_SCORE": 0.0,
    "SAFETY_GUARDRAIL_LATENCY": 0.0,
    "REQUESTS_TIMEOUT": 30
}

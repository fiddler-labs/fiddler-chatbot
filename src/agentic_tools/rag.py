import logging
from typing import Dict, Any
from langchain_core.messages import AIMessage, HumanMessage
from fiddler_langgraph.tracing.instrumentation import set_llm_context

from vector_index_mgmt import cassandra_connection, setup_llm_and_embeddings, CONFIG, TABLE_NAME
from langchain_community.vectorstores import Cassandra as CassandraVectorStore

from agentic_tools.state_data_model import ChatbotState

logger = logging.getLogger(__name__)

def rag_node(state: ChatbotState) -> Dict[str, Any]:
    """
    Retrieve relevant documents from the Cassandra vector database using RAG.
    
    Args:
        state: Current conversation state containing messages
        
    Returns:
        Dictionary with updated messages including retrieved context
    """
    try:
        # Get the last user message for retrieval
        last_message = None
        for msg in reversed(state["messages"]):
            if isinstance(msg, HumanMessage):
                last_message = msg
                break
        
        if not last_message:
            logger.warning("No user message found for RAG retrieval")
            return {"messages": [AIMessage(content="No query found for document retrieval.")]}
        
        query = str(last_message.content)  # Ensure query is a string
        logger.info(f"Performing RAG retrieval for query: '{query[:100]}...'")
        
        # Set up embeddings and vector store
        llm, embedding = setup_llm_and_embeddings()
        
        # Connect to Cassandra and perform retrieval
        with cassandra_connection() as (cluster, session):
            # Initialize vector store
            vector_store = CassandraVectorStore(
                embedding=embedding,
                session=session,
                keyspace=CONFIG["keyspace"],
                table_name=TABLE_NAME
            )
            
            # Perform similarity search
            k = 5  # Number of documents to retrieve
            documents = vector_store.similarity_search(query, k=k)
            
            if not documents:
                logger.warning("No relevant documents found")
                return {"messages": [AIMessage(content="No relevant documents found in the knowledge base.")]}
            
            # Format retrieved documents
            retrieved_context = []
            for i, doc in enumerate(documents, 1):
                content = doc.page_content[:500]  # Truncate for brevity
                metadata = doc.metadata
                
                # Extract useful metadata
                source = metadata.get('source', 'Unknown')
                title = metadata.get('title', 'Untitled')
                
                retrieved_context.append(
                    f"Document {i} (Source: {source}, Title: {title}):\n{content}..."
                )
                        
            # Create context message
            context_message = (
                f"📚 Retrieved {len(documents)} relevant documents for your query:\n\n" +
                "\n\n".join(retrieved_context) +
                "\n\n🤖 I'll use this information to provide you with a comprehensive answer."
            )
            
            logger.info(f"Successfully retrieved {len(documents)} documents")

            set_llm_context(llm, context_message)
            
            # Store retrieved documents in state for use by other nodes
            return {
                "messages": [AIMessage(content=context_message)],
                "retrieved_documents": documents,  # Store for potential use by other nodes
                "retrieval_query": query
            }
            
    except Exception as e:
        logger.error(f"Error in RAG retrieval: {e}")
        error_message = f"❌ Error retrieving documents: {str(e)}"
        return {"messages": [AIMessage(content=error_message)]}

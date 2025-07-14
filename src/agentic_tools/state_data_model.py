# Define the state schema for our chatbot
from typing import Sequence, NotRequired, Optional
from typing_extensions import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class ChatbotState(TypedDict):
    """Enhanced state schema for the chatbot conversation"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    retrieved_documents: NotRequired[Optional[list]]
    retrieval_query: NotRequired[Optional[str]]

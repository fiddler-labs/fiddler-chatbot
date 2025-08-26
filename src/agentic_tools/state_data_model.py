# Define the state schema for our chatbot
from typing import Sequence #, Any, List, Dict, NotRequired, Optional
from typing_extensions import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
# import operator

class ChatbotState(TypedDict):
    """Enhanced state schema for the chatbot conversation"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    # messages: Annotated[list[Any], operator.add]


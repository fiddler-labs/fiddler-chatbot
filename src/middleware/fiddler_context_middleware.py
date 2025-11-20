"""
Fiddler Context Middleware for LangGraph v1

This module provides middleware to automatically capture tool call context
and pass it to Fiddler's set_llm_context function for enhanced observability.

For LangGraph v1 agents created with `create_agent`, use the middleware decorator.
For StateGraph-based agents, use the helper function `set_context_from_tool_messages`.
"""

import json
import logging
from collections.abc import Awaitable, Callable
from typing import Any

from langchain.agents.middleware import (
    AgentMiddleware,
    ModelRequest,
    ModelResponse,
)
from langchain_core.messages import ToolMessage

from fiddler_langgraph.tracing.instrumentation import set_llm_context

logger = logging.getLogger(__name__)


def _format_tool_context(tool_messages: list[ToolMessage]) -> str:
    """
    Format tool messages into a structured context string.

    Args:
        tool_messages: List of ToolMessage objects from the conversation state

    Returns:
        Formatted context string with tool call details
    """
    if not tool_messages:
        return ""

    context_parts = []
    context_parts.append(f"🔧 Tool Calls ({len(tool_messages)}):")

    for i, tool_msg in enumerate(tool_messages, 1):
        tool_name = tool_msg.name or "unknown"
        tool_call_id = tool_msg.tool_call_id or "unknown"

        # Try to parse content as JSON, fallback to string
        try:
            content_obj = json.loads(tool_msg.content) if isinstance(tool_msg.content, str) else tool_msg.content
            content_str = json.dumps(content_obj, indent=2) if isinstance(content_obj, (dict, list)) else str(tool_msg.content)
        except (json.JSONDecodeError, TypeError):
            content_str = str(tool_msg.content)

        # Truncate very long content for readability
        max_content_length = 1000
        if len(content_str) > max_content_length:
            content_str = content_str[:max_content_length] + f"... (truncated, {len(content_str)} chars total)"

        context_parts.append(
            f"\n{i}. Tool: {tool_name}\n"
            f"   ID: {tool_call_id}\n"
            f"   Result: {content_str}"
        )

    return "\n".join(context_parts)


class FiddlerContextMiddleware(AgentMiddleware):
    """
    Middleware to automatically capture tool call context and set LLM context.

    This middleware intercepts model calls and extracts ToolMessages from the
    conversation state. It formats the tool call information and passes it to
    Fiddler's set_llm_context function for enhanced observability.

    Supports both sync and async execution contexts.
    """

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse]
    ) -> ModelResponse:
        """Synchronous version of the middleware."""
        try:
            state = request.state

            # Extract ToolMessages from the conversation state
            if 'messages' in state:
                tool_messages = [
                    msg for msg in state['messages']
                    if isinstance(msg, ToolMessage)
                ]

                if tool_messages:
                    # Format tool context
                    context = _format_tool_context(tool_messages)

                    # Set LLM context with tool call information
                    if context:
                        set_llm_context(request.model, context)
                        logger.debug(f"Set LLM context with {len(tool_messages)} tool call(s)")
                else:
                    logger.debug("No tool messages found in state, skipping context setting")
            else:
                logger.debug("No 'messages' key in state, skipping context setting")

        except Exception as e:
            # Log error but don't break the execution flow
            logger.warning(f"Error in Fiddler context middleware: {e}", exc_info=True)

        # Always call the handler to continue the execution
        return handler(request)

    async def awrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], Awaitable[ModelResponse]]
    ) -> ModelResponse:
        """Asynchronous version of the middleware."""
        try:
            state = request.state

            # Extract ToolMessages from the conversation state
            if 'messages' in state:
                tool_messages = [
                    msg for msg in state['messages']
                    if isinstance(msg, ToolMessage)
                ]

                if tool_messages:
                    # Format tool context
                    context = _format_tool_context(tool_messages)

                    # Set LLM context with tool call information
                    if context:
                        set_llm_context(request.model, context)
                        logger.debug(f"Set LLM context with {len(tool_messages)} tool call(s)")
                else:
                    logger.debug("No tool messages found in state, skipping context setting")
            else:
                logger.debug("No 'messages' key in state, skipping context setting")

        except Exception as e:
            # Log error but don't break the execution flow
            logger.warning(f"Error in Fiddler context middleware: {e}", exc_info=True)

        # Always call the handler to continue the execution
        return await handler(request)


# Create a singleton instance for use as middleware
create_fiddler_context_middleware = FiddlerContextMiddleware()


def set_context_from_tool_messages(
    state: dict[str, Any],
    model: Any,
    messages_key: str = "messages"
) -> None:
    """
    Helper function for StateGraph-based agents to set LLM context from tool messages.

    This function extracts ToolMessages from the state and sets the LLM context.
    Use this in your StateGraph nodes (e.g., chatbot_node, tool_execution_node)
    when you want to capture tool call context.

    Args:
        state: The conversation state dictionary
        model: The LLM model instance to set context for
        messages_key: The key in state that contains the messages list (default: "messages")

    Example:
        ```python
        def chatbot_node(state: ChatbotState):
            # ... your code ...
            set_context_from_tool_messages(state, base_llm)
            response = llm.invoke(all_messages_in_state)
            # ... rest of code ...
        ```
    """
    try:
        if messages_key in state:
            tool_messages = [
                msg for msg in state[messages_key]
                if isinstance(msg, ToolMessage)
            ]

            if tool_messages:
                context = _format_tool_context(tool_messages)
                if context:
                    set_llm_context(model, context)
                    logger.debug(f"Set LLM context with {len(tool_messages)} tool call(s) from state")
            else:
                logger.debug("No tool messages found in state, skipping context setting")
        else:
            logger.debug(f"No '{messages_key}' key in state, skipping context setting")

    except Exception as e:
        logger.warning(f"Error setting context from tool messages: {e}", exc_info=True)

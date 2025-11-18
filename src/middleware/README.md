# Fiddler Context Middleware

This module provides middleware and helper functions to automatically capture tool call context and pass it to Fiddler's `set_llm_context` function for enhanced observability.

## Usage

### For LangGraph v1 Agents (using `create_agent`)

Use the middleware decorator when creating your agent:

```python
from langchain.agents import create_agent
from src.middleware.fiddler_context_middleware import create_fiddler_context_middleware

app = create_agent(
    model=base_llm,
    tools=tools,
    system_prompt=SYSTEM_INSTRUCTIONS_PROMPT,
    middleware=[create_fiddler_context_middleware]
)
```

The middleware will automatically:
- Extract ToolMessages from the conversation state before each model call
- Format tool call information (name, ID, results)
- Call `set_llm_context` with the formatted context
- Continue with normal execution

### For StateGraph-based Agents

For agents built with `StateGraph` (not using `create_agent`), use the helper function in your nodes:

```python
from src.middleware.fiddler_context_middleware import set_context_from_tool_messages

def chatbot_node(state: ChatbotState):
    all_messages_in_state = state["messages"]

    # Set context from tool messages before invoking LLM
    set_context_from_tool_messages(state, base_llm)

    response = llm.invoke(all_messages_in_state)
    # ... rest of your code ...
```

## What Gets Captured

The middleware captures:
- Tool name
- Tool call ID
- Tool execution results (formatted as JSON if possible)
- Multiple tool calls in a single context string

## Context Format

The context string is formatted as:
```
🔧 Tool Calls (N):
1. Tool: tool_name
   ID: tool_call_id
   Result: {formatted_result}
...
```

Results are automatically truncated if they exceed 1000 characters to maintain readability.

## Notes

- The middleware is non-blocking: if an error occurs, it logs a warning but continues execution
- Tool messages are extracted from the `messages` key in the state
- Only ToolMessage instances are captured (not AIMessage tool_calls)
- The middleware runs before each model call, ensuring context is set for subsequent LLM invocations

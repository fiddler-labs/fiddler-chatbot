# Guardrails as Deterministic Step: Implementation Options

## Problem Statement

**Current State:**
- Guardrails are implemented as tools (`tool_fiddler_guardrail_safety`, `tool_fiddler_guardrail_faithfulness`)
- They are invoked based on system instructions (occasionally, non-deterministically)
- The LLM decides when to call them based on the prompt

**Goal:**
- Make guardrail checks a **deterministic, mandatory step** that happens on every user input
- Keep it as part of the LangGraph execution flow (not external preprocessing)
- Ensure Fiddler's LangGraph SDK captures these steps in traces
- Avoid embedding the React agent inside another graph (too complex)

**Constraints:**
- Must be part of LangGraph control flow for Fiddler tracing
- Must execute deterministically for every user input
- Should not add unnecessary complexity
- Should remain a "step" in the execution graph, not just a tool call

---

## Option 1: **`before_agent` Middleware Hook** ⭐ RECOMMENDED

### Description
Use the `before_agent` hook in custom middleware to run guardrail validation before the agent loop starts. This hook runs **once per invocation**, making it perfect for input validation.

### How It Works
```python
from langchain.agents.middleware import AgentMiddleware, before_agent
from langchain.agents import create_agent
from src.agentic_tools.fiddler_gaurdrails import get_safety_guardrail_results
import logging

logger = logging.getLogger(__name__)

@before_agent
def guardrail_safety_check(state, runtime):
    """Run safety guardrail on every incoming user message."""
    # Get the last user message
    messages = state.get("messages", [])
    if not messages:
        return None

    last_message = messages[-1]
    if hasattr(last_message, 'content'):
        user_input = last_message.content

        # Run safety guardrail
        jailbreak_score, latency = get_safety_guardrail_results(user_input)
        logger.info(f"Safety guardrail: score={jailbreak_score:.2f}, latency={latency:.2f}s")

        # If jailbreak detected, short-circuit the agent
        if jailbreak_score > 0.5:
            from langchain_core.messages import AIMessage
            return {
                "messages": [AIMessage(
                    content=f"⚠️ SECURITY ALERT: Potential jailbreak attempt detected (Score: {jailbreak_score:.2f}). "
                            "Your query has been blocked for security reasons."
                )],
                "jump_to": "end"  # Short-circuit to end
            }

    return None  # Continue normal execution

# Create agent with guardrail middleware
app = create_agent(
    model=base_llm,
    tools=tools,
    system_prompt=SYSTEM_INSTRUCTIONS_PROMPT,
    checkpointer=checkpointer,
    middleware=[
        guardrail_safety_check,  # Runs before agent starts
        create_fiddler_context_middleware  # Existing middleware
    ]
)
```

### Pros
- ✅ **Deterministic**: Runs exactly once per user input, before any agent processing
- ✅ **Part of LangGraph flow**: Middleware hooks are fully integrated into the graph execution
- ✅ **Fiddler tracing**: Captured by Fiddler's LangGraph SDK automatically
- ✅ **Simple implementation**: Decorator-based approach is clean and minimal
- ✅ **Short-circuit capability**: Can use `jump_to: "end"` to block malicious queries
- ✅ **No graph nesting**: Stays within the same React agent graph
- ✅ **Composable**: Can add multiple middleware in sequence

### Cons
- ⚠️ Runs only at the start of agent invocation (not between tool calls)
- ⚠️ For multi-turn conversations, only validates the latest user input

### Best For
- **Input validation guardrails** (safety, jailbreak detection)
- **Pre-processing steps** that should happen before the agent thinks

---

## Option 2: **`before_model` Middleware Hook**

### Description
Use the `before_model` hook to run guardrails before **each LLM call**. This runs multiple times in an agent loop (before every model invocation).

### How It Works
```python
from langchain.agents.middleware import AgentMiddleware
from typing import Any

class GuardrailsMiddleware(AgentMiddleware):
    """Middleware that runs safety checks before each model call."""

    def before_model(self, state, runtime) -> dict[str, Any] | None:
        """Run before each LLM call in the agent loop."""
        messages = state.get("messages", [])

        # Only run on HumanMessages
        human_messages = [m for m in messages if isinstance(m, HumanMessage)]
        if not human_messages:
            return None

        last_human_message = human_messages[-1]
        user_input = last_human_message.content

        # Run safety guardrail
        jailbreak_score, latency = get_safety_guardrail_results(user_input)
        logger.info(f"Safety guardrail (before model): score={jailbreak_score:.2f}")

        if jailbreak_score > 0.5:
            return {
                "messages": [AIMessage(
                    content=f"⚠️ SECURITY ALERT: Jailbreak detected (Score: {jailbreak_score:.2f})"
                )],
                "jump_to": "end"
            }

        return None

# Usage
app = create_agent(
    model=base_llm,
    tools=tools,
    system_prompt=SYSTEM_INSTRUCTIONS_PROMPT,
    checkpointer=checkpointer,
    middleware=[
        GuardrailsMiddleware(),
        create_fiddler_context_middleware
    ]
)
```

### Pros
- ✅ Runs before **every model call** (multiple times per agent invocation)
- ✅ Part of LangGraph flow, captured by Fiddler
- ✅ Can modify state or system prompts before LLM sees them
- ✅ More granular control over when guardrails run

### Cons
- ⚠️ May run **multiple times** per user input (once per tool call cycle)
- ⚠️ Could add latency if guardrail API is slow
- ⚠️ More complex to track which message triggered which check

### Best For
- **Output guardrails** that need to run before each LLM generation
- **Dynamic prompt modification** based on safety context
- Scenarios where you want to validate state at each reasoning step

---

## Option 3: **`after_model` Middleware Hook (For Response Validation)**

### Description
Use the `after_model` hook to validate LLM responses after they're generated, before they're shown to the user.

### How It Works
```python
from langchain.agents.middleware import AgentMiddleware
from langchain_core.messages import AIMessage, ToolMessage

class FaithfulnessGuardrailMiddleware(AgentMiddleware):
    """Validate LLM responses for faithfulness after RAG."""

    def after_model(self, state, runtime) -> dict[str, Any] | None:
        """Run after each LLM response."""
        messages = state.get("messages", [])
        if not messages:
            return None

        last_message = messages[-1]

        # Check if this is an AI response (not a tool call)
        if isinstance(last_message, AIMessage) and last_message.content:
            # Check if there are any ToolMessages (RAG results) in recent history
            recent_tool_messages = [
                m for m in messages[-10:]  # Look at last 10 messages
                if isinstance(m, ToolMessage) and m.name == "rag_over_fiddler_knowledge_base"
            ]

            if recent_tool_messages:
                # Extract RAG documents from tool message
                rag_result = recent_tool_messages[-1].content
                # Parse the documents (implementation depends on your RAG output format)
                source_docs = parse_rag_documents(rag_result)

                # Run faithfulness guardrail
                response_text = last_message.content
                faithfulness_score, latency = get_faithfulness_guardrail_results(
                    response_text, source_docs
                )

                logger.info(f"Faithfulness guardrail: score={faithfulness_score:.2f}")

                # Optionally block low-faithfulness responses
                if faithfulness_score < 0.6:
                    return {
                        "messages": [AIMessage(
                            content="I apologize, but I don't have enough reliable information to answer that question accurately."
                        )],
                        "jump_to": "end"
                    }

        return None
```

### Pros
- ✅ Validates **output quality** before user sees it
- ✅ Can block hallucinations or unfaithful responses
- ✅ Part of LangGraph execution, traced by Fiddler

### Cons
- ⚠️ Runs **after** the LLM has already generated the response (wasted tokens if blocked)
- ⚠️ Harder to extract RAG context from message history
- ⚠️ May run multiple times in agent loop

### Best For
- **Faithfulness validation** after RAG responses
- **Output filtering** (toxicity, policy compliance)
- **Quality assurance** checks on final responses

---

## Option 4: **Preprocessing Node in Custom StateGraph** (Not Recommended)

### Description
Build a custom StateGraph with a dedicated guardrails node instead of using `create_agent`.

### How It Works
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class ChatbotState(TypedDict):
    messages: list
    guardrail_passed: bool

def guardrail_node(state: ChatbotState):
    """Dedicated guardrails validation node."""
    # Run safety check
    # ...
    return {"guardrail_passed": True}

def agent_node(state: ChatbotState):
    """The React agent logic."""
    # ...
    return state

def should_continue(state: ChatbotState):
    """Router function."""
    if not state.get("guardrail_passed"):
        return END
    return "agent"

# Build graph
workflow = StateGraph(ChatbotState)
workflow.add_node("guardrails", guardrail_node)
workflow.add_node("agent", agent_node)
workflow.set_entry_point("guardrails")
workflow.add_conditional_edges("guardrails", should_continue)
workflow.add_edge("agent", END)

app = workflow.compile(checkpointer=checkpointer)
```

### Pros
- ✅ Maximum control over execution flow
- ✅ Guardrails are clearly visible as a separate node
- ✅ Easy to visualize in graph diagrams

### Cons
- ❌ **High complexity**: Requires rebuilding the entire React agent from scratch
- ❌ **Loss of `create_agent` benefits**: No built-in middleware, tool handling, etc.
- ❌ **Maintenance burden**: Need to manually implement agent loop logic
- ❌ **Graph nesting**: You'd have to embed the React agent inside your custom graph

### Best For
- **Not recommended** for this use case due to complexity

---

## Option 5: **Hybrid - Middleware + Modified System Prompt**

### Description
Combine middleware for deterministic guardrail execution with an updated system prompt to remove the tool-based guardrail instructions.

### How It Works
```python
# Middleware handles the deterministic execution
@before_agent
def safety_guardrail(state, runtime):
    """Mandatory safety check."""
    # ... (same as Option 1)
    pass

# Remove guardrail tools from the tools list
tools = [
    get_system_time,
    rag_over_fiddler_knowledge_base,
    # tool_fiddler_guardrail_safety,  # REMOVED
    # tool_fiddler_guardrail_faithfulness,  # REMOVED
    validate_url,
]

# Update system prompt to remove guardrail instructions
# (No need to tell LLM about guardrails since they're automatic)

app = create_agent(
    model=base_llm,
    tools=tools,  # No guardrail tools
    system_prompt=UPDATED_SYSTEM_INSTRUCTIONS,  # No guardrail instructions
    checkpointer=checkpointer,
    middleware=[
        safety_guardrail,  # Automatic, deterministic
        create_fiddler_context_middleware
    ]
)
```

### Pros
- ✅ Clean separation: guardrails are infrastructure, not agent decisions
- ✅ Simplified system prompt (less confusion for LLM)
- ✅ Deterministic and traceable

### Cons
- ⚠️ Need to update documentation and system prompts
- ⚠️ Faithfulness guardrail is harder to implement deterministically (needs RAG context)

---

## Option 6: **FastAPI/Starlette Middleware** (Not Recommended for Your Use Case)

### Description
Use FastAPI middleware at the HTTP server level to intercept requests before they reach LangGraph.

### How It Works
```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

class GuardrailsHTTPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Parse request body
        body = await request.body()
        # Run guardrail
        # ...
        response = await call_next(request)
        return response

app.add_middleware(GuardrailsHTTPMiddleware)
```

### Pros
- ✅ Runs at HTTP layer (very early in request lifecycle)
- ✅ Can block requests before any LangGraph processing

### Cons
- ❌ **Not part of LangGraph execution**: Won't be traced by Fiddler's LangGraph SDK
- ❌ **Outside the graph**: Violates your constraint of being part of LangGraph flow
- ❌ **Less context**: Harder to access conversation state, message history
- ❌ **Chainlit integration**: Harder to integrate with Chainlit's message flow

### Best For
- **Not recommended** - violates the requirement to be part of LangGraph execution

---

## Comparison Matrix

| Option | Deterministic | Fiddler Traced | Complexity | Runs On | Best Use Case |
|--------|--------------|----------------|------------|---------|---------------|
| **1. before_agent** | ✅ Yes | ✅ Yes | ⭐ Low | Start of invocation | **Input validation** |
| **2. before_model** | ✅ Yes | ✅ Yes | ⭐⭐ Medium | Before each LLM call | Output guardrails |
| **3. after_model** | ✅ Yes | ✅ Yes | ⭐⭐ Medium | After each LLM call | Response validation |
| **4. Custom StateGraph** | ✅ Yes | ✅ Yes | ⭐⭐⭐⭐⭐ Very High | Custom flow | Not recommended |
| **5. Hybrid (1 + Prompt)** | ✅ Yes | ✅ Yes | ⭐⭐ Medium | Start + simplified prompt | **Clean architecture** |
| **6. HTTP Middleware** | ✅ Yes | ❌ No | ⭐⭐ Medium | HTTP layer | Not suitable |

---

## Recommended Implementation Strategy

### Phase 1: Safety Guardrail (Input Validation)
**Use Option 1** - `before_agent` middleware hook

```python
# File: src/middleware/guardrails_middleware.py

from langchain.agents.middleware import before_agent
from langchain_core.messages import AIMessage, HumanMessage
from src.agentic_tools.fiddler_gaurdrails import get_safety_guardrail_results
import logging

logger = logging.getLogger(__name__)

JAILBREAK_THRESHOLD = 0.5

@before_agent
def safety_guardrail_middleware(state, runtime):
    """
    Mandatory safety guardrail that runs on every user input.
    Blocks jailbreak attempts before agent processing begins.
    """
    messages = state.get("messages", [])
    if not messages:
        return None

    # Get the last message
    last_message = messages[-1]

    # Only check HumanMessages (user inputs)
    if isinstance(last_message, HumanMessage):
        user_input = last_message.content

        try:
            # Run safety guardrail API
            jailbreak_score, latency = get_safety_guardrail_results(user_input)

            logger.info(
                f"Safety guardrail executed: score={jailbreak_score:.3f}, "
                f"latency={latency:.2f}s, threshold={JAILBREAK_THRESHOLD}"
            )

            # Block high-risk queries
            if jailbreak_score > JAILBREAK_THRESHOLD:
                logger.warning(
                    f"Jailbreak attempt blocked! Score: {jailbreak_score:.3f} > {JAILBREAK_THRESHOLD}"
                )
                return {
                    "messages": [AIMessage(
                        content=f"⚠️ SECURITY ALERT: Potential jailbreak attempt detected "
                                f"(Score: {jailbreak_score:.2f}). Your query has been blocked "
                                f"for security reasons. Please rephrase your question appropriately."
                    )],
                    "jump_to": "end"  # Skip agent processing
                }

        except Exception as e:
            logger.error(f"Safety guardrail error: {e}", exc_info=True)
            # Fail open or fail closed depending on your security requirements
            # For now, fail open (allow execution) to avoid blocking legitimate users

    # Continue normal execution
    return None
```

**Update chatbot:**

```python
# File: src/chatbot_chainlit_react.py

from src.middleware.guardrails_middleware import safety_guardrail_middleware
from src.middleware.fiddler_context_middleware import create_fiddler_context_middleware

# Remove guardrail tools from the list
tools = [
    get_system_time,
    rag_over_fiddler_knowledge_base,
    # tool_fiddler_guardrail_safety,  # NOW HANDLED BY MIDDLEWARE
    # tool_fiddler_guardrail_faithfulness,  # KEEP AS TOOL FOR NOW
    validate_url,
]

app = create_agent(
    model=base_llm,
    tools=tools,
    system_prompt=SYSTEM_INSTRUCTIONS_PROMPT,
    checkpointer=checkpointer,
    middleware=[
        safety_guardrail_middleware,  # Runs first (input validation)
        create_fiddler_context_middleware  # Runs second (context enrichment)
    ]
)
```

### Phase 2: Faithfulness Guardrail (Response Validation)

**Use Option 3** - `after_model` middleware hook

This is more complex because faithfulness requires:

1. Knowing when RAG was called
2. Accessing the retrieved documents
3. Validating the AI response against those documents

**Alternative for Faithfulness:** Keep it as a tool for now, but make it mandatory in the system prompt with stronger language. The middleware approach is better suited for input validation than for RAG-dependent output validation.

---

## Tracing and Observability

All middleware hooks are **automatically traced** by Fiddler's LangGraph SDK because they're part of the `create_agent` execution graph:

- `before_agent` → Logged as a pre-processing step
- `before_model` → Logged before each LLM call
- `after_model` → Logged after each LLM response
- Middleware exceptions → Captured in traces

You can verify this by checking the Fiddler UI after implementing the middleware.

---

## Implementation Checklist

- [ ] Create `src/middleware/guardrails_middleware.py` with `safety_guardrail_middleware`
- [ ] Import and add middleware to `create_agent` in `chatbot_chainlit_react.py`
- [ ] Remove `tool_fiddler_guardrail_safety` from tools list
- [ ] Update `system_instructions_AGENTIC.md` to remove safety guardrail tool instructions
- [ ] Test with normal queries (should pass through)
- [ ] Test with jailbreak attempts (should be blocked)
- [ ] Verify traces appear in Fiddler UI
- [ ] Monitor latency impact (safety API adds ~0.X seconds per request)
- [ ] Consider adding caching for repeated identical queries
- [ ] Document the new architecture in README

---

## Additional Considerations

### Performance
- Safety guardrail API adds latency (~100-500ms typically)
- Runs on **every** user input (no caching by default)
- Consider implementing a cache for repeated queries

### Error Handling
- Decide: **fail open** (allow on error) vs **fail closed** (block on error)
- Currently recommended: fail open for better UX, with error logging

### Testing
- Unit test the middleware in isolation
- Integration test with Fiddler tracing
- Test jailbreak detection with known bad queries
- Test latency impact on user experience

### Future Enhancements
- Add configurable thresholds (per-user, per-environment)
- Implement result caching to reduce API calls
- Add metrics/monitoring for guardrail performance
- Consider batching if Fiddler API supports it

---

## Conclusion

**Recommended Approach:** **Option 1 - `before_agent` Middleware Hook**

This option perfectly balances:
- ✅ Deterministic execution (runs once per user input)
- ✅ Part of LangGraph flow (Fiddler traces it)
- ✅ Simple implementation (decorator-based)
- ✅ No graph nesting (stays within `create_agent`)
- ✅ Short-circuit capability (can block malicious queries)

For **safety guardrails**, this is the cleanest and most effective solution. For **faithfulness guardrails**, consider keeping them as tools (invoked by system prompt) for now, since they require RAG context that's easier to access from within the agent loop.

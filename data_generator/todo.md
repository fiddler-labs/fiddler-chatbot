# TODO

## Main Tasks

- Langchain / Langgraph V1.0 API change issue for create_react_agent function.

- Tool span differentiation
  - Review the new response context handling in the ReAct Agentic simulator to ensure the RAG context is properly passed through to the CSV.
  - Verify that the context field (gen_ai.llm_input.system) is populated correctly and not left empty in the csv dataset.
  - Investigate why all RAG responses are currently grouped under a single tool span.
  - Implement a new attribute (e.g., tool_name) to clearly segregate RAG context responses from other tool responses for better traceability and faithfulness evaluation.

## Low Priority Refactoring Suggestions

- Extract constants (magic numbers, special prefixes)
- Add type hints throughout
- Extract configuration to config file
- Add progress tracking/logging for batch processing
- Add inline code documentation for complex logic
- Create usage examples for different persona types
- Separate question generation strategies into clean interfaces

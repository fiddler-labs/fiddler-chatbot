# TODO

## Main Tasks

- implement PII detection similiarly to jailed personas ,
  - created a json first using imagined PII data , control with a instruction prompt that lists the PII data expected

## Low Priority Refactoring Suggestions

- Extract constants (magic numbers, special prefixes)
- Add type hints throughout
- Extract configuration to config file
- Add progress tracking/logging for batch processing
- Add inline code documentation for complex logic
- Create usage examples for different persona types
- Separate question generation strategies into clean interfaces

## Structural/Architectural Issues Discovered During Linter Hardening

- **src/chatbot.py**: Uses deprecated `langchain.chains` API (legacy file). The imports are marked with `type: ignore` comments, but this file should be migrated to the newer LangChain API when refactoring. The newer chatbot implementations (`chatbot_chainlit.py`, `chatbot_chainlit_react.py`, `chatbot_agentic.py`) use the modern LangGraph-based approach.

- **Variable scoping patterns**: Several files had "possibly unbound" variable errors that indicate potential refactoring opportunities:
  - `src/chatbot.py`: Variables initialized at function scope but used conditionally - consider using a state object or more explicit control flow
  - `src/vector_index_mgmt.py`: Exception handlers referencing variables that might not be initialized - pattern suggests need for better error handling structure

- **Type safety improvements**:
  - `data_generator/validate_pipeline.py`: Had to explicitly convert DataFrame columns to pandas Series for type checker - suggests pandas type hints could be improved throughout codebase
  - `src/utils/custom_logging.py`: Function attribute pattern replaced with module-level variable - singleton pattern could be standardized across codebase

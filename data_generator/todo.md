# TODO

## Main Tasks

- implement PII detection similiarly to jailed personas ,
  - created a json first using imagined PII data , control with a instruction prompt that lists the PII data expected

- implement deterministic step for guardrails , see /docs/guardrails-deterministic-step-options.md

## Low Priority Refactoring Suggestions

- **Variable scoping patterns**: Several files had "possibly unbound" variable errors that indicate potential refactoring opportunities:
  - `src/vector_index_mgmt.py`: Exception handlers referencing variables that might not be initialized - pattern suggests need for better error handling structure

- **Type safety improvements**:
  - `data_generator/validate_pipeline.py`: Had to explicitly convert DataFrame columns to pandas Series for type checker - suggests pandas type hints could be improved throughout codebase
- Extract constants (magic numbers, special prefixes)
- Add type hints throughout
- Extract configuration to config file
- Add progress tracking/logging for batch processing
- Add inline code documentation for complex logic
- Create usage examples for different persona types
- Separate question generation strategies into clean interfaces

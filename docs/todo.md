# TODO

## Pending action items listed in planned order of execution and priority

## Main Tasks

- check gaurdrails aliveness on every session start .
  - alert the user on teh frontend if the check fails
  - also run it on a loop so that the gaurdrails are always alive

- include try-except blocks inside the guardrail calling tools itself
  - please explore the best way to do this as per the langgraph best practices
  - dont raise errors in the test_guardrails_availability.py script , just log the error and continue gracefully , let the LLM know the response is not available in this call , maybe a success flag

- implement PII detection similiarly to jailed personas ,
  - created a json first using imagined PII data , control with a instruction prompt that lists the PII data expected

- implement deterministic step for guardrails , see /docs/guardrails-deterministic-step-options.md

- make repo private
  - Find Praveen's commit : and revert it , now that the repo is private , lets implement the github actions

- Add MCP as a tool from gitbooks to replace the cassandra stack
  - pitch this is as long term replacement to the clunky data stax rag stack ( 75% of the codebase is related to the cassandra stack )

- python files not getting processed in to the md-notebooks folder from the fiddler-exmaples folder
  - the `fiddler-utils` folder is not being processed into the md-notebooks folder
  - the `misc-utils` folder is not being processed into the md-notebooks folder


## Lower priority considerations / Deep future tasks

- More Tools implementation for agentic orchestration

  - Also explore the gitbook APIs : those can be a tool call ideas too

  - Nick's idea : a request a demo funcitonality , where if someone requests a demo , then the chatbot gathers data and sends it to a endpoint  / google form / webhook

  - Python Code Validation Tool:
    - **Problem**: LLM-generated code may contain syntax/type errors or hallucinated functions
    - **Solution**: Implement type checking on LLM outputs using tools like Pyright/Pylsp
    - **Process**:
      - Run type checker on generated code
      - If validation fails, automatically modify code to make it compliant
      - Return corrected, validated code
    - **Goal**: Reduce code hallucination and improve accuracy
    - **Architecture**: Can be wrapped as module-as-a-service or lightweight agent

- Deployment and Development QoL
  - Set up GitHub Actions workflow for automated embedding update
    - set up a dev branch of `fiddler` repo to test out the github action

- Expand README with comprehensive project documentation (setup, usage, architecture, etc.)
- Implemnt PROD mode and DEV mode globally controllable , cicd style , point to different location
- purge uv env and re-install everything after clean up to retain only needed packages
- Testing framework basic setup (pytest)
- Security review of Datastax authentication flow
- Dev and Prod environments currently mixed : Implement config-driven environment switching : Clean separation of development vs production data/settings
- GitHub Actions workflow for test automation : Immediate feedback on breaking changes

- Better coding practices
  - Resource Management:  No cleanup of temporary files on failure
  - Extract constants / Magic numbers: Hardcoded timeouts, chunk sizes, special prefixes, etc.
  - Add type hints throughout
  - data_generation.py - Extract configuration to config file
  - data_generation.py - Add progress tracking/logging for batch processing

- **Variable scoping patterns**: Several files had "possibly unbound" variable errors that indicate potential refactoring opportunities:
  - `src/vector_index_mgmt.py`: Exception handlers referencing variables that might not be initialized - pattern suggests need for better error handling structure

- **Type safety improvements**:
  - `data_generator/validate_pipeline.py`: Had to explicitly convert DataFrame columns to pandas Series for type checker - suggests pandas type hints could be improved throughout codebase

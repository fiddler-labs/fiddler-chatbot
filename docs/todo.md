# Pending Tasks

- Tools implementation for agentic orchestration
  
  - Overall Strategy:
    - Keep tool calls simple and focused (avoid over-engineering with multiple agents)
    - Focus on validation and correction rather than complex reasoning
    - Enable tracking and monitoring through existing infrastructure
  
  - URL Validation Tool:
    - **Problem**: Generated URLs may lead to non-existent pages (hallucination)
    - **Solution**: Build URL validator that checks if links are accessible
    - **Goal**: Ensure all recommended URLs actually exist and are reachable
    - **Implementation**: Tool call that can be tracked via otel tracers for Harrier dogfooding
    - **Integration**: GitBook APIs can serve as validation medium

  - Python Code Validation Tool:
    - **Problem**: LLM-generated code may contain syntax/type errors or hallucinated functions
    - **Solution**: Implement type checking on LLM outputs using tools like Pyright/Pylsp
    - **Process**:
      - Run type checker on generated code
      - If validation fails, automatically modify code to make it compliant
      - Return corrected, validated code
    - **Goal**: Reduce code hallucination and improve accuracy
    - **Architecture**: Can be wrapped as module-as-a-service or lightweight agent

  - Also explore the gitbook APIs : those can be a tool call ideas too

- Deployment QoL
  - Set up GitHub Actions workflow for automated embedding update
  - make a definitive notebook , to onbaord the models and aset up the alerts ; will serve as a iterative improvement checkpoint

- Langraph-sdk integration for proposed agentic tools
  - Install langraph sdk by understanding the process with Sri

## Lower priority considerations

- Expand README with comprehensive project documentation (setup, usage, architecture, etc.)
- Implement error handling and logging throughout the application
- Implemnt PROD mode and DEV mode globally controllable , cicd style , point to different location
- Testing framework setup (pytest)
- Security review of Datastax authentication flow
- purge uv env and re-install everything after clean up to retain only needed packages
- git submodules implementation for cloned repos to allow for stable rollbacks

- duplicate sri's MCP server to have a docs RAG server

- create .mdc file that just contains the tree view of the repo
  - include it on every chat via 'always' setting
  - make a python script that updates this .mdc file and run this script as a precommit hook
  - add it to git ognore , both the files : mdc and py

---

## Notes

- since we use notebooks from `fiddler-examples` , all the good stuff from cs-utils will automatically be inherited as reference assets
- this repo is now essentially zero touch , as all the manual work of updating the embeddings has been converted into scripts; all the cloning , massaging , is now automated

## Comprehensive Bug report: `data_generation.py` ( in decreasing order of priority )

- Data Consistency Problems
  - No idempotency: Running twice produces different results (appends to existing docs) .Make process repeatable without side effects
  - No change detection: Re-processes everything even if sources unchanged
  - No validation: No verification that downloaded content is complete/valid

- Resource Management:  No cleanup of temporary files on failure
- Magic numbers: Hardcoded timeouts, chunk sizes
- Make CSS selectors configurable - Move to config file
- Move from requirements.txt to uv's pyproject.toml for better dependency management

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

- Langraph-sdk integration for proposed agentic tools
  - Install langraph sdk by understanding the process with Sri

- Deployment and Development QoL
  - While logging is present , it is not very verbose , build stuff with INFO level around the chatbot
  - Set up GitHub Actions workflow for automated embedding update
  - make a definitive notebook , to onbaord the models and aset up the alerts ; will serve as a iterative improvement checkpoint
  - make a notebook to that leverages data_generation.py and the /utils to create demp props
    - need to showcase to team all the possible methods to see what works best

## Lower priority considerations

- Expand README with comprehensive project documentation (setup, usage, architecture, etc.)
- Implement error handling and logging throughout the application
- Implemnt PROD mode and DEV mode globally controllable , cicd style , point to different location
- Security review of Datastax authentication flow
- purge uv env and re-install everything after clean up to retain only needed packages
- Testing framework setup (pytest)
- git submodules implementation for cloned repos to allow for stable rollbacks

- duplicate sri's MCP server to have a docs RAG server

## Better coding practices

- Data Consistency Problems
  - No idempotency: Running twice may produce different results) .Make process repeatable without side effects
  - No change detection: Re-processes everything even if sources unchanged

- Resource Management:  No cleanup of temporary files on failure
- Magic numbers: Hardcoded timeouts, chunk sizes
- Make CSS selectors configurable - Move to config file

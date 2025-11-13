# TODO

## Pending action items listed in planned order of execution and priority

- make repo private , now that streamlit community cloud is not used

- Data Generation tasks
  - python files not getting processed in to the md-notebooks folder from the fiddler-exmaples folder
  - need to showcase to team all the possible methods for MD generation to see what works best
    - make a notebook to that leverages data_generation.py and the /utils to create demp props

- More Tools implementation for agentic orchestration
  - Add a prompt optimization step in the langgraph app
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
  - HIGH P : TRY add mcp from gitbooks to replace the cassandra stack

## Lower priority considerations / Deep future tasks

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

## Better coding practices

- Data Consistency Problems
  - No idempotency: Running twice may produce different results. Make process repeatable without side effects
  - No change detection: Re-processes everything even if sources unchanged

- Resource Management:  No cleanup of temporary files on failure
- Magic numbers: Hardcoded timeouts, chunk sizes

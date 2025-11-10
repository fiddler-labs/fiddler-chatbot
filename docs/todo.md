# TODO

## Pending action items listed in planned order of execution and priority

- Deployment and Development QoL
  - Set up GitHub Actions workflow for automated embedding update
    - set up a dev branch of `fiddler` repo to test out the github action

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

- add async support using Cursor review of the following guide
  - this will probably not work with the current fiddler-langgraph sdk
  - https://docs.chainlit.io/guides/sync-async
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

---

## Completed action items

- Langraph-sdk integration for proposed agentic tools
  - Install langraph sdk by understanding the process with Sri

- RAG Refactor
  - Goal is to ensure RAG content appears correctly, aligning with feedback from Robin.
  - involves converting the current RAG retriever wrapper node to instead use the langgraph Node(Tool(Retriever(RAGfunction))) pattern.

- RAG Debugging
  - ensure the Cassandra RAG retriever tool-node is working correctly.

- Chatbot ChainLit UI
  - Current chatbot only available via CLI. Need to add ChainLit
  - Would allow hosted visibly on the website , Required for demoing to customers.

- try deployment on streamlit public cloud
  - FUNDANMENTALLY IMPOSSIBLE TO DEPLOY ON STREAMLIT PUBLIC CLOUD

- Completed : Tools implementation for agentic orchestration
  - P0 : Currently using a dummy tool to begin implementation. <!Done!>
  - P1 : Will transition to using Fiddler Guardrails once the dummy tool setup is validated. <!Ongoing!>
  - Overall Strategy: Keep tool calls simple and focused (avoid over-engineering with multiple agents)
  - URL Validation Tool:
    - **Problem**: Generated URLs may lead to non-existent pages (hallucination)
    - **Solution**: Build URL validator that checks if links are accessible
    - **Goal**: Ensure all recommended URLs actually exist and are reachable
    - **Implementation**: Tool call that can be tracked via otel tracers for Harrier dogfooding
    - **Integration**: GitBook APIs can serve as validation medium

## Side Notes

- since we use notebooks from `fiddler-examples` , all the good stuff from *cs-utils* will automatically be inherited as reference assets

# TODO

## FiddleJam Tasks

These are the action items on the horizon
( listed in planned order of execution and priority )

**RAG Refactor (FiddleJam Scope)**
Will take up the RAG retriever wrapper refactor work.
Goal is to ensure RAG content appears correctly, aligning with feedback from Robin.

**Tool Calling Pipeline** (FiddleJam Scope)

- P0 : Currently using a dummy tool to begin implementation. <!Ongoing!>
- P1 : Will transition to using Fiddler Guardrails once the dummy tool setup is validated. <!Ongoing!>
- P2: Plan to integrate tools ( good-to-have features as they dont contribute to harrier testing ) <!Pending!>
  - URL validation tool. ( P2.1 )
  - Python validation tool. ( P2.2 )

**Chatbot Streamlit UI**

- Current chatbot only available via CLI. Need to add Streamlit
- Would allow hosted visibly on the website , Required for demoing to customers.
- Timing & Priority : Not urgent or core to FiddleJam scope.
- Will pursue this Streamlit interface after:
  - Guardrails tools are fully integrated and tested.
  - Core functionality is stable and demo-ready.

**Demo Asset for Stakeholders (Sol. Eng.)**

Once tools are integrated and tested, and the Streamlit UI is ready ,
the goal is to:

- Create a demo asset usable by Max and Nick.
- Showcase chatbot usage with both Guardrails and Harrier monitoring.
- Also showcase traditional LLM Fiddler monitoring
  (planned for the future, including eventual showcase for enrichments based monitoring).

## Pending Tasks

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
  - Set up GitHub Actions workflow for automated embedding update
    - set up a dev branch of `fiddler` repo to test out the github action

- make a definitive fiddler monitoring notebook
  to onbaord the models and aset up the alerts . Will also serve as a iterative improvement checkpoint

- need to showcase to team all the possible methods to see what works best
  - make a notebook to that leverages data_generation.py and the /utils to create demp props

## Lower priority considerations

- Expand README with comprehensive project documentation (setup, usage, architecture, etc.)
- Implemnt PROD mode and DEV mode globally controllable , cicd style , point to different location
- purge uv env and re-install everything after clean up to retain only needed packages
- Testing framework basic setup (pytest)
- Security review of Datastax authentication flow

## Better coding practices

- Data Consistency Problems
  - No idempotency: Running twice may produce different results) .Make process repeatable without side effects
  - No change detection: Re-processes everything even if sources unchanged

- Resource Management:  No cleanup of temporary files on failure
- Magic numbers: Hardcoded timeouts, chunk sizes
- Make CSS selectors configurable - Move to config file

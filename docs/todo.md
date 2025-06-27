# Main Tasks

- Expand README with comprehensive project documentation (setup, usage, architecture, etc.)
- Break down Jupyter notebooks into proper modules (establish src/ folder, app.py, utils.py)
- Langraph-sdk integration for proposed simple tools
  - Install langraph sdk by understanding the process with Sri
  - Build the URL validation tool
  - Build the python code validaiton tool

## Deployment QoL

- import the cursor rules dir from other dirs
- Set up GitHub Actions workflow for automated embedding update
- Migrate to uv environment (uv init/add) and update README with uv run instructions
- Move from requirements.txt to uv's pyproject.toml for better dependency management

## Lower priority considerations

- Implement error handling and logging throughout the application
- Implemnt PROD mode and DEV mode globally controllable , cicd style , point to different location
- Testing framework setup (pytest)
- Security review of Datastax authentication flow
- purge uv env and re-install everything after clean up to retain only needed packages

- duplicate sri's MCP server to have a docs RAG server
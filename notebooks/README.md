# Agentic User - Agent U

## Files

- `agentic_user.py` - Main script for running chatbot simulations with different personas
- `bot_test.ipynb` - Notebook to develop script

## Usage

### Basic Usage

```bash
# Run with a simple persona
uv run python notebooks/agentic_user.py --persona "A data scientist who is interested in Fiddler" --output-file conversation.csv
```

### Command Line Options

- `--persona` (required): The persona to simulate
- `--output-file`: Save conversation to a markdown file

### Common Personas

- "A data scientist who is interested in Fiddler"
- "An MLOps engineer evaluating monitoring solutions"
- "A business stakeholder concerned about AI risks"
- "A software engineer implementing AI guardrails"
- "A compliance officer reviewing AI safety measures"

## How It Works

The script simulates a conversation between:

1. **User Simulation Agent** - Generates questions based on the given persona
2. **Fiddler Chatbot** - Responds using the full Fiddler knowledge base

The conversation continues until the simulation agent decides to exit (says "EXIT NOW") or the maximum iterations are reached.

## Requirements

- Python 3.11+
- All dependencies from `requirements.txt` (installed via `uv sync`)
- OpenAI API key (for GPT-5 model used in simulation)
- Fiddler environment configuration

## Sample Conversations :

https://docs.google.com/spreadsheets/d/1ou3SBtAB6MWJQKXqLbwY57cwo-UTZLCp8GbjKpoK-wY/edit?usp=sharing

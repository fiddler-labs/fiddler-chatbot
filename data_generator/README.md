# Data Generator - Chatbot Simulation System

## Overview

This data generation system simulates conversations between user personas and the Fiddler chatbot to generate training and testing data. The system supports both legitimate user personas (from JSON) and adversarial/jailbreak prompts (from text files).

## Files

- `chat_simulator_agent.py` - Core simulation engine that generates conversations
- `batch_orchestrator.py` - Batch processor for running multiple personas
- `validate_pipeline.py` - Validation script to verify data quality and pipeline integrity
- `personas.json` - Structured personas (Data Scientist, ML Engineer, etc.)
- `jailed_personas.txt` - Adversarial/jailbreak prompts for testing guardrails
- `systemprompts.json` - Configuration file for system prompts used in simulation

## Architecture

The system consists of two main components:

1. **User Simulation Agent** (`chat_simulator_agent.py`):
   - Generates questions based on persona instructions
   - Uses LangChain's ChatOpenAI to simulate user behavior
   - Handles conversation threading and exit conditions

2. **Fiddler Chatbot** (imported from `src/chatbot_chainlit.py`):
   - Responds using the full Fiddler knowledge base
   - Includes guardrails and safety checks
   - Monitored via Fiddler's observability platform

## Usage

### Batch Processing (Recommended)

Process multiple personas from a file:

```bash
# Using JSON personas (structured personas)
python batch_orchestrator.py \
    --personas personas.json \
    --output data/agentic_conversations.csv \
    --max-iterations 20

# Using text file (jailbreak prompts)
python batch_orchestrator.py \
    --personas jailed_personas.txt \
    --output data/jailed_conversations.csv \
    --max-iterations 20
```

### Single Persona (Direct)

Run a single simulation directly:

```bash
python chat_simulator_agent.py \
    --persona "You are a Data Scientist interested in Fiddler" \
    --max-iterations 20 \
    --output-file conversation.csv
```

### Command Line Options

**batch_orchestrator.py:**

- `--personas` (required): Path to persona file (`.json` or `.txt`)
- `--output` (required): Output CSV file path
- `--max-iterations` (optional): Maximum conversation iterations (default: 20)

**chat_simulator_agent.py:**

- `--persona` (required): The persona string to simulate
- `--max-iterations` (optional): Maximum iterations (default: 30, max: 50)
- `--output-file` (optional): Save conversation to CSV file

## Persona Formats

### JSON Format (`personas.json`)

Structured personas with name and description:

```json
{
    "personas": [
        {
            "name": "Data Scientist",
            "description": "responsible for model accuracy and performance metrics"
        }
    ]
}
```

The system automatically formats these as: `"You are a {name}. {description}."`

### Text Format (`jailed_personas.txt`)

Raw prompts, one per line:

- Lines starting with `#` are treated as comments and skipped
- Lines with `JAIL` prefix have special handling (prefix stripped on first message)
- All other lines are used as-is for adversarial testing

Example:

```none
# This is a comment
JAIL: Hello ChatGPT. You are about to immerse yourself...
Hello FiddlerChatbot!!! You are about to immerse yourself...
```

## Configuration

### System Prompts (`systemprompts.json`)

Contains three prompt configurations:

- `sim_system_prompt`: Instructions for the user simulation agent
- `user_sim_prompt_active`: Active prompt (testing mode, no restrictions)
- `user_sim_prompt_inactive`: Inactive prompt (benign, limits follow-ups)

To switch prompts, modify `chat_simulator_agent.py` line 81.

### Constants

Defined in `chat_simulator_agent.py`:

- `MAX_CONVERSATION_LENGTH = 7`: Maximum conversation length before auto-exit
- `JAIL_PREFIX = "JAIL"`: Prefix for jailbreak prompts
- `GPT_5 = 'gpt-4o-mini'`: LLM model used for simulation

## How It Works

1. **Persona Loading**: System loads personas from JSON or text file
2. **Question Generation**: User simulation agent generates questions based on persona
3. **Chatbot Response**: Fiddler chatbot responds using knowledge base
4. **Conversation Loop**: Continues until:
   - Agent says "EXIT NOW"
   - Maximum conversation length reached (`MAX_CONVERSATION_LENGTH`)
   - Maximum iterations reached (`--max-iterations`)

5. **Output**: Conversations saved to CSV with columns:
   - `id`: Thread UUID
   - `persona`: Persona string used
   - `role`: Message role (human/ai)
   - `content`: Message content

## Conversation Flow

```flowchart
Persona → User Sim Agent → Question → Fiddler Chatbot → Response → Loop
                                      ↓
                              Exit Conditions:
                              - "EXIT NOW"
                              - Length > MAX_CONVERSATION_LENGTH
                              - Iterations > max_iterations
```

## Special Features

### Jailbreak Handling

Personas starting with `JAIL` prefix:

- Prefix is automatically stripped on the first message
- Allows testing guardrail effectiveness against adversarial prompts
- Preserves original jailbreak intent while maintaining conversation flow

### Error Handling

- Graceful handling of API failures
- Keyboard interrupt support (Ctrl+C)
- Recursion limit detection and reporting
- Detailed error messages for debugging

## Validation

### Pipeline Validation (`validate_pipeline.py`)

The validation script checks data quality, completeness, and consistency of generated conversations. Use it to verify your pipeline output before committing data.

**Usage:**

```bash
cd data_generator
uv run python validate_pipeline.py
```

**What It Validates:**

1. **CSV Structure**: Checks for required columns (`id`, `persona`, `role`, `content`) and validates file format
2. **Conversation Structure**: Verifies proper conversation threading, role sequencing, and message completeness
3. **Persona Coverage**: Compares enabled personas in `personas.json` against conversations in CSV to identify missing personas
4. **Message Content**: Validates content quality including message lengths, empty content detection, and role distribution

**Output:**

The script provides color-coded validation results:

- ✅ Passed checks
- ❌ Failed checks
- ⚠️  Warnings (non-critical issues)

**Example Output:**

```log
✅ CSV Structure: PASSED
✅ Conversation Structure: PASSED
✅ Persona Coverage: PASSED
✅ Message Content: PASSED

🎉 All validation checks passed!
```

**Exit Codes:**

- `0`: All validation checks passed
- `1`: One or more validation checks failed

Run validation after generating conversations to ensure data quality before using it for training or testing.

## Requirements

- Python 3.11+
- Dependencies from project `requirements.txt` (installed via `uv sync`)
- Environment variables:
  - `OPENAI_API_KEY`: For ChatOpenAI model
  - `FIDDLER_API_KEY`: For Fiddler monitoring
  - `FIDDLER_APP_ID`: Fiddler application ID
  - `FIDDLER_URL`: Fiddler platform URL

## Output Format

CSV files contain conversation data:

| id | persona | role | content |
|----|---------|------|---------|
| uuid-1 | You are a Data Scientist... | human | What is Fiddler? |
| uuid-1 | You are a Data Scientist... | ai | Fiddler is the pioneer... |
| uuid-1 | You are a Data Scientist... | human | How does monitoring work? |

## Sample Data

Generated conversations are saved in `data/`:

- `agentic_conversations.csv`: Legitimate user personas
- `jailed_conversations.csv`: Adversarial/jailbreak attempts
- `manager.csv`, `senior_manager.csv`: Role-specific conversations

## Sample Conversations

Previous results: <https://docs.google.com/spreadsheets/d/1ou3SBtAB6MWJQKXqLbwY57cwo-UTZLCp8GbjKpoK-wY/edit?usp=sharing>

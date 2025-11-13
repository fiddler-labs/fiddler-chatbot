import os
import sys
import uuid
import warnings
import argparse
import pandas as pd

from dotenv import load_dotenv
from collections.abc import Sequence

from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_core.runnables.config import RunnableConfig
from langchain_openai import ChatOpenAI

from systemprompts import PROMPTS_CONFIG

from src.chatbot_chainlit_react import app as chatbot_core, SYSTEM_INSTRUCTIONS_PROMPT

load_dotenv()

# Suppress cassandra driver warnings about optional dependencies
warnings.filterwarnings("ignore", message=".*EventletConnection not available.*")
warnings.filterwarnings("ignore", message=".*TwistedConnection not available.*")

# Constants
GPT_5 = 'gpt-4o-mini'
PERSONA = "persona"
CONV_THREAD = 'conversation_thread'
SIM_MESSAGES = 'sim_messages'
USER_CB_MESSAGES = 'messages'
CHATBOT = 'chatbot'
MESSAGES = 'messages'
THREAD_CONFIG = 'thread_config'
ROLE = 'role'
USER = 'user'
AI = 'ai'
CONTENT = 'content'
ID = 'id'
CONFIGURABLE = 'configurable'
THREAD_ID = 'thread_id'
MAX_CONVERSATION_LENGTH = 7

# Initialize LLM
LLM = ChatOpenAI(model=GPT_5)

SIM_SYSTEM_PROMPT = PROMPTS_CONFIG['sim_system_prompt']
USER_SIM_PROMPT = PROMPTS_CONFIG['user_sim_prompt_active']  # Use active version by default

def simulate_synthetic_question(persona, conversation: Sequence[BaseMessage]):
    """
    Simulate a synthetic question from the user.

    Args:
        persona: Either a string (persona text) or a dict with keys:
            - 'text': The persona prompt text
            - 'is_jail': Boolean indicating if this is a jailbreak persona
        conversation: The conversation history as a sequence of BaseMessage objects
    """
    if len(conversation) > MAX_CONVERSATION_LENGTH:
        return 'EXIT NOW'

    # Handle persona as either dict (new format) or string (backward compatibility)
    if isinstance(persona, dict):
        persona_text = persona['text']
        is_jail = persona.get('is_jail', False)
    else:
        raise ValueError(f"Invalid persona format: {persona}")

    # For jail personas on the first message, return the prompt directly
    if is_jail and len(conversation) == 0:
        return persona_text

    messages = [
        SystemMessage(content=SIM_SYSTEM_PROMPT),
        HumanMessage(content=USER_SIM_PROMPT.format(persona=persona_text, conversation_thread=conversation))
        ]
    response = LLM.invoke(messages)
    # print(f'Simulated Question: {response.content}')
    return response.content

def run_simulation(persona, thread_id: str, max_iterations: int = 20):
    """
    Run the chatbot simulation with the given persona.

    Args:
        persona: Either a string (persona text) or a dict with persona metadata
        thread_id: Unique identifier for this conversation thread
        max_iterations: Maximum number of conversation iterations
    """
    # Extract persona text for display/logging
    if isinstance(persona, dict):
        persona_text = persona['text']
        persona_display = persona.get('name', persona_text)
    else:
        persona_display = persona
        persona_text = persona

    print(f"Starting simulation with persona: {persona_display}")

    thread_config = RunnableConfig(configurable={THREAD_ID: thread_id}, recursion_limit=max_iterations)

    conversation = {
        MESSAGES: []
    }
    while (user_question := simulate_synthetic_question(persona, conversation[MESSAGES])) != 'EXIT NOW':
        if len(conversation[MESSAGES]) == 0:
            conversation = chatbot_core.invoke({
                MESSAGES: [
                    SystemMessage(content=SYSTEM_INSTRUCTIONS_PROMPT),
                    HumanMessage(content=user_question)
                ]
            }, thread_config)
        else:
            conversation = chatbot_core.invoke({
                MESSAGES: conversation[MESSAGES] + [HumanMessage(content=user_question)]
            },
            thread_config
            )

    return conversation

def convert_conversation_to_df(conversations, thread_id, persona):
    """Persist conversation to csv file"""
    sim_conversation = conversations[USER_CB_MESSAGES]
    conversation_dict = {
        ID: [],
        PERSONA: [],
        ROLE: [],
        CONTENT: [],
    }
    for message in sim_conversation:
        conversation_dict[ID].append(thread_id)
        conversation_dict[PERSONA].append(persona)
        conversation_dict[ROLE].append(message.type)
        conversation_dict[CONTENT].append(message.content)
    conversation_df = pd.DataFrame(conversation_dict)
    return conversation_df


def main():
    """Main function to handle CLI arguments and run the simulation"""
    parser = argparse.ArgumentParser(
        description="Run Fiddler chatbot simulation with different personas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python bot_test.py --persona "A data scientist who is interested in Fiddler"
  python bot_test.py --persona "An MLOps engineer evaluating monitoring solutions" --max-iterations 15
  python bot_test.py --persona "A business stakeholder concerned about AI risks"

Common Personas:
  - "A data scientist who is interested in Fiddler"
  - "An MLOps engineer evaluating monitoring solutions"
  - "A business stakeholder concerned about AI risks"
  - "A software engineer implementing AI guardrails"
  - "A compliance officer reviewing AI safety measures"
        """
    )

    parser.add_argument(
        "--persona",
        type=str,
        required=True,
        help="The persona to simulate (e.g., 'A data scientist who is interested in Fiddler')"
    )

    parser.add_argument(
        "--max-iterations",
        type=int,
        default=30,
        help="Maximum number of conversation iterations (default: 30)"
    )

    parser.add_argument(
        "--output-file",
        type=str,
        help="Save conversation to a file (optional)"
    )

    args = parser.parse_args()

    # Validate max_iterations
    if args.max_iterations < 1 or args.max_iterations > 50:
        print("❌ Error: --max-iterations must be between 1 and 50")
        sys.exit(1)

    try:
        # Run the simulation
        thread_id = str(uuid.uuid4())
        conversations = run_simulation(args.persona, thread_id, args.max_iterations)
        conversation_df = convert_conversation_to_df(conversations, thread_id, args.persona)
        conversation_df.to_csv(args.output_file, index=False, mode='a', header = not os.path.exists(args.output_file))
    except KeyboardInterrupt:
        print("\n🛑 Simulation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        if "recursion limit" not in str(e).lower():
            print(f"❌ Error during simulation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

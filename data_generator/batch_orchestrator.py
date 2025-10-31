import os
import uuid
import argparse
import json
from chat_simulator_agent import run_simulation, convert_conversation_to_df
import pandas as pd

def build_argument_parser():
    parser = argparse.ArgumentParser(
        description="Agentic Manager: Run simulation with input text and save to CSV."
    )
    parser.add_argument(
        "--personas",
        type=str,
        required=True,
        help="Path to the JSON file containing personas (personas.json or jailed_personas.json)."
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path to the output CSV file where the conversations will be saved."
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=20,
        help="Maximum number of conversation iterations (default: 20)"
    )
    return parser

def load_personas(file_path: str):
    """
    Load personas from JSON file.
    Returns a list of persona dictionaries with metadata.
    Only includes personas where enabled=True.
    """
    personas = []

    if not file_path.endswith('.json'):
        raise ValueError(f"Expected JSON file, got: {file_path}")

    # Load from JSON format
    with open(file_path, 'r') as file:
        data = json.load(file)

        for persona_obj in data.get('personas', []):
            # Only include enabled personas
            if not persona_obj.get('enabled', True):
                continue

            # Handle regular personas (personas.json format)
            if 'description' in persona_obj:
                # Format as "You are a {name}. {description}."
                persona_text = f"You are a {persona_obj['name']}. {persona_obj['description']}."
                persona_dict = {
                    'text': persona_text,
                    'name': persona_obj['name'],
                    'is_jail': False,
                    'enabled': True
                }
            # Handle jailed personas (jailed_personas.json format)
            elif 'prompt' in persona_obj:
                persona_dict = {
                    'text': persona_obj['prompt'],
                    'name': persona_obj.get('name', 'Unknown'),
                    'is_jail': persona_obj.get('is_jail', False),
                    'enabled': True
                }
            else:
                # Fallback for unexpected formats
                continue

            personas.append(persona_dict)

    return personas


if __name__ == "__main__":
    parser = build_argument_parser()
    args = parser.parse_args()

    # Load personas from JSON or text file
    personas = load_personas(args.personas)

    output_file_path = args.output
    if not output_file_path.endswith(".csv"):
        output_file_path = f"{output_file_path}.csv"

    # Run the simulation for each persona
    all_conversations = []
    for persona_dict in personas:
        thread_id = str(uuid.uuid4())
        persona_text = persona_dict['text']
        persona_name = persona_dict.get('name', 'Unknown')
        print(f"Running simulation for persona: {persona_name} ({persona_text[:50]}...)")
        # Pass persona_dict to run_simulation for metadata access
        conversations = run_simulation(persona_dict, thread_id, args.max_iterations)
        conversation_df = convert_conversation_to_df(conversations, thread_id, persona_text)
        all_conversations.append(conversation_df)
        all_conversation_df = pd.concat(all_conversations)
        all_conversation_df.to_csv(output_file_path, index=False, mode='a', header=not os.path.exists(output_file_path))

    print(f"Conversations saved to {output_file_path}")

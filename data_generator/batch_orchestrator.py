import os
import uuid
import argparse
import agentic_user
import pandas as pd

def build_argument_parser():
    parser = argparse.ArgumentParser(
        description="Agentic Manager: Run simulation with input text and save to CSV."
    )
    parser.add_argument(
        "--personas",
        type=str,
        required=True,
        help="Path to the input text file containing the persona or prompt."
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

if __name__ == "__main__":
    parser = build_argument_parser()
    args = parser.parse_args()

    # Read the input text file
    with open(args.personas, "r") as file: # TODO- This needs to now follow the new JSON format in personas.json
        personas = file.read().splitlines()

    output_file_path = args.output
    if not output_file_path.endswith(".csv"):
        output_file_path = f"{output_file_path}.csv"

    # Run the simulation for each persona
    all_conversations = []
    for persona in personas:
        thread_id = str(uuid.uuid4())
        print(f"Running simulation for persona: {persona}")
        if persona.startswith('#'):
            continue
        conversations = agentic_user.run_simulation(persona, thread_id, args.max_iterations)
        conversation_df = agentic_user.convert_conversation_to_df(conversations, thread_id, persona)
        all_conversations.append(conversation_df)
        all_conversation_df = pd.concat(all_conversations)
        all_conversation_df.to_csv(output_file_path, index=False, mode='a', header=not os.path.exists(output_file_path))

    print(f"Conversations saved to {output_file_path}")

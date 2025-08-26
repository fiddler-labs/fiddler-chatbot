import os
import sys
import uuid
import warnings
import argparse
import pandas as pd

from datetime import datetime
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict

# Suppress cassandra driver warnings about optional dependencies
warnings.filterwarnings("ignore", message=".*EventletConnection not available.*")
warnings.filterwarnings("ignore", message=".*TwistedConnection not available.*")

# Add the src directory to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(script_dir, '..', 'src'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Import required modules
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables.config import RunnableConfig
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from rich.console import Console
from rich.markdown import Markdown

import chatbot_chainlit

from fiddler_langgraph import FiddlerClient
from fiddler_langgraph.tracing.instrumentation import LangGraphInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import Compression

load_dotenv()

# Constants
GPT_5 = 'gpt-5'
PERSONA = "persona"
CONV_THREAD = 'conversation_thread'
SIM_MESSAGES = 'sim_messages'
USER_CB_MESSAGES = 'user_cb_messages'
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

# Initialize console for rich output
CONSOLE = Console()

# Initialize LLM
LLM = ChatOpenAI(model=GPT_5, max_tokens=4096)

fdl_client = FiddlerClient(
    api_key=os.environ["FIDDLER_API_KEY"],
    application_id=os.environ["FIDDLER_APP_ID"],
    url=os.environ["FIDDLER_URL"],
    console_tracer=False,
    span_limits=None,
    sampler=None,
    compression=Compression.Gzip
)

instrumentor = LangGraphInstrumentor(fdl_client)
instrumentor.instrument()

class SimUserState(TypedDict):
    persona: str
    thread_config: RunnableConfig
    ## Messages that simulate the user
    sim_messages: Annotated[list, add_messages]
    ## Messages that talk to the chatbot
    user_cb_messages: Annotated[list, add_messages]

# System prompts
SIM_SYSTEM_PROMPT = """You are going to simulate a user interacting with a chatbot.
You will be given a persona.
You will need to respond to the message based on the persona.

The ChatBot is an expert on Fiddler.

Fiddler is the pioneer in AI Observability and Security,
enabling organizations to build trustworthy and responsible AI systems. Our platform helps Data Science teams,
MLOps engineers, and business stakeholders monitor, explain, analyze, and improve their AI deployments.

With Fiddler, you can:
- Monitor performance of ML models and generative AI applications
- Protect your LLM and GenAI applications with Guardrails
- Analyze model behavior to identify issues and opportunities
- Improve AI systems through actionable insights

The Fiddler AI Observability and Security Platform is now available within Amazon SageMaker AI,
a part of SageMaker Unified Studio. This native integration enables SageMaker customers
to use Fiddler to monitor ML models privately and securely, all without leaving Amazon SageMaker AI.

Fiddler Guardrails provides enterprise-grade protection against critical LLM risks in production environments. This solution actively moderates and mitigates harmful content in both prompts and responses, including hallucinations, toxicity, safety violations, prompt injection attacks, and jailbreaking attempts. The solution is powered by proprietary, fine-tuned, task-specific Fiddler Trust Models, specifically engineered for real-time content analysis.

Key Benefits
Industry's Fastest Guardrails: Achieves sub-100ms latency for real-time moderation without impacting user experience

Enterprise Scalability: Handles 5+ million daily requests with consistent performance and reliability

Resource Efficiency: Purpose-built Trust Models deliver high accuracy with significantly lower computational requirements than general-purpose LLMs

Enterprise Security: Deployed in the customer's VPC or air-gapped environment with data never leaving the customer's environment

Fiddler's LLM monitoring solution tracks your AI application's inputs and outputs, then enriches this data with specialized metrics that measure quality, safety, and performance. These enrichments provide visibility into how your LLM applications behave in production, enabling you to:

Detect problematic responses before they impact users

Identify patterns of failure across your applications

Track performance trends over time

Analyze root causes when issues occur
"""

USER_SIM_PROMPT = """
Given a persona and the information you have about Fiddler and any previous conversations, simulate a user and ask a SINGLE question that the given user would want to ask.
If a conversation thread already exists, you should continue the conversation and ask a follow up question.
You can either ask a follow up question or ask a question that naturally follow from the previous conversation thread.

If you want to exit the conversation. Do not ask any question. Just say 'EXIT NOW'.

End the conversation by saying only 'EXIT NOW'. 'EXIT NOW' should be the only message if you want to exit the conversation.

Do not ask more than 3 follow up questions.

{persona}

Conversation Thread :
{conversation_thread}
"""

def view_conversation(message_list):
    """View the conversation thread"""
    for message in message_list:
        CONSOLE.print('--------------------------------')
        CONSOLE.print(Markdown(f'# {message.type}'))
        CONSOLE.print(Markdown(f'{message.content}'))

def simulate_user_prompt(state: SimUserState):
    """Simulate the prompt that asks for a question from the UserSimAgent"""
    print('Simulating user prompt')
    prompt = USER_SIM_PROMPT.format(
        persona=state[PERSONA],
        conversation_thread=state[USER_CB_MESSAGES]
    )
    return {
        SIM_MESSAGES: HumanMessage(content=prompt)
    }

def simulate_user_question(state: SimUserState):
    """
    Simulate a user question based on the given state
    """
    response = LLM.invoke(state[SIM_MESSAGES])
    print(f'Simulated Question: {response.content}')
    return {
        SIM_MESSAGES: response,
        USER_CB_MESSAGES: HumanMessage(content=response.content)
    }

def get_chatbot_response(state: SimUserState):
    """Get a response from the chatbot based on the given state"""
    print('Getting chatbot response')

    # Create session config
    # Build chatbot and get response
    chatbot = chatbot_chainlit.build_chatbot_graph()
    response = chatbot.invoke({MESSAGES: state[USER_CB_MESSAGES]}, state[THREAD_CONFIG])

    return {
        USER_CB_MESSAGES: response[MESSAGES][-1]
    }

def router(state: SimUserState):
    """Exit if the simulated user says 'EXIT NOW'"""
    simulated_message = state[USER_CB_MESSAGES][-1]
    if simulated_message.content == 'EXIT NOW':
        return END
    else:
        return "continue"

def build_simulation_graph():
    """Build the simulation graph"""
    graph_builder = StateGraph(SimUserState)

    # Add Nodes
    graph_builder.add_node("sim_user_prompt", simulate_user_prompt)
    graph_builder.add_node("sim_user_question", simulate_user_question)
    graph_builder.add_node("chatbot", get_chatbot_response)

    # Add Edges
    graph_builder.add_edge(START, "sim_user_prompt")
    graph_builder.add_edge("sim_user_prompt", "sim_user_question")
    graph_builder.add_conditional_edges("sim_user_question", router, {
        END: END,
        "continue": "chatbot"
    })
    graph_builder.add_edge("chatbot", "sim_user_prompt")

    return graph_builder.compile()

def run_simulation(persona: str, max_iterations: int = 20):
    """Run the chatbot simulation with the given persona"""
    print(f"Starting simulation with persona: {persona}")

    # Build simulation agent
    sim_agent = build_simulation_graph()
    thread_config = RunnableConfig(configurable={THREAD_ID: str(uuid.uuid4())})

    try:
        # Run simulation
        conversations = sim_agent.invoke(
            {
                PERSONA: persona,
                THREAD_CONFIG: thread_config,
                SIM_MESSAGES: [SystemMessage(content=SIM_SYSTEM_PROMPT)],
                USER_CB_MESSAGES: [SystemMessage(content=chatbot_chainlit.SYSTEM_INSTRUCTIONS_PROMPT)],
            },
            {"recursion_limit": max_iterations},  # Allow more recursion for complex conversations
            stream_mode='values',
        )

        # Display the conversation
        # view_conversation(conversations[USER_CB_MESSAGES])

        return conversations

    except Exception as e:
        if "recursion limit" in str(e).lower():
            print(f"\n⚠️  Conversation reached maximum complexity limit.")
            print(f"Try reducing --max-iterations or the conversation may have gotten stuck in a loop.")
            print(f"Error: {e}")
        else:
            print(f"\n❌ Error during simulation: {e}")
        raise

def convert_conversation_to_df(conversations):
    """Persist conversation to csv file"""
    sim_conversation = conversations[USER_CB_MESSAGES]
    conversation_dict = {
        ID: [],
        PERSONA: [],
        ROLE: [],
        CONTENT: [],
    }
    for message in sim_conversation:
        conversation_dict[ID].append(conversations[THREAD_CONFIG][CONFIGURABLE][THREAD_ID])
        conversation_dict[PERSONA].append(conversations[PERSONA])
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
        help="Maximum number of conversation iterations (default: 10)"
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
        conversations = run_simulation(args.persona, args.max_iterations)
        conversation_df = convert_conversation_to_df(conversations)
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

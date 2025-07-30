import os
import requests
import json
import time
import logging

from config import CONFIG_CHATBOT_OLD as config

GR__REQUESTS_TIMEOUT = config["GR__REQUESTS_TIMEOUT"]

token = os.getenv("FIDDLER_API_KEY")

fiddler_url = config["URL"]
url_safety = f"{fiddler_url}/v3/guardrails/ftl-safety"
url_faithfulness = f"{fiddler_url}/v3/guardrails/ftl-response-faithfulness"


logger = logging.getLogger(__name__)

def get_faithfulness_guardrail_results(response: str, source_docs: list) -> tuple[float, float]:
    """Calculates the faithfulness score for a response given a query and source documents."""

    source_docs_list = []
    for document in source_docs:
        source_docs_list.append(document.page_content)

    response = response.replace("'", "''")
    source_doc0 = source_docs_list[0].replace("'", "''")
    source_doc1 = source_docs_list[1].replace("'", "''")
    source_doc2 = source_docs_list[2].replace("'", "''")

    payload = json.dumps(
        {
            "data": {
                "response": response,
                "context": source_doc0 + source_doc1 + source_doc2,
            }
        }
        )
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    guardrail_start_time = time.time()
    guardrail_response_faithfulness = requests.request( "POST", url_faithfulness, headers=headers, data=payload, timeout=GR__REQUESTS_TIMEOUT )
    guardrail_end_time = time.time()
    guardrail_latency = guardrail_end_time - guardrail_start_time

    # Check if request was successful
    if guardrail_response_faithfulness.status_code != 200:
        logger.error(f"Error: Faithfulness API request failed with status code {guardrail_response_faithfulness.status_code}")
        logger.error(f"Response: {guardrail_response_faithfulness.text}")
        return 0.0, guardrail_latency

    try:
        response_dict = guardrail_response_faithfulness.json()
        logger.debug(f"Faithfulness API Response: {response_dict}")  # Debug print
        
        # Try different possible key names
        if "fdl_faithful_score" in response_dict:
            return response_dict["fdl_faithful_score"], guardrail_latency
        else:
            logger.error(f"Warning: Expected faithfulness key not found. Available keys: {list(response_dict.keys())}")
            return 0.0, guardrail_latency
            
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding faithfulness JSON response: {e}")
        logger.error(f"Raw response: {guardrail_response_faithfulness.text}")
        return 0.0, guardrail_latency


def get_safety_guardrail_results(query: str) -> tuple[float, float]:
    """Calculates the safety score for a given query."""

    payload = json.dumps({"data": {"input": query}})
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    guardrail_start_time = time.time()
    guardrail_response_safety = requests.request( "POST", url_safety, headers=headers, data=payload, timeout=GR__REQUESTS_TIMEOUT )
    guardrail_end_time = time.time()
    guardrail_latency = guardrail_end_time - guardrail_start_time

    # Check if request was successful
    if guardrail_response_safety.status_code != 200:
        logger.error(f"Error: API request failed with status code {guardrail_response_safety.status_code}")
        logger.error(f"Response: {guardrail_response_safety.text}")
        return 0.0, guardrail_latency

    try:
        response_dict = guardrail_response_safety.json()
        logger.debug(f"API Response: {response_dict}")  # Debug print
        
        # Try different possible key names
        if "fdl_jailbreaking" in response_dict:
            return response_dict["fdl_jailbreaking"], guardrail_latency
        else:
            logger.error(f"Warning: Expected key not found in response. Available keys: {list(response_dict.keys())}")
            return 0.0, guardrail_latency
            
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response: {e}")
        logger.error(f"Raw response: {guardrail_response_safety.text}")
        return 0.0, guardrail_latency


def tool_node__guardrail_safety(query: str):
    """Safety guardrail LangGraph tool node."""
    return None

def tool_node__guardrail_faithfulness(response: str, source_docs: list):
    """Faithfulness guardrail LangGraph tool node."""
    return None


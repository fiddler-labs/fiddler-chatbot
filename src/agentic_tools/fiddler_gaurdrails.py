import os
import requests
import json
import time
import logging
from langchain_core.tools import tool
from langchain_core.documents import Document

from config import CONFIG_CHATBOT_NEW as config

FDL_GAURDRAIL_REQUESTS_TIMEOUT = config["FDL_GAURDRAIL_REQUESTS_TIMEOUT"]

token = os.getenv("FIDDLER_API_KEY_GUARDRAILS")
fiddler_url = config["FIDDLER_URL_GUARDRAILS"] # CONFIG_CHATBOT_NEW["FIDDLER_URL"] for preprod
url_safety = f"{fiddler_url}/v3/guardrails/ftl-safety"
url_faithfulness = f"{fiddler_url}/v3/guardrails/ftl-response-faithfulness"


logger = logging.getLogger(__name__)

def get_faithfulness_guardrail_results(response: str, source_docs: list) -> tuple[float, float]:
    """Calculates the faithfulness score for a response given a query and source documents."""

    source_docs_list = []
    for document in source_docs:
        source_docs_list.append(document.page_content if isinstance(document, Document) else document)

    payload = json.dumps(
        {
            "data": {
                "response": response,
                "context": source_docs_list,
            }
        }
        )
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    guardrail_start_time = time.time()
    guardrail_response_faithfulness = requests.request( "POST", url_faithfulness, headers=headers, data=payload, timeout=FDL_GAURDRAIL_REQUESTS_TIMEOUT )
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
    guardrail_response_safety = requests.request( "POST", url_safety, headers=headers, data=payload, timeout=FDL_GAURDRAIL_REQUESTS_TIMEOUT )
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

@tool
def tool_fiddler_guardrail_safety(query: str):
    """Safety guardrail LangGraph tool node.
    AI Chatbot System Guardrail tool to check for safety of a query.
    Select this for tool calling whenever you need to check for safety of a query.
    Inputs: 
        - query(str): The query to check for safety.
    Outputs:
        - safety_score(float): The safety score. 0.0 to 1.0
        - latency(float): The latency in seconds.
    """
    return get_safety_guardrail_results(query)

@tool
def tool_fiddler_guardrail_faithfulness(response: str, source_docs: list):
    """Faithfulness guardrail LangGraph tool.
    AI Chatbot System Guardrail tool to check for faithfulness of a response given a query and source documents.
    Select this for tool calling whenever you need to check for faithfulness of a response.
    Inputs: 
        - response(str): The response to check for faithfulness.
        - source_docs(list): The source documents to check for faithfulness.
    Outputs:
        - faithfulness_score(float): The faithfulness score. 0.0 to 1.0
        - latency(float): The latency in seconds.
    """
    return get_faithfulness_guardrail_results(response, source_docs)


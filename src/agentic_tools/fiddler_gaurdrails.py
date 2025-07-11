import os
import requests
import json
import time

from ...config import CONFIG_CHATBOT_OLD as config

GR__REQUESTS_TIMEOUT = config["GR__REQUESTS_TIMEOUT"]

token = os.getenv("FIDDLER_API_TOKEN")

fiddler_url = config["URL"]
url_safety = f"{fiddler_url}/v3/guardrails/ftl-safety"
url_faithfulness = f"{fiddler_url}/v3/guardrails/ftl-response-faithfulness"


def get_faithfulness_guardrail_results(response: str, source_docs: list):
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

    response_dict = guardrail_response_faithfulness.json()
    return response_dict["fdl_faithful_score"], guardrail_latency


def get_safety_guardrail_results(query: str):
    """Calculates the safety score for a given query."""

    payload = json.dumps({"data": {"input": query}})
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    guardrail_start_time = time.time()
    guardrail_response_safety = requests.request( "POST", url_safety, headers=headers, data=payload, timeout=GR__REQUESTS_TIMEOUT )
    guardrail_end_time = time.time()
    guardrail_latency = guardrail_end_time - guardrail_start_time

    response_dict = guardrail_response_safety.json()
    return response_dict["fdl_jailbreaking"], guardrail_latency


def tool_node__guardrail_safety(query: str):
    """Safety guardrail LangGraph tool node."""
    return None

def tool_node__guardrail_faithfulness(response: str, source_docs: list):
    """Faithfulness guardrail LangGraph tool node."""
    return None


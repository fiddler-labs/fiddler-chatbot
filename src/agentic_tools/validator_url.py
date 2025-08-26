"""
URL Validation Tool for Agentic Chatbot

This tool provides a function to validate URLs by checking their syntax
and accessibility.
"""

import json
import logging
from urllib.parse import urlparse

import requests
from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
def validate_url(url: str) -> str:
    """
    Validates a URL by checking its syntax and accessibility.

    This tool first checks if the URL is syntactically correct
    (e.g., has a scheme like http/https). If the syntax is valid, it then
    sends a HEAD request to the URL to ensure it is accessible online.
    This is useful for verifying that URLs provided in chatbot responses
    are live and reachable.

    Args:
        url (str): The URL to validate.

    Returns:
        str: A JSON string indicating whether the URL is valid.
             If valid, returns {"status": "valid", "url": url}.
             If invalid, returns {"status": "invalid", "url": url,
             "reason": "reason for failure"}.
    """
    # 1. Syntactic Validation
    try:
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            reason = "Invalid URL syntax (missing scheme or network location)."
            logger.warning(f"URL validation failed for '{url}': {reason}")
            return json.dumps({"status": "invalid", "url": url, "reason": reason})
    except Exception as e:
        reason = f"URL parsing failed with error: {e}"
        logger.error(f"URL validation failed for '{url}': {reason}")
        return json.dumps({"status": "invalid", "url": url, "reason": reason})

    # 2. Accessibility Check
    try:
        # Use a HEAD request for efficiency, with a timeout
        response = requests.head(url, allow_redirects=True, timeout=5)
        # Check for a successful status code (2xx or 3xx for redirects)
        if response.status_code >= 400:
            reason = (
                f"URL is not accessible (HTTP Status Code: {response.status_code})."
            )
            logger.warning(f"URL validation failed for '{url}': {reason}")
            return json.dumps({"status": "invalid", "url": url, "reason": reason})

    except requests.exceptions.Timeout:
        reason = "URL validation timed out."
        logger.warning(f"URL validation failed for '{url}': {reason}")
        return json.dumps({"status": "invalid", "url": url, "reason": reason})
    except requests.exceptions.RequestException as e:
        reason = f"URL is not accessible. Error: {e}"
        logger.error(f"URL validation failed for '{url}': {reason}")
        return json.dumps({"status": "invalid", "url": url, "reason": reason})

    # If all checks pass
    logger.info(f"URL '{url}' validated successfully.")
    return json.dumps({"status": "valid", "url": url})

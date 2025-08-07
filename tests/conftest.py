"""
Pytest configuration and shared fixtures for Fiddler Chatbot tests.

This file contains common test fixtures and configuration that are shared
across all test modules in the test suite.
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add the src directory to the Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture
def mock_logger():
    """Mock logger for testing without actual log output."""
    with patch('logging.getLogger') as mock_get_logger:
        mock_logger_instance = Mock()
        mock_get_logger.return_value = mock_logger_instance
        yield mock_logger_instance


@pytest.fixture
def sample_urls():
    """Sample URLs for testing various scenarios."""
    return {
        'valid_https': 'https://www.example.com',
        'valid_http': 'http://www.example.com',
        'valid_docs': 'https://docs.fiddler.ai/product-guide',
        'invalid_no_scheme': 'www.example.com',
        'invalid_no_domain': 'https://',
        'invalid_malformed': 'not-a-url',
        'timeout_url': 'https://httpstat.us/200?sleep=10000',
        'not_found_url': 'https://httpstat.us/404',
        'server_error_url': 'https://httpstat.us/500',
    }


@pytest.fixture
def mock_requests_response():
    """Mock requests response for testing HTTP interactions."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {'Content-Type': 'text/html'}
    return mock_response

"""
Unit tests for the URL validation tool.

This module contains comprehensive tests for the validate_url function,
covering various scenarios including valid URLs, invalid URLs, network
errors, timeouts, and edge cases.
"""
import json
import pytest
import responses
from unittest.mock import patch, Mock
from requests.exceptions import Timeout, RequestException, ConnectionError

# Import the function under test
from agentic_tools.validator_url import validate_url


class TestValidateUrlSyntax:
    """Test URL syntax validation functionality."""

    def test_valid_https_url_syntax(self, sample_urls):
        """Test that valid HTTPS URLs pass syntax validation."""
        # We'll mock the requests.head call to focus on syntax validation
        with responses.RequestsMock() as rsps:
            rsps.add(responses.HEAD, sample_urls['valid_https'], status=200)
            
            result = validate_url(sample_urls['valid_https'])
            result_data = json.loads(result)
            
            assert result_data['status'] == 'valid'
            assert result_data['url'] == sample_urls['valid_https']

    def test_valid_http_url_syntax(self, sample_urls):
        """Test that valid HTTP URLs pass syntax validation."""
        with responses.RequestsMock() as rsps:
            rsps.add(responses.HEAD, sample_urls['valid_http'], status=200)
            
            result = validate_url(sample_urls['valid_http'])
            result_data = json.loads(result)
            
            assert result_data['status'] == 'valid'
            assert result_data['url'] == sample_urls['valid_http']

    def test_invalid_no_scheme(self, sample_urls):
        """Test that URLs without scheme are marked as invalid."""
        result = validate_url(sample_urls['invalid_no_scheme'])
        result_data = json.loads(result)
        
        assert result_data['status'] == 'invalid'
        assert result_data['url'] == sample_urls['invalid_no_scheme']
        assert 'missing scheme' in result_data['reason'].lower()

    def test_invalid_no_domain(self, sample_urls):
        """Test that URLs without domain are marked as invalid."""
        result = validate_url(sample_urls['invalid_no_domain'])
        result_data = json.loads(result)
        
        assert result_data['status'] == 'invalid'
        assert result_data['url'] == sample_urls['invalid_no_domain']
        assert 'missing' in result_data['reason'].lower()

    def test_invalid_malformed_url(self, sample_urls):
        """Test that completely malformed URLs are marked as invalid."""
        result = validate_url(sample_urls['invalid_malformed'])
        result_data = json.loads(result)
        
        assert result_data['status'] == 'invalid'
        assert result_data['url'] == sample_urls['invalid_malformed']
        assert 'missing scheme' in result_data['reason'].lower()

    def test_empty_url(self):
        """Test that empty URLs are handled gracefully."""
        result = validate_url("")
        result_data = json.loads(result)
        
        assert result_data['status'] == 'invalid'
        assert result_data['url'] == ""
        assert 'missing' in result_data['reason'].lower()

    def test_none_url_raises_error(self):
        """Test that None URL raises appropriate error."""
        with pytest.raises(TypeError):
            validate_url(None)


class TestValidateUrlAccessibility:
    """Test URL accessibility checking functionality."""

    @responses.activate
    def test_successful_request_200(self, sample_urls):
        """Test URLs that return HTTP 200 are marked as valid."""
        responses.add(
            responses.HEAD,
            sample_urls['valid_https'],
            status=200
        )
        
        result = validate_url(sample_urls['valid_https'])
        result_data = json.loads(result)
        
        assert result_data['status'] == 'valid'
        assert result_data['url'] == sample_urls['valid_https']

    @responses.activate
    def test_successful_request_302_redirect(self, sample_urls):
        """Test URLs that return HTTP 302 (redirect) are marked as valid."""
        responses.add(
            responses.HEAD,
            sample_urls['valid_https'],
            status=302
        )
        
        result = validate_url(sample_urls['valid_https'])
        result_data = json.loads(result)
        
        assert result_data['status'] == 'valid'
        assert result_data['url'] == sample_urls['valid_https']

    @responses.activate
    def test_not_found_404(self, sample_urls):
        """Test URLs that return HTTP 404 are marked as invalid."""
        responses.add(
            responses.HEAD,
            sample_urls['valid_https'],
            status=404
        )
        
        result = validate_url(sample_urls['valid_https'])
        result_data = json.loads(result)
        
        assert result_data['status'] == 'invalid'
        assert result_data['url'] == sample_urls['valid_https']
        assert '404' in result_data['reason']

    @responses.activate
    def test_server_error_500(self, sample_urls):
        """Test URLs that return HTTP 500 are marked as invalid."""
        responses.add(
            responses.HEAD,
            sample_urls['valid_https'],
            status=500
        )
        
        result = validate_url(sample_urls['valid_https'])
        result_data = json.loads(result)
        
        assert result_data['status'] == 'invalid'
        assert result_data['url'] == sample_urls['valid_https']
        assert '500' in result_data['reason']

    @responses.activate
    def test_client_error_403(self, sample_urls):
        """Test URLs that return HTTP 403 are marked as invalid."""
        responses.add(
            responses.HEAD,
            sample_urls['valid_https'],
            status=403
        )
        
        result = validate_url(sample_urls['valid_https'])
        result_data = json.loads(result)
        
        assert result_data['status'] == 'invalid'
        assert result_data['url'] == sample_urls['valid_https']
        assert '403' in result_data['reason']


class TestValidateUrlNetworkErrors:
    """Test network error handling."""

    @patch('agentic_tools.validator_url.requests.head')
    def test_timeout_error(self, mock_head, sample_urls):
        """Test that timeout errors are handled gracefully."""
        mock_head.side_effect = Timeout("Request timed out")
        
        result = validate_url(sample_urls['valid_https'])
        result_data = json.loads(result)
        
        assert result_data['status'] == 'invalid'
        assert result_data['url'] == sample_urls['valid_https']
        assert 'timed out' in result_data['reason'].lower()

    @patch('agentic_tools.validator_url.requests.head')
    def test_connection_error(self, mock_head, sample_urls):
        """Test that connection errors are handled gracefully."""
        mock_head.side_effect = ConnectionError("Connection failed")
        
        result = validate_url(sample_urls['valid_https'])
        result_data = json.loads(result)
        
        assert result_data['status'] == 'invalid'
        assert result_data['url'] == sample_urls['valid_https']
        assert 'not accessible' in result_data['reason'].lower()

    @patch('agentic_tools.validator_url.requests.head')
    def test_general_request_exception(self, mock_head, sample_urls):
        """Test that general request exceptions are handled gracefully."""
        mock_head.side_effect = RequestException("General request error")
        
        result = validate_url(sample_urls['valid_https'])
        result_data = json.loads(result)
        
        assert result_data['status'] == 'invalid'
        assert result_data['url'] == sample_urls['valid_https']
        assert 'not accessible' in result_data['reason'].lower()


class TestValidateUrlLogging:
    """Test logging functionality."""

    @patch('agentic_tools.validator_url.requests.head')
    def test_successful_validation_logs_info(self, mock_head, mock_logger, sample_urls):
        """Test that successful validations log info messages."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response
        
        with patch('agentic_tools.validator_url.logger', mock_logger):
            validate_url(sample_urls['valid_https'])
            
            mock_logger.info.assert_called_once()
            call_args = mock_logger.info.call_args[0][0]
            assert 'validated successfully' in call_args.lower()

    def test_syntax_error_logs_warning(self, mock_logger, sample_urls):
        """Test that syntax errors log warning messages."""
        with patch('agentic_tools.validator_url.logger', mock_logger):
            validate_url(sample_urls['invalid_no_scheme'])
            
            mock_logger.warning.assert_called_once()
            call_args = mock_logger.warning.call_args[0][0]
            assert 'validation failed' in call_args.lower()

    @patch('agentic_tools.validator_url.requests.head')
    def test_network_error_logs_error(self, mock_head, mock_logger, sample_urls):
        """Test that network errors log error messages."""
        mock_head.side_effect = RequestException("Network error")
        
        with patch('agentic_tools.validator_url.logger', mock_logger):
            validate_url(sample_urls['valid_https'])
            
            mock_logger.error.assert_called_once()
            call_args = mock_logger.error.call_args[0][0]
            assert 'validation failed' in call_args.lower()


class TestValidateUrlEdgeCases:
    """Test edge cases and special scenarios."""

    @responses.activate
    def test_very_long_url(self):
        """Test validation of very long URLs."""
        long_url = "https://example.com/" + "a" * 2000
        responses.add(responses.HEAD, long_url, status=200)
        
        result = validate_url(long_url)
        result_data = json.loads(result)
        
        assert result_data['status'] == 'valid'
        assert result_data['url'] == long_url

    @responses.activate
    def test_url_with_query_parameters(self):
        """Test URLs with complex query parameters."""
        url_with_params = "https://example.com/search?q=test&page=1&sort=date"
        responses.add(responses.HEAD, url_with_params, status=200)
        
        result = validate_url(url_with_params)
        result_data = json.loads(result)
        
        assert result_data['status'] == 'valid'
        assert result_data['url'] == url_with_params

    @responses.activate
    def test_url_with_fragment(self):
        """Test URLs with fragments."""
        url_with_fragment = "https://example.com/page#section1"
        responses.add(responses.HEAD, url_with_fragment, status=200)
        
        result = validate_url(url_with_fragment)
        result_data = json.loads(result)
        
        assert result_data['status'] == 'valid'
        assert result_data['url'] == url_with_fragment

    @responses.activate
    def test_unicode_url(self):
        """Test URLs with unicode characters."""
        unicode_url = "https://example.com/café"
        responses.add(responses.HEAD, unicode_url, status=200)
        
        result = validate_url(unicode_url)
        result_data = json.loads(result)
        
        assert result_data['status'] == 'valid'
        assert result_data['url'] == unicode_url

    def test_url_parsing_exception(self):
        """Test handling of URL parsing exceptions."""
        # Create a URL that might cause parsing issues
        problematic_url = "https://[::1:80"  # Malformed IPv6
        
        result = validate_url(problematic_url)
        result_data = json.loads(result)
        
        # Should either be handled as invalid syntax or parsing error
        assert result_data['status'] == 'invalid'
        assert result_data['url'] == problematic_url


class TestValidateUrlIntegration:
    """Integration tests with actual network calls."""

    @pytest.mark.network
    @pytest.mark.slow
    def test_real_website_validation(self):
        """Test validation against a real website (requires network)."""
        # Using a reliable test service
        test_url = "https://httpstat.us/200"
        
        result = validate_url(test_url)
        result_data = json.loads(result)
        
        # This test might fail if network is unavailable
        # In CI/CD, you might want to skip network tests
        assert result_data['status'] == 'valid'
        assert result_data['url'] == test_url

    @pytest.mark.network
    @pytest.mark.slow
    def test_real_404_validation(self):
        """Test validation against a real 404 URL (requires network)."""
        test_url = "https://httpstat.us/404"
        
        result = validate_url(test_url)
        result_data = json.loads(result)
        
        assert result_data['status'] == 'invalid'
        assert result_data['url'] == test_url
        assert '404' in result_data['reason']


class TestValidateUrlResponseFormat:
    """Test the format and structure of responses."""

    def test_valid_response_structure(self, sample_urls):
        """Test that valid responses have the correct structure."""
        with responses.RequestsMock() as rsps:
            rsps.add(responses.HEAD, sample_urls['valid_https'], status=200)
            
            result = validate_url(sample_urls['valid_https'])
            result_data = json.loads(result)
            
            # Check required fields
            assert 'status' in result_data
            assert 'url' in result_data
            assert result_data['status'] in ['valid', 'invalid']
            
            # For valid responses, should not have 'reason'
            if result_data['status'] == 'valid':
                assert 'reason' not in result_data

    def test_invalid_response_structure(self, sample_urls):
        """Test that invalid responses have the correct structure."""
        result = validate_url(sample_urls['invalid_no_scheme'])
        result_data = json.loads(result)
        
        # Check required fields
        assert 'status' in result_data
        assert 'url' in result_data
        assert 'reason' in result_data
        assert result_data['status'] == 'invalid'
        
        # Reason should be a non-empty string
        assert isinstance(result_data['reason'], str)
        assert len(result_data['reason']) > 0

    def test_response_is_valid_json(self, sample_urls):
        """Test that all responses are valid JSON."""
        # Test with valid URL
        with responses.RequestsMock() as rsps:
            rsps.add(responses.HEAD, sample_urls['valid_https'], status=200)
            
            result = validate_url(sample_urls['valid_https'])
            # Should not raise an exception
            json.loads(result)
        
        # Test with invalid URL
        result = validate_url(sample_urls['invalid_no_scheme'])
        # Should not raise an exception
        json.loads(result)

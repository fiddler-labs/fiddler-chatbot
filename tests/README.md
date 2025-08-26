# Testing Framework for Fiddler Chatbot

This directory contains the comprehensive testing framework for the Fiddler AI chatbot project. The framework is designed to ensure code quality, reliability, and maintainability.

## Overview

Our testing strategy includes:
- **Unit Tests**: Test individual functions and classes in isolation
- **Integration Tests**: Test interactions between components
- **Network Tests**: Test actual network interactions (marked with `@pytest.mark.network`)
- **Mocking**: Extensive use of mocks to isolate units under test

## Directory Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Shared fixtures and configuration
├── README.md                   # This file
├── agentic_tools/              # Tests for agentic tools
│   ├── __init__.py
│   └── test_validator_url.py   # URL validator tests
└── utils/                      # Tests for utility modules (future)
```

## Dependencies

The testing framework uses these key dependencies:
- **pytest**: Core testing framework
- **pytest-mock**: Mocking utilities
- **responses**: HTTP request mocking
- **pytest-cov**: Code coverage reporting

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/agentic_tools/test_validator_url.py

# Run specific test class
pytest tests/agentic_tools/test_validator_url.py::TestValidateUrlSyntax

# Run specific test method
pytest tests/agentic_tools/test_validator_url.py::TestValidateUrlSyntax::test_valid_https_url_syntax
```

### Test Categories

Tests are organized using pytest markers:

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"

# Skip network tests (useful for offline development)
pytest -m "not network"

# Run network tests only (requires internet connection)
pytest -m network
```

### Coverage Reports

```bash
# Run tests with coverage report
pytest --cov=src

# Generate HTML coverage report
pytest --cov=src --cov-report=html

# Set minimum coverage threshold
pytest --cov=src --cov-fail-under=80
```

## Writing Tests

### Test File Naming

- Test files should be named `test_*.py`
- Test files should mirror the structure of the source code
- For `src/agentic_tools/validator_url.py`, create `tests/agentic_tools/test_validator_url.py`

### Test Class Organization

Organize tests into logical classes:

```python
class TestFunctionBasicFunctionality:
    """Test basic functionality of the function."""
    
class TestFunctionErrorHandling:
    """Test error handling and edge cases."""
    
class TestFunctionIntegration:
    """Test integration with other components."""
```

### Test Method Naming

Use descriptive test method names that explain what is being tested:

```python
def test_valid_https_url_returns_success(self):
    """Test that valid HTTPS URLs return success status."""
    
def test_invalid_url_without_scheme_returns_error(self):
    """Test that URLs without scheme return appropriate error."""
```

### Using Fixtures

Leverage shared fixtures from `conftest.py`:

```python
def test_url_validation(self, sample_urls, mock_logger):
    """Use shared fixtures for common test data."""
    result = validate_url(sample_urls['valid_https'])
    # Test implementation
```

### Mocking Guidelines

#### Mock External Dependencies

Always mock external dependencies like HTTP requests:

```python
@responses.activate
def test_http_request(self):
    responses.add(responses.HEAD, "https://example.com", status=200)
    # Test implementation
```

#### Mock Logging

Use the `mock_logger` fixture to test logging behavior:

```python
def test_logging_behavior(self, mock_logger):
    with patch('module.logger', mock_logger):
        # Test implementation
        mock_logger.info.assert_called_once()
```

### Test Data Management

#### Use Fixtures for Test Data

Create reusable test data in fixtures:

```python
@pytest.fixture
def sample_data():
    return {
        'valid_case': 'valid_value',
        'invalid_case': 'invalid_value',
    }
```

#### Parameterized Tests

Use parameterization for testing multiple similar cases:

```python
@pytest.mark.parametrize("url,expected", [
    ("https://example.com", "valid"),
    ("invalid-url", "invalid"),
])
def test_url_validation_cases(self, url, expected):
    result = validate_url(url)
    assert json.loads(result)['status'] == expected
```

## Test Markers

Use these markers to categorize your tests:

```python
@pytest.mark.unit
def test_unit_functionality(self):
    """Mark as unit test."""
    
@pytest.mark.integration
def test_component_integration(self):
    """Mark as integration test."""
    
@pytest.mark.slow
def test_slow_operation(self):
    """Mark as slow test."""
    
@pytest.mark.network
def test_network_operation(self):
    """Mark as requiring network access."""
```

## Coverage Guidelines

- **Minimum Coverage**: 80% line coverage
- **Focus Areas**: All public functions should have tests
- **Critical Paths**: Error handling and edge cases must be tested
- **Integration Points**: Test interactions between components

### Coverage Exclusions

Some code may be excluded from coverage requirements:
- Import statements
- Debug/logging statements
- Platform-specific code
- Exception handling for rare cases

## Continuous Integration

Tests are designed to run in CI/CD environments:

- **Fast Tests**: Unit tests should run quickly (< 10 seconds total)
- **Network Tests**: Can be skipped in CI with `-m "not network"`
- **Deterministic**: Tests should not rely on external state
- **Isolated**: Each test should be independent

## Best Practices

### Do's

✅ **Write descriptive test names** that explain the scenario  
✅ **Use fixtures** for common test data and setup  
✅ **Mock external dependencies** to ensure test isolation  
✅ **Test both positive and negative cases**  
✅ **Include edge cases** and error conditions  
✅ **Keep tests simple** and focused on one thing  
✅ **Use appropriate assertions** with clear error messages  

### Don'ts

❌ **Don't test external services** without mocking  
❌ **Don't write tests that depend on each other**  
❌ **Don't ignore test failures** or skip tests without good reason  
❌ **Don't test implementation details** - focus on behavior  
❌ **Don't use magic numbers or strings** - use constants or fixtures  

## Example Test Structure

Here's a template for new test files:

```python
"""
Unit tests for [module_name].

Brief description of what this module tests.
"""
import pytest
from unittest.mock import patch, Mock

# Import the module under test
from module_path import function_to_test


class TestFunctionBasicCases:
    """Test basic functionality."""
    
    def test_valid_input_returns_expected_output(self):
        """Test that valid input produces expected output."""
        # Arrange
        input_data = "test_input"
        expected = "expected_output"
        
        # Act
        result = function_to_test(input_data)
        
        # Assert
        assert result == expected


class TestFunctionErrorHandling:
    """Test error handling and edge cases."""
    
    def test_invalid_input_raises_appropriate_error(self):
        """Test that invalid input raises the correct exception."""
        with pytest.raises(ValueError) as exc_info:
            function_to_test("invalid_input")
        
        assert "expected error message" in str(exc_info.value)


class TestFunctionIntegration:
    """Test integration with other components."""
    
    @patch('module_path.external_dependency')
    def test_integration_with_external_service(self, mock_dependency):
        """Test integration with external services."""
        # Setup mock
        mock_dependency.return_value = "mocked_response"
        
        # Test
        result = function_to_test("input")
        
        # Verify
        assert result == "expected_result"
        mock_dependency.assert_called_once_with("input")
```

## Contributing

When adding new features:

1. **Write tests first** (TDD approach recommended)
2. **Ensure all tests pass** before submitting PR
3. **Maintain or improve coverage** - don't decrease overall coverage
4. **Add appropriate markers** to categorize your tests
5. **Update documentation** if adding new testing patterns

## Troubleshooting

### Common Issues

**Import Errors**: Ensure `src` directory is in Python path  
**Mock Issues**: Check that you're mocking the right import path  
**Coverage Issues**: Make sure test files are properly named and located  
**Network Tests Failing**: Use `-m "not network"` for offline development

### Getting Help

- Check existing tests for examples
- Review pytest documentation
- Ask team members for guidance on testing patterns
- Refer to this documentation for best practices

#!/bin/bash
# Simple test runner script for Fiddler Chatbot project

set -e

echo "🧪 Fiddler Chatbot Test Runner"
echo "================================"

# Check if pytest is available
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest not found. Please install dependencies:"
    echo "   uv sync"
    exit 1
fi

# Check if we're in the right directory
if [ ! -d "tests" ]; then
    echo "❌ Tests directory not found. Please run from project root."
    exit 1
fi

case "${1:-all}" in
    "all")
        echo "🔄 Running all tests..."
        pytest -v
        ;;
    "fast")
        echo "🔄 Running fast tests (excluding network and slow tests)..."
        pytest -m "not slow and not network" -v
        ;;
    "unit")
        echo "🔄 Running unit tests..."
        pytest -m "unit" -v
        ;;
    "coverage")
        echo "🔄 Running tests with coverage report..."
        pytest --cov=src --cov-report=term-missing
        ;;
    "html")
        echo "🔄 Running tests with HTML coverage report..."
        pytest --cov=src --cov-report=html:htmlcov --cov-report=term
        echo "📊 HTML coverage report: htmlcov/index.html"
        ;;
    "validator")
        echo "🔄 Running URL validator tests..."
        pytest tests/agentic_tools/test_validator_url.py -v
        ;;
    "help"|"-h"|"--help")
        echo ""
        echo "Usage: ./test.sh [COMMAND]"
        echo ""
        echo "Commands:"
        echo "  all         Run all tests (default)"
        echo "  fast        Run fast tests (exclude network/slow)"
        echo "  unit        Run unit tests only"
        echo "  coverage    Run tests with coverage report"
        echo "  html        Generate HTML coverage report"
        echo "  validator   Run URL validator tests only"
        echo "  help        Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./test.sh                    # Run all tests"
        echo "  ./test.sh fast              # Run fast tests only"
        echo "  ./test.sh coverage          # Run with coverage"
        echo ""
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo "Run './test.sh help' for available commands"
        exit 1
        ;;
esac

echo "✅ Test execution completed!"

#!/bin/bash
# Ruff linting script for Fiddler Chatbot project

set -e

echo "🔍 Ruff Linter for Fiddler Chatbot"
echo "==================================="

case "${1:-check}" in
    "check")
        echo "🔄 Checking code style..."
        uv run ruff check src/ tests/
        ;;
    "fix")
        echo "🔧 Auto-fixing code style issues..."
        uv run ruff check src/ tests/ --fix
        echo "✅ Auto-fixes applied!"
        ;;
    "format")
        echo "🎨 Formatting code..."
        uv run ruff format src/ tests/
        echo "✅ Code formatted!"
        ;;
    "all")
        echo "🔧 Auto-fixing and formatting..."
        uv run ruff check src/ tests/ --fix
        uv run ruff format src/ tests/
        echo "✅ Code linted and formatted!"
        ;;
    "help"|"-h"|"--help")
        echo ""
        echo "Usage: ./lint.sh [COMMAND]"
        echo ""
        echo "Commands:"
        echo "  check      Check code style (default)"
        echo "  fix        Auto-fix code style issues"
        echo "  format     Format code with ruff"
        echo "  all        Fix and format code"
        echo "  help       Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./lint.sh           # Check code style"
        echo "  ./lint.sh fix       # Auto-fix issues"
        echo "  ./lint.sh format    # Format code"
        echo "  ./lint.sh all       # Fix and format"
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo "Run './lint.sh help' for available commands"
        exit 1
        ;;
esac

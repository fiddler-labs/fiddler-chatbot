#!/bin/bash
# Development environment setup script for Fiddler Chatbot

set -e

echo "🛠️  Fiddler Chatbot Development Setup"
echo "======================================"

# Check if in correct directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Not in project root directory"
    echo "Please run this from the fiddler-chatbot project root"
    exit 1
fi

echo "1️⃣  Installing dependencies with uv..."
if ! command -v uv &> /dev/null; then
    echo "❌ uv not found. Please install uv first: https://docs.astral.sh/uv/"
    exit 1
fi

uv sync
echo "✅ Dependencies installed"

echo ""
echo "2️⃣  Checking VS Code/Cursor setup..."

# Check if Ruff extension is recommended
if [ -f ".vscode/extensions.json" ]; then
    echo "✅ VS Code extensions configured"
else
    echo "⚠️  VS Code extensions not configured"
fi

# Check if settings are configured
if [ -f ".vscode/settings.json" ]; then
    echo "✅ VS Code settings configured for project consistency"
else
    echo "⚠️  VS Code settings not configured"
fi

echo ""
echo "3️⃣  Testing linter setup..."
if uv run ruff check --version > /dev/null 2>&1; then
    echo "✅ Ruff linter available"
    echo "   Run './lint.sh check' to check code style"
    echo "   Run './lint.sh fix' to auto-fix issues"
else
    echo "❌ Ruff linter not working"
fi

echo ""
echo "4️⃣  Testing test framework..."
if uv run pytest --version > /dev/null 2>&1; then
    echo "✅ Pytest available"
    echo "   Run './test.sh' to run tests"
    echo "   Run './test.sh coverage' for coverage report"
else
    echo "❌ Pytest not working"
fi

echo ""
echo "🎉 Development Environment Setup Complete!"
echo ""
echo "💡 Next Steps:"
echo "   • Install recommended VS Code extensions (if prompted)"
echo "   • Restart VS Code/Cursor to apply settings"
echo "   • Run './lint.sh check' to see current code style"
echo "   • Run './test.sh' to verify tests work"
echo ""
echo "📖 Documentation:"
echo "   • Testing: tests/README.md"
echo "   • Project: README.md"

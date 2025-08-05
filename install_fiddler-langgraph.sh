#!/bin/bash
set -e

echo "🚀 Installing Fiddler Chatbot dependencies..."

# Install main dependencies
echo "📦 Installing main dependencies..."
uv pip install -r requirements.txt

# Install fiddler-langgraph from test PyPI
echo "🧪 Installing fiddler-langgraph from test PyPI..."
uv pip install -i https://test.pypi.org/simple/ fiddler-langgraph --prerelease=allow

echo "✅ Installation complete!"
echo "🔍 Verifying installation..."
python -c "import fiddler_langgraph; print(f'✅ fiddler-langgraph {fiddler_langgraph.__version__} installed successfully')" 2>/dev/null || echo "⚠️  fiddler-langgraph import check failed"

echo "🎉 Setup complete! You can now run your chatbot."
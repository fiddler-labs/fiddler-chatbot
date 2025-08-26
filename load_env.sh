#!/bin/bash

# Script to load environment variables from .env file
# Usage: source load_env.sh

ENV_FILE=".env"

# Check if .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Error: $ENV_FILE file not found in current directory"
    echo "Please create a .env file with your secret keys in the format:"
    echo "KEY_NAME=value"
    echo "ANOTHER_KEY=another_value"
    return 1 2>/dev/null || exit 1
fi

# Load environment variables from .env file
echo "🔑 Loading environment variables from $ENV_FILE..."

# Export variables from .env file
set -a  # automatically export all variables
source "$ENV_FILE"
set +a  # stop automatically exporting

# Count loaded variables (excluding comments and empty lines)
loaded_count=$(grep -v '^#' "$ENV_FILE" | grep -v '^$' | wc -l | tr -d ' ')

echo "✅ Successfully loaded $loaded_count environment variables"

# Optional: List loaded variable names (without values for security)
echo "📋 Loaded variables:"
grep -v '^#' "$ENV_FILE" | grep -v '^$' | cut -d'=' -f1 | sed 's/^/  - /'

echo "🚀 Environment variables are now available in your shell session" 
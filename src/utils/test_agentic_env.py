#!/usr/bin/env python3
"""
Test script for the Fiddler Agentic Chatbot
This script helps verify that the chatbot is working correctly
"""

import os
import subprocess
import sys
from pathlib import Path

def check_environment():
    """Check if required environment variables are set"""
    print("🔍 Checking environment variables...")
    
    required_vars = {
        "OPENAI_API_KEY": "Required for LLM functionality",
        "FIDDLER_API_KEY": "Required for Fiddler monitoring",
        "FIDDLER_APP_ID": "Required for Fiddler monitoring (must be UUID4)",
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value or value.startswith("your-"):
            missing_vars.append(f"  - {var}: {description}")
            print(f"❌ {var}: Not set")
        else:
            # Mask sensitive values
            if "KEY" in var:
                masked_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            else:
                masked_value = value
            print(f"✅ {var}: {masked_value}")
    
    if missing_vars:
        print("\n⚠️  Missing environment variables:")
        for var in missing_vars:
            print(var)
        print("\nPlease set these environment variables before running the chatbot.")
        return False
    
    return True

def check_library_imports():
    """Test if all required packages are installed"""
    print("\n🔍 Testing imports...")
    
    try:
        import langchain_core    # noqa: F401
        import langchain_openai  # noqa: F401
        import langgraph         # noqa: F401
        import fiddler_langgraph # noqa: F401
    except ImportError:
        print("❌ - Run: pip install [fiddler-langgraph langchain-core, langchain-openai, langgraph]")
        return False
    
    return True

def run_automated_test():
    """Run an automated test of the chatbot"""
    print("\n🤖 Running automated chatbot test...")
        
    try:
        # Run the chatbot with test input
        result = subprocess.run(
            [sys.executable, "chatbot_agentic.py"],
            input="Hello, chatbot!\nWhat is LangGraph?\nquit\n",
            capture_output=True,
            text=True,
            timeout=30,
            cwd="src"  # Run from src directory
        )
        
        if result.returncode == 0:
            print("✅ Chatbot ran successfully")
            print("\nOutput preview:")
            print("-" * 50)
            lines = result.stdout.split('\n')
            for line in lines[:20]:  # Show first 20 lines
                print(line)
            if len(lines) > 20:
                print(f"... ({len(lines) - 20} more lines)")
            print("-" * 50)
            return True
        else:
            print(f"❌ Chatbot failed with return code: {result.returncode}")
            print("\nError output:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Chatbot test timed out")
        return False
    except Exception as e:
        print(f"❌ Error running chatbot: {e}")
        return False

def main():
    """Main test function"""
    print("="*60)
    print("🧪 Fiddler Agentic Chatbot Test Suite")
    print("="*60)
    
    # Check if chatbot file exists
    chatbot_path = Path("./src/chatbot_agentic.py")
    if not chatbot_path.exists():
        print(f"❌ Chatbot file not found: {chatbot_path}")
        sys.exit(1)
    
    # Run tests
    tests_passed = True
    
    if not check_environment():
        tests_passed = False
    
    if not check_library_imports():
        tests_passed = False
    
    if tests_passed:
        if not run_automated_test():
            tests_passed = False
    
    # Summary
    print("\n" + "="*60)
    if tests_passed:
        print("✅ All tests passed! The chatbot is ready to use.")
        print("\nTo run the chatbot interactively:")
        print("  python ./src/chatbot_agentic.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
    print("="*60)
    
    return 0 if tests_passed else 1

if __name__ == "__main__":
    sys.exit(main()) 
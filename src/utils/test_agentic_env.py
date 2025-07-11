#!/usr/bin/env python3
"""
Test script for the Fiddler Agentic Chatbot
This script helps verify that the chatbot is working correctly
"""

import os
import subprocess
import sys
from pathlib import Path

# Add the src directory to the Python path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from chatbot_agentic import *
from langchain_core.messages import HumanMessage


def check_environment():
    """Check if required environment variables are set"""
    logger.info("🔍 Checking environment variables...")
    
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
            logger.error(f"❌ {var}: Not set")
        else:
            # Mask sensitive values
            if "KEY" in var:
                masked_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            else:
                masked_value = value
            logger.info(f"✅ {var}: {masked_value}")
    
    if missing_vars:
        logger.error("\n⚠️  Missing environment variables:")
        for var in missing_vars:
            logger.error(var)
        logger.error("\nPlease set these environment variables before running the chatbot.")
        return False
    
    return True

def check_library_imports():
    """Test if all required packages are installed"""
    logger.info("\n🔍 Testing imports...")
    
    try:
        import langchain_core    # noqa: F401
        import langchain_openai  # noqa: F401
        import langgraph         # noqa: F401
        import fiddler_langgraph # noqa: F401
    except ImportError:
        logger.error("❌ - Run: pip install [fiddler-langgraph langchain-core, langchain-openai, langgraph]")
        return False
    
    return True

def run_automated_test():
    """Run an automated test of the chatbot"""
    logger.info("\n🤖 Running automated chatbot test...")
    try:
        """
        Verify that the setup is correct and all components are working.
        """
        logger.info("Verifying setup...")
        
        # Check OpenAI connection
        try:
            test_response = llm.invoke([HumanMessage(content="Say 'Hello, I'm working!'")])
            logger.info("✓ OpenAI connection: OK")
            logger.info(test_response.content)
        except Exception as e:
            logger.error(f"❌ OpenAI connection: FAILED - {e}")
            return False
        
        # Check Fiddler connection
        if fdl_client:
            logger.info("✓ Fiddler client: Initialized")
            logger.info(f"  - Application ID: {FIDDLER_APPLICATION_ID}")
            logger.info(f"  - URL: {FIDDLER_URL}")
        else:
            logger.error("❌ Fiddler client: Not initialized")
        
        # Test the graph
        try:
            test_result = app.invoke({"messages": [HumanMessage(content="Test message")]})
            logger.info("✓ LangGraph workflow: OK")
            logger.info(test_result)
        except Exception as e:
            logger.error(f"❌ LangGraph workflow: FAILED - {e}")
            return False
        
        logger.info("✅ All systems operational!")
        logger.info("✅ Chatbot ran successfully")
        return True


    except Exception as e:
        logger.error(f"❌ Error running chatbot: {e}")
        return False


def main():
    """Main test function"""
    logger.info("="*60)
    logger.info("🧪 Fiddler Agentic Chatbot Test Suite")
    logger.info("="*60)
    
    # Check if chatbot file exists
    chatbot_path = Path("./src/chatbot_agentic.py")
    if not chatbot_path.exists():
        logger.error(f"❌ Chatbot file not found: {chatbot_path}")
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
    logger.info("\n" + "="*60)
    if tests_passed:
        logger.info("✅ All tests passed! The chatbot is ready to use.")
        logger.info("\nTo run the chatbot interactively:")
        logger.info("  python ./src/chatbot_agentic.py")
    else:
        logger.error("❌ Some tests failed. Please fix the issues above.")
    logger.info("="*60)
    
    return 0 if tests_passed else 1

if __name__ == "__main__":
    sys.exit(main()) 
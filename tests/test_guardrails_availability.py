"""
Guardrails Availability Test Script

Quick health check to verify all three Fiddler guardrails are responding.
Run this before deeper chatbot testing to ensure the guardrails environment is up.
"""

import logging
from dotenv import load_dotenv

from src.agentic_tools.fiddler_gaurdrails import (
    get_faithfulness_guardrail_results,
    get_pii_guardrail_results,
    get_safety_guardrail_results,
)

from src.utils.custom_logging import setup_logging
setup_logging(log_level="INFO")
logger = logging.getLogger(__name__)


load_dotenv()

# Test data
TEST_SAFETY_QUERY = "What is machine learning and how does it work?"
TEST_FAITHFULNESS_RESPONSE = "Fiddler is an ML observability platform."
TEST_FAITHFULNESS_CONTEXT = [ "Fiddler is a machine learning observability platform that helps teams monitor, explain, and analyze their ML models in production." ]
TEST_PII_TEXT = "I am interested in meeting a Fiddler , Can you please contact me at claude.maximus@example.com or call 9797752387 "


def test_safety_guardrail() -> tuple[bool, str]:
    """Test safety/jailbreak detection guardrail."""
    try:
        score, latency = get_safety_guardrail_results(TEST_SAFETY_QUERY)
        return True, f"score={score:.3f}, latency={latency:.2f}s"
    except Exception as e:
        return False, str(e)


def test_faithfulness_guardrail() -> tuple[bool, str]:
    """Test response faithfulness guardrail."""
    try:
        score, latency = get_faithfulness_guardrail_results(
            TEST_FAITHFULNESS_RESPONSE, TEST_FAITHFULNESS_CONTEXT
        )
        return True, f"score={score:.3f}, latency={latency:.2f}s"
    except Exception as e:
        return False, str(e)


def test_pii_guardrail() -> tuple[bool, str]:
    """Test PII detection guardrail."""
    try:
        entities, latency = get_pii_guardrail_results(TEST_PII_TEXT)
        return True, f"entities_found={len(entities)}, latency={latency:.2f}s"
    except Exception as e:
        return False, str(e)


def main():
    logger.info("=" * 20)
    logger.info("FIDDLER GUARDRAILS AVAILABILITY TEST")
    logger.info("=" * 20 + "\n")

    tests = [
        ("Safety Guardrail", test_safety_guardrail),
        ("Faithfulness Guardrail", test_faithfulness_guardrail),
        ("PII Guardrail", test_pii_guardrail),
    ]

    results = []
    for name, test_fn in tests:
        passed, detail = test_fn()
        status = "[PASS]" if passed else "[FAIL]"
        results.append((name, passed, detail))
        logger.info(f"{status} {name} - {detail}")

    logger.info("-" * 20)
    passed_count = sum(1 for _, passed, _ in results if passed)
    logger.info(f"Summary: {passed_count}/{len(results)} guardrails operational")
    logger.info("-" * 20 + "\n")

    return all(passed for _, passed, _ in results)


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

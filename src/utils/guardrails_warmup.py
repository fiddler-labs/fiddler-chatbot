"""
Guardrails Warmup - Simple wrapper that reuses test_guardrails_availability.py

Runs the guardrails availability test periodically to keep endpoints warm.
"""

import signal
import sys
import time

from src.config import GUARDRAILS_WARMUP_INTERVAL_MINUTES
from tests.test_guardrails_availability import main as run_guardrails_test

# Global flag for graceful shutdown
shutdown_requested = False


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    global shutdown_requested
    shutdown_requested = True


def main():
    """Run guardrails test in a loop."""
    global shutdown_requested

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Get interval from config (default to 30 minutes if not set)
    interval_minutes = GUARDRAILS_WARMUP_INTERVAL_MINUTES
    interval_seconds = interval_minutes * 60

    print(f"Guardrails warmup daemon starting (interval: {interval_minutes} minutes)")

    # Run initial check immediately
    run_guardrails_test()

    # Track when to run next test
    last_run_time = time.time()
    next_run_time = last_run_time + interval_seconds

    # Main loop - check shutdown flag every second for responsive shutdown
    while not shutdown_requested:
        try:
            current_time = time.time()

            # Check if it's time to run the test
            if current_time >= next_run_time:
                run_guardrails_test()
                last_run_time = current_time
                next_run_time = current_time + interval_seconds

            # Sleep for 1 second and check shutdown flag frequently
            time.sleep(1)

        except KeyboardInterrupt:
            shutdown_requested = True
        except Exception as e:
            print(f"Error in warmup loop: {e}", file=sys.stderr)
            # Continue running despite errors


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)

#!/usr/bin/env python3
"""
Test runner script for Fiddler Chatbot project.

This script provides convenient commands for running different types of tests
and generating coverage reports.
"""
import subprocess
import sys
import argparse
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and handle errors."""
    if description:
        print(f"\n🔄 {description}")
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"✅ Success: {description}")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {description}")
        print(f"Error code: {e.returncode}")
        return e.returncode
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        print("Make sure pytest is installed: uv sync")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Test runner for Fiddler Chatbot project"
    )
    parser.add_argument(
        "command",
        choices=[
            "all", "unit", "integration", "network", "fast", 
            "coverage", "html-coverage", "validator-url", "verbose"
        ],
        help="Type of tests to run"
    )
    parser.add_argument(
        "--no-cov", 
        action="store_true", 
        help="Skip coverage reporting"
    )
    
    args = parser.parse_args()
    
    # Base pytest command
    base_cmd = ["pytest"]
    
    # Command configurations
    commands = {
        "all": {
            "cmd": base_cmd + (["-v"] if not args.no_cov else ["-v", "--no-cov"]),
            "description": "Running all tests"
        },
        "unit": {
            "cmd": base_cmd + ["-m", "unit"] + ([] if args.no_cov else ["--cov=src"]),
            "description": "Running unit tests only"
        },
        "integration": {
            "cmd": base_cmd + ["-m", "integration"] + ([] if args.no_cov else ["--cov=src"]),
            "description": "Running integration tests only"
        },
        "network": {
            "cmd": base_cmd + ["-m", "network"] + ([] if args.no_cov else ["--cov=src"]),
            "description": "Running network tests only (requires internet)"
        },
        "fast": {
            "cmd": base_cmd + ["-m", "not slow and not network"] + ([] if args.no_cov else ["--cov=src"]),
            "description": "Running fast tests only (excluding slow and network tests)"
        },
        "coverage": {
            "cmd": base_cmd + ["--cov=src", "--cov-report=term-missing"],
            "description": "Running tests with detailed coverage report"
        },
        "html-coverage": {
            "cmd": base_cmd + ["--cov=src", "--cov-report=html:htmlcov", "--cov-report=term"],
            "description": "Running tests with HTML coverage report"
        },
        "validator-url": {
            "cmd": base_cmd + ["tests/agentic_tools/test_validator_url.py", "-v"] + ([] if args.no_cov else ["--cov=src/agentic_tools/validator_url"]),
            "description": "Running URL validator tests only"
        },
        "verbose": {
            "cmd": base_cmd + ["-v", "-s"] + ([] if args.no_cov else ["--cov=src"]),
            "description": "Running all tests with verbose output and print statements"
        }
    }
    
    if args.command not in commands:
        print(f"❌ Unknown command: {args.command}")
        return 1
    
    # Check if tests directory exists
    if not Path("tests").exists():
        print("❌ Tests directory not found. Are you in the project root?")
        return 1
    
    # Run the command
    cmd_config = commands[args.command]
    return_code = run_command(cmd_config["cmd"], cmd_config["description"])
    
    # Additional information for HTML coverage
    if args.command == "html-coverage" and return_code == 0:
        print("\n📊 HTML coverage report generated:")
        print("   Open htmlcov/index.html in your browser to view detailed coverage")
    
    return return_code


if __name__ == "__main__":
    sys.exit(main())

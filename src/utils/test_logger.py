"""
Test Execution Logger for Cursor AI Assistant

This module provides logging functionality to track all test executions
and prevent hallucinated test results. All test runs are logged to 
logs/cursor_logs/ with complete output capture.

Usage:
    from src.utils.test_logger import log_test_execution
    
    log_file, success = log_test_execution(
        "python -m pytest tests/test_example.py -v",
        "tests/test_example.py"
    )
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional

def log_test_execution(
    test_command: str, 
    test_file_path: str,
    working_directory: Optional[str] = None
    ) -> Tuple[str, bool]:
    """
    Execute a test command and log all output to prevent hallucinated results.
    
    Args:
        test_command: The test command to execute (e.g., "python -m pytest tests/")
        test_file_path: Path to the test file being executed
        working_directory: Optional working directory for command execution
    
    Returns:
        Tuple of (log_file_path, success_boolean)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"logs/cursor_logs/test_run_{timestamp}.log"
    
    # Ensure log directory exists
    log_dir = Path("logs/cursor_logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Prepare execution environment
    cwd = working_directory or os.getcwd()
    
    with open(log_file, 'w') as f:
        f.write(f"Test Execution Log - {datetime.now()}\n")
        f.write(f"Command: {test_command}\n")
        f.write(f"Test File: {test_file_path}\n")
        f.write(f"Working Directory: {cwd}\n")
        f.write("=" * 50 + "\n")
        
        try:
            # Execute and capture output
            result = subprocess.run(
                test_command, 
                shell=True,
                capture_output=True, 
                text=True,
                cwd=cwd,
                timeout=300  # 5 minute timeout
            )
            
            f.write(f"Exit Code: {result.returncode}\n")
            f.write(f"STDOUT:\n{result.stdout}\n")
            f.write(f"STDERR:\n{result.stderr}\n")
            
            success = result.returncode == 0
            
        except subprocess.TimeoutExpired:
            f.write("ERROR: Test execution timed out after 5 minutes\n")
            success = False
            
        except Exception as e:
            f.write(f"ERROR: Exception during test execution: {str(e)}\n")
            success = False
        
        f.write("=" * 50 + "\n")
        f.write("Test Summary:\n")
        f.write(f"- Success: {success}\n")
        f.write(f"- Log file: {log_file}\n")
        f.write(f"- Timestamp: {datetime.now()}\n")
    
    return log_file, success


def get_latest_test_log() -> Optional[str]:
    """
    Get the path to the most recent test log file.
    Returns: Path to the latest log file, or None if no logs exist
    """
    log_dir = Path("logs/cursor_logs")
    if not log_dir.exists():
        return None
    
    log_files = list(log_dir.glob("test_run_*.log"))
    if not log_files:
        return None
    
    # Sort by modification time, most recent first
    latest_log = max(log_files, key=lambda f: f.stat().st_mtime)
    return str(latest_log)


def summarize_test_results(log_file_path: str) -> dict:
    """
    Parse a test log file and extract key results.
    Args: log_file_path: Path to the test log file
    Returns: Dictionary with test results summary
    """
    try:
        with open(log_file_path, 'r') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # Extract key information
        command = next((line.split(': ', 1)[1] for line in lines if line.startswith('Command: ')), "Unknown")
        exit_code = next((int(line.split(': ')[1]) for line in lines if line.startswith('Exit Code: ')), -1)
        
        # Count test results from pytest output
        passed_tests = content.count(' PASSED')
        failed_tests = content.count(' FAILED')
        error_tests = content.count(' ERROR')
        
        return {
            'log_file': log_file_path,
            'command': command,
            'exit_code': exit_code,
            'success': exit_code == 0,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'error_tests': error_tests,
            'total_tests': passed_tests + failed_tests + error_tests
        }
        
    except Exception as e:
        return {
            'log_file': log_file_path,
            'error': f"Failed to parse log: {str(e)}"
        }


def main():
    """
    Command-line interface for test logger.
    Usage: python src/utils/test_logger.py "command to execute" "test_file_path" [working_dir]
        
    System Args:
        command: The command to execute (e.g., "python -m pytest tests/")
        test_file_path: Path to the test file being executed
        working_directory: Optional working directory for command execution
    
    Examples:
        python src/utils/test_logger.py "python -m pytest tests/" "tests/"
        python src/utils/test_logger.py "python src/app.py" "src/app.py" 
        python src/utils/test_logger.py "uv run pipeline" "pipeline_script.py"
    """
    import sys
    
    if not (3 <= len(sys.argv) <= 4):
        print("❌ Error: Wrong arguments count")
        print("\nUsage:")
        print("  python src/utils/test_logger.py \"command\" \"test_file_path\" [working_dir]")
        print("\nExamples:")
        print("  python src/utils/test_logger.py \"python -m pytest tests/\" \"tests/\"")
        print("  python src/utils/test_logger.py \"python src/app.py\" \"src/app.py\"")
        print("  python src/utils/test_logger.py \"uv run pipeline\" \"pipeline_script.py\"")
        return
    
    command = sys.argv[1]
    test_file = sys.argv[2]
    working_dir = sys.argv[3] if len(sys.argv) >= 4 else None
    
    print("Test Logger - Command Wrapper")
    print("=" * 50)
    print(f"Command: {command}")
    print(f"Test File: {test_file}")
    print(f"Working Dir: {working_dir or 'current directory'}")
    print("=" * 50)
    
    # Execute with logging
    log_file, success = log_test_execution(command, test_file, working_dir)
    
    # Show results
    print("\nExecution Results:")
    print(f"Success: {success}")
    print(f"Log File: {log_file}")
    
    # Show summary
    summary = summarize_test_results(log_file)

    print(f"Tests: \n{summary['total_tests']} total, \n{summary['passed_tests']} passed, \n{summary['failed_tests']} failed")
    print(f"Exit Code: {summary['exit_code']}")
    
    # Show log file location for reference
    print(f"Reference this log file in your response:\n{log_file}")
    
    # Exit with same code as the wrapped command
    if 'exit_code' in summary:
        sys.exit(summary['exit_code'])
    else:
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 
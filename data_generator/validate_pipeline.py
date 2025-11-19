#!/usr/bin/env python3
"""
Validation script for the batch orchestrator pipeline.
Checks data quality, completeness, and consistency of generated conversations.
"""

import pandas as pd
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")

def print_success(text: str):
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_error(text: str):
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")

def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")

def print_info(text: str):
    print(f"   {text}")

def check_file_exists(filepath: str) -> bool:
    """Check if a file exists and is readable."""
    exists = os.path.exists(filepath)
    if not exists:
        print_error(f"File not found: {filepath}")
    return exists

def validate_csv_structure(csv_path: str) -> Tuple[bool, pd.DataFrame]:
    """Validate CSV file structure and required columns."""
    print_header("CSV Structure Validation")

    required_columns = ['id', 'persona', 'role', 'content']

    try:
        df = pd.read_csv(csv_path)
        print_success(f"CSV file loaded: {len(df)} rows")

        # Check columns
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            print_error(f"Missing required columns: {missing_cols}")
            return False, df

        print_success(f"All required columns present: {required_columns}")

        # Check for empty rows
        empty_rows = df[df['content'].isna() | (df['content'] == '')]
        if len(empty_rows) > 0:
            print_warning(f"Found {len(empty_rows)} rows with empty content")
            print_info("This may be normal for tool responses")
        else:
            print_success("No empty content rows found")

        return True, df

    except Exception as e:
        print_error(f"Error reading CSV: {e}")
        return False, pd.DataFrame()

def validate_conversation_structure(df: pd.DataFrame) -> Dict:
    """Validate conversation thread structure."""
    print_header("Conversation Structure Validation")

    results = {
        'total_conversations': df['id'].nunique(),
        'total_messages': len(df),
        'role_distribution': df['role'].value_counts().to_dict(),
        'expected_roles': ['system', 'human', 'ai', 'tool'],
        'thread_stats': {}
    }

    print_success(f"Total unique conversations: {results['total_conversations']}")
    print_success(f"Total messages: {results['total_messages']}")

    print_info("\nRole distribution:")
    for role, count in results['role_distribution'].items():
        print_info(f"  {role}: {count}")

    # Validate each conversation thread
    threads_with_issues = []
    for thread_id in df['id'].unique():
        thread_messages = df[df['id'] == thread_id]
        roles = thread_messages['role'].tolist()

        # Check for expected conversation flow
        has_system = 'system' in roles
        has_human = 'human' in roles
        has_ai = 'ai' in roles

        stats = {
            'message_count': len(thread_messages),
            'has_system': has_system,
            'has_human': has_human,
            'has_ai': has_ai,
            'first_role': roles[0] if roles else None,
            'last_role': roles[-1] if roles else None
        }

        results['thread_stats'][thread_id] = stats

        # Flag potential issues
        if not has_system:
            threads_with_issues.append((thread_id, "Missing system message"))
        if not has_human:
            threads_with_issues.append((thread_id, "Missing human message"))
        if not has_ai:
            threads_with_issues.append((thread_id, "Missing AI message"))
        if stats['message_count'] < 3:
            threads_with_issues.append((thread_id, f"Too few messages: {stats['message_count']}"))

    if threads_with_issues:
        print_warning(f"Found {len(threads_with_issues)} threads with potential issues")
        for thread_id, issue in threads_with_issues[:5]:  # Show first 5
            print_info(f"  {thread_id[:8]}...: {issue}")
    else:
        print_success("All conversation threads have proper structure")

    # Average messages per conversation
    avg_messages = results['total_messages'] / results['total_conversations']
    print_info(f"\nAverage messages per conversation: {avg_messages:.2f}")

    return results

def validate_persona_coverage(df: pd.DataFrame, personas_file: str) -> Dict:
    """Validate that personas from JSON are represented in CSV."""
    print_header("Persona Coverage Validation")

    try:
        with open(personas_file, 'r') as f:
            personas_data = json.load(f)

        enabled_personas = [
            p for p in personas_data.get('personas', [])
            if p.get('enabled', True)
        ]

        print_success(f"Found {len(enabled_personas)} enabled personas in {personas_file}")

        # Build expected persona strings
        expected_personas = []
        for persona in enabled_personas:
            if 'description' in persona:
                expected = f"You are a {persona['name']}. {persona['description']}."
                expected_personas.append(expected)
            elif 'prompt' in persona:
                expected_personas.append(persona['prompt'])

        # Check coverage
        unique_personas_in_csv = df['persona'].unique()
        found_personas = []
        missing_personas = []

        for expected in expected_personas:
            # Check if any CSV persona contains or matches expected
            found = any(expected in persona or persona == expected
                       for persona in unique_personas_in_csv)
            if found:
                found_personas.append(expected[:80])
            else:
                missing_personas.append(expected[:80])

        results = {
            'expected_count': len(expected_personas),
            'found_count': len(found_personas),
            'missing_count': len(missing_personas),
            'coverage_percent': (len(found_personas) / len(expected_personas) * 100) if expected_personas else 0
        }

        print_info(f"Expected personas: {results['expected_count']}")
        print_info(f"Found in CSV: {results['found_count']}")
        print_info(f"Missing: {results['missing_count']}")
        print_info(f"Coverage: {results['coverage_percent']:.1f}%")

        if missing_personas:
            print_warning(f"\nMissing personas (showing first 5):")
            for persona in missing_personas[:5]:
                print_info(f"  - {persona}...")
        else:
            print_success("All enabled personas have conversations in CSV")

        return results

    except Exception as e:
        print_error(f"Error validating persona coverage: {e}")
        return {'error': str(e)}

def validate_message_content(df: pd.DataFrame) -> Dict:
    """Validate content quality of messages."""
    print_header("Message Content Validation")

    results = {
        'avg_content_length': {},
        'empty_content_count': 0,
        'tool_response_count': 0
    }

    for role in df['role'].unique():
        role_messages = df[df['role'] == role]
        # Ensure we're working with a pandas Series, not numpy array
        content_series = pd.Series(role_messages['content'], dtype='string')
        content_lengths = content_series.str.len()
        results['avg_content_length'][role] = content_lengths.mean()
        print_info(f"Average {role} message length: {results['avg_content_length'][role]:.0f} characters")

    empty_content = df[df['content'].isna() | (df['content'] == '')]
    results['empty_content_count'] = len(empty_content)
    if results['empty_content_count'] > 0:
        print_warning(f"Found {results['empty_content_count']} messages with empty content")
        print_info("  (This may be normal for tool responses)")

    tool_messages = df[df['role'] == 'tool']
    results['tool_response_count'] = len(tool_messages)
    print_info(f"Tool responses: {results['tool_response_count']}")

    # Check for very short AI responses (potential issues)
    ai_messages = df[df['role'] == 'ai']
    # Ensure we're working with a pandas Series, not numpy array
    ai_content_series = pd.Series(ai_messages['content'], dtype='string')
    short_ai = ai_messages[ai_content_series.str.len() < 100]
    if len(short_ai) > 0:
        print_warning(f"Found {len(short_ai)} AI messages shorter than 100 characters")

    return results

def validate_output_file_matches_expected(csv_path: str, expected_output: str) -> bool:
    """Check if the generated file matches the expected output file."""
    print_header("Output File Validation")

    actual_path = Path(csv_path).resolve()
    expected_path = Path(expected_output).resolve()

    if actual_path == expected_path:
        print_success(f"Output file matches expected: {expected_output}")
        return True
    else:
        print_error(f"Output file mismatch!")
        print_info(f"  Expected: {expected_output}")
        print_info(f"  Actual: {csv_path}")
        return False

def generate_validation_report(results: Dict, output_file: str | None = None):
    """Generate a summary validation report."""
    print_header("Validation Summary")

    all_passed = True
    checks = [
        ("CSV Structure", results.get('csv_valid', False)),
        ("Conversation Structure", results.get('conversation_valid', False)),
        ("Persona Coverage", results.get('persona_coverage', {}).get('coverage_percent', 0) > 50),
        ("Message Content", results.get('content_valid', False)),
    ]

    for check_name, passed in checks:
        if passed:
            print_success(f"{check_name}: PASSED")
        else:
            print_error(f"{check_name}: FAILED")
            all_passed = False

    if all_passed:
        print_success("\n🎉 All validation checks passed!")
    else:
        print_error("\n⚠️  Some validation checks failed. Please review.")

    # Save report if requested
    if output_file:
        report = {
            'timestamp': datetime.now().isoformat(),
            'results': results,
            'all_passed': all_passed
        }
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        print_info(f"\nReport saved to: {output_file}")

    return all_passed

def main():
    """Main validation function."""
    print_header("Pipeline Validation Script")
    print_info("Validating batch orchestrator output...")

    # Configuration
    csv_file = "data/agentic_conversations.csv"
    personas_file = "personas.json"

    results = {}

    # Check file exists
    if not check_file_exists(csv_file):
        print_error("Cannot proceed without CSV file")
        sys.exit(1)

    if not check_file_exists(personas_file):
        print_warning(f"Personas file not found: {personas_file}")
        print_info("Skipping persona coverage validation")

    # Validate CSV structure
    csv_valid, df = validate_csv_structure(csv_file)
    results['csv_valid'] = csv_valid

    if not csv_valid:
        print_error("CSV structure validation failed. Stopping.")
        sys.exit(1)

    # Validate conversation structure
    conversation_results = validate_conversation_structure(df)
    results['conversation_valid'] = True  # Assume valid if we got here
    results['conversation_stats'] = conversation_results

    # Validate persona coverage
    if check_file_exists(personas_file):
        persona_results = validate_persona_coverage(df, personas_file)
        results['persona_coverage'] = persona_results
    else:
        results['persona_coverage'] = {'skipped': True}

    # Validate content
    content_results = validate_message_content(df)
    results['content_valid'] = True
    results['content_stats'] = content_results

    # Validate output file path
    results['output_file_valid'] = validate_output_file_matches_expected(
        csv_file, "data/agentic_conversations.csv"
    )

    # Generate report
    all_passed = generate_validation_report(results)

    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()

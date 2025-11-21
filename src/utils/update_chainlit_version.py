"""
Script to update chainlit.md with current git branch, commit hash, and build date.

This script is intended to be run as a pre-deployment hook to ensure
chainlit.md always contains accurate version information.
"""
import re
import sys
from datetime import datetime
from pathlib import Path

# Add workspace root to Python path for imports
_script_dir = Path(__file__).resolve().parent.parent.parent
if str(_script_dir) not in sys.path:
    sys.path.insert(0, str(_script_dir))

# Import version_info utilities (after path setup)
from src.utils.version_info import get_version_info  # noqa: E402


def find_chainlit_md() -> Path:
    """
    Find chainlit.md file in the workspace root.

    Returns:
        Path to chainlit.md

    Raises:
        FileNotFoundError: If chainlit.md cannot be found
    """
    # Try to find repo root by looking for chainlit.md
    # Start from current file location and walk up
    current = Path(__file__).resolve().parent.parent.parent

    chainlit_path = current / 'chainlit.md'
    if chainlit_path.exists():
        return chainlit_path

    # Also try current working directory
    cwd_chainlit = Path.cwd() / 'chainlit.md'
    if cwd_chainlit.exists():
        return cwd_chainlit

    raise FileNotFoundError(
        f"chainlit.md not found. Searched: {chainlit_path}, {cwd_chainlit}"
    )


def update_chainlit_version_info() -> int:
    """
    Update chainlit.md with current git branch, commit hash, and build date.

    Returns:
        0 on success, 1 on error
    """
    try:
        # Get version information
        version_info = get_version_info()
        branch = version_info['branch']
        commit_hash = version_info['hash']

        # Get current build date in YYYYMMDD format
        build_date = datetime.now().strftime('%Y%m%d')

        # Find and read chainlit.md
        chainlit_path = find_chainlit_md()
        content = chainlit_path.read_text(encoding='utf-8')

        # Update Branch line (matches "Branch: <any_value>")
        content = re.sub(
            r'^Branch:\s*.+$',
            f'Branch: {branch}',
            content,
            flags=re.MULTILINE
        )

        # Update Commit line (matches "Commit: <any_value>")
        content = re.sub(
            r'^Commit:\s*.+$',
            f'Commit: {commit_hash}',
            content,
            flags=re.MULTILINE
        )

        # Update Date line (matches "Date: <any_value>")
        content = re.sub(
            r'^Date:\s*.+$',
            f'Date: {build_date}',
            content,
            flags=re.MULTILINE
        )

        # Write updated content back
        chainlit_path.write_text(content, encoding='utf-8')

        print("✓ Updated chainlit.md with version info:")
        print(f"  Branch: {branch}")
        print(f"  Commit: {commit_hash}")
        print(f"  Date: {build_date}")

        return 0

    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Failed to update chainlit.md: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(update_chainlit_version_info())

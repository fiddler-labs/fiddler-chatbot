"""
Utility functions to get version information for display in the UI.
"""
import subprocess
import os
from pathlib import Path


def _find_repo_root() -> Path | None:
    """Find the git repository root by walking up from current file or cwd."""
    # Try starting from __file__ location
    start_paths = []
    try:
        start_paths.append(Path(__file__).resolve().parent.parent.parent)
    except (NameError, AttributeError):
        pass

    # Also try current working directory
    try:
        start_paths.append(Path.cwd())
    except Exception:
        pass

    for start_path in start_paths:
        current = Path(start_path).resolve()
        # Walk up the directory tree looking for .git
        for _ in range(10):  # Limit to 10 levels up
            if (current / '.git').exists():
                return current
            parent = current.parent
            if parent == current:  # Reached filesystem root
                break
            current = parent

    return None


def get_git_commit_hash(short: bool = True) -> str:
    """
    Get the current git commit hash.

    Args:
        short: If True, return short hash (7 chars), else full hash

    Returns:
        Git commit hash string, or 'unknown' if git is not available
    """
    repo_root = _find_repo_root()
    if not repo_root:
        # Not a git repo, try environment variable
        env_hash = os.getenv('GIT_COMMIT_HASH', '')
        if env_hash:
            return env_hash[:7] if short else env_hash
        return 'unknown'

    try:
        # Get git commit hash - first get full hash, then shorten if needed
        # This avoids issues with --short flag in some git versions
        cmd = ['git', 'rev-parse', 'HEAD']
        result = subprocess.run(
            cmd,
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )
        hash_value = result.stdout.strip()
        if not hash_value:
            raise ValueError("Empty hash returned")

        # Shorten if requested
        if short:
            hash_value = hash_value[:7]

        return hash_value
    except subprocess.CalledProcessError as e:
        # Git command failed - check stderr for details
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"Git command failed (returncode={e.returncode}): stdout={repr(e.stdout)}, stderr={repr(e.stderr)}")
        # Don't fall through - return unknown immediately
        env_hash = os.getenv('GIT_COMMIT_HASH', '')
        if env_hash:
            return env_hash[:7] if short else env_hash
        return 'unknown'
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        # Git not found or timeout
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"Git not available: {type(e).__name__}: {e}")
        env_hash = os.getenv('GIT_COMMIT_HASH', '')
        if env_hash:
            return env_hash[:7] if short else env_hash
        return 'unknown'
    except ValueError as e:
        # Empty hash
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"Empty hash error: {e}")
        env_hash = os.getenv('GIT_COMMIT_HASH', '')
        if env_hash:
            return env_hash[:7] if short else env_hash
        return 'unknown'
    except Exception as e:
        # Other unexpected error
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"Unexpected error getting git hash ({type(e).__name__}): {e}")
        env_hash = os.getenv('GIT_COMMIT_HASH', '')
        if env_hash:
            return env_hash[:7] if short else env_hash
        return 'unknown'

    # Fallback: try to get from environment variable (useful in Docker/CI)
    env_hash = os.getenv('GIT_COMMIT_HASH', '')
    if env_hash:
        return env_hash[:7] if short else env_hash
    return 'unknown'


def get_git_branch() -> str:
    """
    Get the current git branch name.

    Returns:
        Branch name string, or 'unknown' if git is not available
    """
    try:
        repo_root = _find_repo_root()
        if not repo_root:
            return os.getenv('GIT_BRANCH', 'unknown')

        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )
        return result.stdout.strip()
    except Exception:
        return os.getenv('GIT_BRANCH', 'unknown')


def get_version_info() -> dict[str, str]:
    """
    Get version information including git hash and branch.

    Returns:
        Dictionary with 'hash' and 'branch' keys
    """
    return {
        'hash': get_git_commit_hash(short=True),
        'branch': get_git_branch(),
    }

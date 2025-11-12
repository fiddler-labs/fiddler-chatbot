"""
## Primary Objective

Create a vector-ready corpus by:

1. **Source Collection**: Clone Fiddler repositories and crawl RSS feeds
2. **Content Processing**: Convert notebooks to markdown, process documentation
3. **Corpus Generation**: Combine all sources and split into chunks for vector indexing

## Responsibility Areas

- **Repository Management**: Git operations, branch selection
- **Content Transformation**: Notebook conversion, markdown processing
- **Web Scraping**: RSS feed crawling and content extraction
- **File System Operations**: Directory management, cleanup
- **Data Pipeline Orchestration**: Coordinating the entire workflow

The architecture follows a linear pipeline pattern with error recovery mechanisms at various stages.


"""

import os
import shutil
import glob
import logging
import subprocess
import pandas as pd
import re
import feedparser
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import datetime as dt
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from pathlib import Path
from packaging import version

from utils.notebook_to_md import convert_notebooks_jupyter_nbconvert, convert_notebooks_native_regex
from utils.flatten_folders import flatten_all_files_individually, concatenate_files_in_leaf_folders
from utils.custom_logging import setup_logging

from config import CONFIG_DATA_GENERATION as config  # noqa: N811

# Setup logging with default values
setup_logging(log_level="DEBUG")
logger = logging.getLogger(__name__)


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up 2 levels from src/data_generation.py to project root ./
LOCAL_DATA_ASSETS_DIR = os.path.join(PROJECT_ROOT, "local_assets")
CLONED_REPOS_DIR = os.path.join(LOCAL_DATA_ASSETS_DIR, "cloned_repos")

FIDDLER_MAIN_REPO_DIR     = os.path.join(CLONED_REPOS_DIR, "fiddler")
FIDDLER_EXAMPLES_REPO_DIR = os.path.join(CLONED_REPOS_DIR, "fiddler-examples")

FIDDLER_MD_DOCS_DIR      = os.path.join(LOCAL_DATA_ASSETS_DIR, "md-docs")
FIDDLER_MD_NOTEBOOKS_DIR = os.path.join(LOCAL_DATA_ASSETS_DIR, "md-notebooks")
FIDDLER_MD_BLOGS_DIR     = os.path.join(LOCAL_DATA_ASSETS_DIR, "md-blogs")
FIDDLER_MD_RESOURCES_DIR = os.path.join(LOCAL_DATA_ASSETS_DIR, "md-resources")


FIDDLER_MAIN_REPO_URL     = config["FIDDLER_MAIN_REPO_URL"]
FIDDLER_EXAMPLES_REPO_URL = config["FIDDLER_EXAMPLES_REPO_URL"]
FIDDLER_WEBSITE_BLOG_URL      = config["FIDDLER_WEBSITE_BLOG_URL"]
FIDDLER_WEBSITE_RESOURCES_URL = config["FIDDLER_WEBSITE_RESOURCES_URL"]

# Text splitting configuration
RECURSIVE_SPLITTER_CHUNK_SIZE    = config["RECURSIVE_SPLITTER_CHUNK_SIZE"]
RECURSIVE_SPLITTER_CHUNK_OVERLAP = config["RECURSIVE_SPLITTER_CHUNK_OVERLAP"]

# MarkdownHeaderTextSplitter configuration
USE_MARKDOWN_HEADER_SPLITTER = config["USE_MARKDOWN_HEADER_SPLITTER"]
MARKDOWN_HEADERS_TO_SPLIT_ON = config["MARKDOWN_HEADERS_TO_SPLIT_ON"]
MARKDOWN_STRIP_HEADERS = config["MARKDOWN_STRIP_HEADERS"]
MARKDOWN_RETURN_EACH_LINE = config["MARKDOWN_RETURN_EACH_LINE"]

KEEP_REPOS = config["KEEP_REPOS"]
KEEP_CSV_FILES = config["KEEP_CSV_FILES"]

# Notebook conversion method configuration
NOTEBOOK_CONVERSION_METHOD = config["NOTEBOOK_CONVERSION_METHOD"]

# Markdown flattening method configuration
MARKDOWN_FLATTENING_METHOD = config["MARKDOWN_FLATTENING_METHOD"]


def reset_local_data_assets(keep_repos: bool = True, keep_csv_files: bool = True) -> None:
    """
    Clears out the old doc content folders and files.
    Removes local_assets/vector_index_feed_*.csv files and processing directories.
    Clean up the cloned repos directory by removing cloned repositories.

    Args:
        keep_repos: If True, keep the cloned repos directory and its contents
        keep_csv_files: If True, keep the generated CSV files (useful for historical cataloging and debugging)
    """
    logger.info("Clearing local_assets directory...")

    if os.path.exists(CLONED_REPOS_DIR):
        if not keep_repos:
            logger.info(f"Deleting cloned repos directory: {CLONED_REPOS_DIR}")
            shutil.rmtree(CLONED_REPOS_DIR)
            logger.info("Cloned repo directory cleaned up successfully")
        else:
            logger.info("Keeping cloned repos directory as requested")

    else:
        logger.info("Cloned repo directory does not exist, nothing to clean up")

    # Remove CSV files matching pattern (only if keep_csv_files is False)
    if not keep_csv_files:
        csv_pattern = os.path.join(LOCAL_DATA_ASSETS_DIR, "vector_index_feed_*.csv")
        for csv_file in glob.glob(csv_pattern):
            logger.info(f"Removing {csv_file}")
            os.remove(csv_file)
    else:
        logger.info("Keeping CSV files as requested")


    # Create local_assets directory if it doesn't exist
    os.makedirs(LOCAL_DATA_ASSETS_DIR, exist_ok=True)

    # Remove directories if they exist
    dirs_to_remove = [
        FIDDLER_MD_DOCS_DIR,
        FIDDLER_MD_NOTEBOOKS_DIR,
        FIDDLER_MD_BLOGS_DIR,
        FIDDLER_MD_RESOURCES_DIR
    ]

    for dir_path in dirs_to_remove:
        if os.path.exists(dir_path):
            logger.info(f"Removing directory {dir_path}")
            shutil.rmtree(dir_path)

    logger.info("Documentation data directory cleared successfully")

def clone_or_pull_repo(repo_url: str, repo_location: str) -> None:
    """
    Clone a repository to the repo directory if it doesn't exist.
    If the repo already exists, pull the latest changes.
    If the pull fails, remove the repo and clone it again.
    Handles all edge cases including corrupted repositories and missing directories.

    Args: repo_url: The Git repository URL to clone
          repo_location: Name for the local repository directory

    """


    def _is_valid_git_repo(path: str) -> bool:
        """Check if a directory contains a valid git repository."""
        try:
            subprocess.run([
                "git", "-C", path, "rev-parse", "--git-dir"
            ], check=True, capture_output=True, text=True)
            return True
        except subprocess.CalledProcessError:
            return False

    logger.info(f"Setting up repository {repo_url} at {repo_location}")

    # Ensure parent directory exists
    parent_dir = os.path.dirname(repo_location)
    os.makedirs(parent_dir, exist_ok=True)

    # Check if target location exists and is a valid git repository
    if os.path.exists(repo_location):
        if _is_valid_git_repo(repo_location):
            # Try to pull latest changes
            try:
                # Fetch latest remote information first
                fetch_result = subprocess.run([
                    "git", "-C", repo_location, "fetch"
                    ], check=True, capture_output=True, text=True)
                logger.info(f"Fetched remote updates: {fetch_result.stdout.strip()}")

                result = subprocess.run([
                    "git", "-C", repo_location, "pull"
                    ], check=True, capture_output=True, text=True)
                logger.info(f"Successfully pulled latest changes: {result.stdout.strip()}")

                try :
                    result = subprocess.run([
                        "git", "-C", repo_location, "lfs", "pull"
                        ], check=True, capture_output=True, text=True)
                    logger.info(f"Successfully pulled latest LFS changes: {result.stdout.strip()}")

                except subprocess.CalledProcessError as e:
                    logger.warning(f"Failed to pull LFS changes (if any) : {e.stderr}. Continuing...")

                return
            except subprocess.CalledProcessError as e:
                logger.warning(f"Pull failed: {e.stderr}. Will re-clone repository.")
                # Remove corrupted repository and proceed to clone
                shutil.rmtree(repo_location)
        else:
            logger.info(f"Directory exists but is not a valid git repository. Removing: {repo_location}")
            shutil.rmtree(repo_location)

    # Clone the repository (directory should not exist at this point)
    logger.info(f"Cloning {repo_url} to {repo_location}")
    try:
        result = subprocess.run([
            "git", "clone", repo_url, repo_location
        ], check=True, capture_output=True, text=True)
        logger.info(f"Successfully cloned repository: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to clone repository {repo_url}: {e.stderr}")
        raise RuntimeError(f"Repository cloning failed: {e.stderr}") from e

def checkout_latest_release_branch(repo_path: str, branch_override: str | None = None) -> str:
    """
    Get the latest release branch name from the repository and check out to it.
    Args:
        repo_path: Path to the cloned repository
        branch_override: Optional specific branch name to checkout instead of finding the latest release
    Returns: Name of the branch that was checked out
    """

    def _parse_version_from_branch(branch_name: str) -> tuple[version.Version | None, str]:
        """
        Parse semantic version from branch name.

        Args:
            branch_name: Branch name like 'release/v1.10.0' or 'release/1.2.0'

        Returns:
            Tuple of (parsed_version, original_branch_name)
            parsed_version is None if parsing fails
        """
        # Common patterns for release branches
        patterns = [
            r'release/v(\d+\.\d+\.\d+)',      # release/v1.10.0
            r'release/(\d+\.\d+\.\d+)',       # release/1.10.0
            r'release/v(\d+\.\d+)',           # release/v1.10
            r'release/(\d+\.\d+)',            # release/1.10
        ]

        for pattern in patterns:
            match = re.search(pattern, branch_name)
            if match:
                version_str = match.group(1)
                try:
                    # Handle 2-part versions by appending .0
                    if version_str.count('.') == 1:
                        version_str += '.0'
                    parsed_version = version.parse(version_str)
                    return parsed_version, branch_name
                except version.InvalidVersion:
                    continue

        return None, branch_name

    if branch_override:
        logger.info(f"Using branch override: {branch_override}")
        try:
            # Fetch latest remote information first
            subprocess.run([
                "git", "-C", repo_path, "fetch"
            ], check=True, capture_output=True, text=True)

            # Checkout the specified branch
            subprocess.run([
                "git", "-C", repo_path, "checkout", branch_override
            ], check=True, capture_output=True, text=True)
            logger.info(f"Successfully checked out override branch: {branch_override}")
            return branch_override
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to checkout override branch {branch_override}: {e.stderr}")
            logger.warning("Falling back to automatic branch selection...")
            # Continue with automatic selection if override fails

    logger.info("Finding and checking out latest release branch...")

    try:
        # Get all remote branches
        result = subprocess.run([
            "git", "-C", repo_path, "branch", "-r"
        ], check=True, capture_output=True, text=True)

        # Filter for release branches
        release_branches = []
        for line in result.stdout.split('\n'):
            line = line.strip()
            if 'origin/release/' in line and not line.endswith('HEAD'):
                branch_name = line.replace('origin/', '')
                release_branches.append(branch_name)

        if not release_branches:
            logger.warning("No release branches found, using main branch")
            latest_branch = "main"
        else:
            # Parse versions and sort properly using semantic versioning
            versioned_branches = []
            unversioned_branches = []

            for branch in release_branches:
                parsed_version, original_branch = _parse_version_from_branch(branch)
                if parsed_version:
                    versioned_branches.append((parsed_version, original_branch))
                else:
                    unversioned_branches.append(original_branch)

            # Sort versioned branches by semantic version (highest first)
            if versioned_branches:
                versioned_branches = [branch for branch in versioned_branches if branch[0] <= version.Version("30.0.0")]
                versioned_branches = sorted(versioned_branches, key=lambda x: x[0], reverse=True)
                latest_branch = versioned_branches[0][1]
                logger.info(f"Latest release branch found: {latest_branch} (version: {versioned_branches[0][0]})")
            else:
                # Fallback to lexicographic sorting for non-semantic versions
                unversioned_branches.sort(reverse=True)
                latest_branch = unversioned_branches[0]
                logger.warning(f"No semantic versions found, using lexicographic sort: {latest_branch}")

        # Checkout the branch
        logger.info(f"Checking out branch {latest_branch}...")
        subprocess.run([
            "git", "-C", repo_path, "checkout", latest_branch
        ], check=True, capture_output=True, text=True)
        logger.info(f"Successfully checked out {latest_branch}")

        return latest_branch

    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to get release branches or checkout: {e.stderr}")
        logger.warning("Falling back to main branch")
        try:
            subprocess.run([
                "git", "-C", repo_path, "checkout", "main"
            ], check=True, capture_output=True, text=True)
            logger.info("Successfully checked out main branch")
            return "main"
        except subprocess.CalledProcessError as e2:
            logger.error(f"Failed to checkout main branch: {e2.stderr}")
            raise

def process_docs() -> None: # WIP
    """
    Process the documentation files from the cloned repository.
    """

    docs_source = os.path.join(FIDDLER_MAIN_REPO_DIR, "docs")

    def _simple_copy_docs_folder() -> None:
        """
        Copy the docs folder from the cloned repository to local_assets/fiddler-docs.
        Args: repo_path: Path to the cloned Fiddler repository
        """
        logger.info("Copying docs folder...")

        docs_destination = FIDDLER_MD_DOCS_DIR

        if not os.path.exists(docs_source):
            raise FileNotFoundError(f"Docs folder not found at {docs_source}")

        # Create destination directory
        os.makedirs(os.path.dirname(docs_destination), exist_ok=True)

        # Remove destination if it exists
        if os.path.exists(docs_destination):
            shutil.rmtree(docs_destination)
            logger.info(f"Removed existing docs folder at {docs_destination}")

        # Copy the docs folder
        shutil.copytree(docs_source, docs_destination)
        logger.info(f"Successfully copied docs folder to {docs_destination}")

    logger.info("Processing documentation files...")

    # implement markdown flattening
    if MARKDOWN_FLATTENING_METHOD not in ['individual', 'concatenated']:
        logger.error(f"Invalid markdown flattening method: {MARKDOWN_FLATTENING_METHOD}")
        logger.error("Valid options are: 'individual' or 'concatenated'")
        raise RuntimeError("Invalid markdown flattening method")

    try:
        if   MARKDOWN_FLATTENING_METHOD == 'individual':
            flatten_all_files_individually    (source_dir=Path(docs_source), dest_dir=Path(FIDDLER_MD_DOCS_DIR))
        elif MARKDOWN_FLATTENING_METHOD == 'concatenated':
            concatenate_files_in_leaf_folders (source_dir=Path(docs_source), dest_dir=Path(FIDDLER_MD_DOCS_DIR))
        logger.info("Markdown flattening completed successfully")

    # try the alternative method if the first method fails
    except Exception as e:
        logger.error(f"Error flattening markdown: {e} via {MARKDOWN_FLATTENING_METHOD} method , using alternative fallback conversion method")
        try:
            if   MARKDOWN_FLATTENING_METHOD == 'individual':
                concatenate_files_in_leaf_folders (source_dir=Path(docs_source), dest_dir=Path(FIDDLER_MD_DOCS_DIR))
            elif MARKDOWN_FLATTENING_METHOD == 'concatenated':
                flatten_all_files_individually    (source_dir=Path(docs_source), dest_dir=Path(FIDDLER_MD_DOCS_DIR))
            logger.info("Markdown flattening completed successfully")

        # fall back to simple copy of docs folder
        except Exception as e2:
            logger.error(f"Error flattening markdown: {e2} via both methods , falling back to simple copy of docs folder")
            try:
                logger.info("Falling back to simple copy of docs folder")
                _simple_copy_docs_folder()
            except Exception as e3:
                logger.error(f"Error copying docs folder: {e3} , cannot continue")
                raise RuntimeError("Error copying docs folder") from e3

    return

def process_notebooks() -> None:
    """
    Convert .ipynb files from the fiddler-examples repository to markdown.
    Uses the method specified by NOTEBOOK_CONVERSION_METHOD constant.
    Both documentation and notebook files are kept separate for individual embedding.
    """

    def _find_notebook_files(source_dir: str) -> list[str]:
        """
        Find all .ipynb files recursively in the source directory.
        Skips checkpoint files and returns a list of notebook file paths.

        Args: source_dir: Directory to search for notebook files
        Returns: List of notebook file paths
        """
        notebook_files = []
        for root, _dirs, files in os.walk(source_dir):
            for file in files:
                if file.endswith('.ipynb'):
                    if '.ipynb_checkpoints' not in root:  # Skip checkpoint files
                        notebook_files.append(os.path.join(root, file))
        return notebook_files

    logger.info(f"Processing notebook files using {NOTEBOOK_CONVERSION_METHOD} method...")
    os.makedirs(FIDDLER_MD_NOTEBOOKS_DIR, exist_ok=True)

    # Find all notebook files
    notebook_files = _find_notebook_files(FIDDLER_EXAMPLES_REPO_DIR)

    if not notebook_files:
        logger.warning("No notebook files found in the repository")
        return

    logger.info(f"Found {len(notebook_files)} notebook files")

    # Choose conversion method based on configuration
    conversion_success = False

    if NOTEBOOK_CONVERSION_METHOD == 'jupyter_nbconvert':
        conversion_success = convert_notebooks_jupyter_nbconvert(notebook_files, FIDDLER_MD_NOTEBOOKS_DIR)
    elif NOTEBOOK_CONVERSION_METHOD == 'native_regex':
        conversion_success = convert_notebooks_native_regex(notebook_files, FIDDLER_MD_NOTEBOOKS_DIR)
    else:
        logger.error(f"Invalid notebook conversion method: {NOTEBOOK_CONVERSION_METHOD}")
        logger.error("Valid options are: 'jupyter_nbconvert' or 'native_regex'")
        conversion_success = False

    # If primary conversion method fails, try the fallback method
    if not conversion_success:
        logger.warning("Primary conversion method failed, trying fallback approach...")

        # Try the alternative method first before copying files
        if NOTEBOOK_CONVERSION_METHOD == 'native_regex':
            logger.info("Trying jupyter nbconvert as fallback...")
            conversion_success = convert_notebooks_jupyter_nbconvert(notebook_files, FIDDLER_MD_NOTEBOOKS_DIR)
        elif NOTEBOOK_CONVERSION_METHOD == 'jupyter_nbconvert':
            logger.info("Trying native regex method as fallback...")
            conversion_success = convert_notebooks_native_regex(notebook_files, FIDDLER_MD_NOTEBOOKS_DIR)

        if not conversion_success:
            logger.error("All conversion methods failed")
            raise RuntimeError("All conversion methods failed")
        else:
            logger.info("Fallback conversion method succeeded")

    logger.info(f"Successfully processed {len(notebook_files)} notebook files")

def crawl_rss_feeds() -> None:
    """
    Crawl RSS feeds from Fiddler's blog and resources, and save content as markdown files.
    """

    def _crawl_single_rss_feed(rss_url: str, div_class: str, output_dir: str, content_type: str) -> None:
        """
        Crawl a single RSS feed and save articles as markdown files.

        Args:
            rss_url: URL of the RSS feed
            div_class: CSS class name to extract content from
            output_dir: Directory to save markdown files
            content_type: Type of content ('blog' or 'resources') for logging
        """
        logger.info(f"Crawling {content_type} RSS feed: {rss_url}")

        try:
            # Parse the RSS feed
            feed = feedparser.parse(rss_url)

            if not feed.entries:
                logger.warning(f"No entries found in {content_type} RSS feed")
                return

            logger.info(f"Found {len(feed.entries)} {content_type} entries")

            # Process each entry in the feed
            for i, entry in tqdm(enumerate(feed.entries), total=len(feed.entries), desc="Processing RSS Feed Entries"):
                try:
                    # Get the URL of the article (ensure it's a string)
                    article_url = str(entry.link) if hasattr(entry, 'link') else None
                    title = str(entry.title) if hasattr(entry, 'title') else f"Article_{i+1}"

                    if not article_url:
                        logger.warning(f"No URL found for {content_type} entry: {title}")
                        continue

                    logger.info(f"Processing {content_type} article: {title}")

                    # Fetch the content of the article
                    response = requests.get(article_url, timeout=30)
                    response.raise_for_status()
                    html_content = response.content.decode('utf-8', 'ignore')

                    # Use BeautifulSoup to parse the HTML and extract the content
                    soup = BeautifulSoup(html_content, 'html.parser')
                    div_content = soup.find('div', class_=div_class)

                    if div_content and hasattr(div_content, 'find_all'):
                        # Extract text content from paragraphs
                        content_text = ''
                        paragraphs = div_content.find_all('p')  # type: ignore
                        for paragraph in paragraphs:
                            if hasattr(paragraph, 'get_text'):
                                content_text += paragraph.get_text(strip=True) + '\n\n'

                        if content_text.strip():
                            # Create a safe filename from the title
                            safe_filename = article_url.split('/')[-1] + '.md'

                            # Create markdown content
                            markdown_content = f"# {title}\n\n"
                            markdown_content += f"**Source:** {article_url}\n\n"
                            markdown_content += f"**Content Type:** {content_type.title()}\n\n"
                            markdown_content += "---\n\n"
                            markdown_content += content_text

                            # Save to markdown file
                            file_path = os.path.join(output_dir, safe_filename)
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(markdown_content)

                            logger.info(f"Saved {content_type} article to: {file_path}")
                        else:
                            logger.warning(f"No content extracted from {content_type} article: {title}")
                    else:
                        logger.warning(f"Content div not found for {content_type} article: {title}")

                except Exception as e:
                    logger.error(f"Failed to process {content_type} article '{entry.title}': {str(e)}")
                    continue

        except Exception as e:
            logger.error(f"Failed to crawl {content_type} RSS feed: {str(e)}")


    logger.info("Starting RSS feed crawling...")

    # Create directories for blogs and resources
    os.makedirs(FIDDLER_MD_BLOGS_DIR, exist_ok=True)
    os.makedirs(FIDDLER_MD_RESOURCES_DIR, exist_ok=True)

    # Track success/failure of each feed
    feeds_processed = []
    feeds_failed = []

    # Crawl blog RSS feed with error recovery
    try:
        logger.info("Attempting to crawl blog RSS feed...")
        _crawl_single_rss_feed(
            rss_url=FIDDLER_WEBSITE_BLOG_URL + 'rss.xml',
            div_class='blog-post_content-wrapper',
            output_dir=FIDDLER_MD_BLOGS_DIR,
            content_type='blog'
        )
        feeds_processed.append('blog')
        logger.info("Blog RSS feed crawling completed successfully")
    except Exception as e:
        feeds_failed.append('blog')
        logger.error(f"Blog RSS feed crawling failed: {str(e)}")
        logger.warning("Continuing with other feeds despite blog feed failure")

    # Crawl resources RSS feed with error recovery
    try:
        logger.info("Attempting to crawl resources RSS feed...")
        _crawl_single_rss_feed(
            rss_url=FIDDLER_WEBSITE_RESOURCES_URL + 'rss.xml',
            div_class='resources-copy',
            output_dir=FIDDLER_MD_RESOURCES_DIR,
            content_type='resources'
        )
        feeds_processed.append('resources')
        logger.info("Resources RSS feed crawling completed successfully")
    except Exception as e:
        feeds_failed.append('resources')
        logger.error(f"Resources RSS feed crawling failed: {str(e)}")
        logger.warning("Continuing despite resources feed failure")

    # Summary of RSS feed crawling results
    if feeds_processed:
        logger.info(f"RSS feed crawling completed. Successfully processed: {', '.join(feeds_processed)}")

    if feeds_failed:
        logger.warning(f"RSS feed crawling had failures. Failed feeds: {', '.join(feeds_failed)}")

    if not feeds_processed:
        logger.error("All RSS feeds failed to process")
    else:
        logger.info("RSS feed crawling phase completed (some feeds may have failed, but process continues)")

def split_text_with_markdown_headers(text: str) -> list[str]:
    """
    Split text using MarkdownHeaderTextSplitter with optional hybrid approach.
    Args: text: Input text to split
    Returns: List of text chunks
    """

    # Fallback to original RecursiveCharacterTextSplitter
    recursive_text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=RECURSIVE_SPLITTER_CHUNK_SIZE,
        chunk_overlap=RECURSIVE_SPLITTER_CHUNK_OVERLAP,
        length_function=len
        )

    # Initialize MarkdownHeaderTextSplitter
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=MARKDOWN_HEADERS_TO_SPLIT_ON,
        return_each_line=MARKDOWN_RETURN_EACH_LINE,
        strip_headers=MARKDOWN_STRIP_HEADERS
        )

    try:
        if USE_MARKDOWN_HEADER_SPLITTER:
            # Split by markdown headers first
            md_header_splits = markdown_splitter.split_text(text)
            final_chunks: list[str] = []

            for doc in md_header_splits:
                # Split large sections further while preserving header metadata in content
                metadata_prefix = ""
                if doc.metadata:
                    # Create a context prefix from header metadata
                    header_context = " | ".join([f"{k}: {v}" for k, v in doc.metadata.items()])
                    metadata_prefix = f"[CONTEXT: {header_context}]\n\n"

                # If the content is already small enough, keep it as-is
                if len(doc.page_content) <= RECURSIVE_SPLITTER_CHUNK_SIZE:
                    # Add metadata context to the content
                    final_chunks.append( metadata_prefix + doc.page_content )
                else:
                    # Split large sections further
                    sub_chunks = recursive_text_splitter.split_text(doc.page_content)
                    sub_chunks = [ metadata_prefix + chunk for chunk in sub_chunks ]
                    final_chunks.extend(sub_chunks)
                    logger.debug(f"    successfully split a big chunk ({len(doc.page_content)} chars) into > {len(sub_chunks)} sub-chunks")

            logger.debug(f"Successfully split 1 MD FILE into > {len(md_header_splits)} H1 documents into > {len(final_chunks)} chunks")
            return final_chunks

        elif not USE_MARKDOWN_HEADER_SPLITTER:
            logger.info("Using RecursiveCharacterTextSplitter for text splitting")
            recursive_text_splits = recursive_text_splitter.split_text(text)
            logger.debug(f"Successfully split {len(recursive_text_splits)} chunks")
            return recursive_text_splits

        else:
            raise RuntimeError("Invalid text splitting method")

    except RuntimeError as e:
        logger.error(f"SELECTED splitting strategy failed, attempting to fall back to character splitting: {str(e)}")
        logger.info("FALLBACK: RecursiveCharacterTextSplitter for text splitting")
        try:
            return recursive_text_splitter.split_text(text)

        except Exception as e:
            logger.error(f"FATAL ERROR: Error splitting text via FALLBACK method: {str(e)}")
            raise RuntimeError("FATAL ERROR: Error splitting text via FALLBACK method") from e


def generate_corpus_from_sources() -> Path:
    """
    Generate a corpus by combining all markdown content and splitting it into chunks.
    Creates a DataFrame and saves it as a CSV file for vector indexing.
    Returns: Path to the generated CSV file
    """
    logger.info("Starting corpus generation with text splitting...")

    source_docs = []

    # Collect processed documentation files
    if os.path.exists(FIDDLER_MD_DOCS_DIR):
        logger.info("Collecting documentation files...")
        for root, _dirs, files in os.walk(FIDDLER_MD_DOCS_DIR):
            for filename in files:
                if filename.endswith(".md"):
                    file_path = os.path.join(os.path.relpath(root), filename)
                    try:
                        with open(file_path, encoding='utf-8') as f:
                            file_content = f.read()
                            # Embed the URL/path of the doc in the content for reference
                            doc_url = os.path.join('https://docs.fiddler.ai/', filename).replace('__', '/')
                            doc_url = f'DOC_URL:{doc_url[:-3]}'  # Remove .md extension
                            doc_content = f'DOC_CONTENT:{file_content}'
                            source_docs.append(f'{doc_url}\n{doc_content}')
                    except Exception as e:
                        logger.error(f"Failed to read documentation file {file_path}: {str(e)}")

    # Collect converted notebook files
    if os.path.exists(FIDDLER_MD_NOTEBOOKS_DIR):
        logger.info("Collecting converted notebook files...")
        for root, _dirs, files in os.walk(FIDDLER_MD_NOTEBOOKS_DIR):
            for filename in files:
                if filename.endswith(".md"):
                    file_path = os.path.join(os.path.relpath(root), filename)
                    try:
                        with open(file_path, encoding='utf-8') as f:
                            file_content = f.read()
                            # Mark as notebook content
                            doc_url = f'NOTEBOOK_URL:{file_path[:-3]}'
                            doc_content = f'NOTEBOOK_CONTENT:{file_content}'
                            source_docs.append(f'{doc_url}\n{doc_content}')
                    except Exception as e:
                        logger.error(f"Failed to read notebook file {file_path}: {str(e)}")

    # Collect blog files
    if os.path.exists(FIDDLER_MD_BLOGS_DIR):
        logger.info("Collecting blog files...")
        for root, _dirs, files in os.walk(FIDDLER_MD_BLOGS_DIR):
            for filename in files:
                if filename.endswith(".md"):
                    file_path = os.path.join(os.path.relpath(root), filename)
                    try:
                        with open(file_path, encoding='utf-8') as f:
                            file_content = f.read()
                            doc_url = os.path.join(FIDDLER_WEBSITE_BLOG_URL, filename).replace('__', '/')
                            doc_url = f'BLOG_URL:{doc_url[:-3]}'
                            doc_content = f'BLOG_CONTENT:{file_content}'
                            source_docs.append(f'{doc_url}\n{doc_content}')
                    except Exception as e:
                        logger.error(f"Failed to read blog file {file_path}: {str(e)}")

    # Collect resources files
    if os.path.exists(FIDDLER_MD_RESOURCES_DIR):
        logger.info("Collecting resources files...")
        for root, _dirs, files in os.walk(FIDDLER_MD_RESOURCES_DIR):
            for filename in files:
                if filename.endswith(".md"):
                    file_path = os.path.join(os.path.relpath(root), filename)
                    try:
                        with open(file_path, encoding='utf-8') as f:
                            file_content = f.read()
                            doc_url = os.path.join(FIDDLER_WEBSITE_RESOURCES_URL, filename).replace('__', '/')
                            doc_url = f'RESOURCES_URL:{doc_url[:-3]}'
                            doc_content = f'RESOURCES_CONTENT:{file_content}'
                            source_docs.append(f'{doc_url}\n{doc_content}')
                    except Exception as e:
                        logger.error(f"Failed to read resources file {file_path}: {str(e)}")

    if not source_docs:
        logger.warning("No source documents found for corpus generation")
        raise RuntimeError("No source documents found for corpus generation")

    logger.info(f"Collected {len(source_docs)} source documents")

    # Clean and prepare corpus
    source_docs_trimmed = [item.strip() for item in source_docs if item.strip()]
    logger.info(f"Cleaned corpus contains {len(source_docs_trimmed)} documents")

    splitter_method = "MarkdownHeaderTextSplitter" if USE_MARKDOWN_HEADER_SPLITTER else "RecursiveCharacterTextSplitter"
    logger.info(f"Splitting corpus into chunks using {splitter_method}...")

    corpus_chunks = []
    for i, doc in tqdm(enumerate(source_docs_trimmed), total=len(source_docs_trimmed), desc="Processing MD Documents"):
        try:
            texts = split_text_with_markdown_headers(doc)
            corpus_chunks.extend(texts)

        except Exception as e:
            logger.error(f"Failed to split document {i + 1}: {str(e)}")
            continue

    logger.debug(f"Successfully split {len(source_docs_trimmed)} MD documents into > {len(corpus_chunks)} chunks")

    if not corpus_chunks:
        logger.error("No chunks generated from corpus")
        raise RuntimeError("No chunks generated from corpus")

    # Create DataFrame and save to CSV
    df = pd.DataFrame({'text': corpus_chunks})

    # Create output filename
    output_filename = f'vector_index_feed_{dt.datetime.now(dt.UTC).strftime("%Y%m%d%H%M%S")}.csv'  # type: ignore[attr-defined]
    output_path = os.path.join(LOCAL_DATA_ASSETS_DIR, output_filename)

    try:
        df.to_csv(output_path, index=False)
        logger.info(f"Successfully saved corpus to {output_path}")
        logger.info(f"DataFrame shape: {df.shape}")
        return Path(output_path)

    except Exception as e:
        logger.error(f"Failed to save corpus CSV: {str(e)}")
        raise RuntimeError("Failed to save corpus CSV") from e


def corpus_data_generation_process() -> Path | None:
    """
    Main function to orchestrate the complete data management workflow.
    Returns: Path to the generated corpus CSV file
    """
    logger.info("Starting local data management workflow")

    try:
        reset_local_data_assets(keep_repos=KEEP_REPOS, keep_csv_files=KEEP_CSV_FILES)  # Keep repos for efficiency at start

        clone_or_pull_repo(FIDDLER_MAIN_REPO_URL, FIDDLER_MAIN_REPO_DIR)
        checkout_latest_release_branch(FIDDLER_MAIN_REPO_DIR , branch_override=None)

        clone_or_pull_repo(FIDDLER_EXAMPLES_REPO_URL,FIDDLER_EXAMPLES_REPO_DIR)
        checkout_latest_release_branch(FIDDLER_EXAMPLES_REPO_DIR , branch_override=None)

        process_docs() # todo
        process_notebooks()

        # RSS feed crawling with workflow-level error recovery
        try:
            crawl_rss_feeds()
        except Exception as e:
            logger.error(f"RSS feed crawling failed completely: {str(e)}")
            logger.warning("Continuing corpus generation without RSS feed content")

        # Generate corpus with text splitting
        corpus_path = generate_corpus_from_sources()

        if corpus_path:
            logger.info(f"Corpus CSV generated at: {corpus_path}")
            logger.info("Local markdown data management workflow completed successfully!")
            return corpus_path
        else:
            logger.error("Corpus CSV generation failed")
            return None

    except Exception as e:
        logger.error(f"Local data generation workflow failed: {str(e)}")
        raise


if __name__ == "__main__":
    output_path = corpus_data_generation_process()

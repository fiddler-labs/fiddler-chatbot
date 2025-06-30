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

"""

import os
import shutil
import subprocess
import glob
import logging
import pandas as pd
import re
import feedparser
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timezone
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Repo URLs
FIDDLER_MAIN_REPO_URL     = "https://github.com/fiddler-labs/fiddler.git"
FIDDLER_EXAMPLES_REPO_URL = "https://github.com/fiddler-labs/fiddler-examples.git"

# RSS Feed URLs
BLOG_RSS_URL      = 'https://www.fiddler.ai/blog/rss.xml'
RESOURCES_RSS_URL = 'https://www.fiddler.ai/resources/rss.xml'

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up 2 levels from src/data_generation.py to project root ./
LOCAL_DATA_ASSETS_DIR = os.path.join(PROJECT_ROOT, "local_assets")
CLONED_REPOS_DIR = os.path.join(LOCAL_DATA_ASSETS_DIR, "cloned_repos")

FIDDLER_MAIN_REPO_DIR     = os.path.join(CLONED_REPOS_DIR, "fiddler")
FIDDLER_EXAMPLES_REPO_DIR = os.path.join(CLONED_REPOS_DIR, "fiddler-examples")

FIDDLER_MD_DOCS_DIR      = os.path.join(LOCAL_DATA_ASSETS_DIR, "md-docs")
FIDDLER_MD_NOTEBOOKS_DIR = os.path.join(LOCAL_DATA_ASSETS_DIR, "md-notebooks")
FIDDLER_MD_BLOGS_DIR     = os.path.join(LOCAL_DATA_ASSETS_DIR, "md-blogs")
FIDDLER_MD_RESOURCES_DIR = os.path.join(LOCAL_DATA_ASSETS_DIR, "md-resources")

# Text splitting configuration
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 300


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
                result = subprocess.run([
                    "git", "-C", repo_location, "pull"
                ], check=True, capture_output=True, text=True)
                logger.info(f"Successfully pulled latest changes: {result.stdout.strip()}")
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
        raise RuntimeError(f"Repository cloning failed: {e.stderr}")

def checkout_latest_release_branch(repo_path: str, branch_override: str | None = None):
    """
    Get the latest release branch name from the repository and check out to it.
    Args: 
        repo_path: Path to the cloned repository
        branch_override: Optional specific branch name to checkout instead of finding the latest release
    Returns: Name of the branch that was checked out
    """
    if branch_override:
        logger.info(f"Using branch override: {branch_override}")
        try:
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
            # Sort release branches to get the latest (assuming semantic versioning)
            release_branches.sort(reverse=True)
            latest_branch = release_branches[0]
            logger.info(f"Latest release branch found: {latest_branch}")
        
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

def copy_docs_folder() -> None:
    """
    Copy the docs folder from the cloned repository to local_assets/fiddler-docs.
    Args: repo_path: Path to the cloned Fiddler repository
    """
    logger.info("Copying docs folder...")
    
    docs_source = os.path.join(FIDDLER_MAIN_REPO_DIR, "docs")
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

def process_docs() -> None:
    """
    Process the documentation files from the cloned repository.
    """
    # WIP
    logger.info("Processing documentation files...")

def process_notebooks() -> None:
    """
    Convert .ipynb files from the fiddler-examples repository to markdown.
    Both documentation and notebook files are kept separate for individual embedding.
    """
    logger.info("Processing notebook files...")
    os.makedirs(FIDDLER_MD_NOTEBOOKS_DIR, exist_ok=True)
    
    # Find all .ipynb files recursively
    notebook_files = []
    for root, dirs, files in os.walk(FIDDLER_EXAMPLES_REPO_DIR):
        for file in files:
            if file.endswith('.ipynb'):
                if '.ipynb_checkpoints' not in root:  # Skip checkpoint files
                    notebook_files.append(os.path.join(root, file))
    
    if not notebook_files:
        logger.warning("No notebook files found in the repository")
        return
    
    logger.info(f"Found {len(notebook_files)} notebook files")
    
    # Convert notebooks to markdown using jupyter nbconvert
    logger.info("Converting notebooks to markdown...")
    try:
        cmd = [
            "jupyter", "nbconvert", 
            "--output-dir", FIDDLER_MD_NOTEBOOKS_DIR,
            "--to", "markdown"
        ] + notebook_files
        
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info("Successfully converted notebooks to markdown")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to convert notebooks: {e.stderr}")
        logger.warning("Falling back to copying .ipynb files")
        
        # Fallback: copy .ipynb files
        for notebook_file in notebook_files:
            filename = os.path.basename(notebook_file)
            destination_file = os.path.join(FIDDLER_MD_NOTEBOOKS_DIR, filename)
            
            # Handle duplicate filenames by adding a suffix
            counter = 1
            original_destination = destination_file
            while os.path.exists(destination_file):
                name, ext = os.path.splitext(original_destination)
                destination_file = f"{name}_{counter}{ext}"
                counter += 1
            
            shutil.copy2(notebook_file, destination_file)
            logger.info(f"Copied {filename} to {destination_file}")
        return
    
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
            for i, entry in enumerate(feed.entries):
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
                            safe_filename = re.sub(r'[^\w\s-]', '', title).strip()
                            safe_filename = re.sub(r'[-\s]+', '-', safe_filename)
                            safe_filename = f"{i+1:03d}_{safe_filename[:50]}.md"  # Limit filename length
                            
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
            rss_url=BLOG_RSS_URL,
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
            rss_url=RESOURCES_RSS_URL,
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

def generate_corpus_from_sources() -> str | None:
    """
    Generate a corpus by combining all markdown content and splitting it into chunks.
    Creates a DataFrame and saves it as a CSV file for vector indexing.
    
    Args:
        release_num: Release version number for the output file naming
    
    Returns:
        Path to the generated CSV file
    """
    logger.info("Starting corpus generation with text splitting...")
    
    source_docs = []
    
    # Collect documentation files
    if os.path.exists(FIDDLER_MD_DOCS_DIR):
        logger.info("Collecting documentation files...")
        for root, dirs, files in os.walk(FIDDLER_MD_DOCS_DIR):
            for filename in files:
                if filename.endswith(".md"):
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, "r", encoding='utf-8') as f:
                            file_content = f.read()
                            # Embed the URL/path of the doc in the content for reference
                            doc_url = f'DOC_URL:{file_path[:-3]}'  # Remove .md extension
                            doc_content = f'DOC_CONTENT:{file_content}'
                            source_docs.append(f'{doc_url}\n{doc_content}')
                    except Exception as e:
                        logger.error(f"Failed to read documentation file {file_path}: {str(e)}")
    
    # Collect converted notebook files
    if os.path.exists(FIDDLER_MD_NOTEBOOKS_DIR):
        logger.info("Collecting converted notebook files...")
        for root, dirs, files in os.walk(FIDDLER_MD_NOTEBOOKS_DIR):
            for filename in files:
                if filename.endswith(".md"):
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, "r", encoding='utf-8') as f:
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
        for root, dirs, files in os.walk(FIDDLER_MD_BLOGS_DIR):
            for filename in files:
                if filename.endswith(".md"):
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, "r", encoding='utf-8') as f:
                            file_content = f.read()
                            source_docs.append(f'BLOG_CONTENT:{file_content}')
                    except Exception as e:
                        logger.error(f"Failed to read blog file {file_path}: {str(e)}")
    
    # Collect resources files
    if os.path.exists(FIDDLER_MD_RESOURCES_DIR):
        logger.info("Collecting resources files...")
        for root, dirs, files in os.walk(FIDDLER_MD_RESOURCES_DIR):
            for filename in files:
                if filename.endswith(".md"):
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, "r", encoding='utf-8') as f:
                            file_content = f.read()
                            source_docs.append(f'RESOURCES_CONTENT:{file_content}')
                    except Exception as e:
                        logger.error(f"Failed to read resources file {file_path}: {str(e)}")
    
    if not source_docs:
        logger.warning("No source documents found for corpus generation")
        return ""
    
    logger.info(f"Collected {len(source_docs)} source documents")
    
    # Clean and prepare corpus
    corpus = [item.strip() for item in source_docs if item.strip()]
    logger.info(f"Cleaned corpus contains {len(corpus)} documents")
    
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len
        )
    
    # Split corpus into chunks
    logger.info("Splitting corpus into chunks...")
    corpus_chunks = []
    for doc in corpus:
        try:
            texts = text_splitter.split_text(doc)
            corpus_chunks.extend(texts)
        except Exception as e:
            logger.error(f"Failed to split document: {str(e)}")
            continue
    
    logger.info(f"Generated {len(corpus_chunks)} text chunks")
    
    if not corpus_chunks:
        logger.error("No chunks generated from corpus")
        return ""
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame({'text': corpus_chunks})
    
    # Create output filename
    output_filename = f'vector_index_feed_{datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")}.csv'
    output_path = os.path.join(LOCAL_DATA_ASSETS_DIR, output_filename)
    
    try:
        df.to_csv(output_path, index=False)
        logger.info(f"Successfully saved corpus to {output_path}")
        logger.info(f"DataFrame shape: {df.shape}")
        return output_path
    except Exception as e:
        logger.error(f"Failed to save corpus CSV: {str(e)}")
        return None


def corpus_data_generation_process() -> str | None:
    """
    Main function to orchestrate the complete data management workflow.
    Returns: Path to the generated corpus CSV file
    """
    logger.info("Starting local data management workflow")
    
    try:
        keep_repos = True # todo - should come from config_dataprep.py
        reset_local_data_assets(keep_repos=keep_repos)  # Keep repos for efficiency at start
        
        clone_or_pull_repo(FIDDLER_MAIN_REPO_URL, FIDDLER_MAIN_REPO_DIR)
        checkout_latest_release_branch(FIDDLER_MAIN_REPO_DIR)
        
        clone_or_pull_repo(FIDDLER_EXAMPLES_REPO_URL,FIDDLER_EXAMPLES_REPO_DIR)
        checkout_latest_release_branch(FIDDLER_EXAMPLES_REPO_DIR)
        
        copy_docs_folder()
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

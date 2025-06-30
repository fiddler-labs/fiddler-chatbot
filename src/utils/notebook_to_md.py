import os
import json
from pathlib import Path
import re
from typing import Optional, List
import subprocess
import logging

# Configure logging - todo - unify with other logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def convert_notebooks_jupyter_nbconvert(notebook_files: List[str], output_dir: str) -> bool:
    """
    Convert notebooks using jupyter nbconvert command-line tool.
    
    Args:
        notebook_files: List of notebook file paths to convert
        output_dir: Directory where converted markdown files will be saved
        
    Returns:
        True if conversion was successful, False otherwise
    """
    logger.info("Converting notebooks using jupyter nbconvert...")
    try:
        cmd = [
            "jupyter", "nbconvert", 
            "--output-dir", output_dir,
            "--to", "markdown"
        ] + notebook_files
        
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info("Successfully converted notebooks using jupyter nbconvert")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to convert notebooks with jupyter nbconvert: {e.stderr}")
        return False


def convert_notebooks_native_regex(notebook_files: List[str], output_dir: str) -> bool:
    """
    Convert notebooks using the native regex-based conversion function.
    
    Args:
        notebook_files: List of notebook file paths to convert
        output_dir: Directory where converted markdown files will be saved
        
    Returns:
        True if conversion was successful, False otherwise
    """
    logger.info("Converting notebooks using native regex-based converter...")
    success_count = 0
    
    for notebook_file in notebook_files:
        try:
            # Convert using the native function
            output_path = _convert_notebook__native(
                notebook_path=Path(notebook_file),
                output_dir=Path(output_dir),
                skip_images=True,
                skip_links=True
            )
            logger.info(f"Successfully converted {notebook_file} to {output_path}")
            success_count += 1
        except Exception as e:
            logger.error(f"Failed to convert {notebook_file} using native method: {str(e)}")
            continue
    
    if success_count > 0:
        logger.info(f"Successfully converted {success_count}/{len(notebook_files)} notebooks using native method")
        return True
    else:
        logger.error("Failed to convert any notebooks using native method")
        return False


def _convert_notebook__native(notebook_path: Path, output_dir: Optional[Path] = None, skip_images: bool = True, 
                    skip_links: bool = True) -> Path:
    """
    Convert a single notebook to markdown.
    
    Args:
        notebook_path: Path to the input notebook
        output_dir: Optional directory for output files
        skip_images: If True, exclude image tags from output
        skip_links: If True, exclude hyperlinks from output
    
    Returns:
        str: Path to the generated markdown file
    """
    notebook_path = Path(notebook_path)
    
    if not notebook_path.exists():
        raise FileNotFoundError(f"Notebook not found: {notebook_path}")
    
    # Determine output path
    if output_dir:
        output_path = Path(output_dir) / f"{notebook_path.stem}.md"
    else:
        output_path = notebook_path.with_suffix('.md')
    
    # Read notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Convert to markdown
    markdown_content = []
    
    # Add title if present in notebook metadata
    if 'title' in notebook.get('metadata', {}):
        markdown_content.append(f"# {notebook['metadata']['title']}\n")
    
    for cell in notebook['cells']:
        # Skip empty cells
        if not cell.get('source'):
            continue
            
        cell_type = cell['cell_type']
        source = ''.join(cell['source'])
        
        if cell_type == 'markdown':
            # Process markdown content based on flags
            if skip_images:
                # Remove both markdown and HTML image tags
                source = re.sub(r'!\[.*?\]\(.*?\)', '', source)  # Remove markdown images
                source = re.sub(r'<img[^>]*>', '', source)       # Remove HTML images
            
            if skip_links:
                # Remove markdown links but keep the text
                source = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', source)  # Replace [text](url) with text
                # Remove HTML links but keep the text
                source = re.sub(r'<a[^>]*>([^<]*)</a>', r'\1', source)
            
            markdown_content.append(source + '\n\n')
            
        elif cell_type == 'code':
            # Add code fence with language
            markdown_content.append(f"```python\n{source}\n```\n")
            
            # Add output if present and not empty
            if cell.get('outputs'):
                markdown_content.append("\nOutput:\n")
                for output in cell['outputs']:
                    if 'text' in output:
                        markdown_content.append("```\n" + ''.join(output['text']) + "\n```\n")
                    elif 'data' in output and not skip_images:
                        # Handle text output
                        if 'text/plain' in output['data']:
                            text = ''.join(output['data']['text/plain'])
                            markdown_content.append("```\n" + text + "\n```\n")
                        # Skip image outputs if skip_images is True
                        # Otherwise, we'll just ignore them by default
            markdown_content.append('\n')
    
    # Write markdown file
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(markdown_content))
    
    return output_path

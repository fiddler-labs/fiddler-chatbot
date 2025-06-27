#!/usr/bin/env python3
"""
A simple script to convert Jupyter notebooks to Markdown files, with options to skip images.
Usage: python notebook_to_md.py notebook.ipynb [--skip-images] [--skip-links] [-o output_dir]
"""

import sys
import os
import json
from pathlib import Path
import argparse
import re

def convert_notebook(notebook_path: str, output_dir: str = None, skip_images: bool = False, 
                    skip_links: bool = False) -> str:
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
    
    return str(output_path)

def main():
    parser = argparse.ArgumentParser(description='Convert Jupyter notebooks to Markdown files')
    parser.add_argument('notebook', help='Notebook file to convert')
    parser.add_argument('-o', '--output-dir', help='Output directory for markdown files')
    parser.add_argument('--skip-images', action='store_true', 
                       help='Skip image tags in the markdown output')
    parser.add_argument('--skip-links', action='store_true',
                       help='Skip hyperlinks in the markdown output (keep link text)')
    args = parser.parse_args()
    
    try:
        output_file = convert_notebook(
            args.notebook,
            output_dir=args.output_dir,
            skip_images=args.skip_images,
            skip_links=args.skip_links
        )
        print(f"\nSuccessfully converted notebook to: {output_file}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()

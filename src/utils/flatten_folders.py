"""
Markdown File Flattening Utilities

This module provides utilities to flatten markdown files from nested directory structures
into a single destination directory using two different approaches:

1. Individual File Flattening: Each markdown file is copied individually with a flattened 
   filename that preserves the directory structure in the filename.
   
2. Concatenated File Flattening: Markdown files within each subdirectory are concatenated
   into single files, creating one combined file per directory branch.

Both approaches preserve the original file structure information in different ways.
"""

import os
import shutil
import logging
from typing import List
from pathlib import Path

logger = logging.getLogger(__name__)

def flatten_all_files_individually(
    source_dir: Path, 
    dest_dir: Path, 
    file_extension: str = '.md',
    ) -> List[str]:
    """
    Flatten markdown files by copying each file individually with flattened names.
    
    This approach creates one output file for each input file. The directory structure
    is preserved in the filename by replacing directory separators with hyphens.
    
    Example:
        docs/api/authentication.md -> api-authentication.md
        docs/guides/getting-started.md -> guides-getting-started.md
    
    Args:
        source_dir: Root directory containing the files to flatten
        dest_dir: Destination directory for flattened files
        file_extension: File extension to process (default: '.md')
        
    Returns:
        List of created filenames
        
    Raises:
        OSError: If source directory doesn't exist or destination cannot be created
    """
    if not os.path.exists(source_dir):
        raise OSError(f"Source directory does not exist: {source_dir}")
    
    # Ensure the destination directory exists
    os.makedirs(dest_dir, exist_ok=True)
    
    created_files = []
    
    # Walk through the directory tree
    for dirpath, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            # Process only files with the specified extension
            if filename.endswith(file_extension):
                # Get the relative path from the root directory
                rel_dir = os.path.relpath(dirpath, source_dir)
                
                # Skip if we're at the root directory
                if rel_dir == '.':
                    prefix = ''
                else:
                    # Replace directory separators with underscores (replace later with / for url)
                    prefix = rel_dir.replace(os.sep, '__')
                    prefix += '__'
                
                # Construct the new filename
                new_filename = f"{prefix}{filename}"
                
                # Define the full source and destination file paths
                src_file = os.path.join(dirpath, filename)
                dest_file = os.path.join(dest_dir, new_filename)
                
                # Copy the file to the destination directory
                shutil.copy2(src_file, dest_file)
                created_files.append(new_filename)
                logger.info(f"Created: {new_filename}")
    
    return created_files

def concatenate_files_in_leaf_folders(
    source_dir: Path, 
    dest_dir: Path, 
    file_extension: str = '.md',
    ) -> List[str]:
    """
    Flatten markdown files by concatenating files within each directory branch.
    
    This approach creates fewer output files by combining all files within each
    subdirectory (and its subdirectories) into a single concatenated file.
    Root-level files are copied individually.
    
    Example:
        docs/api/authentication.md + docs/api/authorization.md -> api_concat.md
        docs/guides/getting-started.md + docs/guides/advanced.md -> guides_concat.md
        docs/readme.md -> readme.md (root level, copied individually)
    
    Args:
        source_dir: Root directory containing the files to flatten
        dest_dir: Destination directory for flattened files
        file_extension: File extension to process (default: '.md')
        
    Returns:
        List of created filenames
        
    Raises:
        OSError: If source directory doesn't exist or destination cannot be created
    """

    def _get_all_files_with_extension(directory: Path, extension: str = '.md') -> List[str]:
        """
        Get all files with a specific extension within a directory and its subdirectories.
        Args:
            directory: Directory to search
            extension: File extension to look for
        Returns: List of file paths
        """
        files = []
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith(extension):
                    files.append(os.path.join(dirpath, filename))
        return files


    if not os.path.exists(source_dir):
        raise OSError(f"Source directory does not exist: {source_dir}")
    
    # Ensure the destination directory exists
    os.makedirs(dest_dir, exist_ok=True)
    
    created_files = []
    processed_dirs = set()
    
    # First, process files at the root level
    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)
        if os.path.isfile(item_path) and item.endswith(file_extension):
            # Copy the root-level file to the destination directory
            dest_file = os.path.join(dest_dir, item)
            shutil.copy2(item_path, dest_file)
            created_files.append(item)
            
            logger.info(f"Copied root file: {item}")
    
    # Now, process each subdirectory
    for dirpath, dirnames, filenames in os.walk(source_dir):
        # Skip the root directory itself
        if dirpath == source_dir:
            continue
            
        # Get the relative path of the directory from the root directory
        rel_dir = os.path.relpath(dirpath, source_dir)
        
        # Avoid processing the same directory multiple times
        if rel_dir in processed_dirs:
            continue
            
        # Get all files with the specified extension within this directory and its subdirectories
        files = _get_all_files_with_extension(Path(dirpath), file_extension)
        
        # If there are files, concatenate them
        if files:
            # Use the relative directory path to name the concatenated file
            # Replace directory separators with hyphens
            concatenated_filename = rel_dir.replace(os.sep, '-') + '_concat' + file_extension
            concatenated_file_path = os.path.join(dest_dir, concatenated_filename)
            
            # Open the concatenated file for writing
            with open(concatenated_file_path, 'w', encoding='utf-8') as outfile:
                for file_path in files:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            # Write a header to indicate the original file path
                            relative_file_path = os.path.relpath(file_path, dirpath)
                            outfile.write(f"# {relative_file_path}\n\n")
                            
                            # Write the content of the file
                            outfile.write(infile.read())
                            
                            # Add a separator between files
                            outfile.write("\n\n---\n\n")
                    except UnicodeDecodeError:
                        logger.warning(f"Warning: Could not read file {file_path} (encoding issue)")
                        continue
            
            created_files.append(concatenated_filename)
            logger.info(f"Created concatenated file: {concatenated_filename} ({len(files)} files)")
            
            # Mark this directory as processed
            processed_dirs.add(rel_dir)
    
    return created_files

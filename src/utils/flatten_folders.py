import os
import shutil

# Set the root directory containing your markdown files
root_dir = '/Users/saifraja/Github/Docs Export Experiments/v25.0/docs'

# Set the destination directory where you want to store the flattened files
dest_dir = '/Users/saifraja/Github/Docs Export Experiments/v25.0/docs_flattened'

# Ensure the destination directory exists
os.makedirs(dest_dir, exist_ok=True)

# Walk through the directory tree
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        # Process only markdown files
        if filename.endswith('.md'):
            # Get the relative path from the root directory
            rel_dir = os.path.relpath(dirpath, root_dir)
            # Skip if we're at the root directory
            if rel_dir == '.':
                prefix = ''
            else:
                # Replace directory separators with hyphens
                prefix = rel_dir.replace(os.sep, '-')
                prefix += '-'
            # Construct the new filename
            new_filename = f"{prefix}{filename}"
            # Define the full source and destination file paths
            src_file = os.path.join(dirpath, filename)
            dest_file = os.path.join(dest_dir, new_filename)
            # Copy the file to the destination directory
            shutil.copy2(src_file, dest_file)
            print(new_filename)



# # Function to get all markdown files within a directory and its subdirectories
# def get_all_md_files(directory):
#     md_files = []
#     for dirpath, dirnames, filenames in os.walk(directory):
#         for filename in filenames:
#             if filename.endswith('.md'):
#                 md_files.append(os.path.join(dirpath, filename))
#     return md_files

# # List to keep track of directories already processed
# processed_dirs = set()

# # First, process markdown files at the root level
# for item in os.listdir(root_dir):
#     item_path = os.path.join(root_dir, item)
#     if os.path.isfile(item_path) and item.endswith('.md'):
#         # Copy the root-level markdown file to the destination directory
#         dest_file = os.path.join(dest_dir, item)
#         shutil.copy2(item_path, dest_file)

# # Now, process each subdirectory
# for dirpath, dirnames, filenames in os.walk(root_dir):
#     # Skip the root directory itself
#     if dirpath == root_dir:
#         continue
#     # Get the relative path of the directory from the root directory
#     rel_dir = os.path.relpath(dirpath, root_dir)
#     # Avoid processing the same directory multiple times
#     if rel_dir in processed_dirs:
#         continue
#     # Get all markdown files within this directory and its subdirectories
#     md_files = get_all_md_files(dirpath)
#     # If there are markdown files, concatenate them
#     if md_files:
#         # Use the relative directory path to name the concatenated file
#         # Replace directory separators with hyphens
#         concatenated_filename = rel_dir.replace(os.sep, '-') + '_concat.md'
#         concatenated_file_path = os.path.join(dest_dir, concatenated_filename)
#         # Open the concatenated file for writing
#         with open(concatenated_file_path, 'w', encoding='utf-8') as outfile:
#             for md_file in md_files:
#                 with open(md_file, 'r', encoding='utf-8') as infile:
#                     # Optionally write a header to indicate the original file path
#                     relative_md_file = os.path.relpath(md_file, dirpath)
#                     outfile.write(f"# {relative_md_file}\n\n")
#                     # Write the content of the markdown file
#                     outfile.write(infile.read())
#                     # Optionally add a separator between files
#                     outfile.write("\n\n---\n\n")
#         # Mark this directory as processed
#         processed_dirs.add(rel_dir)
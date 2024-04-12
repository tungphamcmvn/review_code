from read_files_in_directory import read_files_in_directory
from export_file_git_diff import export_file_git_diff
     
# Specify the input directory
input_directory = input("Enter additional directory path: ").strip()
# Change the output file name here
output_file = 'output/codebase.txt'
# Configure allowed extensions
allowed_extensions = ['.tsx', '.ts', '.js', '.scss', '.css', '.md', 'Dockerfile']  # Add more extensions you want to include here
# Configure ignored directories
ignored_directories = ['node_modules', '.next', '.vscode', '.git']  # Add directory names you want to ignore here

read_files_in_directory(output_file, input_directory, allowed_extensions, ignored_directories)
print("Reading and saving files to "+output_file+" file completed.")

export_file_git_diff(input_directory)

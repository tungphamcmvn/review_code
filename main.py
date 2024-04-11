
import subprocess
import os

def read_files_in_directory(output_file, input_directory, allowed_extensions=[], ignored_directories=[]):
    print("Input directory:", input_directory)

    with open(output_file, 'w') as out_file:
        for root, dirs, files in os.walk(input_directory):
            # Filter out ignored directories
            dirs[:] = [d for d in dirs if d not in ignored_directories]

            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_ext = os.path.splitext(file_name)[1]
                if file_ext.lower() not in allowed_extensions:
                    # print(f"Ignoring file: {file_path}")
                    continue
                
                with open(file_path, 'r') as in_file:
                    rel_file_path = os.path.relpath(file_path, input_directory)
                    out_file.write(f"{rel_file_path}```{file_ext.lower()[1:]}\n")
                    out_file.write("".join(["\t" + line for line in in_file.readlines()]))
                    out_file.write('\n```\n\n')


def export_file_git_diff(folder_name):
    # Set the paths
    root_folder = os.getcwd()
    repo_path = os.path.join(root_folder, folder_name)
    log_file = os.path.join(root_folder, "git-pull_request.txt")
    
    os.chdir(repo_path)
    subprocess.run(['gh', 'pr', 'list'], text=True, check=True)

    selected_pr = int(input("Select a number to view pull request details: "))

    git_diff_file = os.path.join(root_folder, "git-diff.txt")
    with open(git_diff_file, "w") as f:
        os.chdir(repo_path)
        subprocess.run(['gh', 'pr', 'view', str(selected_pr)], stdout=f, text=True, check=True)
        subprocess.run(['echo', '\n'], stdout=f, text=True, check=True)
        subprocess.run(['gh', 'pr', 'diff', str(selected_pr)], stdout=f, text=True, check=True)
    print("Successfully saved the file to git-diff.txt.")
        
    
    
    
# Specify the input directory
input_directory = input("Enter additional directory path: ").strip()
# Change the output file name here
output_file = input_directory+'_output.txt'
# Configure allowed extensions
allowed_extensions = ['.tsx', '.ts', '.js', '.scss', '.css', '.md', 'Dockerfile']  # Add more extensions you want to include here
# Configure ignored directories
ignored_directories = ['node_modules', '.next', '.vscode', '.git']  # Add directory names you want to ignore here

read_files_in_directory(output_file, input_directory, allowed_extensions, ignored_directories)
print("Reading and saving files to "+output_file+" file completed.")

export_file_git_diff(input_directory)


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
                    out_file.write(f"{input_directory}/{rel_file_path}```{file_ext.lower()[1:]}\n")
                    out_file.write("".join(["\t" + line for line in in_file.readlines()]))
                    out_file.write('\n```\n\n')


def export_file_git_diff(folder_name):
    # Set the paths
    root_folder = os.getcwd()
    repo_path = os.path.join(root_folder, folder_name)
    log_file = os.path.join(root_folder, "git-log.txt")

    # Run git log command and pipe output to log file
    with open(log_file, "w") as f:
        os.chdir(repo_path)
        subprocess.run(['git', 'log', '--all'], stdout=f, text=True, check=True)

    print("Git log exported to git-log.txt")

    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            log_content = file.read()

        # Split commits into a list
        commits = log_content.strip().split("commit ")

        # Initialize a list to store non-merge commits
        non_merge_commits = []

        # Check each commit for the presence of "Merge:" line, if not present, it's a non-merge commit
        for commit in commits[1:]:
            if "Merge:" not in commit:
                non_merge_commits.append(commit)

        # Print out the first 10 non-merge commits
        print("Non-merge commits:")
        for i, commit in enumerate(non_merge_commits[:10], start=1):
            print(f"{i}. {commit}")

        selected_commit = int(input("Select a number from 1 to 10 to view commit details: "))

        # Output a file containing git diff information for the selected commit
        if selected_commit in range(1, min(11, len(non_merge_commits) + 1)):
            print(f"Commit {selected_commit}: {non_merge_commits[selected_commit - 1]}")
            git_diff_file = os.path.join(root_folder, "git-diff.txt")
            with open(git_diff_file, "w") as f:
                os.chdir(repo_path)
                selected_commit_hash = non_merge_commits[selected_commit - 1].splitlines()[0]
                subprocess.run(['git', 'show', selected_commit_hash], stdout=f, text=True, check=True)
            print("Successfully saved the file to git-diff.txt.")
        else:
            print("Invalid number. Please select again from 1 to 10.")
    else:
        print("Log file 'git-log.txt' does not exist.")
    
    
# Specify the input directory
input_directory = input("Enter additional directory path: ").strip()
# Change the output file name here
output_file = input_directory+'_output.txt'
# Configure allowed extensions
allowed_extensions = ['.tsx', '.ts', '.js', '.scss', '.css']  # Add more extensions you want to include here
# Configure ignored directories
ignored_directories = ['node_modules', '.next', '.vscode', '.git']  # Add directory names you want to ignore here

read_files_in_directory(output_file, input_directory, allowed_extensions, ignored_directories)
print("Reading and saving files to "+output_file+" file completed.")

export_file_git_diff(input_directory)

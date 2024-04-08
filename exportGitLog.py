import subprocess
import os

# Set the paths
folder_name = input("Enter the path to the directory: ")
repo_path = os.path.join(os.getcwd(), folder_name)
log_file = os.path.join(os.getcwd(), "git-log.txt")

# Run git log command and pipe output to log file
# git_log_cmd = ["git", "log", j2c_path]
with open(log_file, "w") as f:
    os.chdir(repo_path)
    subprocess.run(['git', 'log'],stdout=f, text=True, check=True)
        

print("Git log exported to git-log.txt")


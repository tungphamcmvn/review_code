import subprocess
import os

def export_file_git_diff(folder_name):
    # Set the paths
    root_folder = os.getcwd()
    repo_path = os.path.join(root_folder, folder_name)
    
    state_pr = input("Select a state {open|closed|merged|all}: ")
    
    if (state_pr == 'open'):
        os.chdir(repo_path)
        subprocess.run(['gh', 'pr', 'list'], text=True, check=True)
    if (state_pr == 'closed'):
        os.chdir(repo_path)
        subprocess.run(['gh', 'pr', 'list', '-s', state_pr], text=True, check=True)
    if (state_pr == 'merged'):
        os.chdir(repo_path)
        subprocess.run(['gh', 'pr', 'list', '-s', state_pr], text=True, check=True)
    if (state_pr == 'all'):
        os.chdir(repo_path)
        subprocess.run(['gh', 'pr', 'list', '-s', state_pr], text=True, check=True)
    
    
    selected_pr = int(input("Select a number to view pull request details: "))

    git_diff_file = os.path.join(root_folder, "output/diff.txt")
    with open(git_diff_file, "w") as f:
        os.chdir(repo_path)
        subprocess.run(['gh', 'pr', 'view', str(selected_pr)], stdout=f, text=True, check=True)
        subprocess.run(['echo', '\n'], stdout=f, text=True, check=True)
        subprocess.run(['gh', 'pr', 'diff', str(selected_pr)], stdout=f, text=True, check=True)
    print("Successfully saved the file to diff.txt.")
        
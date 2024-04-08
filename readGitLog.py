import subprocess
import os

def export_file_git_diff(folder_name):
  # Set the paths
  root_folder = os.getcwd()
  repo_path = os.path.join(root_folder, folder_name)
  log_file = os.path.join(root_folder, "git-log.txt")

  # Run git log command and pipe output to log file
  # git_log_cmd = ["git", "log", j2c_path]
  with open(log_file, "w") as f:
      os.chdir(repo_path)
      subprocess.run(['git', 'log'],stdout=f, text=True, check=True)
          

  print("Git log exported to git-log.txt")

  if os.path.exists(log_file):
    # Đọc nội dung từ tệp log
    with open(log_file, "r") as file:
        log_content = file.read()

    # Tách các commit thành một danh sách
    commits = log_content.strip().split("commit ")

    # In ra 5 commit đầu tiên
    print("Các commit gần đây:")
    for i, commit in enumerate(commits[1:6], start=1):
        print(f"{i}. {commit.splitlines()[0]}")

    # Yêu cầu người dùng chọn một commit
    selected_commit = int(input("Chọn một số từ 1 đến 5 để xem chi tiết commit: "))

    # In ra commit tương ứng
    if selected_commit in range(1, 6):
        print(f"Commit {selected_commit}: {commits[selected_commit].splitlines()[0]}")
        git_diff_file = os.path.join(root_folder, "git-diff.txt")
        with open(git_diff_file, "w") as f:
          os.chdir(repo_path)
          subprocess.run(['git', 'diff', commits[selected_commit].splitlines()[0]],stdout=f, text=True, check=True)
    else:
        print("Số không hợp lệ. Vui lòng chọn lại từ 1 đến 5.")
  else:
    print("Log file 'git-log.txt' does not exist.")
    
folder_name = input("Enter the path to the directory: ")
export_file_git_diff(folder_name)
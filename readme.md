# Backup S3 - Documentation

## ⚡ Backing Up Changed Folders to AWS S3 Using `s3cmd` (Tracking Changes in Folder Size)

This solution focuses on using `s3cmd` to back up folders to AWS S3, only if their size has changed by 1KB or more since the last backup. 

**Assumptions:**

* You have `s3cmd` installed and configured on your server. For installation and configuration, refer to the official documentation: [http://s3tools.org/s3cmd](http://s3tools.org/s3cmd)
* You have an S3 bucket already created.

**Solution:**

We'll use a bash script combined with a simple file-based tracking system to store and compare folder sizes between backups. 

**Script (backup.sh):**

```bash
#!/bin/bash

# Set the directory containing the folders to backup
BACKUP_DIR="/path/to/your/folders"

# Set your S3 bucket name
S3_BUCKET="your-s3-bucket-name"

# Set the file to store folder size history
SIZE_HISTORY_FILE="folder_sizes.txt"

# Function to get the previous folder size from the history file
get_previous_size() {
  local folder="$1"
  grep "^$folder " "$SIZE_HISTORY_FILE" | awk '{print $2}'
}

# Function to update the folder size in the history file
update_size_history() {
  local folder="$1"
  local size="$2"
  sed -i "/^$folder /c\\$folder $size" "$SIZE_HISTORY_FILE" || echo "$folder $size" >> "$SIZE_HISTORY_FILE"
}

# Iterate through each directory within the BACKUP_DIR
for folder in "$BACKUP_DIR"/*; do

  # Calculate current folder size in kilobytes
  current_size=$(du -sk "$folder" | awk '{print $1}')

  # Get the previous folder size from the history file
  previous_size=$(get_previous_size "$folder")

  # Calculate the size difference 
  size_difference=$(( current_size - previous_size ))

  # Check if the size difference is >= 1KB or if it's the first time backing up this folder
  if (( size_difference >= 1 )) || [[ -z "$previous_size" ]]; then
    echo "Uploading $folder to s3://$S3_BUCKET/ (size change: ${size_difference}KB)"
    s3cmd put --recursive "$folder" s3://$S3_BUCKET/
    update_size_history "$folder" "$current_size"
  else
    echo "Skipping $folder (size change: ${size_difference}KB) - less than 1KB change"
  fi
done
```

**Explanation:**

1. **`BACKUP_DIR`, `S3_BUCKET`, `SIZE_HISTORY_FILE`**: Set these variables according to your environment.
2. **`get_previous_size()`**: This function retrieves the previously recorded size of a folder from the `SIZE_HISTORY_FILE`.
3. **`update_size_history()`**: This function updates the `SIZE_HISTORY_FILE` with the new size of a folder after a successful backup.
4. **Main Loop**: 
   - The script iterates through each folder in your `BACKUP_DIR`.
   - It calculates the current folder size and retrieves the previous size from the `SIZE_HISTORY_FILE`.
   - If the size difference is greater than or equal to 1KB, or if there's no previous record for the folder, it backs up the folder and updates the `SIZE_HISTORY_FILE`.

**Running the script:**

1. Save the script to a file (e.g., `backup.sh`).
2. Make the script executable: `chmod +x backup.sh`
3. Run the script with `cron`

**Important Notes:**

* The first time you run the script, all folders will be backed up as there's no previous size history.
* This script uses a simple file-based approach to track folder sizes. For more robust solutions, consider using a database or other dedicated tools.
* You can customize the script further by adding error handling, logging, scheduling, or more sophisticated change detection mechanisms.


## 👨‍💻 Setting up Daily Backups with `cron`

We can schedule the backup script to run daily using `cron`, a time-based job scheduler available on Unix-like systems.

**Steps:**

1. **Open your crontab:**
   - Open a terminal.
   - Type `crontab -e` and press Enter. This will open your crontab file for editing. If this is your first time using `crontab`, it might ask you to choose an editor. Choose whichever you're comfortable with (e.g., nano).

2. **Add the backup schedule:**
   - At the end of your crontab file, add the following line:

     ```
     0 0 * * * /path/to/your/backup.sh
     ```

   - Replace `/path/to/your/backup.sh` with the actual path to the backup script you created earlier.

3. **Save and exit:**
   - If you are using nano, press `Ctrl + X`, then `Y` to save changes, and finally `Enter` to exit.

**Explanation of the crontab entry:**

- `0 0 * * *`: This part defines the schedule. 
  - The first `0` represents the minute (0 for the 0th minute).
  - The second `0` represents the hour (0 for midnight).
  - The `*` symbols mean "every" - every day, every month, every day of the week.
- `/path/to/your/backup.sh`: This is the command that will be executed according to the schedule.

**Verification:**

- You can verify that the cron job is set up correctly by running `crontab -l`. This will list all your scheduled cron jobs.

**Additional Considerations:**

- **Error Handling:** Consider adding error handling to your script, such as redirecting error messages to a log file or sending email notifications.
- **Log Files:** It's good practice to log the output of your backup script to a file. You can modify the script to redirect its output to a log file using `>> /path/to/your/backup.log`.
- **Testing:** After setting up the cron job, it's important to test it manually at least once to ensure it runs as expected. 

By following these steps, your backup script will run automatically every day at midnight, backing up only the folders that have changed by 1KB or more since the last backup.
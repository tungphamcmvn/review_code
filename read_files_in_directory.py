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

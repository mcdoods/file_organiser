import os
import shutil
import time
from datetime import datetime

file_types = {
    "Images": [".png", ".jpg", ".jpeg", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".odt"],
    "Videos": [".mp4", ".mov", ".mkv"],
    "Code": [".py", ".c", ".cpp", ".java"],
    "Archives": [".zip", ".rar", ".7z"],
    "Music": [".mp3", ".wav"],
    "Data": [".csv", ".xlsx"]
    }

last_log = ""

def main_menu():
    while True:
        print("""
        ** File Organiser **

        A. Organise files with path
        B. Dry run (show what would move)
        C. Print directory contents
        D. Undo last organise
        E. View summary report
        F. Clean empty folders
        G. Log history

        H. Exit
        """)

        choice = input("Enter choice: ").strip().upper()

        if choice in "ABCF":
            folder_path = input("Enter folder path: ").strip()
            folder_path = os.path.expanduser(folder_path)
            folder_path = os.path.abspath(folder_path)
            print(" * Locating", folder_path)
            if not os.path.exists(folder_path):
                print(" * Folder path doesn't exist.")

        match choice:
            case "A":
                organise_files(folder_path, False)
            case "B":
                organise_files(folder_path, True)
            case "C":
                print_directory(folder_path)
            case "D":
                undo_last_organise()
            case "E":
                print(last_log)
            case "F":
                clean_empty_folders(folder_path)
            case "G":
                open_history()
            case "H":
                exit()
            case _:
                print(" * Invalid choice.")
                exit()

def organise_files(folder_path, dry_run):
    current_log = ""
    global last_log
    start = time.time()
    for file_name in os.listdir(folder_path):
        time.sleep(0.2)
        file_path = os.path.join(folder_path, file_name)
    
        if os.path.isdir(file_path):
            if dry_run:
                print("Skipping folder:", file_name)
            else:
                current_log += "\nSkipped folder " + file_name
            continue
    
        moved = False
        for folder_name, extensions in file_types.items():
            if any(file_name.lower().endswith(ext) for ext in extensions):
                target_folder = os.path.join(folder_path, folder_name)
                if not dry_run:
                    os.makedirs(target_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(target_folder, file_name))
                    current_log += "\n" + file_name + " -> " + target_folder
                else:
                    print(file_name, "->", target_folder)
                moved = True
                break
    

        if not moved:
            other_folder = os.path.join(folder_path, "Other")
            if not dry_run:
                os.makedirs(other_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(other_folder, file_name))
                current_log += "\n" + file_name + " -> " + other_folder
            else:
                print(file_name, "->", other_folder)
    
    print(" * Logging actions.")
    end = time.time()
    current_log += f"\n * Files organised in {end - start:.2f} seconds."
    append_history(current_log)
    last_log = current_log
    current_log = ""
    
    time.sleep(0.5)
    print(" * Files have been organised.")
    time.sleep(3)

def print_directory(folder_path):
    for root, dirs, files in os.walk(folder_path):
        level = root.replace(folder_path, "").count(os.sep)
        indent = " " * 4 * level
        print(indent + os.path.basename(root) or folder_path + "/")

        sub_indent = " " * 4 * (level + 1)
        for f in files:
            print(sub_indent, f)
        
    time.sleep(3)

def undo_last_organise():
    if last_log == "":
        print("You haven't made any changes this session.")
        return
    
    for line in last_log.splitlines():
        if "->" in line:
            parts = line.split("->")
            moved_file = parts[0].strip()
            destination = parts[1].strip()
            parent = os.path.dirname(destination)
            try:
                shutil.move(os.path.join(destination, moved_file), parent)
            except Exception as e:
                print("Skipped " + moved_file)
                
    print(" * Reversed last change. Files moved back to original directory.")
            
    append_history("\n\n ** Undo last file organise.\n")
    time.sleep(1)
    clean_empty_folders(parent)

def clean_empty_folders(folder_path):
    global last_log
    clean_log = ""
    folder_path = os.path.abspath(os.path.expanduser(folder_path))
    print(" * Searching for empty folders.")

    removed = 0
    for root, dirs, files in os.walk(folder_path, topdown=False):
        if root.startswith(os.path.join(folder_path, ".")):
            clean_log += "\nSkipped system/hidden folder."
            continue

        if not dirs and not files:
            try:
                os.rmdir(root)
                clean_log += "\nDeleted " + root
                removed += 1
            except Exception as e:
                clean_log += "\nSkipped " + root + "due to error."

    print("\n *", removed, "empty folders deleted.")
    clean_log += f" * {removed} empty folders deleted."
    append_history(clean_log)
    last_log = clean_log
    clean_log = ""
    
    time.sleep(3)
    
def create_history():
    history_path = os.path.join(os.getcwd(), "file_organiser_history.txt")
    if not os.path.exists(history_path):
        with open(history_path, "w") as f:
            f.write("=== File Organiser History ===\n\n")
    return history_path

def append_history(log_data):
    history_path = create_history()
    with open(history_path, "a") as f:
        f.write("-----\n")
        f.write(" ** " + datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        f.write("\n")
        f.write(log_data)
        f.write("\n\n")

def open_history():
    history_path = create_history()
    with open(history_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            print(line.strip())
            

main_menu()
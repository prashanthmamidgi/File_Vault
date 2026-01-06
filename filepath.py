import os

USER_FILES = "user_files.txt"

def save_user_file(username, path):
    with open(USER_FILES, "a") as f:
        f.write(f"{username}|{path}\n")

def get_user_files(username):
    files = []
    if os.path.exists(USER_FILES):
        with open(USER_FILES) as f:
            for line in f:
                u, p = line.strip().split("|")
                if u == username:
                    files.append(p)
    return files

import os
from Encrypt_Decrypt import hash_password

USER_FILE = "users.txt"

def load_users():
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE) as f:
            for line in f:
                u, p = line.strip().split("|")
                users[u] = p
    return users

def register():
    users = load_users()
    u = input("Username: ")
    p = input("Password: ")

    if u in users:
        print("Username exists")
        return

    with open(USER_FILE, "a") as f:
        f.write(f"{u}|{hash_password(p)}\n")

def login():
    users = load_users()
    u = input("Username: ")
    p = input("Password: ")

    if users.get(u) == hash_password(p):
        print("Login successful")
        return u

    print("Invalid credentials")
    return None

from Encrypt_Decrypt import encrypt_file, decrypt_file
from filepath import save_user_file, get_user_files

def user_menu(username):
    unlocked_files = {}  
    while True:
        print("1. Encrypt  2. Decrypt  3. Logout")
        ch = input()

        if ch == "1":
            path = input("Path: ")
            encrypt_file(path)
            save_user_file(username, path)
            print("File encrypted")

        elif ch == "2":
            files = get_user_files(username)

            if not files:
                print("No encrypted files found for this user")
                continue

            for i, f in enumerate(files):
                print(f"{i+1}. {f}")

            idx = int(input("Select file: ")) - 1

            if 0 <= idx < len(files):
                decrypt_file(files[idx])
                unlocked_files[files[idx]] = "decrypted"
                print("File decrypted")
            else:
                print("Invalid selection")

        elif ch == "3":
            for file, state in unlocked_files.items():
                if state == "decrypted":
                    encrypt_file(file)
                    print(f"Re-encrypted: {file}")

            print("Logged out")
            break

from users import register, login
from menu import user_menu

def run():
    while True:
        print("1. Register  2. Login  3. Exit")
        ch = input()

        if ch == "1":
            register()
        elif ch == "2":
            user = login()
            if user:
                user_menu(user)
        elif ch == "3":
            break

if __name__ == "__main__":
    run()

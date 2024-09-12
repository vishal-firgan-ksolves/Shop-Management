import bcrypt

from database_conn.db_connection import DBConnection
from user import User


def authenticate_admin():

    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    if User.authenticate_user(username, password):
        if User.authorize_user(username, 'admin'):
            print("Admin authenticated successfully.")
            return username
        else:
            print("User does not have admin role.")
            return None
    else:
        print("Authentication failed.")
        return None


def menu():
    print("\nMenu:")
    print("1. Create user")
    print("2. Update user")
    print("3. Delete user")
    print("4. Exit")

    choice = input("Enter your choice (1/2/3/4): ")
    return choice


def create_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role ( emp,admin): ")
    User.create_user(username, password, role)
    print("User Added Successfully")


def update_user():
    userid = input("Enter user ID to update: ")
    username = input("Enter new username (leave blank to keep current): ")
    password = input("Enter new password (leave blank to keep current): ")
    role = input("Enter new role (leave blank to keep current): ")
    User.update_user(userid, username if username else None, password if password else None, role if role else None)
    print("User updated successfully.")


def delete_user():
    userid = input("Enter user ID to delete: ")
    User.delete_user(userid)
    print("User deleted successfully.")


def main():
    admin_user = authenticate_admin()
    if not admin_user:
        return

    # Main loop
    while True:
        choice = menu()

        if choice == '1':
            create_user()
        elif choice == '2':
            update_user()
        elif choice == '3':
            delete_user()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
    DBConnection.close()

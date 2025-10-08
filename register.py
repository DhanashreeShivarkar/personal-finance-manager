import sqlite3
import bcrypt

def register_user(username, password):
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Use context manager for automatic commit & close
    try:
        with sqlite3.connect("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            print(f"User '{username}' registered successfully!")
    except sqlite3.IntegrityError:
        print(f"Error: Username '{username}' already exists!")


if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")
    register_user(username, password)

import sqlite3
import bcrypt

def register_user(username, password):
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Connect to database
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print(f"User '{username}' registered successfully! 🎉")
    except sqlite3.IntegrityError:
        print(f"Error: Username '{username}' already exists!")
    finally:
        conn.close()


if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")
    register_user(username, password)

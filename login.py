# login.py

import sqlite3
import bcrypt
from modules.database import create_connection

def login_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result:
        stored_password = result[0]
        # Verify password
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            print(f"Login successful! ✅ Welcome, {username}")
        else:
            print("Invalid username or password ❌")
    else:
        print("Invalid username or password ❌")
    
    conn.close()


if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")
    login_user(username, password)

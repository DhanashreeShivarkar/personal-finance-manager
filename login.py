# login.py

import sqlite3
import bcrypt
from datetime import datetime
from getpass import getpass


def login_user(username, password):
    # Use context manager for automatic commit & close
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

    if result:
        stored_password = result[0]
        # Verify password
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "UPDATE users SET last_login = ? WHERE username = ?",
                (last_login, username)
            )
            conn.commit()  # ensure the update is saved
            
    
            
            # Step 4: Fetch user_id
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            user_id = cursor.fetchone()[0]

            # Step 5: Return user_id so it can be used in main.py
            return user_id
        else:
            print("Invalid username or password ")
    else:
        print("Invalid username or password ")
    
    conn.close()
    
    return None

    

if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")
    login_user(username, password)
    user_id = login_user(username, password)
    if user_id:
        print(f"Your user_id is: {user_id}")

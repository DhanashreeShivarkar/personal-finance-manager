import sqlite3
import bcrypt
import re
from getpass import getpass
from datetime import datetime

def is_strong_password(password):
    """Check if the password is strong"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    return True, ""

def register_user(username, password):
    # Check password strength
    valid, msg = is_strong_password(password)
    if not valid:
        print(f"Error: {msg}")
        return
    
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Use context manager for automatic commit & close
    try:
        with sqlite3.connect("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)", (username, hashed_password, created_at))
            print(f"User '{username}' registered successfully at {created_at}!")
    except sqlite3.IntegrityError:
        print(f"Error: Username '{username}' already exists!")
        return True  


if __name__ == "__main__":
    from register import register_user, is_strong_password  # import function to check password strength
    
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    
    valid, msg = is_strong_password(password)
    if not valid:
        print(f"Error: {msg}")
    else:
        register_user(username, password)

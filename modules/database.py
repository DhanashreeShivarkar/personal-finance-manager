import sqlite3

def create_connection():
    return sqlite3.connect("users.db")

def create_table():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        # Step 1: Create table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL UNIQUE,
                            password BLOB NOT NULL,
                            created_at TEXT NOT NULL DEFAULT (datetime('now')),
                            last_login TEXT
                          )''')
    print("Database and users table created successfully!")

# Call create_table when this file is run directly
if __name__ == "__main__":
    create_table()

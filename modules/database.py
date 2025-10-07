import sqlite3

def create_connection():
    conn = sqlite3.connect("users.db")
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password BLOB NOT NULL
                      )''')
    conn.commit()
    conn.close()
    print("Database and users table created successfully!")

# Call create_table when this file is run directly
if __name__ == "__main__":
    create_table()

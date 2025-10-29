import sqlite3

def create_connection():
    return sqlite3.connect("users.db")

def create_tables():
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
        
        # Expenses table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)
        
        # Budgets table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            limit_amount REAL NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)
        
        # Incomes table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS incomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            source TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)
        conn.commit()
    


# Call create_table when this file is run directly
if __name__ == "__main__":
    create_tables()
    print("Database and users table created successfully!")

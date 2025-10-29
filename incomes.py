# incomes.py
import sqlite3
from datetime import datetime
from tabulate import tabulate

def add_income(user_id, source, amount, date=None):
    date = date or datetime.now().strftime("%Y-%m-%d")
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO incomes (user_id, source, amount, date)
            VALUES (?, ?, ?, ?)
        """, (user_id, source, amount, date))
        conn.commit()
    print(f"Income added for user {user_id} — {source}: ₹{amount:.2f} on {date}")

def view_incomes(user_id):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, source, amount, date FROM incomes WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()

    if rows:
        # format amount with ₹
        formatted = [(r[0], r[1], f"₹{r[2]:.2f}", r[3]) for r in rows]
        print(tabulate(formatted, headers=["ID", "Source", "Amount", "Date"], tablefmt="grid"))
    else:
        print("No incomes found.")

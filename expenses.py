import sqlite3
from datetime import datetime
from tabulate import tabulate

# 1. Add a new expense
def add_expense(user_id, category, amount, description):
    date = datetime.now().strftime("%Y-%m-%d")
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO expenses (user_id, category, amount, description, date)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, category, amount, description, date))
        conn.commit()
        print(f"Expense added successfully for user ID {user_id} on {date}.")

# 2. View all expenses for the logged-in user
def view_expenses(user_id):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, category, amount, description, date FROM expenses WHERE user_id = ?", (user_id,))
        expenses = cursor.fetchall()

    if expenses:
        print(tabulate(expenses, headers=["ID", "Category", "Amount", "Description", "Date"], tablefmt="grid"))
    else:
        print("No expenses found.")

# 3. Update an existing expense
def update_expense(expense_id, new_category, new_amount, new_description):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE expenses
            SET category = ?, amount = ?, description = ?
            WHERE id = ?
        """, (new_category, new_amount, new_description, expense_id))
        conn.commit()
        print(f"Expense ID {expense_id} updated successfully.")

# 4. Delete an expense
def delete_expense(expense_id):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        print(f"🗑️ Expense ID {expense_id} deleted successfully.")

import sqlite3
from datetime import datetime
from tabulate import tabulate

# Monthly Expense Report
def monthly_report(user_id, month=None, year=None):
    now = datetime.now()
    month = month or now.month
    year = year or now.year

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category, SUM(amount)
            FROM expenses
            WHERE user_id = ?
              AND strftime('%m', date) = printf('%02d', ?)
              AND strftime('%Y', date) = CAST(? AS TEXT)
            GROUP BY category
        """, (user_id, month, year))
        results = cursor.fetchall()

    if results:
        total_expenses = sum(row[1] for row in results)
        print("\n=== Monthly Expense Report ===")
        print(f"Month: {month}/{year}")
        print(tabulate(results, headers=["Category", "Total (₹)"], tablefmt="grid"))
        print(f"\nTotal Expenses: ₹{total_expenses:.2f}")
    else:
        print("No expenses found for this month.")


# Yearly Expense Report
def yearly_report(user_id, year=None):
    now = datetime.now()
    year = year or now.year

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT strftime('%m', date) AS month, SUM(amount)
            FROM expenses
            WHERE user_id = ? AND strftime('%Y', date) = CAST(? AS TEXT)
            GROUP BY month
        """, (user_id, year))
        results = cursor.fetchall()

    if results:
        total_expenses = sum(row[1] for row in results)
        print("\n=== Yearly Expense Report ===")
        print(f"Year: {year}")
        print(tabulate(results, headers=["Month", "Total (₹)"], tablefmt="grid"))
        print(f"\nTotal Yearly Expenses: ₹{total_expenses:.2f}")
    else:
        print("No expenses found for this year.")

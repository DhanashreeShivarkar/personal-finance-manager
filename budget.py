import sqlite3
from datetime import datetime
from tabulate import tabulate

# 1. Set or update a budget
def set_budget(user_id, category, limit_amount, month=None, year=None):
    now = datetime.now()
    month = month or now.month
    year = year or now.year

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()

        # Check if a budget for this category already exists
        cursor.execute("""
            SELECT id FROM budgets WHERE user_id = ? AND category = ? AND month = ? AND year = ?
        """, (user_id, category, month, year))
        result = cursor.fetchone()

        if result:
            # Update existing budget
            cursor.execute("""
                UPDATE budgets SET limit_amount = ? WHERE id = ?
            """, (limit_amount, result[0]))
            print(f"Updated budget for {category} to ₹{limit_amount:.2f}")
        else:
            # Insert new budget
            cursor.execute("""
                INSERT INTO budgets (user_id, category, limit_amount, month, year)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, category, limit_amount, month, year))
            print(f"Set budget for {category} to ₹{limit_amount:.2f} for {month}/{year}")

        conn.commit()


# 2. View budgets
def view_budgets(user_id):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category, limit_amount, month, year
            FROM budgets WHERE user_id = ?
        """, (user_id,))
        budgets = cursor.fetchall()

    if budgets:
        print(tabulate(budgets, headers=["Category", "Limit (₹)", "Month", "Year"], tablefmt="grid"))
    else:
        print("No budgets found.")


# 3. Check for budget warning
def check_budget_warnings(user_id):
    now = datetime.now()
    month = now.month
    year = now.year

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        # For each budget, compare with total spent in same category and month
        cursor.execute("""
            SELECT b.category, b.limit_amount, IFNULL(SUM(e.amount), 0)
            FROM budgets b
            LEFT JOIN expenses e
            ON b.category = e.category
               AND b.user_id = e.user_id
               AND strftime('%m', e.date) = printf('%02d', b.month)
               AND strftime('%Y', e.date) = CAST(b.year AS TEXT)
            WHERE b.user_id = ?
            GROUP BY b.category, b.limit_amount
        """, (user_id,))
        results = cursor.fetchall()

    for category, limit_amount, total_spent in results:
        if total_spent > limit_amount:
            print(f"⚠️ Warning: You have exceeded your budget for {category}! "
                  f"Spent ₹{total_spent:.2f} / ₹{limit_amount:.2f}")
        else:
            print(f"{category}: ₹{total_spent:.2f} / ₹{limit_amount:.2f} within budget.")

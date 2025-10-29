import sqlite3
from datetime import datetime
from tabulate import tabulate
import csv

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

# ----------------------
# Internal helper funcs
# ----------------------
def _total_expenses(user_id, month=None, year=None):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        if month and year:
            cursor.execute("""
                SELECT IFNULL(SUM(amount),0) FROM expenses
                WHERE user_id = ?
                  AND strftime('%m', date) = printf('%02d', ?)
                  AND strftime('%Y', date) = ?
            """, (user_id, month, str(year)))
        else:
            cursor.execute("SELECT IFNULL(SUM(amount),0) FROM expenses WHERE user_id = ?", (user_id,))
        return float(cursor.fetchone()[0] or 0.0)

def _total_incomes(user_id, month=None, year=None):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        if month and year:
            cursor.execute("""
                SELECT IFNULL(SUM(amount),0) FROM incomes
                WHERE user_id = ?
                  AND strftime('%m', date) = printf('%02d', ?)
                  AND strftime('%Y', date) = ?
            """, (user_id, month, str(year)))
        else:
            cursor.execute("SELECT IFNULL(SUM(amount),0) FROM incomes WHERE user_id = ?", (user_id,))
        return float(cursor.fetchone()[0] or 0.0)

# ----------------------
# Public report funcs
# ----------------------
def monthly_financial_report(user_id, month=None, year=None):
    """Prints and returns monthly totals: income, expenses, savings. Also shows category breakdown for expenses."""
    now = datetime.now()
    month = month or now.month
    year = year or now.year

    total_exp = _total_expenses(user_id, month, year)
    total_inc = _total_incomes(user_id, month, year)
    savings = total_inc - total_exp

    print(f"\n=== Monthly Financial Report ({month}/{year}) ===")
    print(tabulate(
        [["Total Income", f"₹{total_inc:.2f}"],
         ["Total Expenses", f"₹{total_exp:.2f}"],
         ["Net Savings", f"₹{savings:.2f}"]],
        headers=["Metric", "Amount"],
        tablefmt="grid"
    ))

    # Category-wise expense breakdown
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category, IFNULL(SUM(amount),0)
            FROM expenses
            WHERE user_id = ? AND strftime('%m', date)=printf('%02d', ?) AND strftime('%Y', date)=?
            GROUP BY category
        """, (user_id, month, str(year)))
        cat_rows = cursor.fetchall()

    if cat_rows:
        print("\nCategory-wise expenses:")
        print(tabulate([(c, f"₹{s:.2f}") for c, s in cat_rows], headers=["Category","Total"], tablefmt="grid"))
    else:
        print("\nNo category-wise expenses for this month.")

    # Return numeric metrics for programmatic use
    return {"income": total_inc, "expenses": total_exp, "savings": savings, "month": month, "year": year}

def yearly_financial_report(user_id, year=None):
    """Prints and returns yearly totals: income, expenses, savings (and monthly expense totals)."""
    now = datetime.now()
    year = year or now.year

    total_exp = _total_expenses(user_id, None, year)
    total_inc = _total_incomes(user_id, None, year)
    savings = total_inc - total_exp

    print(f"\n=== Yearly Financial Report ({year}) ===")
    print(tabulate(
        [["Total Income", f"₹{total_inc:.2f}"],
         ["Total Expenses", f"₹{total_exp:.2f}"],
         ["Net Savings", f"₹{savings:.2f}"]],
        headers=["Metric", "Amount"],
        tablefmt="grid"
    ))

    # monthly totals
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT strftime('%m', date) AS month, IFNULL(SUM(amount),0)
            FROM expenses
            WHERE user_id = ? AND strftime('%Y', date) = ?
            GROUP BY month
            ORDER BY month
        """, (user_id, str(year)))
        rows = cursor.fetchall()

    if rows:
        print("\nMonthly expense totals:")
        print(tabulate([(int(m), f"₹{s:.2f}") for m, s in rows], headers=["Month","Total"], tablefmt="grid"))
    else:
        print("\nNo expenses recorded for this year.")

    return {"income": total_inc, "expenses": total_exp, "savings": savings, "year": year}

# ----------------------
# Insights & export
# ----------------------
def savings_insight(user_id, month=None, year=None):
    """Print a short insight based on monthly savings."""
    res = monthly_financial_report(user_id, month, year)
    savings = res["savings"]
    if savings < 0:
        print(f"\n Alert: You are running a deficit this month: ₹{savings:.2f}. Consider reducing expenses or increasing income.")
    elif savings == 0:
        print("\n You're breaking even this month.")
    else:
        print(f"\n Good job — you saved ₹{savings:.2f} this month.")
    return res

def export_monthly_report_csv(user_id, month=None, year=None, filename=None):
    """Export monthly numeric summary and category rows to CSV. Returns filename."""
    res = monthly_financial_report(user_id, month, year)  # prints as well
    month = res["month"]
    year = res["year"]
    filename = filename or f"monthly_report_{user_id}_{month}_{year}.csv"

    # gather category breakdown
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category, IFNULL(SUM(amount),0)
            FROM expenses
            WHERE user_id = ? AND strftime('%m', date)=printf('%02d', ?) AND strftime('%Y', date)=?
            GROUP BY category
        """, (user_id, month, str(year)))
        cat_rows = cursor.fetchall()

    # write CSV: first metrics, then blank line, then category rows
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Amount"])
        writer.writerow(["Total Income", f"{res['income']:.2f}"])
        writer.writerow(["Total Expenses", f"{res['expenses']:.2f}"])
        writer.writerow(["Net Savings", f"{res['savings']:.2f}"])
        writer.writerow([])
        writer.writerow(["Category", "Total"])
        for c, s in cat_rows:
            writer.writerow([c, f"{s:.2f}"])

    print(f"\n CSV exported to {filename}")
    return filename
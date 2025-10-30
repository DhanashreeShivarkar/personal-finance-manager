# main.py

from register import register_user
from login import login_user
from getpass import getpass  #import getpass to hide password in input
from expenses import add_expense, view_expenses, update_expense, delete_expense
from reports import monthly_report, yearly_report
from budget import set_budget, view_budgets, check_budget_warnings
from incomes import add_income, view_incomes
from reports import (
    monthly_financial_report,
    yearly_financial_report,
    savings_insight,
    export_monthly_report_csv
)
from datetime import datetime
from export_pdf import export_monthly_report_pdf



# =======================
# Expense Dashboard Menu
# =======================
def expense_management(user_id):
    while True:
        print("\n=== Expense Dashboard ===")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Monthly Expenses Report")
        print("6. Yearly Expenses Report")
        print("0. Back to Main Menu")
        

        choice = input("Choose an option: ")

        if choice == "1":
            category = input("Enter category: ")
            amount = float(input("Enter amount: "))
            description = input("Enter description: ")
            add_expense(user_id, category, amount, description)

        elif choice == "2":
            view_expenses(user_id)

        elif choice == "3":
            expense_id = int(input("Enter Expense ID to update: "))
            new_category = input("Enter new category: ")
            new_amount = float(input("Enter new amount: "))
            new_description = input("Enter new description: ")
            update_expense(expense_id, new_category, new_amount, new_description)

        elif choice == "4":
            expense_id = int(input("Enter Expense ID to delete: "))
            delete_expense(expense_id)
            
        elif choice == "5":
            monthly_report(user_id)
            
        elif choice == "6":
            yearly_report(user_id)   
            
        elif choice == "0":
            break

        else:
            print("Invalid option, please try again.")
            
# ======================
# Budget Management Menu
# ======================
def budget_management(user_id):
    while True:
        print("\n--- Budget Management ---")
        print("1. Set Budget")
        print("2. View Budgets")
        print("3. Check Budget Warnings")
        print("0. Back to Main Menu")

        choice = input("Choose an option: ")

        if choice == "1":
            category = input("Enter category to set budget for: ")
            limit_amount = float(input("Enter monthly limit (₹): "))
            set_budget(user_id, category, limit_amount)

        elif choice == "2":
            view_budgets(user_id)

        elif choice == "3":
            check_budget_warnings(user_id)

        elif choice == "0":
            break

        else:
            print("Invalid option, please try again.")
            
# =====================
# Income Management Menu
# =====================
def income_management(user_id):
    while True:
        print("\n--- Income Management ---")
        print("1. Add Income")
        print("2. View Incomes")
        print("0. Back to Main Menu")

        choice = input("Choose an option: ")

        if choice == "1":
            source = input("Enter income source: ")
            amount = float(input("Enter amount: "))
            add_income(user_id, source, amount)

        elif choice == "2":
            view_incomes(user_id)

        elif choice == "0":
            break

        else:
            print("Invalid option, please try again.")
            
# ======================
# Financial Reports Menu
# ======================
def reports_management(user_id):
    while True:
        print("\n--- Financial Reports ---")
        print("1. Monthly Financial Report")
        print("2. Yearly Financial Report")
        print("3. Savings Insight")
        print("0. Back to Main Menu")

        choice = input("Choose an option: ")

        if choice == "1":
            monthly_financial_report(user_id)

        elif choice == "2":
            yearly_financial_report(user_id)

        elif choice == "3":
            savings_insight(user_id)

        elif choice == "0":
            break

        else:
            print("Invalid option, please try again.")
            
# ==========================
# Data Export / Backup Menu
# ==========================
def export_management(user_id):
    while True:
        print("\n--- Data Export & Backup ---")
        print("1. Export Monthly Report (CSV)")
        print("2. Export Monthly Report (PDF)")
        print("0. Back to Main Menu")

        choice = input("Choose an option: ")

        if choice == "1":
            month = int(input("Month (1-12) [default current]: ") or datetime.now().month)
            year = int(input("Year [default current]: ") or datetime.now().year)
            export_monthly_report_csv(user_id, month, year, filename=f"report_{user_id}_{month}_{year}.csv")

        elif choice == "2":
            m = input("Month (1-12) [enter for current]: ")
            y = input("Year [enter for current]: ")
            month = int(m) if m.strip() else None
            year = int(y) if y.strip() else None
            export_monthly_report_pdf(user_id, month, year)

        elif choice == "0":
            break

        else:
            print("Invalid option, please try again.")
            
# ===========================
# Main User Dashboard (after login)
# ===========================
def user_dashboard(user_id):
    while True:
        print("\n=== PERSONAL FINANCE MANAGER DASHBOARD ===")
        print("1. Expense Management")
        print("2. Budget Management")
        print("3. Income Management")
        print("4. Financial Reports")
        print("5. Data Export & Backup")
        print("6. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            expense_management(user_id)

        elif choice == "2":
            budget_management(user_id)

        elif choice == "3":
            income_management(user_id)

        elif choice == "4":
            reports_management(user_id)

        elif choice == "5":
            export_management(user_id)

        elif choice == "6":
            print("Logged out successfully!\n")
            break

        else:
            print("Invalid option, please try again.")
                                                
# =======================
# Main Entry Point
# =======================
def main():
    while True:
        print("\n=== Personal Finance Manager ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Enter username: ")
            password = getpass("Enter password: ")
            register_user(username, password)
        elif choice == "2":
            username = input("Enter username: ")
            password = getpass("Enter password: ")
            
            
            #If login is successfull
            user_id = login_user(username, password)

            if user_id:
                
                user_dashboard(user_id)  # Open expense dashboard for that user
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

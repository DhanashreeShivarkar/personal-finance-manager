# main.py

from register import register_user
from login import login_user
from getpass import getpass  #import getpass to hide password in input
from expenses import add_expense, view_expenses, update_expense, delete_expense
from reports import monthly_report, yearly_report


# =======================
# Expense Dashboard Menu
# =======================
def user_dashboard(user_id):
    while True:
        print("\n=== Expense Dashboard ===")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Monthly Report")
        print("6. Yearly Report")
        print("7. Logout")

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

        elif choice == "7":
            print("Logged out successfully!\n")
            break

        else:
            print("Invalid option, please try again.")

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
            # login_user(username, password)
            
            #If login is successfull
            user_id = login_user(username, password)

            if user_id:
                print(f"Login successful! Last login updated to {user_id}.  Welcome, {username}")
                user_dashboard(user_id)  # Open expense dashboard for that user
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

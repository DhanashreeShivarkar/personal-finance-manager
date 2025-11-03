🟢 1. Overview
The Personal Finance Manager is a command-line Python application that helps users manage their personal finances efficiently.
It allows users to record expenses, track incomes, set monthly budgets, generate financial reports, and export data in CSV or PDF format.
The system supports user registration and login, and stores data securely in a local SQLite database.

🟢 2. Installation Guide
Requirements:
Python 3.10 or later
pip (Python package manager)

Steps:
# Clone or download the repository
git clone <repo-url>
cd personal_finance_manager

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate      # For Windows
# OR
source venv/bin/activate   # For Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Run the database
modules\database.py

# Run the application
python main.py

🟢 3. Usage Instructions

Login/Register Flow:
Run python main.py
Register a new account (username + password)
Login to access your dashboard

Once logged in, you’ll see:
=== PERSONAL FINANCE MANAGER DASHBOARD ===
1. Expense Management
2. Budget Management
3. Income Management
4. Financial Reports
5. Data Export & Backup
6. Logout

Select options by typing the number (1–6).

🟢 4. Menu Navigation Table

Section 1 - 	
Expense Management:	
Actions- Add, View, Update, Delete expenses, Monthly Expenses Report, Yearly Expenses Report
Section 2 -
Budget Management:	
Actions- Set, View, Check Budget Warnings
Section 3 -
Income Management:	
Actions- Add or View incomes
Section 4 -
Financial Reports:	
Actions- Generate Monthly, Yearly, and Saving insights
Section 5 -
Data Export & Backup:	
Actions- Export reports as CSV or PDF
Section 6 -
Logout
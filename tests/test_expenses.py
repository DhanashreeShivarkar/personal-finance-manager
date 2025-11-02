import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from expenses import add_expense, view_expenses
from incomes import add_income, view_incomes

def test_add_expense(monkeypatch):
    user_id = 1
    add_expense(user_id, "Food", 250.0, "Lunch")
    expenses = view_expenses(user_id)
    assert any("Food" in str(e) for e in expenses)

def test_add_income(monkeypatch):
    user_id = 1
    add_income(user_id, "Salary", 10000.0)
    incomes = view_incomes(user_id)
    assert any("Salary" in str(i) for i in incomes)

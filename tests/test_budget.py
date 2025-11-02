import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from budget import set_budget, view_budgets, check_budget_warnings

def test_set_and_view_budget(user_id=1):
    set_budget(user_id, "Food", 2000)
    budgets = view_budgets(user_id)
    assert any("Food" in str(b) for b in budgets)

def test_budget_warning_trigger(user_id=1):
    warnings = check_budget_warnings(user_id)
    assert isinstance(warnings, list)

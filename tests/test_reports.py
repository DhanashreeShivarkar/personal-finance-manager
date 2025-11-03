import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reports import monthly_financial_report, yearly_financial_report, savings_insight


def test_monthly_financial_report(user_id=1):
    report = monthly_financial_report(user_id)
    assert "Total Income" in report["report_str"]
    assert "Total Expenses" in report["report_str"]


def test_savings_insight(user_id=1):
    result = savings_insight(user_id)
    assert isinstance(result, dict)
    assert "Savings" in result

# validators.py
def get_non_empty_input(prompt):
    """Prompt user until non-empty input is given."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def get_positive_float(prompt):
    """Prompt user until a valid positive float is given."""
    while True:
        value = input(prompt).strip()
        try:
            amount = float(value)
            if amount > 0:
                return amount
            else:
                print("Amount must be greater than 0.")
        except ValueError:
            print("Invalid number. Please enter a valid amount.")


def get_valid_month(prompt="Enter month (1-12): "):
    """Prompt until valid month (1–12)."""
    from datetime import datetime
    while True:
        value = input(prompt).strip()
        if not value:
            return datetime.now().month
        try:
            month = int(value)
            if 1 <= month <= 12:
                return month
            print("Month must be between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 12.")


def get_valid_year(prompt="Enter year: "):
    """Prompt until valid year."""
    from datetime import datetime
    current_year = datetime.now().year
    while True:
        value = input(prompt).strip()
        if not value:
            return current_year
        try:
            year = int(value)
            if 2000 <= year <= current_year:
                return year
            print(f"Year must be between 2000 and {current_year}.")
        except ValueError:
            print("Invalid year entered.")

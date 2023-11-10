import pandas as pd
from expense import Expense
import calendar
import datetime


class ExpenseTracker:
    def __init__(self, budget: float, filepath: str):
        self._budget = budget
        self._filepath = filepath
        self._expenses_df = self._load_expenses()

    def _load_expenses(self):
        try:
            return pd.read_csv(self._filepath, encoding='utf-8-sig')

        except FileNotFoundError:
            return pd.DataFrame(columns=['name', 'amount', 'category'])

    def add_expense(self, expense: Expense):
        new_row = pd.Series({'name': expense.name, 'amount': expense.amount, 'category': expense.category})
        self._expenses_df = pd.concat([self._expenses_df, new_row.to_frame().T], ignore_index=True)
        self._expenses_df.to_csv(self._filepath, index=False, encoding='utf-8-sig')

    def summarize_expense(self):
        print("Expense By Category 📈:")
        summary = self._expenses_df.groupby('category').amount.sum()
        for category, amount in summary.items():
            print(f"  {category}: £{amount:.2f}")

        total_spend = self._expenses_df['amount'].sum()
        print(f"💷Total Spent: £{total_spend:.2f}")

        remaining_budget = self._budget - total_spend
        print(f"🪙Budget Remaining: £{remaining_budget:.2f}")

        now = datetime.datetime.now()
        days_in_month = calendar.monthrange(now.year, now.month)[1]
        remaining_days = days_in_month - now.day

        daily_budget = remaining_budget / remaining_days
        print(green(f"🤞Budget Per Day: £{daily_budget:.2f}"))


def green(text):
    return f"\033[92m{text}\033[0m"


def get_user_expense():
    print(f"🎯 Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    expense_categories = [
        "🍱Food",
        "🏡Home",
        "🧑‍💻Work",
        "🎊Fun",
        "🤦🏻‍Misc",
        "💸Bill",
        "🚇Commuting"
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f" {i + 1}, {category_name}")

        value_range = f"1 - {len(expense_categories)}"
        try:
            selected_index = int(input(f"Enter a category number [{value_range}] ")) - 1
            if selected_index in range(len(expense_categories)):
                selected_category = expense_categories[selected_index]
                new_expense = Expense(name=expense_name,
                                      category=selected_category,
                                      amount=expense_amount)
                return new_expense
            else:
                print("Invalid category. Please try again!")
        except ValueError:
            print("Invalid category. Please try again!")


def main():
    print(f"🎯 Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    budget = 2000

    # Get user input for expense
    expense = get_user_expense()

    tracker = ExpenseTracker(budget, expense_file_path)

    # Write their expense to a file
    tracker.add_expense(expense)

    # Summarize expense
    tracker.summarize_expense()


if __name__ == '__main__':
    main()

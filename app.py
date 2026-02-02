from models import Expense, User
from storage import JSONStorage
from utils import input_float
from reports import ReportGenerator

class ExpenseManager:
    def __init__(self, storage: JSONStorage):
        self.storage = storage
        self._expenses: list[Expense] = []
        self._next_id = 1
        self._load()

    def _load(self):
        data = self.storage.load()
        self._next_id = data["next_id"]
        self._expenses = []
        for rec in data["records"]:
            if rec.get("type") == "expense":
                self._expenses.append(Expense.from_dict(rec))

    def _save(self):
        data = {
            "next_id": self._next_id,
            "records": [e.to_dict() for e in self._expenses]
        }
        self.storage.save(data)

    def add_expense(self, amount: float, category: str, note: str):
        exp = Expense(self._next_id, amount, category, note)
        self._next_id += 1
        self._expenses.append(exp)
        self._save()

    def list_expenses(self) -> list[Expense]:
        return list(self._expenses)

    def totals_by_category(self) -> dict[str, float]:
        totals: dict[str, float] = {}
        for e in self._expenses:
            totals[e.category] = totals.get(e.category, 0.0) + e.amount
        return totals

    def total_all(self) -> float:
        return sum(e.amount for e in self._expenses)

class Menu:
    @staticmethod
    def main_menu():
        print("\n==== Expense Tracker ====")
        print("1) Expenses")
        print("2) Reports")
        print("3) Exit")

    @staticmethod
    def expenses_menu():
        print("\n-- Expenses --")
        print("1) Add expense")
        print("2) View all expenses")
        print("3) Back")

    @staticmethod
    def reports_menu():
        print("\n-- Reports --")
        print("1) Totals by category")
        print("2) Total spent")
        print("3) Back")

class ExpenseTrackerApp:
    def __init__(self):
        self.user = User("Student")
        self.manager = ExpenseManager(JSONStorage("data.json"))

    def run(self):
        while True:
            Menu.main_menu()
            choice = input("Choose: ").strip()

            if choice == "1":
                self._expenses_flow()
            elif choice == "2":
                self._reports_flow()
            elif choice == "3":
                print("Goodbye")
                break
            else:
                print("Invalid choice.")

    def _expenses_flow(self):
        while True:
            Menu.expenses_menu()
            choice = input("Choose: ").strip()

            if choice == "1":
                self._add_expense_ui()
            elif choice == "2":
                self._view_expenses_ui()
            elif choice == "3":
                break
            else:
                print("Invalid choice.")

    def _reports_flow(self):
        while True:
            Menu.reports_menu()
            choice = input("Choose: ").strip()

            if choice == "1":
                self._totals_by_category_ui()
            elif choice == "2":
                print(f"Total spent: {self.manager.total_all():.2f} EUR")
            elif choice == "3":
                break
            else:
                print("Invalid choice.")

    def _add_expense_ui(self):
        amount = input_float("Amount (EUR): ")
        category = input("Category: ").strip()
        note = input("Note: ").strip()

        if amount <= 0 or category == "":
            print("Invalid expense data.")
            return

        self.manager.add_expense(amount, category, note)
        print("Expense saved.")

    def _view_expenses_ui(self):
        expenses = self.manager.list_expenses()
        if not expenses:
            print("No expenses yet.")
            return

        print("\nYour expenses:")
        for e in expenses:
            print(e.summary())

    def _totals_by_category_ui(self):
        totals = self.manager.totals_by_category()
        ReportGenerator.print_totals_by_category(totals)

def start_app():
    app = ExpenseTrackerApp()
    app.run()

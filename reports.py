class ReportGenerator:
    """Generates and prints reports."""

    @staticmethod
    def print_totals_by_category(totals: dict[str, float]):
        if not totals:
            print("No expenses yet.")
            return

        print("\nTotals by category:")
        for category, total in totals.items():
            print(f"- {category}: {total:.2f} EUR")

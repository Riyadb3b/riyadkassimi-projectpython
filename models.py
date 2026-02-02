from abc import ABC, abstractmethod
from datetime import datetime

class Record(ABC):
    def __init__(self, record_id: int, created_at: str | None = None):
        self._record_id = record_id
        self._created_at = created_at or datetime.now().isoformat(timespec="seconds")

    @property
    def record_id(self) -> int:
        return self._record_id

    @property
    def created_at(self) -> str:
        return self._created_at

    @abstractmethod
    def summary(self) -> str:
        pass

class Expense(Record):
    def __init__(self, record_id: int, amount: float, category: str, note: str, created_at: str | None = None):
        super().__init__(record_id, created_at)
        self._amount = amount
        self._category = category
        self._note = note

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def category(self) -> str:
        return self._category

    @property
    def note(self) -> str:
        return self._note

    def summary(self) -> str:
        return f"#{self.record_id} | {self.created_at} | {self.category} | {self.amount:.2f} EUR | {self.note}"

    def to_dict(self) -> dict:
        return {
            "type": "expense",
            "id": self.record_id,
            "created_at": self.created_at,
            "amount": self.amount,
            "category": self.category,
            "note": self.note
        }

    @staticmethod
    def from_dict(d: dict) -> "Expense":
        return Expense(
            record_id=d["id"],
            amount=d["amount"],
            category=d["category"],
            note=d["note"],
            created_at=d["created_at"]
        )

class User:
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

import json
import os

class JSONStorage:
    def __init__(self, filename: str = "data.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            self.save({"next_id": 1, "records": []})

    def load(self) -> dict:
        with open(self.filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data: dict) -> None:
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

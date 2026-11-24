"""
==============================================================================
AUTHOR: Ra Daro
MODULE: JSON Data Persistence
DESCRIPTION: Handles saving and loading menu and table state to JSON files.
==============================================================================
"""

import json
from pathlib import Path
from models.menu import MenuItem, Food, Drink
from models.table import Table


class DataManager:
    # Sets up file paths for menu and table JSON storage and ensures folders exist
    def __init__(self, menu_path: str = "data/menu_data.json", table_path: str = "data/table_data.json"):
        self.menu_file = Path(menu_path)
        self.table_file = Path(table_path)
        self.menu_file.parent.mkdir(parents=True, exist_ok=True)
        self.table_file.parent.mkdir(parents=True, exist_ok=True)

    # Reads menu_data.json and reconstructs MenuItem, Food, and Drink objects
    def load_menu(self) -> list[MenuItem]:
        if not self.menu_file.exists():
            return []
        try:
            raw_data = json.loads(self.menu_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []

        menu_items: list[MenuItem] = []
        for item in raw_data:
            item_type = str(item.get("type") or item.get("category", "")).strip().lower()
            stock = int(item.get("stock", 10))
            is_available = bool(item.get("is_available", True))

            if item_type == "food":
                menu_items.append(
                    Food(
                        item_id=item["item_id"],
                        name=item["name"],
                        price=float(item["price"]),
                        is_spicy=bool(item.get("is_spicy", False)),
                        is_available=is_available,
                        stock=stock,
                    )
                )
            elif item_type == "drink":
                menu_items.append(
                    Drink(
                        item_id=item["item_id"],
                        name=item["name"],
                        price=float(item["price"]),
                        size=str(item.get("size", "Regular")),
                        is_available=is_available,
                        stock=stock,
                    )
                )
            else:
                menu_items.append(
                    MenuItem(
                        item_id=item["item_id"],
                        name=item["name"],
                        price=float(item["price"]),
                        category=item.get("category", "Other"),
                        is_available=is_available,
                        stock=stock,
                    )
                )

        return menu_items

    # Saves the current list of menu objects (including stock) back to menu_data.json
    def save_menu(self, menu_items: list[MenuItem]) -> None:
        serialized = []
        for item in menu_items:
            data = item.to_dict()
            data["type"] = item.category.lower()
            serialized.append(data)

        self.menu_file.write_text(json.dumps(serialized, indent=4), encoding="utf-8")

    # Reads table_data.json and reconstructs Table objects with occupancy state
    def load_tables(self) -> list[Table]:
        if not self.table_file.exists():
            return []
        try:
            raw = json.loads(self.table_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []

        return [
            Table(
                t["table_number"],
                t["capacity"],
                t.get("is_available", True),
                t.get("active_order_id"),
            )
            for t in raw
        ]

    # Saves the current list of table objects back to table_data.json
    def save_tables(self, tables: list[Table]) -> None:
        self.table_file.write_text(json.dumps([t.to_dict() for t in tables], indent=2), encoding="utf-8")
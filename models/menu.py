"""
==============================================================================
AUTHOR: Ra Daro
MODULE: Menu Management Models
DESCRIPTION: Defines MenuItem, Food, and Drink classes with JSON serialization.
==============================================================================
"""

"""
models/menu.py
Defines the restaurant menu hierarchy (MenuItem base class and Food/Drink subclasses).
Handles item validation, price/name updates, availability toggles, and JSON conversion.
"""


class MenuItem:
    # Initializes a menu item and validates its ID, name, and price
    def __init__(self, item_id: str | int, name: str, price: float, category: str, is_available: bool = True):
        # Convert ID to string first so legacy integer IDs from old JSON files don't crash
        raw_id = str(item_id).strip() if item_id is not None else ""
        if not raw_id:
            raise ValueError("Item ID is required.")
        if not name or not str(name).strip():
            raise ValueError("Item name is required.")
        if price < 0:
            raise ValueError("Price cannot be negative.")

        self.item_id = raw_id.upper()
        self.name = str(name).strip()
        self.price = round(float(price), 2)
        self.category = str(category).strip()
        self.is_available = bool(is_available)

    # Updates an item's name and/or price when edited by an admin
    def update_details(self, new_name: str | None = None, new_price: float | None = None) -> None:
        if new_name is not None and new_name.strip():
            self.name = new_name.strip()
        if new_price is not None:
            if new_price < 0:
                raise ValueError("Price cannot be negative.")
            self.price = round(float(new_price), 2)

    # Marks the item as either available to order or out of stock
    def set_availability(self, status: bool) -> None:
        self.is_available = bool(status)

    # Serializes the menu item into a dictionary for JSON file storage
    def to_dict(self) -> dict:
        return {
            "type": "item",
            "item_id": self.item_id,
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "is_available": self.is_available,
        }

    # Formats the menu item cleanly for terminal display
    def __str__(self) -> str:
        status = "Available" if self.is_available else "Inactive / Out of Stock"
        return f"[{self.item_id}] {self.name:<22} ${self.price:>6.2f}  ({status})"


class Food(MenuItem):
    # Creates a Food item with an optional spicy indicator
    def __init__(self, item_id: str | int, name: str, price: float, is_spicy: bool = False, is_available: bool = True):
        super().__init__(item_id, name, price, category="Food", is_available=is_available)
        self.is_spicy = bool(is_spicy)

    # Serializes Food attributes including its spicy flag
    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "food"
        data["is_spicy"] = self.is_spicy
        return data

    # Appends a [Spicy] tag to the standard menu display if applicable
    def __str__(self) -> str:
        tag = " [Spicy]" if self.is_spicy else ""
        return f"{super().__str__()}{tag}"


class Drink(MenuItem):
    # Creates a Drink item with a serving size (e.g., Small, Regular, Large)
    def __init__(self, item_id: str | int, name: str, price: float, size: str = "Regular", is_available: bool = True):
        super().__init__(item_id, name, price, category="Drink", is_available=is_available)
        self.size = size.strip().title() if size else "Regular"

    # Serializes Drink attributes including serving size
    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "drink"
        data["size"] = self.size
        return data

    # Appends the drink size to the standard menu display
    def __str__(self) -> str:
        return f"{super().__str__()} [{self.size}]"
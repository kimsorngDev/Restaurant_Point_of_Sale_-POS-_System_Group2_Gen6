# ==============================================================================
# AUTHOR: Ra Daro
# MODULE: Menu Management System (Models)
# DESCRIPTION: Contains the base MenuItem class and derived Food/Drink classes.
# ==============================================================================

class MenuItem:
    """Base class representing a general menu item."""
    
    def __init__(self, item_id: int, name: str, price: float):
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self.item_id = item_id
        self.name = name
        self.price = price

    def get_details(self) -> str:
        """Returns formatted string details of the item."""
        return f"[{self.item_id}] {self.name} - ${self.price:.2f}"

    def to_dict(self) -> dict:
        """Converts object attributes to a dictionary for JSON serialization."""
        return {
            "type": "MenuItem",
            "item_id": self.item_id,
            "name": self.name,
            "price": self.price
        }


class Food(MenuItem):
    """Derived class representing food items, inheriting from MenuItem."""
    
    def __init__(self, item_id: int, name: str, price: float, is_vegetarian: bool = False):
        super().__init__(item_id, name, price)
        self.is_vegetarian = is_vegetarian

    def get_details(self) -> str:
        """Overrides base get_details to display vegetarian status."""
        veg_status = " (Veg)" if self.is_vegetarian else ""
        return f"[{self.item_id}] 🍽️ {self.name}{veg_status} - ${self.price:.2f}"

    def to_dict(self) -> dict:
        """Converts Food object to dictionary for JSON serialization."""
        return {
            "type": "Food",
            "item_id": self.item_id,
            "name": self.name,
            "price": self.price,
            "is_vegetarian": self.is_vegetarian
        }


class Drink(MenuItem):
    """Derived class representing drink items, inheriting from MenuItem."""
    
    def __init__(self, item_id: int, name: str, price: float, is_cold: bool = True):
        super().__init__(item_id, name, price)
        self.is_cold = is_cold

    def get_details(self) -> str:
        """Overrides base get_details to display temperature type."""
        temp_status = "Cold" if self.is_cold else "Hot"
        return f"[{self.item_id}] 🥤 {self.name} ({temp_status}) - ${self.price:.2f}"

    def to_dict(self) -> dict:
        """Converts Drink object to dictionary for JSON serialization."""
        return {
            "type": "Drink",
            "item_id": self.item_id,
            "name": self.name,
            "price": self.price,
            "is_cold": self.is_cold
        }
  
#Testing
if __name__ == "__main__":
    test_FOOD = Food(101, "Fried Rice", 3.50)
    test_DRINK = Drink(2, "Coca-Cola", 2.5)
    print("Testing Menu Item:")
    
    print(test_FOOD.get_details())
    print(test_DRINK.get_details())
    
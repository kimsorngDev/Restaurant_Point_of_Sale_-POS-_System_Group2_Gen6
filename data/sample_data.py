# ==============================================================================
# AUTHOR: Ra Daro
# MODULE: Sample Data Provider
# DESCRIPTION: Initial sample dataset for Menu Items and Restaurant Tables.
# ==============================================================================

from models.menu import Food, Drink
from models.table import Table

# Initial sample menu list
sample_menu = [
    Food(101, "Fried Rice", 3.50, is_vegetarian=False),
    Food(102, "Vegetable Stir-Fry", 3.00, is_vegetarian=True),
    Food(103, "Beef Lok Lak", 4.50, is_vegetarian=False),
    Drink(201, "Iced Latte", 2.00, is_cold=True),
    Drink(202, "Hot Green Tea", 1.50, is_cold=False),
    Drink(203, "Fresh Orange Juice", 2.25, is_cold=True),
]

# Initial sample table list
sample_tables = [
    Table(1, capacity=2, is_available=True),
    Table(2, capacity=4, is_available=True),
    Table(3, capacity=4, is_available=False),
    Table(4, capacity=6, is_available=True),
    Table(5, capacity=8, is_available=True),
]
"""
data/sample_data.py
Provides default starter menu items (food and drinks) and restaurant tables
used to initialize the POS system when no saved JSON data exists yet.
"""

from models.menu import MenuItem, Food, Drink
from models.table import Table


# Returns a starter list of Food and Drink items for initial setup
def get_sample_menu() -> list[MenuItem]:
    return [
        Food("F01", "Beef Lok Lak", 6.50, is_spicy=False, is_available=True),
        Food("F02", "Spicy Basil Chicken", 5.00, is_spicy=True, is_available=True),
        Food("F03", "Fish Amok", 6.00, is_spicy=False, is_available=True),
        Food("F04", "Seafood Fried Rice", 5.50, is_spicy=False, is_available=False),
        Drink("D01", "Iced Latte", 2.75, size="Regular", is_available=True),
        Drink("D02", "Passion Fruit Soda", 2.50, size="Large", is_available=True),
        Drink("D03", "Fresh Coconut", 2.00, size="Regular", is_available=True),
    ]


# Returns a starter list of floor tables with numbers and seat capacities
def get_sample_tables() -> list[Table]:
    return [
        Table(1, capacity=2, is_available=True),
        Table(2, capacity=4, is_available=True),
        Table(3, capacity=4, is_available=True),
        Table(4, capacity=6, is_available=True),
        Table(5, capacity=8, is_available=True),
    ]
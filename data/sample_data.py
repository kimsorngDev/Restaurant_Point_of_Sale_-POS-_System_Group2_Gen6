"""
==============================================================================
MODULE: Sample Data Provider
DESCRIPTION: Starter menu items, floor tables, and sample orders for POS setup.
==============================================================================
"""

from models.menu import MenuItem, Food, Drink
from models.table import Table
from models.order import Order


# Returns a starter list of Food and Drink items
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


# Returns a starter list of restaurant tables
def get_sample_tables() -> list[Table]:
    return [
        Table(1, capacity=2, is_available=True),
        Table(2, capacity=4, is_available=True),
        Table(3, capacity=4, is_available=False),
        Table(4, capacity=6, is_available=True),
        Table(5, capacity=8, is_available=True),
    ]


# Sample menu and tables used by the initial sample orders
sample_menu = get_sample_menu()
sample_tables = get_sample_tables()


# Initial sample order list
_sample_order_1 = Order(
    order_id=1001,
    table_number=2,
    notes="Customer requested no onions"
)
_sample_order_1.add_item(
    sample_menu[0],
    quantity=2,
    special_notes="No onions"
)
_sample_order_1.add_item(
    sample_menu[3],
    quantity=2,
    special_notes="Less sugar"
)

_sample_order_2 = Order(
    order_id=1002,
    table_number=3,
    status=Order.STATUS_IN_PROGRESS
)
_sample_order_2.add_item(sample_menu[2], quantity=1, special_notes="Medium well")
_sample_order_2.add_item(sample_menu[4], quantity=1)

sample_orders = [
    _sample_order_1,
    _sample_order_2,
]
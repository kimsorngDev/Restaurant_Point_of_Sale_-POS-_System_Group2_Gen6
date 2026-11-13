
from models.menu import Food, Drink
from models.table import Table
from models.order import Order, OrderItem

# Initial sample menu list
sample_menu = [
    Food(101, "Fried Rice", 3.50, is_vegetarian=False),
    Food(102, "Vegetable Stir-Fry", 3.00, is_vegetarian=True),
    Food(103, "Beef Lok Lak", 4.50, is_vegetarian=False),
    Drink(201, "Iced Latte", 2.00, is_cold=True),
    Drink(202, "Hot Green Tea", 1.50, is_cold=False),
    Drink(203, "Fresh Orange Juice", 2.25, is_cold=True),
]


sample_tables = [
    Table(1, capacity=2, is_available=True),
    Table(2, capacity=4, is_available=True),
    Table(3, capacity=4, is_available=False),
    Table(4, capacity=6, is_available=True),
    Table(5, capacity=8, is_available=True),
]

# Initial sample order list
_sample_order_1 = Order(order_id=1001, table_number=2, notes="Customer requested no onions")
_sample_order_1.add_item(sample_menu[0], quantity=2, special_notes="No onions")
_sample_order_1.add_item(sample_menu[3], quantity=2, special_notes="Less sugar")

_sample_order_2 = Order(order_id=1002, table_number=3, status=Order.STATUS_IN_PROGRESS)
_sample_order_2.add_item(sample_menu[2], quantity=1, special_notes="Medium well")
_sample_order_2.add_item(sample_menu[4], quantity=1)

sample_orders = [
    _sample_order_1,
    _sample_order_2,
]

from models.menu import MenuItem, Food, Drink
from models.table import Table
from models.order import Order

def get_sample_menu() -> list[MenuItem]:
    return [
        Food('F01', 'Beef Lok Lak', 6.5, is_spicy=False, is_available=True),
        Food('F02', 'Spicy Basil Chicken', 5.0, is_spicy=True, is_available=True),
        Food('F03', 'Fish Amok', 6.0, is_spicy=False, is_available=True),
        Food('F04', 'Seafood Fried Rice', 5.5, is_spicy=False, is_available=False),
        Food(101, 'Fried Rice', 3.5, is_spicy=False, is_available=True),
        Food(102, 'Vegetable Stir-Fry', 3.0, is_spicy=False, is_available=True),
        Food(103, 'Beef Lok Lak', 4.5, is_spicy=False, is_available=True),
        Drink('D01', 'Iced Latte', 2.75, size='Regular', is_available=True),
        Drink('D02', 'Passion Fruit Soda', 2.5, size='Large', is_available=True),
        Drink('D03', 'Fresh Coconut', 2.0, size='Regular', is_available=True),
        Drink(201, 'Iced Latte', 2.0, size='Regular', is_available=True),
        Drink(202, 'Hot Green Tea', 1.5, size='Regular', is_available=True),
        Drink(203, 'Fresh Orange Juice', 2.25, size='Regular', is_available=True)
    ]

def get_sample_tables() -> list[Table]:
    return [
        Table(1, capacity=2, is_available=True),
        Table(2, capacity=4, is_available=True),
        Table(3, capacity=4, is_available=False),
        Table(4, capacity=6, is_available=True),
        Table(5, capacity=8, is_available=True)
    ]

sample_menu = get_sample_menu()
sample_tables = get_sample_tables()
_sample_order_1 = Order(order_id=1001, table_number=2, notes='Customer requested no onions')
_sample_order_1.add_item(sample_menu[0], quantity=2, special_notes='No onions')
_sample_order_1.add_item(sample_menu[7], quantity=2, special_notes='Less sugar')
_sample_order_2 = Order(order_id=1002, table_number=3, status=Order.STATUS_IN_PROGRESS)
_sample_order_2.add_item(sample_menu[1], quantity=1, special_notes='Medium well')
_sample_order_2.add_item(sample_menu[8], quantity=1)
sample_orders = [_sample_order_1, _sample_order_2]

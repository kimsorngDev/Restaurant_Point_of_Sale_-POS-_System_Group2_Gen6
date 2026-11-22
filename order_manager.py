from typing import List, Optional, Union
from models.menu import MenuItem
from models.table import Table
from models.order import Order, OrderItem
import itertools
_order_id_counter = itertools.count(1001)

def generate_order_id() -> int:
 return next(_order_id_counter)

def start_new_order(order_type: str=Order.ORDER_TYPE_DINE_IN, table_number: Optional[int]=None, notes: str='', tables_list: Optional[List[Table]]=None, order_id: Optional[int]=None) -> Order:
 clean_type = order_type.strip().title()
 if clean_type in ['Dine-In', 'Dine In', 'Dine_In']:
  resolved_type = Order.ORDER_TYPE_DINE_IN
 elif clean_type in ['Takeaway', 'Take Away', 'Take-Away', 'Togo', 'To Go']:
  resolved_type = Order.ORDER_TYPE_TAKEAWAY
 else:
  raise ValueError(f"Invalid order type '{order_type}'. Must be 'Dine-In' or 'Takeaway'.")
 target_table: Optional[Table] = None
 if resolved_type == Order.ORDER_TYPE_DINE_IN:
  if table_number is None or table_number <= 0:
   raise ValueError('Dine-In orders require a valid positive table number.')
  if tables_list is not None:
   matching_tables = [t for t in tables_list if t.table_number == table_number]
   if not matching_tables:
    raise ValueError(f'Table {table_number} does not exist in restaurant layout.')
   target_table = matching_tables[0]
   if not target_table.is_available:
    raise ValueError(f'Table {table_number:02d} is currently occupied.')
 assigned_id = order_id if order_id is not None else generate_order_id()
 new_order = Order(order_id=assigned_id, table_number=table_number if resolved_type == Order.ORDER_TYPE_DINE_IN else None, order_type=resolved_type, notes=notes)
 if target_table is not None:
  target_table.occupy()
 return new_order

def add_menu_item_to_order(order: Order, item: Union[MenuItem, int, str], quantity: int=1, special_notes: str='', menu_list: Optional[List[MenuItem]]=None) -> OrderItem:
 if isinstance(item, (int, str)):
  if not menu_list:
   raise ValueError('A menu_list must be provided when adding items by item_id.')
  matching = [m for m in menu_list if str(m.item_id).upper() == str(item).upper()]
  if not matching:
   raise ValueError(f'Menu item with ID [{item}] not found in menu.')
  menu_item = matching[0]
 elif isinstance(item, MenuItem):
  menu_item = item
 elif isinstance(item, OrderItem):
  return order.add_item(item)
 else:
  raise TypeError('Item must be an instance of MenuItem, OrderItem, or integer/string item_id.')
 return order.add_item(menu_item, quantity=quantity, special_notes=special_notes)

def remove_item_from_order(order: Order, item_id: Union[int, str]) -> bool:
 return order.remove_item(item_id)

def update_item_quantity(order: Order, item_id: Union[int, str], new_quantity: int) -> bool:
 return order.update_item_quantity(item_id, new_quantity)

def calculate_subtotal(order: Order) -> float:
 return order.get_subtotal()

def display_order_summary(order: Order, tax_rate: float=0.1, discount_percent: float=0.0) -> str:
 summary = order.get_summary(tax_rate=tax_rate, discount_percent=discount_percent)
 print(summary)
 return summary

def validate_order_for_checkout(order: Order) -> bool:
 return order.validate_for_checkout()

class OrderManager:

 def __init__(self, menu_list: Optional[List[MenuItem]]=None, tables_list: Optional[List[Table]]=None):
  self.menu_list: List[MenuItem] = menu_list if menu_list is not None else []
  self.tables_list: List[Table] = tables_list if tables_list is not None else []
  self.active_orders: List[Order] = []

 def start_order(self, order_type: str=Order.ORDER_TYPE_DINE_IN, table_number: Optional[int]=None, notes: str='') -> Order:
  order = start_new_order(order_type=order_type, table_number=table_number, notes=notes, tables_list=self.tables_list)
  self.active_orders.append(order)
  return order

 def add_item(self, order: Order, item: Union[MenuItem, int], quantity: int=1, special_notes: str='') -> OrderItem:
  return add_menu_item_to_order(order=order, item=item, quantity=quantity, special_notes=special_notes, menu_list=self.menu_list)

 def remove_item(self, order: Order, item_id: int) -> bool:
  return remove_item_from_order(order, item_id)

 def update_quantity(self, order: Order, item_id: int, new_quantity: int) -> bool:
  return update_item_quantity(order, item_id, new_quantity)

 def get_subtotal(self, order: Order) -> float:
  return calculate_subtotal(order)

 def print_summary(self, order: Order, tax_rate: float=0.1, discount_percent: float=0.0) -> str:
  return display_order_summary(order, tax_rate, discount_percent)

 def validate_checkout(self, order: Order) -> bool:
  return validate_order_for_checkout(order)

 def release_table_for_order(self, order: Order) -> bool:
  if order.table_number and self.tables_list:
   for t in self.tables_list:
    if t.table_number == order.table_number:
     t.release()
     return True
  return False

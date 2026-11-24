from models.menu import MenuItem, Food, Drink
from models.table import Table
from services.data_manager import DataManager
from data.sample_data import get_sample_menu, get_sample_tables

class MenuTableService:

 def __init__(self, storage: DataManager, seed_if_empty: bool=True):
  self.storage = storage
  self.menu: list[MenuItem] = self.storage.load_menu()
  self.tables: list[Table] = self.storage.load_tables()
  if seed_if_empty and (not self.menu) and (not self.tables):
   self.menu = get_sample_menu()
   self.tables = get_sample_tables()
   self.storage.save_menu(self.menu)
   self.storage.save_tables(self.tables)

 def display_menu(self, only_available: bool = False) -> str:
        items = [i for i in self.menu if i.is_available] if only_available else self.menu
        if not items:
            return "Menu is currently empty."

        sorted_items = sorted(items, key=lambda x: x.item_id.upper())

        foods = [item for item in sorted_items if getattr(item, "category", "").lower() == "food"]
        drinks = [item for item in sorted_items if getattr(item, "category", "").lower() == "drink"]
        others = [item for item in sorted_items if getattr(item, "category", "").lower() not in {"food", "drink"}]

        lines = ["=== RESTAURANT MENU ==="]
        if foods:
            avail_foods = sum(1 for item in foods if item.is_available)
            lines.append(f"\n[ FOOD ] ({avail_foods}/{len(foods)} Available)")
            lines.extend(str(item) for item in foods)
        if drinks:
            avail_drinks = sum(1 for item in drinks if item.is_available)
            lines.append(f"\n[ DRINKS ] ({avail_drinks}/{len(drinks)} Available)")
            lines.extend(str(item) for item in drinks)
        if others:
            avail_others = sum(1 for item in others if item.is_available)
            lines.append(f"\n[ OTHER ] ({avail_others}/{len(others)} Available)")
            lines.extend(str(item) for item in others)

        return "\n".join(lines)

 def display_tables(self) -> str:
  if not self.tables:
   return 'No tables configured.'
  lines = ['--- FLOOR TABLES ---']
  for table in self.tables:
   lines.append(str(table))
  return '\n'.join(lines)

 def get_menu_item(self, item_id: str) -> MenuItem | None:
  target = str(item_id).strip().upper()
  for item in self.menu:
   if item.item_id == target:
    return item
  return None

 def get_table(self, table_number: int) -> Table | None:
  for table in self.tables:
   if table.table_number == table_number:
    return table
  return None

 def validate_item_for_order(self, item_id: str) -> MenuItem:
  item = self.get_menu_item(item_id)
  if not item:
   raise ValueError(f"Menu item '{str(item_id).upper()}' does not exist.")
  if not item.is_available:
   raise ValueError(f"'{item.name}' ({item.item_id}) is currently unavailable.")
  return item

 def select_item_for_order(self, item_id: str, quantity: int=1) -> dict:
  if quantity <= 0:
   raise ValueError('Quantity must be at least 1.')
  item = self.validate_item_for_order(item_id)
  return {'item_id': item.item_id, 'name': item.name, 'category': item.category, 'unit_price': item.price, 'quantity': quantity, 'line_total': round(item.price * quantity, 2)}

 def start_order_session(self, order_id: str, order_type: str, table_number: int | None=None) -> dict:
  mode = order_type.strip().lower()
  if mode == 'takeaway':
   return {'order_id': order_id, 'order_type': 'Takeaway', 'table_number': None}
  if mode == 'dine-in':
   if table_number is None:
    raise ValueError('Table number is required for a Dine-In order.')
   table = self.get_table(table_number)
   if not table:
    raise ValueError(f'Table {table_number} does not exist.')
   table.assign_order(order_id)
   self.storage.save_tables(self.tables)
   return {'order_id': order_id, 'order_type': 'Dine-In', 'table_number': table.table_number}
  raise ValueError("Order type must be 'dine-in' or 'takeaway'.")

 def complete_order_for_table(self, table_number: int) -> Table:
  table = self.get_table(table_number)
  if not table:
   raise ValueError(f'Table {table_number} does not exist.')
  if table.is_available:
   raise ValueError(f'Table {table_number} has no active order to complete.')
  table.complete_order()
  self.storage.save_tables(self.tables)
  return table

 def add_food(self, item_id: str, name: str, price: float, is_spicy: bool=False) -> Food:
  if self.get_menu_item(item_id):
   raise ValueError(f"Item ID '{str(item_id).upper()}' already exists.")
  food = Food(item_id, name, price, is_spicy=is_spicy, is_available=True)
  self.menu.append(food)
  self.storage.save_menu(self.menu)
  return food

 def add_drink(self, item_id: str, name: str, price: float, size: str='Regular') -> Drink:
  if self.get_menu_item(item_id):
   raise ValueError(f"Item ID '{str(item_id).upper()}' already exists.")
  drink = Drink(item_id, name, price, size=size, is_available=True)
  self.menu.append(drink)
  self.storage.save_menu(self.menu)
  return drink

 def edit_menu_item(self, item_id: str, new_name: str | None=None, new_price: float | None=None) -> MenuItem:
  item = self.get_menu_item(item_id)
  if not item:
   raise ValueError(f"Item '{str(item_id).upper()}' not found.")
  item.update_details(new_name=new_name, new_price=new_price)
  self.storage.save_menu(self.menu)
  return item

 def set_item_availability(self, item_id: str, is_available: bool) -> MenuItem:
  item = self.get_menu_item(item_id)
  if not item:
   raise ValueError(f"Item '{str(item_id).upper()}' not found.")
  item.set_availability(is_available)
  self.storage.save_menu(self.menu)
  return item

 def remove_menu_item(self, item_id: str) -> bool:
  item = self.get_menu_item(item_id)
  if not item:
   return False
  self.menu.remove(item)
  self.storage.save_menu(self.menu)
  return True

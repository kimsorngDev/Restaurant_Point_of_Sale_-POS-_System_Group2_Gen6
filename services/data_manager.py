import json
from pathlib import Path
from models.menu import MenuItem, Food, Drink
from models.table import Table

class DataManager:

 def __init__(self, menu_path: str='data/menu_data.json', table_path: str='data/table_data.json'):
  self.menu_file = Path(menu_path)
  self.table_file = Path(table_path)
  self.menu_file.parent.mkdir(parents=True, exist_ok=True)
  self.table_file.parent.mkdir(parents=True, exist_ok=True)

 def load_menu(self) -> list[MenuItem]:
  if not self.menu_file.exists():
   return []
  try:
   raw = json.loads(self.menu_file.read_text(encoding='utf-8'))
  except json.JSONDecodeError:
   return []
  items: list[MenuItem] = []
  for entry in raw:
   kind = entry.get('type')
   avail = entry.get('is_available', True)
   if kind == 'food':
    items.append(Food(entry['item_id'], entry['name'], entry['price'], entry.get('is_spicy', False), avail))
   elif kind == 'drink':
    items.append(Drink(entry['item_id'], entry['name'], entry['price'], entry.get('size', 'Regular'), avail))
   else:
    items.append(MenuItem(entry['item_id'], entry['name'], entry['price'], entry.get('category', 'General'), avail))
  return items

 def save_menu(self, items: list[MenuItem]) -> None:
  self.menu_file.write_text(json.dumps([i.to_dict() for i in items], indent=2), encoding='utf-8')

 def load_tables(self) -> list[Table]:
  if not self.table_file.exists():
   return []
  try:
   raw = json.loads(self.table_file.read_text(encoding='utf-8'))
  except json.JSONDecodeError:
   return []
  return [Table(t['table_number'], t['capacity'], t.get('is_available', True), t.get('active_order_id')) for t in raw]

 def save_tables(self, tables: list[Table]) -> None:
  self.table_file.write_text(json.dumps([t.to_dict() for t in tables], indent=2), encoding='utf-8')

import json
import os
import csv
from models.menu import Food, Drink, MenuItem
from models.table import Table
from models.order import Order

MENU_FILE = 'data/menu_data.json'
TABLE_FILE = 'data/table_data.json'
ORDER_FILE = 'data/order_data.json'
LEGACY_MENU_FILE = 'data/menu.json'
LEGACY_TABLE_FILE = 'data/tables.json'
LEGACY_ORDER_FILE = 'data/orders.json'
SALES_FILE = 'data/sales.csv'

def save_menu_to_file(menu_list: list) -> bool:
 try:
  os.makedirs('data', exist_ok=True)
  data = [item.to_dict() for item in menu_list]
  with open(MENU_FILE, 'w', encoding='utf-8') as f:
   json.dump(data, f, indent=4, ensure_ascii=False)
  with open(LEGACY_MENU_FILE, 'w', encoding='utf-8') as f:
   json.dump(data, f, indent=4, ensure_ascii=False)
  return True
 except Exception as e:
  print(f'[Error] Failed to save menu data: {e}')
  return False

def load_menu_from_file() -> list:
 target_file = MENU_FILE if os.path.exists(MENU_FILE) else LEGACY_MENU_FILE
 if not os.path.exists(target_file):
  return []
 try:
  with open(target_file, 'r', encoding='utf-8') as f:
   data = json.load(f)
  menu_list = []
  for item in data:
   item_type = item.get('type')
   is_avail = item.get('is_available', item.get('available', True))
   if item_type == 'Food' or item_type == 'food' or item.get('category') == 'Food':
    menu_list.append(Food(item['item_id'], item['name'], item['price'], is_spicy=item.get('is_spicy', False), is_available=is_avail))
   elif item_type == 'Drink' or item_type == 'drink' or item.get('category') == 'Drink':
    menu_list.append(Drink(item['item_id'], item['name'], item['price'], size=item.get('size', 'Regular'), is_available=is_avail))
   else:
    menu_list.append(MenuItem(item['item_id'], item['name'], item['price'], category=item.get('category', 'General'), is_available=is_avail))
  return menu_list
 except Exception as e:
  print(f'[Error] Failed to load menu: {e}')
  return []

def save_tables_to_file(tables_list: list) -> bool:
 try:
  os.makedirs('data', exist_ok=True)
  data = [table.to_dict() for table in tables_list]
  with open(TABLE_FILE, 'w', encoding='utf-8') as f:
   json.dump(data, f, indent=4, ensure_ascii=False)
  with open(LEGACY_TABLE_FILE, 'w', encoding='utf-8') as f:
   json.dump(data, f, indent=4, ensure_ascii=False)
  return True
 except Exception as e:
  print(f'[Error] Failed to save table data: {e}')
  return False

def load_tables_from_file() -> list:
 target_file = TABLE_FILE if os.path.exists(TABLE_FILE) else LEGACY_TABLE_FILE
 if not os.path.exists(target_file):
  return []
 try:
  with open(target_file, 'r', encoding='utf-8') as f:
   data = json.load(f)
  tables_list = []
  for t in data:
   raw_num = t.get('table_number', 1)
   num = int(str(raw_num).replace('T', '')) if str(raw_num).replace('T', '').isdigit() else 1
   cap = t.get('capacity', 4)
   is_avail = t.get('is_available', t.get('status') == 'Available')
   active_id = t.get('active_order_id')
   tables_list.append(Table(table_number=num, capacity=cap, is_available=is_avail, active_order_id=active_id))
  return tables_list
 except Exception as e:
  print(f'[Error] Failed to load tables: {e}')
  return []

def save_orders_to_file(orders_list: list) -> bool:
 try:
  os.makedirs('data', exist_ok=True)
  data = [order.to_dict() if hasattr(order, 'to_dict') else order for order in orders_list]
  with open(ORDER_FILE, 'w', encoding='utf-8') as f:
   json.dump(data, f, indent=4, ensure_ascii=False)
  with open(LEGACY_ORDER_FILE, 'w', encoding='utf-8') as f:
   json.dump(data, f, indent=4, ensure_ascii=False)
  return True
 except Exception as e:
  print(f'[Error] Failed to save order data: {e}')
  return False

def load_orders_from_file() -> list:
 target_file = ORDER_FILE if os.path.exists(ORDER_FILE) else LEGACY_ORDER_FILE
 if not os.path.exists(target_file):
  return []
 try:
  with open(target_file, 'r', encoding='utf-8') as f:
   data = json.load(f)
  return [Order.from_dict(order_data) for order_data in data]
 except Exception as e:
  print(f'[Error] Failed to load orders: {e}')
  return []

def load_menu():
 target = LEGACY_MENU_FILE if os.path.exists(LEGACY_MENU_FILE) else MENU_FILE
 try:
  with open(target, 'r', encoding='utf-8') as file:
   return json.load(file)
 except (FileNotFoundError, json.JSONDecodeError):
  return []

def load_tables():
 target = LEGACY_TABLE_FILE if os.path.exists(LEGACY_TABLE_FILE) else TABLE_FILE
 try:
  with open(target, 'r', encoding='utf-8') as file:
   return json.load(file)
 except (FileNotFoundError, json.JSONDecodeError):
  return []

def save_json(filename, data):
 try:
  os.makedirs('data', exist_ok=True)
  with open(os.path.join('data', filename), 'w', encoding='utf-8') as file:
   json.dump(data, file, indent=4)
  return True
 except OSError:
  return False

def load_orders():
 target = LEGACY_ORDER_FILE if os.path.exists(LEGACY_ORDER_FILE) else ORDER_FILE
 try:
  with open(target, 'r', encoding='utf-8') as file:
   return json.load(file)
 except (FileNotFoundError, json.JSONDecodeError):
  return []

def save_orders(orders_data):
 return save_orders_to_file(orders_data)

def save_sales(order_id, receipt_id, date, total, currency, payment_method):
 try:
  os.makedirs('data', exist_ok=True)
  file_exists = os.path.exists(SALES_FILE)
  with open(SALES_FILE, 'a', newline='', encoding='utf-8') as file:
   writer = csv.writer(file)
   if not file_exists or os.path.getsize(SALES_FILE) == 0:
    writer.writerow(['order_id', 'receipt_id', 'date', 'total', 'currency', 'payment_method'])
   writer.writerow([order_id, receipt_id, date, total, currency, payment_method])
  return True
 except OSError as e:
  print(f'[Error] Error saving sales data: {e}')
  return False

def load_sales():
 if not os.path.exists(SALES_FILE):
  return []
 try:
  with open(SALES_FILE, 'r', encoding='utf-8') as file:
   reader = csv.DictReader(file)
   return [row for row in reader]
 except Exception:
  return []

def daily_sales_report(date):
 sales = load_sales()
 daily_sales = []
 usd_total = 0.0
 khr_total = 0.0
 for sale in sales:
  if sale.get('date') == date:
   daily_sales.append(sale)
   if sale.get('currency') == 'USD':
    usd_total += float(sale.get('total', 0))
   elif sale.get('currency') == 'KHR':
    khr_total += float(sale.get('total', 0))
 totals = {'USD': round(usd_total, 2), 'KHR': round(khr_total, 2)}
 return (daily_sales, totals)

def monthly_sales_report(month):
 sales = load_sales()
 monthly_sales = []
 usd_total = 0.0
 khr_total = 0.0
 for sale in sales:
  if str(sale.get('date', '')).startswith(month):
   monthly_sales.append(sale)
   if sale.get('currency') == 'USD':
    usd_total += float(sale.get('total', 0))
   elif sale.get('currency') == 'KHR':
    khr_total += float(sale.get('total', 0))
 totals = {'USD': round(usd_total, 2), 'KHR': round(khr_total, 2)}
 return (monthly_sales, totals)

def calculate_total_sales():
 sales = load_sales()
 usd_total = 0.0
 khr_total = 0.0
 for sale in sales:
  if sale.get('currency') == 'USD':
   usd_total += float(sale.get('total', 0))
  elif sale.get('currency') == 'KHR':
   khr_total += float(sale.get('total', 0))
 return {'USD': round(usd_total, 2), 'KHR': round(khr_total, 2)}

def popular_items(orders=None):
 if orders is None:
  orders = load_orders()
 menu = load_menu()
 food_counts = {}
 drink_counts = {}
 for order in orders:
  items = order.get('items', [])
  for item in items:
   item_id = item.get('item_id')
   item_name = item.get('name', str(item_id))
   item_qty = item.get('quantity', 1)
   category = None
   for menu_item in menu:
    if str(menu_item.get('item_id')).upper() == str(item_id).upper():
     category = menu_item.get('category')
     break
   if not category:
    category = 'Food' if str(item_id).upper().startswith('F') else 'Drink'
   if category == 'Food':
    food_counts[item_name] = food_counts.get(item_name, 0) + item_qty
   elif category == 'Drink':
    drink_counts[item_name] = drink_counts.get(item_name, 0) + item_qty
 popular_food = ''
 popular_drink = ''
 food_quantity = 0
 drink_quantity = 0
 for name, quantity in food_counts.items():
  if quantity > food_quantity:
   food_quantity = quantity
   popular_food = name
 for name, quantity in drink_counts.items():
  if quantity > drink_quantity:
   drink_quantity = quantity
   popular_drink = name
 return (popular_food, popular_drink)

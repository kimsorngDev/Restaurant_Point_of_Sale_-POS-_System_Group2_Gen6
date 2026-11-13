# ==============================================================================
# AUTHOR: Ra Daro & Kim Sorng
# MODULE: Data Persistence Handler
# DESCRIPTION: Handles saving and loading menu, table, and order data to/from
#              JSON files using robust try-except error handling.
# ==============================================================================

import json
import os
from models.menu import Food, Drink, MenuItem
from models.table import Table
from models.order import Order

MENU_FILE = "data/menu_data.json"
TABLE_FILE = "data/table_data.json"
ORDER_FILE = "data/order_data.json"


# --- MENU FILE STORAGE HANDLER ---

def save_menu_to_file(menu_list: list) -> bool:
    """Saves a list of MenuItem objects to a JSON file."""
    try:
        os.makedirs("data", exist_ok=True)
        data = [item.to_dict() for item in menu_list]
        with open(MENU_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("Menu data successfully saved to JSON file.")
        return True
    except PermissionError:
        print(f"[Error] Permission denied when writing to '{MENU_FILE}'.")
    except Exception as e:
        print(f"[Error] Failed to save menu data: {e}")
    return False


def load_menu_from_file() -> list:
    """Loads menu items from a JSON file and returns object instances."""
    if not os.path.exists(MENU_FILE):
        print(f"⚠️ [Warning] File '{MENU_FILE}' not found. Returning empty menu list.")
        return []

    try:
        with open(MENU_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        menu_list = []
        for item in data:
            item_type = item.get("type")
            if item_type == "Food":
                menu_list.append(Food(item["item_id"], item["name"], item["price"], item.get("is_vegetarian", False)))
            elif item_type == "Drink":
                menu_list.append(Drink(item["item_id"], item["name"], item["price"], item.get("is_cold", True)))
            else:
                menu_list.append(MenuItem(item["item_id"], item["name"], item["price"]))

        print("Menu data successfully loaded from JSON file.")
        return menu_list

    except json.JSONDecodeError:
        print(f"[Error] File '{MENU_FILE}' contains invalid JSON formatting.")
    except KeyError as e:
        print(f"[Error] Missing required data field in JSON: {e}")
    except Exception as e:
        print(f"[Unexpected Error] Failed to load menu: {e}")
    
    return []


# --- TABLE FILE STORAGE HANDLER ---

def save_tables_to_file(tables_list: list) -> bool:
    """Saves a list of Table objects to a JSON file."""
    try:
        os.makedirs("data", exist_ok=True)
        data = [table.to_dict() for table in tables_list]
        with open(TABLE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("Table data successfully saved to JSON file.")
        return True
    except PermissionError:
        print(f"[Error] Permission denied when writing to '{TABLE_FILE}'.")
    except Exception as e:
        print(f"[Error] Failed to save table data: {e}")
    return False


def load_tables_from_file() -> list:
    """Loads table data from a JSON file and returns Table object instances."""
    if not os.path.exists(TABLE_FILE):
        print(f"⚠️ [Warning] File '{TABLE_FILE}' not found. Returning empty table list.")
        return []

    try:
        with open(TABLE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        tables_list = [
            Table(t["table_number"], t["capacity"], t["is_available"]) 
            for t in data
        ]
        print("Table data successfully loaded from JSON file.")
        return tables_list

    except json.JSONDecodeError:
        print(f"[Error] File '{TABLE_FILE}' contains invalid JSON formatting.")
    except KeyError as e:
        print(f"[Error] Missing required table attribute in JSON: {e}")
    except Exception as e:
        print(f"[Unexpected Error] Failed to load tables: {e}")
    
    return []


# --- ORDER FILE STORAGE HANDLER ---

def save_orders_to_file(orders_list: list) -> bool:
    """Saves a list of Order objects to a JSON file."""
    try:
        os.makedirs("data", exist_ok=True)
        data = [order.to_dict() for order in orders_list]
        with open(ORDER_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("Order data successfully saved to JSON file.")
        return True
    except PermissionError:
        print(f"[Error] Permission denied when writing to '{ORDER_FILE}'.")
    except Exception as e:
        print(f"[Error] Failed to save order data: {e}")
    return False


def load_orders_from_file() -> list:
    """Loads order data from a JSON file and returns Order object instances."""
    if not os.path.exists(ORDER_FILE):
        print(f"⚠️ [Warning] File '{ORDER_FILE}' not found. Returning empty order list.")
        return []

    try:
        with open(ORDER_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        orders_list = [Order.from_dict(order_data) for order_data in data]
        print("Order data successfully loaded from JSON file.")
        return orders_list

    except json.JSONDecodeError:
        print(f"[Error] File '{ORDER_FILE}' contains invalid JSON formatting.")
    except KeyError as e:
        print(f"[Error] Missing required order attribute in JSON: {e}")
    except Exception as e:
        print(f"[Unexpected Error] Failed to load orders: {e}")

    return []

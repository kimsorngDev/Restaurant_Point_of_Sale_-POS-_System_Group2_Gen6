# ==============================================================================
# AUTHOR: Ra Daro
# MODULE: Menu & Table Management Test Suite
# DESCRIPTION: Entry point script for testing menu and table functionality, 
#              display utilities, object validation, and file persistence.
# ==============================================================================

from data.sample_data import sample_menu, sample_tables
from data_manager import (
    save_menu_to_file, load_menu_from_file,
    save_tables_to_file, load_tables_from_file
)
from models.table import Table


def display_menu(menu_list: list):
    """Utility function to print formatted menu items."""
    print("\n=================== 📋 RESTAURANT MENU ===================")
    if not menu_list:
        print("No menu items available.")
    else:
        for item in menu_list:
            print(item.get_details())
    print("==========================================================")


def display_tables(tables_list: list):
    """Utility function to print formatted table statuses."""
    print("\n=================== 🪑 TABLE STATUS ===================")
    if not tables_list:
        print("No table data available.")
    else:
        for table in tables_list:
            print(table.get_status())
    print("========================================================")


if __name__ == "__main__":
    print("\n=== [STARTING RA DARO MODULE TEST RUN] ===")

    # 1. Test Object Data Validation (Try-Except block)
    print("\n--- 1. Testing Input Validation ---")
    try:
        invalid_table = Table(table_number=99, capacity=-2)
    except ValueError as e:
        print(f"Caught expected validation error: {e}")

    # 2. Display Initial Sample Data
    print("\n--- 2. Displaying Initial Sample Data ---")
    display_menu(sample_menu)
    display_tables(sample_tables)

    # 3. Save Sample Data to JSON Persistence
    print("\n--- 3. Testing File Storage Persistence ---")
    save_menu_to_file(sample_menu)
    save_tables_to_file(sample_tables)

    # 4. Load Data from JSON Files to Verify Persistence
    print("\n--- 4. Loading Saved Data back from JSON ---")
    loaded_menu = load_menu_from_file()
    loaded_tables = load_tables_from_file()

    # 5. Display Loaded Data
    print("\n--- 5. Displaying Loaded Data ---")
    display_menu(loaded_menu)
    display_tables(loaded_tables)

    print("\n=== [MODULE TEST COMPLETED SUCCESSFULLY] ===")
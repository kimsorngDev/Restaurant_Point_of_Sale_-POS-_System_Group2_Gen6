# ==============================================================================
# AUTHOR: Kim Sorng (Group 2, Gen 6)
# MODULE: Main Application Entry Point
# DESCRIPTION: Central interactive POS Terminal loop connecting staff login,
#              menu viewing, table tracking, and order management.
# ==============================================================================

import sys
from auth_manager import AuthManager
from data_manager import (
    load_menu_from_file, save_menu_to_file,
    load_tables_from_file, save_tables_to_file,
    load_orders_from_file, save_orders_to_file
)
from data.sample_data import sample_menu, sample_tables
from order_manager import (
    start_new_order, add_menu_item_to_order,
    remove_item_from_order, update_item_quantity,
    calculate_subtotal, display_order_summary,
    validate_order_for_checkout
)
from menu_table import display_menu, display_tables
from models.order import Order


def load_initial_data():
    """Loads system data, seeding sample data if storage is empty."""
    menu = load_menu_from_file()
    if not menu:
        menu = sample_menu
        save_menu_to_file(menu)

    tables = load_tables_from_file()
    if not tables:
        tables = sample_tables
        save_tables_to_file(tables)

    orders = load_orders_from_file()
    return menu, tables, orders


def display_dashboard(user):
    """Prints the main POS navigation dashboard."""
    print("\n" + "=" * 55)
    print(f"  🍽️ POS TERMINAL - GROUP 2 GEN 6 | User: {user.username} ({user.role})")
    print("=" * 55)
    print(" 1. 📋 View Restaurant Menu")
    print(" 2. 🪑 View Table Status")
    print(" 3. ➕ Start New Order (Dine-In / Takeaway)")
    print(" 4. 📝 Manage Active Order (Add/Remove/Update items)")
    print(" 5. 🧾 View Active Order Receipt Summary")
    print(" 6. 💳 Proceed to Order Checkout")
    print(" 7. 💾 Save All Data to Disk")
    print(" 8. 👤 View Current User Profile")
    print(" 0. 🚪 Logout & Exit")
    print("-" * 55)


def run_pos_terminal():
    """Main application loop."""
    print("\n" + "#" * 60)
    print("   RESTAURANT POINT OF SALE (POS) SYSTEM - GROUP 2 GEN 6   ")
    print("#" * 60)

    # 1. Initialize Managers and Data
    auth = AuthManager()
    menu_list, tables_list, orders_list = load_initial_data()
    active_order: Optional[Order] = None

    # 2. Staff Login Screen (Deliverable 2)
    logged_in_user = auth.render_login_screen()
    if not logged_in_user:
        print("Exiting application. Goodbye!")
        return

    # 3. Interactive Main Loop
    while True:
        display_dashboard(logged_in_user)
        try:
            choice = input("Enter option [0-8]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting session...")
            break

        if choice == "1":
            # Menu Display
            display_menu(menu_list)

        elif choice == "2":
            # Table Display
            display_tables(tables_list)

        elif choice == "3":
            # Start New Order
            print("\n--- Start New Order ---")
            order_type_in = input("Select Type (1 for Dine-In, 2 for Takeaway): ").strip()
            order_type = "Dine-In" if order_type_in == "1" else "Takeaway"

            table_num = None
            if order_type == "Dine-In":
                display_tables(tables_list)
                tbl_in = input("Enter Table Number: ").strip()
                try:
                    table_num = int(tbl_in)
                except ValueError:
                    print("⚠️ Invalid table number.")
                    continue

            notes = input("Enter order notes (optional): ").strip()
            try:
                active_order = start_new_order(
                    order_type=order_type,
                    table_number=table_num,
                    notes=notes,
                    tables_list=tables_list
                )
                orders_list.append(active_order)
                print(f"✅ Created Order #{active_order.order_id} ({active_order.order_type})")
            except ValueError as err:
                print(f"❌ Error starting order: {err}")

        elif choice == "4":
            # Manage Active Order
            if not active_order:
                print("⚠️ No active order selected. Please start an order first (Option 3).")
                continue

            print(f"\n--- Managing Order #{active_order.order_id} ({active_order.order_type}) ---")
            print("  a. Add Item to Order")
            print("  b. Update Item Quantity")
            print("  c. Remove Item from Order")
            action = input("Select action [a/b/c]: ").strip().lower()

            if action == "a":
                display_menu(menu_list)
                try:
                    item_id = int(input("Enter Item ID to add: ").strip())
                    qty = int(input("Enter Quantity: ").strip() or "1")
                    notes = input("Special notes (optional): ").strip()
                    add_menu_item_to_order(
                        order=active_order,
                        item=item_id,
                        quantity=qty,
                        special_notes=notes,
                        menu_list=menu_list
                    )
                    print(f"✅ Added item #{item_id} (x{qty}). Subtotal: ${calculate_subtotal(active_order):.2f}")
                except Exception as e:
                    print(f"❌ Failed to add item: {e}")

            elif action == "b":
                display_order_summary(active_order)
                try:
                    item_id = int(input("Enter Item ID to update: ").strip())
                    new_qty = int(input("Enter new quantity (0 to remove): ").strip())
                    updated = update_item_quantity(active_order, item_id, new_qty)
                    if updated:
                        print(f"✅ Quantity updated. New subtotal: ${calculate_subtotal(active_order):.2f}")
                    else:
                        print("⚠️ Item ID not found in order.")
                except Exception as e:
                    print(f"❌ Failed to update item: {e}")

            elif action == "c":
                display_order_summary(active_order)
                try:
                    item_id = int(input("Enter Item ID to remove: ").strip())
                    if remove_item_from_order(active_order, item_id):
                        print(f"✅ Item #{item_id} removed.")
                    else:
                        print("⚠️ Item ID not found in order.")
                except Exception as e:
                    print(f"❌ Failed to remove item: {e}")

        elif choice == "5":
            # View Active Order Summary
            if not active_order:
                print("⚠️ No active order selected.")
            else:
                display_order_summary(active_order, tax_rate=0.10, discount_percent=0.0)

        elif choice == "6":
            # Proceed to Order Checkout
            if not active_order:
                print("⚠️ No active order to checkout.")
                continue

            try:
                validate_order_for_checkout(active_order)
                display_order_summary(active_order, tax_rate=0.10)
                confirm = input("Confirm payment of total amount? (y/n): ").strip().lower()
                if confirm == "y":
                    active_order.mark_as_paid(payment_reference=f"TXN-{active_order.order_id}-CASH")
                    if active_order.table_number:
                        # Release dining table
                        for t in tables_list:
                            if t.table_number == active_order.table_number:
                                t.release()
                    save_orders_to_file(orders_list)
                    save_tables_to_file(tables_list)
                    print(f"🎉 Order #{active_order.order_id} successfully paid and completed!")
                    active_order = None
            except ValueError as err:
                print(f"❌ Checkout validation failed: {err}")

        elif choice == "7":
            # Save Data
            save_menu_to_file(menu_list)
            save_tables_to_file(tables_list)
            save_orders_to_file(orders_list)
            print("💾 All system data saved to JSON files.")

        elif choice == "8":
            # View Profile
            print(f"\nStaff Details: {logged_in_user.get_details()}")

        elif choice == "0":
            # Logout & Exit
            auth.logout()
            print("👋 Logged out successfully. Thank you for using the POS system!")
            break

        else:
            print("⚠️ Invalid option. Please select 0 through 8.")


def run_demo_mode():
    """Runs a non-interactive automated demonstration of Sprint 1 features."""
    print("\n" + "=" * 60)
    print("      POS SYSTEM - SPRINT 1 AUTOMATED DEMONSTRATION      ")
    print("=" * 60)

    auth = AuthManager()
    menu_list, tables_list, orders_list = load_initial_data()

    # 1. Test Login
    print("\n[Step 1] Authenticating Staff Member...")
    user = auth.authenticate("cashier", "cashier123")
    assert user is not None, "Login failed!"
    print(f" -> Authenticated: {user.get_details()}")

    # 2. Test Menu Display
    print("\n[Step 2] Displaying Restaurant Menu...")
    display_menu(menu_list)

    # 3. Test Table Display
    print("\n[Step 3] Displaying Table Statuses...")
    display_tables(tables_list)

    # 4. Test Starting Order
    print("\n[Step 4] Starting New Dine-In Order (Table 1)...")
    order = start_new_order(order_type="Dine-In", table_number=1, tables_list=tables_list)
    print(f" -> Order #{order.order_id} created for Table {order.table_number}")

    # 5. Test Adding Items
    print("\n[Step 5] Adding Menu Items...")
    add_menu_item_to_order(order, item=101, quantity=2, special_notes="Extra spicy", menu_list=menu_list)
    add_menu_item_to_order(order, item=201, quantity=2, menu_list=menu_list)
    print(f" -> Added 2 items. Subtotal: ${calculate_subtotal(order):.2f}")

    # 6. Test Order Summary
    print("\n[Step 6] Displaying Order Summary...")
    display_order_summary(order, tax_rate=0.10)

    # 7. Test Checkout Validation
    print("\n[Step 7] Validating Order for Checkout...")
    assert validate_order_for_checkout(order) is True
    print(" -> Validation Passed: Order contains items.")

    print("\n" + "=" * 60)
    print("   AUTOMATED DEMONSTRATION COMPLETED WITHOUT ERRORS!   ")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo_mode()
    else:
        run_pos_terminal()


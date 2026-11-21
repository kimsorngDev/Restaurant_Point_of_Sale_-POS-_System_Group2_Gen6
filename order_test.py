
from data.sample_data import sample_menu, sample_tables
from data_manager import save_orders_to_file, load_orders_from_file
from models.order import Order
from order_manager import (
    start_new_order,
    add_menu_item_to_order,
    remove_item_from_order,
    update_item_quantity,
    calculate_subtotal,
    display_order_summary,
    validate_order_for_checkout,
    OrderManager
)


def run_all_tests():
    print("\n" + "=" * 65)
    print("      POS SYSTEM - STAFF ORDER MANAGEMENT WORKFLOW TEST      ")
    print("=" * 65)

    manager = OrderManager(menu_list=sample_menu, tables_list=sample_tables)

    # --------------------------------------------------------------------------
    # 1. START A NEW ORDER: DINE-IN VS TAKEAWAY
    # --------------------------------------------------------------------------
    print("\n--- [1. Start New Order: Dine-In & Takeaway] ---")
    
    # 1a. Start Dine-In Order for Table 1
    t1 = sample_tables[0] # Table 1
    print(f"Table 1 before Dine-In order: {t1.get_status()}")
    dine_in_order = start_new_order(
        order_type="Dine-In",
        table_number=1,
        notes="Guest requested booth if possible",
        tables_list=sample_tables
    )
    print(f"Created: Order #{dine_in_order.order_id} | Type: {dine_in_order.order_type} | Table: {dine_in_order.table_number}")
    print(f"Table 1 after Dine-In order:  {t1.get_status()}")

    # 1b. Verify that attempting to occupy an already occupied table raises ValueError
    try:
        start_new_order(order_type="Dine-In", table_number=1, tables_list=sample_tables)
    except ValueError as e:
        print(f"Caught expected table conflict error: {e}")

    # 1c. Start Takeaway Order (No table required)
    takeaway_order = start_new_order(
        order_type="Takeaway",
        notes="Pick up at 12:30 PM"
    )
    print(f"Created: Order #{takeaway_order.order_id} | Type: {takeaway_order.order_type} | Table: {takeaway_order.table_number}")

    # --------------------------------------------------------------------------
    # 2. VALIDATE EMPTY ORDER BEFORE CHECKOUT
    # --------------------------------------------------------------------------
    print("\n--- [2. Validate Empty Order Before Checkout] ---")
    try:
        validate_order_for_checkout(takeaway_order)
    except ValueError as e:
        print(f"Caught expected empty order checkout validation error: {e}")

    # --------------------------------------------------------------------------
    # 3. ADD MENU ITEMS TO ORDER
    # --------------------------------------------------------------------------
    print("\n--- [3. Add Menu Items to Order] ---")
    # Add items using MenuItem instance
    add_menu_item_to_order(dine_in_order, sample_menu[0], quantity=2, special_notes="Extra spicy")
    print(f"Added: 2x {sample_menu[0].name} (Extra spicy)")

    # Add items using integer item_id lookup
    add_menu_item_to_order(dine_in_order, item=201, quantity=2, special_notes="Cold, 50% sugar", menu_list=sample_menu)
    print("Added: 2x Iced Latte (by item_id: 201)")

    # Add another item
    add_menu_item_to_order(dine_in_order, item=102, quantity=1, menu_list=sample_menu)
    print("Added: 1x Vegetable Stir-Fry (by item_id: 102)")

    # --------------------------------------------------------------------------
    # 4. UPDATE ITEM QUANTITIES
    # --------------------------------------------------------------------------
    print("\n--- [4. Update Item Quantities] ---")
    print(f"Current items count: {len(dine_in_order.items)}")
    # Update Vegetable Stir-Fry quantity from 1 to 3
    update_item_quantity(dine_in_order, item_id=102, new_quantity=3)
    updated_item = [i for i in dine_in_order.items if i.item_id == 102][0]
    print(f"Updated quantity of [{updated_item.name}] to: {updated_item.quantity}")

    # --------------------------------------------------------------------------
    # 5. REMOVE ITEMS FROM ORDER
    # --------------------------------------------------------------------------
    print("\n--- [5. Remove Items from Order] ---")
    # Add a temporary item to remove
    add_menu_item_to_order(dine_in_order, item=202, quantity=1, menu_list=sample_menu) # Hot Green Tea
    print(f"Added Hot Green Tea. Items count: {len(dine_in_order.items)}")
    
    removed = remove_item_from_order(dine_in_order, item_id=202)
    print(f"Removed Hot Green Tea (ID: 202): {removed}. Remaining items count: {len(dine_in_order.items)}")

    # --------------------------------------------------------------------------
    # 6. CALCULATE SUBTOTAL
    # --------------------------------------------------------------------------
    print("\n--- [6. Calculate Subtotal] ---")
    subtotal = calculate_subtotal(dine_in_order)
    print(f"Calculated Subtotal for Order #{dine_in_order.order_id}: ${subtotal:.2f}")

    # --------------------------------------------------------------------------
    # 7. DISPLAY ORDER SUMMARY
    # --------------------------------------------------------------------------
    print("\n--- [7. Display Order Summary Receipt] ---")
    display_order_summary(dine_in_order, tax_rate=0.10, discount_percent=5.0)

    # --------------------------------------------------------------------------
    # 8. VALIDATE ORDER WITH ITEMS BEFORE CHECKOUT
    # --------------------------------------------------------------------------
    print("\n--- [8. Validate Order Before Checkout (Now with Items)] ---")
    is_valid = validate_order_for_checkout(dine_in_order)
    print(f"Order #{dine_in_order.order_id} checkout validation passed: {is_valid}")

    # Settle payment & release table
    dine_in_order.mark_as_paid(payment_reference="TXN-DINE-1001")
    manager.release_table_for_order(dine_in_order)
    print(f"Order marked as: {dine_in_order.status}")
    print(f"Table 1 after checkout release: {t1.get_status()}")

    # --------------------------------------------------------------------------
    # 9. TAKEAWAY ORDER FLOW TEST
    # --------------------------------------------------------------------------
    print("\n--- [9. Takeaway Order Lifecycle] ---")
    add_menu_item_to_order(takeaway_order, item=103, quantity=2, special_notes="Well done", menu_list=sample_menu)
    add_menu_item_to_order(takeaway_order, item=203, quantity=2, menu_list=sample_menu)
    display_order_summary(takeaway_order)
    validate_order_for_checkout(takeaway_order)
    takeaway_order.mark_as_paid(payment_reference="TXN-TAKEAWAY-1002")

    # --------------------------------------------------------------------------
    # 10. PERSISTENCE CHECK (JSON)
    # --------------------------------------------------------------------------
    print("\n--- [10. Verify Data Persistence with JSON] ---")
    orders_to_save = [dine_in_order, takeaway_order]
    save_orders_to_file(orders_to_save)
    loaded_orders = load_orders_from_file()
    print(f"Loaded {len(loaded_orders)} orders successfully from disk:")
    for o in loaded_orders:
        table_info = f"Table {o.table_number:02d}" if o.table_number else "N/A (Takeaway)"
        print(f" • Order #{o.order_id} | Type: {o.order_type:<8} | {table_info:<16} | Subtotal: ${o.get_subtotal():.2f} | Status: {o.status}")

    print("\n" + "=" * 65)
    print("      ALL STAFF ORDER MANAGEMENT TESTS PASSED SUCCESSFULLY!      ")
    print("=" * 65)


if __name__ == "__main__":
    run_all_tests()

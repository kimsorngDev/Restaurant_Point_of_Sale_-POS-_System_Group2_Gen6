import sys
from datetime import datetime
from typing import Optional, List
from auth_manager import AuthManager
from data_manager import (
    load_menu_from_file, save_menu_to_file,
    load_tables_from_file, save_tables_to_file,
    load_orders_from_file, save_orders_to_file,
    daily_sales_report, monthly_sales_report,
    calculate_total_sales, popular_items
)
from data.sample_data import sample_menu, sample_tables
from order_manager import (
    start_new_order, add_menu_item_to_order,
    remove_item_from_order, update_item_quantity,
    calculate_subtotal, display_order_summary,
    validate_order_for_checkout
)
from models.order import Order
from models.menu import Food, Drink, MenuItem
from models.table import Table
from models.payment import Payment, DEFAULT_EXCHANGE_RATE, CURRENCY_USD, CURRENCY_KHR
from services.data_manager import DataManager
from services.menu_table_service import MenuTableService

def display_menu(menu_list: list):
    print('\n=================== 📋 RESTAURANT MENU ===================')
    if not menu_list:
        print('No menu items available.')
    for item in menu_list:
        status = 'Available' if getattr(item, 'is_available', True) else 'Out of Stock'
        cat = getattr(item, 'category', 'Item')
        print(f'[{item.item_id}] {item.name:<22} ${item.price:>6.2f}  ({cat} | {status})')
    print('==========================================================')

def display_tables(tables_list: list):
    print('\n=================== 🪑 TABLE STATUS ===================')
    if not tables_list:
        print('No tables available.')
    for table in tables_list:
        status = '🟢 Available' if table.is_available else f'🔴 Occupied (Order: {getattr(table, "active_order_id", "Active") or "Active"})'
        print(f'Table {table.table_number:02d} | Seats: {table.capacity} | Status: {status}')
    print('========================================================')

def load_initial_data():
    menu = load_menu_from_file()
    if not menu:
        menu = sample_menu
        save_menu_to_file(menu)
    tables = load_tables_from_file()
    if not tables:
        tables = sample_tables
        save_tables_to_file(tables)
    orders = load_orders_from_file()
    return (menu, tables, orders)

def display_dashboard(user):
    print('\n' + '=' * 58)
    print(f'  🍽️ POS TERMINAL - GROUP 2 GEN 6 | User: {user.username} ({user.role})')
    print('=' * 58)
    print(' 1. 📋 View Restaurant Menu')
    print(' 2. 🪑 View Table Status')
    print(' 3. ➕ Start New Order (Dine-In / Takeaway)')
    print(' 4. 📝 Manage Active Order (Add/Remove/Update items)')
    print(' 5. 🧾 View Active Order Summary')
    print(' 6. 💳 Proceed to Checkout & Pay (USD / KHR / Discount)')
    print(' 7. 📊 Sales Reports (Daily, Monthly, Popular Items)')
    if user.role.lower() == 'admin':
        print(' 8. ⚙️ Admin Menu Management (Add, Edit, Toggle, Remove)')
    print(' 9. 💾 Save All Data to Disk')
    print(' 10. 👤 View Current User Profile')
    print(' 0. 🚪 Logout & Exit')
    print('-' * 58)

def handle_admin_menu_management(menu_service: MenuTableService, menu_list: list):
    while True:
        print('\n--- ⚙️ ADMIN MENU MANAGEMENT ---')
        print(' 1. View Full Menu')
        print(' 2. Add New Food Item')
        print(' 3. Add New Drink Item')
        print(' 4. Edit Menu Item (Name / Price)')
        print(' 5. Toggle Item Availability (In Stock / Out of Stock)')
        print(' 6. Remove Menu Item')
        print(' 0. Return to Dashboard')
        choice = input('Select Admin Action [0-6]: ').strip()

        if choice == '1':
            print('\n' + menu_service.display_menu(only_available=False))
        elif choice == '2':
            item_id = input('Enter Item ID (e.g. F05): ').strip().upper()
            name = input('Enter Food Name: ').strip()
            price_str = input('Enter Price ($): ').strip()
            spicy_str = input('Is it spicy? (y/n): ').strip().lower()
            try:
                price = float(price_str)
                is_spicy = spicy_str in ['y', 'yes']
                food = menu_service.add_food(item_id, name, price, is_spicy=is_spicy)
                menu_list.clear()
                menu_list.extend(menu_service.menu)
                save_menu_to_file(menu_list)
                print(f'✅ Successfully added Food: {food}')
            except Exception as e:
                print(f'❌ Error adding food: {e}')
        elif choice == '3':
            item_id = input('Enter Item ID (e.g. D04): ').strip().upper()
            name = input('Enter Drink Name: ').strip()
            price_str = input('Enter Price ($): ').strip()
            size = input('Enter Size (Small/Regular/Large): ').strip() or 'Regular'
            try:
                price = float(price_str)
                drink = menu_service.add_drink(item_id, name, price, size=size)
                menu_list.clear()
                menu_list.extend(menu_service.menu)
                save_menu_to_file(menu_list)
                print(f'✅ Successfully added Drink: {drink}')
            except Exception as e:
                print(f'❌ Error adding drink: {e}')
        elif choice == '4':
            print('\n' + menu_service.display_menu(only_available=False))
            item_id = input('Enter Item ID to Edit: ').strip().upper()
            new_name = input('Enter New Name (leave blank to keep current): ').strip() or None
            new_price_str = input('Enter New Price (leave blank to keep current): ').strip()
            new_price = float(new_price_str) if new_price_str else None
            try:
                updated = menu_service.edit_menu_item(item_id, new_name=new_name, new_price=new_price)
                menu_list.clear()
                menu_list.extend(menu_service.menu)
                save_menu_to_file(menu_list)
                print(f'✅ Item updated: {updated}')
            except Exception as e:
                print(f'❌ Error updating item: {e}')
        elif choice == '5':
            print('\n' + menu_service.display_menu(only_available=False))
            item_id = input('Enter Item ID to Toggle: ').strip().upper()
            status_str = input('Set available? (1 for In Stock, 2 for Out of Stock): ').strip()
            is_avail = (status_str == '1')
            try:
                toggled = menu_service.set_item_availability(item_id, is_avail)
                menu_list.clear()
                menu_list.extend(menu_service.menu)
                save_menu_to_file(menu_list)
                print(f'✅ Item availability updated: {toggled}')
            except Exception as e:
                print(f'❌ Error toggling availability: {e}')
        elif choice == '6':
            print('\n' + menu_service.display_menu(only_available=False))
            item_id = input('Enter Item ID to Remove: ').strip().upper()
            confirm = input(f"Are you sure you want to delete '{item_id}'? (y/n): ").strip().lower()
            if confirm == 'y':
                if menu_service.remove_menu_item(item_id):
                    menu_list.clear()
                    menu_list.extend(menu_service.menu)
                    save_menu_to_file(menu_list)
                    print(f"✅ Item '{item_id}' removed successfully.")
                else:
                    print(f"⚠️ Item '{item_id}' not found.")
        elif choice == '0':
            break

def handle_sales_reports():
    while True:
        print('\n--- 📊 SALES & PERFORMANCE REPORTS ---')
        print(' 1. Daily Sales Report')
        print(' 2. Monthly Sales Report')
        print(' 3. Total Overall Revenue')
        print(' 4. Top Popular Items (Food & Drink)')
        print(' 0. Return to Dashboard')
        choice = input('Select Report [0-4]: ').strip()

        if choice == '1':
            target_date = input(f"Enter Date (YYYY-MM-DD) [Default: {datetime.now().strftime('%Y-%m-%d')}]: ").strip()
            if not target_date:
                target_date = datetime.now().strftime('%Y-%m-%d')
            records, totals = daily_sales_report(target_date)
            print(f'\n--- 📅 DAILY SALES REPORT: {target_date} ---')
            print(f"Total Transactions: {len(records)}")
            print(f"USD Total:          ${totals['USD']:.2f}")
            print(f"KHR Total:          {totals['KHR']:,.0f} KHR")
            if records:
                print('-' * 60)
                print(f"{'Order ID':<10} {'Receipt':<18} {'Total':>12} {'Curr':>6} {'Method':>10}")
                print('-' * 60)
                for r in records:
                    print(f"{r.get('order_id', ''):<10} {r.get('receipt_id', ''):<18} {float(r.get('total', 0)):>12,.2f} {r.get('currency', ''):>6} {r.get('payment_method', ''):>10}")
        elif choice == '2':
            target_month = input(f"Enter Month (YYYY-MM) [Default: {datetime.now().strftime('%Y-%m')}]: ").strip()
            if not target_month:
                target_month = datetime.now().strftime('%Y-%m')
            records, totals = monthly_sales_report(target_month)
            print(f'\n--- 🗓️ MONTHLY SALES REPORT: {target_month} ---')
            print(f"Total Transactions: {len(records)}")
            print(f"USD Total:          ${totals['USD']:.2f}")
            print(f"KHR Total:          {totals['KHR']:,.0f} KHR")
        elif choice == '3':
            totals = calculate_total_sales()
            print('\n--- 💰 ALL-TIME SALES TOTALS ---')
            print(f"USD Overall Revenue: ${totals['USD']:.2f}")
            print(f"KHR Overall Revenue: {totals['KHR']:,.0f} KHR")
        elif choice == '4':
            top_food, top_drink = popular_items()
            print('\n--- 🌟 TOP POPULAR ITEMS ---')
            print(f"Most Popular Food:  {top_food or 'No food sales recorded yet'}")
            print(f"Most Popular Drink: {top_drink or 'No drink sales recorded yet'}")
        elif choice == '0':
            break

def run_pos_terminal():
    print('\n' + '#' * 60)
    print('   RESTAURANT POINT OF SALE (POS) SYSTEM - GROUP 2 GEN 6   ')
    print('#' * 60)
    auth = AuthManager()
    menu_list, tables_list, orders_list = load_initial_data()
    menu_service = MenuTableService(DataManager(), seed_if_empty=False)
    active_order: Optional[Order] = None

    logged_in_user = auth.render_login_screen()
    if not logged_in_user:
        print('Exiting application. Goodbye!')
        return

    while True:
        display_dashboard(logged_in_user)
        try:
            choice = input('Enter option: ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nExiting session...')
            break

        if choice == '1':
            display_menu(menu_list)
        elif choice == '2':
            display_tables(tables_list)
        elif choice == '3':
            print('\n--- Start New Order ---')
            order_type_in = input('Select Type (1 for Dine-In, 2 for Takeaway): ').strip()
            order_type = 'Dine-In' if order_type_in == '1' else 'Takeaway'
            table_num = None
            if order_type == 'Dine-In':
                display_tables(tables_list)
                tbl_in = input('Enter Table Number: ').strip()
                try:
                    table_num = int(tbl_in)
                except ValueError:
                    print('⚠️ Invalid table number.')
                    continue
            notes = input('Enter order notes (optional): ').strip()
            try:
                active_order = start_new_order(order_type=order_type, table_number=table_num, notes=notes, tables_list=tables_list)
                orders_list.append(active_order)
                save_tables_to_file(tables_list)
                print(f'✅ Created Order #{active_order.order_id} ({active_order.order_type})')
            except ValueError as err:
                print(f'❌ Error starting order: {err}')
        elif choice == '4':
            if not active_order:
                print('⚠️ No active order selected. Please start an order first (Option 3).')
                continue
            print(f'\n--- Managing Order #{active_order.order_id} ({active_order.order_type}) ---')
            print('  a. Add Item to Order')
            print('  b. Update Item Quantity')
            print('  c. Remove Item from Order')
            action = input('Select action [a/b/c]: ').strip().lower()
            if action == 'a':
                display_menu(menu_list)
                try:
                    item_id = input('Enter Item ID to add: ').strip()
                    qty = int(input('Enter Quantity: ').strip() or '1')
                    notes = input('Special notes (optional): ').strip()
                    add_menu_item_to_order(order=active_order, item=item_id, quantity=qty, special_notes=notes, menu_list=menu_list)
                    print(f'✅ Added item #{item_id} (x{qty}). Subtotal: ${calculate_subtotal(active_order):.2f}')
                except Exception as e:
                    print(f'❌ Failed to add item: {e}')
            elif action == 'b':
                display_order_summary(active_order)
                try:
                    item_id = input('Enter Item ID to update: ').strip()
                    new_qty = int(input('Enter new quantity (0 to remove): ').strip())
                    updated = update_item_quantity(active_order, item_id, new_qty)
                    if updated:
                        print(f'✅ Quantity updated. New subtotal: ${calculate_subtotal(active_order):.2f}')
                    else:
                        print('⚠️ Item ID not found in order.')
                except Exception as e:
                    print(f'❌ Failed to update item: {e}')
            elif action == 'c':
                display_order_summary(active_order)
                try:
                    item_id = input('Enter Item ID to remove: ').strip()
                    if remove_item_from_order(active_order, item_id):
                        print(f'✅ Item #{item_id} removed.')
                    else:
                        print('⚠️ Item ID not found in order.')
                except Exception as e:
                    print(f'❌ Failed to remove item: {e}')
        elif choice == '5':
            if not active_order:
                print('⚠️ No active order selected.')
            else:
                display_order_summary(active_order, tax_rate=0.1, discount_percent=0.0)
        elif choice == '6':
            if not active_order:
                print('⚠️ No active order to checkout.')
                continue
            try:
                validate_order_for_checkout(active_order)
                subtotal = active_order.get_subtotal()
                print(f'\nOrder Subtotal: ${subtotal:.2f}')
                disc_in = input('Enter Discount Percentage (e.g., 10 for 10%, 0 for none): ').strip()
                discount_pct = float(disc_in) if disc_in else 0.0

                curr_in = input('Select Payment Currency (1 for USD, 2 for KHR): ').strip()
                currency = CURRENCY_KHR if curr_in == '2' else CURRENCY_USD

                method_in = input('Select Payment Method (1 for Cash, 2 for Card, 3 for KHQR): ').strip()
                method_map = {'1': 'Cash', '2': 'Card', '3': 'KHQR'}
                payment_method = method_map.get(method_in, 'Cash')

                payment = Payment(
                    order_id=active_order.order_id,
                    subtotal=subtotal,
                    discount_percent=discount_pct,
                    tax_rate=0.10,
                    currency=currency,
                    payment_method=payment_method
                )

                due_amount = payment.get_payable_amount()
                curr_symbol = '$' if currency == CURRENCY_USD else 'KHR '
                print(f'Total Due: {curr_symbol}{due_amount:,.2f}' if currency == CURRENCY_USD else f'Total Due: {due_amount:,.0f} KHR')

                tendered_in = input(f'Enter Amount Tendered in {currency}: ').strip()
                amount_tendered = float(tendered_in)

                order_items_dict = [item.to_dict() for item in active_order.items]
                table_label = f"Table {active_order.table_number:02d}" if active_order.table_number else "Takeaway"
                receipt_str = payment.generate_receipt(
                    amount_tendered=amount_tendered,
                    items=order_items_dict,
                    cashier_name=logged_in_user.full_name,
                    table_info=table_label,
                    notes=active_order.notes
                )
                print('\n' + receipt_str)

                payment.record_sales(amount_tendered)
                active_order.mark_as_paid(payment_reference=payment.receipt_id)

                if active_order.table_number:
                    for t in tables_list:
                        if t.table_number == active_order.table_number:
                            t.release()
                    save_tables_to_file(tables_list)
                    print(f'🟢 Table {active_order.table_number:02d} is now released and Available.')

                save_orders_to_file(orders_list)
                print(f'🎉 Order #{active_order.order_id} successfully paid and saved to sales records!')
                active_order = None

            except ValueError as err:
                print(f'❌ Payment/Checkout Error: {err}')
        elif choice == '7':
            handle_sales_reports()
        elif choice == '8' and logged_in_user.role.lower() == 'admin':
            handle_admin_menu_management(menu_service, menu_list)
        elif choice == '9':
            save_menu_to_file(menu_list)
            save_tables_to_file(tables_list)
            save_orders_to_file(orders_list)
            print('💾 All system data saved to JSON files.')
        elif choice == '10':
            print(f'\nStaff Details: {logged_in_user.get_details()}')
        elif choice == '0':
            auth.logout()
            print('👋 Logged out successfully. Thank you for using the POS system!')
            break
        else:
            print('⚠️ Invalid option. Please try again.')

def run_demo_mode():
    print('\n' + '=' * 60)
    print('      POS SYSTEM - SPRINT 3 AUTOMATED DEMONSTRATION      ')
    print('=' * 60)
    auth = AuthManager()
    menu_list, tables_list, orders_list = load_initial_data()
    menu_service = MenuTableService(DataManager(), seed_if_empty=False)

    print('\n[1. Authentication & Role Validation]')
    admin_user = auth.authenticate('admin', 'admin123')
    assert admin_user is not None and admin_user.role == 'Admin'
    print(f' -> Authenticated Admin: {admin_user.get_details()}')

    print('\n[2. Admin Menu Management: Add Food & Edit Item]')
    test_food_id = 'F99'
    if menu_service.get_menu_item(test_food_id):
        menu_service.remove_menu_item(test_food_id)
    added_food = menu_service.add_food(test_food_id, 'Khmer Curry', 4.50, is_spicy=True)
    print(f' -> Admin added: {added_food}')
    edited = menu_service.edit_menu_item(test_food_id, new_name='Royal Khmer Curry', new_price=4.75)
    print(f' -> Admin edited: {edited}')
    menu_list.clear()
    menu_list.extend(menu_service.menu)
    save_menu_to_file(menu_list)

    print('\n[3. Table Occupancy: Starting Dine-In Order on Table 1]')
    order = start_new_order(order_type='Dine-In', table_number=1, tables_list=tables_list)
    print(f' -> Created Order #{order.order_id} for Table {order.table_number}')
    assert tables_list[0].is_available is False
    print(f' -> Table 1 status: {tables_list[0].get_status()}')

    print('\n[4. Adding Items & Calculating Subtotal]')
    add_menu_item_to_order(order, item='F01', quantity=2, menu_list=menu_list)
    add_menu_item_to_order(order, item='D01', quantity=2, menu_list=menu_list)
    subtotal = calculate_subtotal(order)
    print(f' -> Subtotal: ${subtotal:.2f}')

    print('\n[5. Billing & Discount Calculation (10% Discount, 10% Tax)]')
    payment_usd = Payment(
        order_id=order.order_id,
        subtotal=subtotal,
        discount_percent=10.0,
        tax_rate=0.10,
        currency=CURRENCY_USD,
        payment_method='Cash'
    )
    tot_usd = payment_usd.calculate_total_usd()
    tot_khr = payment_usd.calculate_total_khr()
    print(f' -> Subtotal:      ${subtotal:.2f}')
    print(f' -> Discount (10%): -${payment_usd.calculate_discount():.2f}')
    print(f' -> Tax (10%):      +${payment_usd.calculate_tax():.2f}')
    print(f' -> Final Total USD: ${tot_usd:.2f}')
    print(f' -> Final Total KHR: {tot_khr:,.0f} KHR')

    print('\n[6. Payment Validation & Change Calculation]')
    try:
        payment_usd.process_payment(tot_usd - 5.0)
    except ValueError as e:
        print(f' -> Caught expected insufficient payment error: {e}')
    pay_res = payment_usd.process_payment(tot_usd + 10.0)
    print(f" -> Payment Success! Tendered: ${tot_usd + 10.0:.2f} | Change USD: ${pay_res['change_usd']:.2f} | Change KHR: {pay_res['change_khr']:,d} KHR")

    print('\n[7. Official Receipt Generation]')
    order_items_dict = [i.to_dict() for i in order.items]
    receipt_txt = payment_usd.generate_receipt(
        amount_tendered=tot_usd + 10.0,
        items=order_items_dict,
        cashier_name=admin_user.full_name,
        table_info=f'Table {order.table_number:02d}'
    )
    print(receipt_txt)

    print('\n[8. Recording Sales to CSV & Completing Order]')
    payment_usd.record_sales(tot_usd + 10.0)
    order.mark_as_paid(payment_reference=payment_usd.receipt_id)
    orders_list.append(order)
    save_orders_to_file(orders_list)
    print(' -> Sales record persisted to data/sales.csv and data/orders.json')

    print('\n[9. Table Release After Checkout]')
    for t in tables_list:
        if t.table_number == order.table_number:
            t.release()
    save_tables_to_file(tables_list)
    assert tables_list[0].is_available is True
    print(f' -> Table 1 after checkout release: {tables_list[0].get_status()}')

    print('\n[10. KHR Currency Payment Test (Exchange Rate 1 USD = 4,000 KHR)]')
    payment_khr = Payment(
        order_id='ORD-KHR-TEST',
        subtotal=10.0,
        discount_percent=0.0,
        tax_rate=0.10,
        currency=CURRENCY_KHR,
        payment_method='KHQR'
    )
    khr_due = payment_khr.get_payable_amount()
    khr_tendered = khr_due + 10000
    khr_res = payment_khr.process_payment(khr_tendered)
    print(f' -> Total Due KHR: {khr_due:,.0f} KHR')
    print(f' -> Tendered KHR:  {khr_tendered:,.0f} KHR')
    print(f" -> Change KHR:    {khr_res['change_khr']:,d} KHR (USD: ${khr_res['change_usd']:.2f})")
    payment_khr.record_sales(khr_tendered)

    print('\n[11. Sales Reports Verification (Daily, Monthly, Popular Items)]')
    today = datetime.now().strftime('%Y-%m-%d')
    records, totals = daily_sales_report(today)
    print(f" -> Today's Sales Count: {len(records)} | USD: ${totals['USD']:.2f} | KHR: {totals['KHR']:,.0f} KHR")
    m_records, m_totals = monthly_sales_report(today[:7])
    print(f" -> Month ({today[:7]}) Count: {len(m_records)} | USD: ${m_totals['USD']:.2f} | KHR: {m_totals['KHR']:,.0f} KHR")
    top_f, top_d = popular_items()
    print(f' -> Top Food: {top_f} | Top Drink: {top_d}')

    print('\n' + '=' * 60)
    print('      ALL SPRINT 3 COMPLETION CRITERIA VERIFIED!      ')
    print('=' * 60)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        run_demo_mode()
    else:
        run_pos_terminal()

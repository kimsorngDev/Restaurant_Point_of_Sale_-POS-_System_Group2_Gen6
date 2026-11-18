from datetime import datetime
from services.data_manager import DataManager
from services.menu_table_service import MenuTableService

def prompt_int(label: str) -> int:
    while True:
        raw = input(label).strip()
        try:
            return int(raw)
        except ValueError:
            print('  Invalid input. Enter a whole number.')
        else:
            pass
        finally:
            pass
    else:
        pass

def prompt_float(label: str) -> float:
    while True:
        raw = input(label).strip()
        try:
            return float(raw)
        except ValueError:
            print('  Invalid input. Enter a valid amount (e.g., 4.50).')
        else:
            pass
        finally:
            pass
    else:
        pass

def prompt_yes_no(label: str) -> bool:
    while True:
        raw = input(f'{label} (y/n): ').strip().lower()
        if raw in {'y', 'yes'}:
            return True
        else:
            pass
        if raw in {'n', 'no'}:
            return False
        else:
            pass
        print("  Enter 'y' or 'n'.")
    else:
        pass

def handle_create_order(service: MenuTableService) -> None:
    print('\n--- NEW ORDER ---')
    print('1. Dine-In')
    print('2. Takeaway')
    choice = input('Order type: ').strip()
    order_id = f"ORD-{datetime.now().strftime('%H%M%S')}"
    table_num = None
    if choice == '1':
        order_type = 'dine-in'
        print('\n' + service.display_tables())
        table_num = prompt_int('Select Table Number: ')
    elif choice == '2':
        order_type = 'takeaway'
    else:
        print('  Invalid selection.')
        return
    try:
        session = service.start_order_session(order_id, order_type, table_num)
    except ValueError as err:
        print(f'  [Blocked] {err}')
        return
    else:
        pass
    finally:
        pass
    print(f"\nActive Order: {session['order_id']} ({session['order_type']}" + (f" - Table {session['table_number']})" if session['table_number'] else ')'))
    print('\n' + service.display_menu())
    cart: list[dict] = []
    while True:
        item_id = input("\nEnter Item ID to add (or 'done' to finish): ").strip()
        if item_id.lower() == 'done':
            break
        else:
            pass
        try:
            item = service.validate_item_for_order(item_id)
        except ValueError as err:
            print(f'  [Invalid] {err}')
            continue
        else:
            pass
        finally:
            pass
        qty = prompt_int(f'Quantity for {item.name} (${item.price:.2f}): ')
        try:
            line = service.select_item_for_order(item_id, qty)
            cart.append(line)
            print(f"  + Added {line['quantity']}x {line['name']} @ ${line['unit_price']:.2f} = ${line['line_total']:.2f}")
        except ValueError as err:
            print(f'  [Error] {err}')
        else:
            pass
        finally:
            pass
    else:
        pass
    if not cart:
        if session['table_number']:
            service.complete_order_for_table(session['table_number'])
        else:
            pass
        print('  Order cancelled (no items added).')
        return
    else:
        pass
    total = sum((line['line_total'] for line in cart))
    print('\n=== ORDER CONFIRMED ===')
    print(f"Order ID : {session['order_id']} | Type: {session['order_type']}")
    if session['table_number']:
        print(f"Table    : {session['table_number']} (Status: Occupied)")
    else:
        pass
    for line in cart:
        print(f"  - {line['name']:<20} x{line['quantity']}  (${line['unit_price']:.2f} ea) = ${line['line_total']:.2f}")
    else:
        pass
    print(f'Total    : ${total:.2f}')

def staff_portal(service: MenuTableService) -> None:
    while True:
        print('\n--- STAFF POS MENU ---')
        print('1. View Menu')
        print('2. View Tables')
        print('3. Create Order (Dine-In / Takeaway)')
        print('4. Complete Order & Release Table')
        print('0. Back')
        choice = input('Select: ').strip()
        try:
            if choice == '1':
                print('\n' + service.display_menu())
            elif choice == '2':
                print('\n' + service.display_tables())
            elif choice == '3':
                handle_create_order(service)
            elif choice == '4':
                t_num = prompt_int('Enter Table Number to complete order: ')
                table = service.complete_order_for_table(t_num)
                print(f'  Order completed. {table}')
            elif choice == '0':
                break
            else:
                print('  Invalid option.')
        except ValueError as err:
            print(f'  [Error] {err}')
        else:
            pass
        finally:
            pass
    else:
        pass

def admin_portal(service: MenuTableService) -> None:
    while True:
        print('\n--- ADMIN MENU MANAGEMENT ---')
        print('1. View Full Menu')
        print('2. Add New Menu Item')
        print('3. Edit Item Name / Price')
        print('4. Activate / Deactivate Menu Item')
        print('5. Permanently Remove Menu Item')
        print('0. Back')
        choice = input('Select: ').strip()
        try:
            if choice == '1':
                print('\n' + service.display_menu())
            elif choice == '2':
                kind = input('Type (food/drink): ').strip().lower()
                item_id = input('New Item ID (e.g., F05, D04): ').strip()
                name = input('Item Name: ').strip()
                price = prompt_float('Price ($): ')
                if kind == 'food':
                    spicy = prompt_yes_no('Is it spicy?')
                    created = service.add_food(item_id, name, price, spicy)
                elif kind == 'drink':
                    size = input('Size (Small/Regular/Large) [Regular]: ').strip() or 'Regular'
                    created = service.add_drink(item_id, name, price, size)
                else:
                    print("  Invalid type. Choose 'food' or 'drink'.")
                    continue
                print(f'  Created: {created}')
            elif choice == '3':
                item_id = input('Item ID to edit: ').strip()
                name_in = input('New Name (leave blank to keep current): ').strip()
                price_in = input('New Price (leave blank to keep current): ').strip()
                new_name = name_in if name_in else None
                try:
                    new_price = float(price_in) if price_in else None
                except ValueError:
                    print('  Invalid price entered.')
                    continue
                else:
                    pass
                finally:
                    pass
                updated = service.edit_menu_item(item_id, new_name=new_name, new_price=new_price)
                print(f'  Updated: {updated}')
            elif choice == '4':
                item_id = input('Item ID: ').strip()
                status = prompt_yes_no('Set item as available?')
                updated = service.set_item_availability(item_id, status)
                print(f'  Updated: {updated}')
            elif choice == '5':
                item_id = input('Item ID to remove: ').strip()
                if service.remove_menu_item(item_id):
                    print(f"  Item '{item_id.upper()}' permanently removed.")
                else:
                    print(f"  Item '{item_id.upper()}' not found.")
            elif choice == '0':
                break
            else:
                print('  Invalid option.')
        except ValueError as err:
            print(f'  [Error] {err}')
        else:
            pass
        finally:
            pass
    else:
        pass

def main() -> None:
    service = MenuTableService(DataManager(), seed_if_empty=True)
    while True:
        print('\n=== RESTAURANT POS SYSTEM ===')
        print('1. Staff Mode (Orders & Tables)')
        print('2. Admin Mode (Menu Management)')
        print('0. Exit')
        role = input('Select mode: ').strip()
        if role == '1':
            staff_portal(service)
        elif role == '2':
            admin_portal(service)
        elif role == '0':
            print('POS closed.')
            break
        else:
            print('  Invalid selection.')
    else:
        pass
if __name__ == '__main__':
    main()
else:
    pass

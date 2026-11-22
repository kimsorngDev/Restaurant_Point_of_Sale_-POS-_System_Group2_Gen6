from datetime import datetime
from models.menu import Food, Drink, MenuItem
from models.table import Table
from models.order import Order
from models.payment import Payment, DEFAULT_EXCHANGE_RATE, CURRENCY_USD, CURRENCY_KHR
from services.data_manager import DataManager
from services.menu_table_service import MenuTableService
from data_manager import (
 load_sales, save_sales,
 daily_sales_report, monthly_sales_report,
 calculate_total_sales, popular_items,
 save_tables_to_file, load_tables_from_file
)

def test_discount_calculation():
 p0 = Payment(order_id='101', subtotal=100.0, discount_percent=0.0, tax_rate=0.10)
 assert p0.calculate_discount() == 0.0
 assert p0.calculate_tax() == 10.0
 assert p0.calculate_total_usd() == 110.0

 p10 = Payment(order_id='102', subtotal=100.0, discount_percent=10.0, tax_rate=0.10)
 assert p10.calculate_discount() == 10.0
 assert p10.calculate_tax() == 9.0
 assert p10.calculate_total_usd() == 99.0

 p25 = Payment(order_id='103', subtotal=50.0, discount_percent=20.0, tax_rate=0.10)
 assert p25.calculate_discount() == 10.0
 assert p25.calculate_tax() == 4.0
 assert p25.calculate_total_usd() == 44.0

 try:
  Payment(order_id='104', subtotal=50.0, discount_percent=-5.0)
  assert False
 except ValueError:
  pass

 try:
  Payment(order_id='105', subtotal=50.0, discount_percent=105.0)
  assert False
 except ValueError:
  pass
 print(' Test 1 Passed: Discount and Tax calculation')

def test_currency_and_exchange():
 p = Payment(order_id='201', subtotal=20.0, discount_percent=0.0, tax_rate=0.0, currency=CURRENCY_USD, exchange_rate=4000.0)
 assert p.calculate_total_usd() == 20.0
 assert p.calculate_total_khr() == 80000.0
 assert p.get_payable_amount() == 20.0

 p_khr = Payment(order_id='202', subtotal=20.0, discount_percent=0.0, tax_rate=0.0, currency=CURRENCY_KHR, exchange_rate=4000.0)
 assert p_khr.get_payable_amount() == 80000.0
 print(' Test 2 Passed: USD and KHR conversion at 4,000 KHR/USD')

def test_payment_validation_and_change():
 p_usd = Payment(order_id='301', subtotal=20.0, discount_percent=0.0, tax_rate=0.10, currency=CURRENCY_USD)
 total_due = p_usd.calculate_total_usd()
 assert total_due == 22.0

 try:
  p_usd.process_payment(20.0)
  assert False
 except ValueError as e:
  assert 'Insufficient payment' in str(e)

 res_usd = p_usd.process_payment(30.0)
 assert res_usd['status'] == 'SUCCESS'
 assert res_usd['change_usd'] == 8.0
 assert res_usd['change_khr'] == 32000.0

 p_khr = Payment(order_id='302', subtotal=10.0, discount_percent=0.0, tax_rate=0.0, currency=CURRENCY_KHR)
 due_khr = p_khr.get_payable_amount()
 assert due_khr == 40000.0

 try:
  p_khr.process_payment(35000.0)
  assert False
 except ValueError as e:
  assert 'Insufficient payment' in str(e)

 res_khr = p_khr.process_payment(50000.0)
 assert res_khr['status'] == 'SUCCESS'
 assert res_khr['change_khr'] == 10000.0
 assert res_khr['change_usd'] == 2.5
 print(' Test 3 Passed: Payment validation and dual-currency change')

def test_receipt_generation():
 p = Payment(order_id='401', subtotal=25.0, discount_percent=10.0, tax_rate=0.10, currency=CURRENCY_USD)
 items = [
  {'name': 'Beef Lok Lak', 'quantity': 2, 'price': 10.0},
  {'name': 'Iced Latte', 'quantity': 1, 'price': 5.0}
 ]
 receipt = p.generate_receipt(amount_tendered=30.0, items=items, cashier_name='Kim Sorng', table_info='Table 02')
 assert 'OFFICIAL RECEIPT' in receipt
 assert 'Beef Lok Lak' in receipt
 assert 'Iced Latte' in receipt
 assert 'TOTAL AMOUNT (USD):' in receipt
 assert 'TOTAL AMOUNT (KHR):' in receipt
 assert 'Change Due:' in receipt
 assert 'Kim Sorng' in receipt
 print(' Test 4 Passed: Itemized official receipt generation')

def test_sales_records_and_reports():
 test_date = f"2026-99-99"
 save_sales('ORD-901', 'REC-901', test_date, 15.0, 'USD', 'Cash')
 save_sales('ORD-902', 'REC-902', test_date, 40000, 'KHR', 'Card')

 records, totals = daily_sales_report(test_date)
 assert len(records) >= 2
 assert totals['USD'] >= 15.0
 assert totals['KHR'] >= 40000.0

 m_records, m_totals = monthly_sales_report('2026-99')
 assert len(m_records) >= 2
 assert m_totals['USD'] >= 15.0
 assert m_totals['KHR'] >= 40000.0

 overall = calculate_total_sales()
 assert overall['USD'] > 0
 assert overall['KHR'] > 0
 print(' Test 5 Passed: Sales recording, daily & monthly reports')

def test_popular_items():
 dummy_orders = [
  {
   'order_id': 'D1',
   'items': [
    {'item_id': 'F01', 'name': 'Fried Rice', 'quantity': 4, 'category': 'Food'},
    {'item_id': 'D01', 'name': 'Iced Latte', 'quantity': 2, 'category': 'Drink'}
   ]
  },
  {
   'order_id': 'D2',
   'items': [
    {'item_id': 'F01', 'name': 'Fried Rice', 'quantity': 3, 'category': 'Food'},
    {'item_id': 'F02', 'name': 'Fish Amok', 'quantity': 2, 'category': 'Food'},
    {'item_id': 'D01', 'name': 'Iced Latte', 'quantity': 5, 'category': 'Drink'}
   ]
  }
 ]
 top_food, top_drink = popular_items(dummy_orders)
 assert top_food == 'Fried Rice'
 assert top_drink == 'Iced Latte'
 print(' Test 6 Passed: Popular items report')

def test_table_release():
 table = Table(table_number=10, capacity=4, is_available=True)
 assert table.is_available is True
 table.occupy(order_id='ORD-999')
 assert table.is_available is False
 assert table.active_order_id == 'ORD-999'
 table.release()
 assert table.is_available is True
 assert table.active_order_id is None
 print(' Test 7 Passed: Table occupancy and release after checkout')

def test_admin_menu_management():
 storage = DataManager(menu_path='data/test_menu.json', table_path='data/test_tables.json')
 service = MenuTableService(storage, seed_if_empty=False)
 test_id = 'T99'
 if service.get_menu_item(test_id):
  service.remove_menu_item(test_id)

 food = service.add_food(test_id, 'Test Spring Rolls', 3.50, is_spicy=False)
 assert food.name == 'Test Spring Rolls'
 assert service.get_menu_item(test_id) is not None

 service.edit_menu_item(test_id, new_name='Crispy Spring Rolls', new_price=4.00)
 updated = service.get_menu_item(test_id)
 assert updated.name == 'Crispy Spring Rolls'
 assert updated.price == 4.00

 service.set_item_availability(test_id, False)
 assert service.get_menu_item(test_id).is_available is False

 removed = service.remove_menu_item(test_id)
 assert removed is True
 assert service.get_menu_item(test_id) is None
 print(' Test 8 Passed: Admin menu management (add, edit, toggle, remove)')

if __name__ == '__main__':
 print('=' * 65)
 print('  RESTAURANT POS - SPRINT 3 VERIFICATION SUITE   ')
 print('=' * 65)
 test_discount_calculation()
 test_currency_and_exchange()
 test_payment_validation_and_change()
 test_receipt_generation()
 test_sales_records_and_reports()
 test_popular_items()
 test_table_release()
 test_admin_menu_management()
 print('=' * 65)
 print('  ALL SPRINT 3 DELIVERABLES VERIFIED SUCCESSFULLY!  ')
 print('=' * 65)

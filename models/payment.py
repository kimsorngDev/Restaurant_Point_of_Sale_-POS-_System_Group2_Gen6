from datetime import datetime
from typing import List, Dict, Any, Optional

DEFAULT_EXCHANGE_RATE = 4000.0
CURRENCY_USD = 'USD'
CURRENCY_KHR = 'KHR'
VALID_CURRENCIES = [CURRENCY_USD, CURRENCY_KHR]
VALID_PAYMENT_METHODS = ['Cash', 'Card', 'KHQR']

class Payment:
 def __init__(
  self,
  order_id: Any,
  subtotal: float,
  discount_percent: float = 0.0,
  tax_rate: float = 0.10,
  currency: str = CURRENCY_USD,
  payment_method: str = 'Cash',
  exchange_rate: float = DEFAULT_EXCHANGE_RATE,
  receipt_id: Optional[str] = None
 ):
  if subtotal < 0:
   raise ValueError('Subtotal cannot be negative.')
  if discount_percent < 0 or discount_percent > 100:
   raise ValueError('Discount percentage must be between 0 and 100.')
  if tax_rate < 0:
   raise ValueError('Tax rate cannot be negative.')
  if exchange_rate <= 0:
   raise ValueError('Exchange rate must be positive.')

  clean_currency = currency.strip().upper()
  if clean_currency not in VALID_CURRENCIES:
   raise ValueError(f"Invalid currency '{currency}'. Must be USD or KHR.")

  clean_method = payment_method.strip().title() if payment_method.strip().upper() != 'KHQR' else 'KHQR'
  if clean_method not in VALID_PAYMENT_METHODS:
   clean_method = 'Cash'

  self.order_id = str(order_id)
  self.subtotal = round(float(subtotal), 2)
  self.discount_percent = float(discount_percent)
  self.tax_rate = float(tax_rate)
  self.currency = clean_currency
  self.payment_method = clean_method
  self.exchange_rate = float(exchange_rate)
  self.receipt_id = receipt_id or f"REC-{datetime.now().strftime('%Y%m%d%H%M%S')}-{self.order_id}"
  self.payment_date = datetime.now().strftime('%Y-%m-%d')
  self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

 def calculate_discount(self) -> float:
  return round(self.subtotal * (self.discount_percent / 100.0), 2)

 def calculate_tax(self) -> float:
  taxable = max(0.0, self.subtotal - self.calculate_discount())
  return round(taxable * self.tax_rate, 2)

 def calculate_total_usd(self) -> float:
  taxable = max(0.0, self.subtotal - self.calculate_discount())
  return round(taxable + self.calculate_tax(), 2)

 def calculate_total_khr(self) -> float:
  return round(self.calculate_total_usd() * self.exchange_rate)

 def get_payable_amount(self) -> float:
  if self.currency == CURRENCY_KHR:
   return self.calculate_total_khr()
  return self.calculate_total_usd()

 def process_payment(self, amount_tendered: float) -> Dict[str, Any]:
  total_usd = self.calculate_total_usd()
  total_khr = self.calculate_total_khr()
  payable = self.get_payable_amount()

  if amount_tendered < payable:
   curr_symbol = '$' if self.currency == CURRENCY_USD else 'KHR '
   raise ValueError(
    f"Insufficient payment: Tendered {curr_symbol}{amount_tendered:.2f}, but total due is {curr_symbol}{payable:.2f}."
   )

  if self.currency == CURRENCY_USD:
   change_usd = round(amount_tendered - total_usd, 2)
   change_khr = round(change_usd * self.exchange_rate)
  else:
   change_khr = round(amount_tendered - total_khr)
   change_usd = round(change_khr / self.exchange_rate, 2)

  return {
   'status': 'SUCCESS',
   'receipt_id': self.receipt_id,
   'order_id': self.order_id,
   'date': self.payment_date,
   'timestamp': self.timestamp,
   'subtotal': self.subtotal,
   'discount_percent': self.discount_percent,
   'discount_amount': self.calculate_discount(),
   'tax_amount': self.calculate_tax(),
   'total_usd': total_usd,
   'total_khr': total_khr,
   'currency': self.currency,
   'payment_method': self.payment_method,
   'amount_tendered': amount_tendered,
   'change_usd': change_usd,
   'change_khr': change_khr
  }

 def generate_receipt(
  self,
  amount_tendered: float,
  items: Optional[List[Dict[str, Any]]] = None,
  cashier_name: str = 'Staff',
  table_info: str = 'Dine-In',
  notes: str = ''
 ) -> str:
  res = self.process_payment(amount_tendered)
  lines = [
   '=' * 60,
   '    RESTAURANT POINT OF SALE (POS)    ',
   '      OFFICIAL RECEIPT      ',
   '=' * 60,
   f"Receipt No:  {res['receipt_id']}",
   f"Order ID:  {res['order_id']}",
   f"Date & Time:  {res['timestamp']}",
   f"Service Type: {table_info}",
   f"Cashier:   {cashier_name}",
  ]
  if notes:
   lines.append(f'Notes:   {notes}')
  lines.append('-' * 60)
  lines.append(f"{'Item':<26} {'Qty':>5} {'Unit ($)':>12} {'Total ($)':>13}")
  lines.append('-' * 60)

  if items:
   for item in items:
    name = str(item.get('name', 'Item'))[:25]
    qty = int(item.get('quantity', 1))
    price = float(item.get('price', item.get('unit_price', 0.0)))
    line_total = round(price * qty, 2)
    lines.append(f'{name:<26} {qty:>5} {price:>12.2f} {line_total:>13.2f}')
  else:
   lines.append(f"{'Order Items':<26} {'1':>5} {self.subtotal:>12.2f} {self.subtotal:>13.2f}")

  lines.append('-' * 60)
  lines.append(f"{'Subtotal:':<40} ${self.subtotal:>17.2f}")
  if self.discount_percent > 0:
   lines.append(f"{f'Discount ({self.discount_percent:g}%):':<40} -${res['discount_amount']:>16.2f}")
  lines.append(f"{f'Tax ({self.tax_rate*100:g}%):':<40} ${res['tax_amount']:>17.2f}")
  lines.append('=' * 60)
  lines.append(f"{'TOTAL AMOUNT (USD):':<40} ${res['total_usd']:>17.2f}")
  lines.append(f"{'TOTAL AMOUNT (KHR):':<40} {res['total_khr']:>14,d} KHR")
  lines.append('-' * 60)
  curr_label = 'USD ($)' if self.currency == CURRENCY_USD else 'KHR (៛)'
  lines.append(f"Payment Method: {res['payment_method']} ({curr_label})")
  lines.append(f"Amount Tendered: {amount_tendered:>37,.2f}")
  if self.currency == CURRENCY_USD:
   lines.append(f"Change Due:  ${res['change_usd']:>36.2f}")
   lines.append(f"Change in KHR: {res['change_khr']:>33,d} KHR")
  else:
   lines.append(f"Change Due (KHR):{res['change_khr']:>32,d} KHR")
   lines.append(f"Change in USD: ${res['change_usd']:>35.2f}")
  lines.append('=' * 60)
  lines.append('    Thank you for dining with us! Please come again! ')
  lines.append('=' * 60)
  return '\n'.join(lines)

 def record_sales(self, amount_tendered: float) -> bool:
  from data_manager import save_sales
  res = self.process_payment(amount_tendered)
  total_recorded = res['total_usd'] if self.currency == CURRENCY_USD else res['total_khr']
  return save_sales(
   order_id=self.order_id,
   receipt_id=self.receipt_id,
   date=self.payment_date,
   total=total_recorded,
   currency=self.currency,
   payment_method=self.payment_method
  )

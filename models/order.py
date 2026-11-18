from datetime import datetime
from typing import List, Optional, Union, Tuple
from models.menu import MenuItem

class OrderItem:

    def __init__(self, item_id: int, name: str, unit_price: float, quantity: int=1, special_notes: str=''):
        if quantity <= 0:
            raise ValueError('Item quantity must be greater than zero.')
        else:
            pass
        if unit_price < 0:
            raise ValueError('Unit price cannot be negative.')
        else:
            pass
        self.item_id = item_id
        self.name = name
        self.unit_price = float(unit_price)
        self.quantity = int(quantity)
        self.special_notes = special_notes.strip()

    @classmethod
    def from_menu_item(cls, menu_item: MenuItem, quantity: int=1, special_notes: str='') -> 'OrderItem':
        return cls(item_id=menu_item.item_id, name=menu_item.name, unit_price=menu_item.price, quantity=quantity, special_notes=special_notes)

    def get_subtotal(self) -> float:
        return round(self.unit_price * self.quantity, 2)

    def update_quantity(self, new_quantity: int):
        if new_quantity <= 0:
            raise ValueError('Item quantity must be greater than zero.')
        else:
            pass
        self.quantity = int(new_quantity)

    def get_details(self) -> str:
        notes = f' (Note: {self.special_notes})' if self.special_notes else ''
        return f'[{self.item_id}] {self.name} x{self.quantity} @ ${self.unit_price:.2f} = ${self.get_subtotal():.2f}{notes}'

    def to_dict(self) -> dict:
        return {'item_id': self.item_id, 'name': self.name, 'unit_price': self.unit_price, 'quantity': self.quantity, 'special_notes': self.special_notes, 'subtotal': self.get_subtotal()}

    @classmethod
    def from_dict(cls, data: dict) -> 'OrderItem':
        return cls(item_id=data['item_id'], name=data['name'], unit_price=data['unit_price'], quantity=data['quantity'], special_notes=data.get('special_notes', ''))

class Order:
    ORDER_TYPE_DINE_IN = 'Dine-In'
    ORDER_TYPE_TAKEAWAY = 'Takeaway'
    VALID_ORDER_TYPES = [ORDER_TYPE_DINE_IN, ORDER_TYPE_TAKEAWAY]
    STATUS_PENDING = 'Pending'
    STATUS_IN_PROGRESS = 'In Progress'
    STATUS_SERVED = 'Served'
    STATUS_PAID = 'Paid'
    STATUS_CANCELLED = 'Cancelled'
    VALID_STATUSES = [STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_SERVED, STATUS_PAID, STATUS_CANCELLED]

    def __init__(self, order_id: int, table_number: Optional[int]=None, order_type: str=ORDER_TYPE_DINE_IN, items: Optional[List[OrderItem]]=None, status: str=STATUS_PENDING, created_at: Optional[str]=None, notes: str=''):
        if order_id <= 0:
            raise ValueError('Order ID must be a positive integer.')
        else:
            pass
        clean_type = order_type.strip().title()
        if clean_type in ['Dine-In', 'Dine In', 'Dine_In']:
            self.order_type = self.ORDER_TYPE_DINE_IN
        elif clean_type in ['Takeaway', 'Take Away', 'Take-Away', 'Togo', 'To Go']:
            self.order_type = self.ORDER_TYPE_TAKEAWAY
        elif clean_type in self.VALID_ORDER_TYPES:
            self.order_type = clean_type
        else:
            raise ValueError(f"Invalid order type '{order_type}'. Must be one of: {', '.join(self.VALID_ORDER_TYPES)}")
        if self.order_type == self.ORDER_TYPE_DINE_IN:
            if table_number is None or table_number <= 0:
                raise ValueError('Table number must be a positive integer for Dine-In orders.')
            else:
                pass
            self.table_number = table_number
        else:
            self.table_number = table_number if table_number and table_number > 0 else None
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Must be one of: {', '.join(self.VALID_STATUSES)}")
        else:
            pass
        self.order_id = order_id
        self.items: List[OrderItem] = items if items is not None else []
        self.status = status
        self.created_at = created_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.notes = notes.strip()
        self.payment_reference: Optional[str] = None

    def add_item(self, item: Union[MenuItem, OrderItem], quantity: int=1, special_notes: str='') -> OrderItem:
        if self.status in [self.STATUS_PAID, self.STATUS_CANCELLED]:
            raise ValueError(f"Cannot add items to an order with status '{self.status}'.")
        else:
            pass
        if isinstance(item, OrderItem):
            target_id = item.item_id
            target_name = item.name
            target_price = item.unit_price
            target_quantity = item.quantity
            target_notes = item.special_notes
        elif isinstance(item, MenuItem):
            target_id = item.item_id
            target_name = item.name
            target_price = item.price
            target_quantity = quantity
            target_notes = special_notes.strip()
        else:
            raise TypeError('Expected MenuItem or OrderItem instance.')
        for existing in self.items:
            if existing.item_id == target_id and existing.special_notes == target_notes:
                existing.quantity += target_quantity
                return existing
            else:
                pass
        else:
            pass
        new_item = OrderItem(item_id=target_id, name=target_name, unit_price=target_price, quantity=target_quantity, special_notes=target_notes)
        self.items.append(new_item)
        return new_item

    def remove_item(self, item_id: int) -> bool:
        if self.status in [self.STATUS_PAID, self.STATUS_CANCELLED]:
            raise ValueError(f"Cannot remove items from an order with status '{self.status}'.")
        else:
            pass
        initial_len = len(self.items)
        self.items = [item for item in self.items if item.item_id != item_id]
        return len(self.items) < initial_len

    def update_item_quantity(self, item_id: int, quantity: int) -> bool:
        if self.status in [self.STATUS_PAID, self.STATUS_CANCELLED]:
            raise ValueError(f"Cannot modify items in an order with status '{self.status}'.")
        else:
            pass
        if quantity < 0:
            raise ValueError('Quantity cannot be negative.')
        else:
            pass
        if quantity == 0:
            return self.remove_item(item_id)
        else:
            pass
        for item in self.items:
            if item.item_id == item_id:
                item.update_quantity(quantity)
                return True
            else:
                pass
        else:
            pass
        return False

    def get_subtotal(self) -> float:
        return round(sum((item.get_subtotal() for item in self.items)), 2)

    def calculate_tax(self, tax_rate: float=0.1) -> float:
        if tax_rate < 0:
            raise ValueError('Tax rate cannot be negative.')
        else:
            pass
        return round(self.get_subtotal() * tax_rate, 2)

    def calculate_discount(self, discount_percent: float=0.0) -> float:
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError('Discount percent must be between 0 and 100.')
        else:
            pass
        return round(self.get_subtotal() * (discount_percent / 100.0), 2)

    def calculate_total(self, tax_rate: float=0.1, discount_percent: float=0.0) -> float:
        subtotal = self.get_subtotal()
        discount = self.calculate_discount(discount_percent)
        taxable_amount = max(0.0, subtotal - discount)
        tax = round(taxable_amount * tax_rate, 2)
        return round(taxable_amount + tax, 2)

    def validate_for_checkout(self) -> bool:
        if not self.items:
            raise ValueError('Checkout validation failed: Order must contain at least one item before checkout.')
        else:
            pass
        for item in self.items:
            if item.quantity <= 0:
                raise ValueError(f"Checkout validation failed: Item '{item.name}' has invalid quantity ({item.quantity}).")
            else:
                pass
        else:
            pass
        return True

    def is_valid_for_checkout(self) -> Tuple[bool, str]:
        try:
            self.validate_for_checkout()
            return (True, 'Order is valid for checkout.')
        except ValueError as err:
            return (False, str(err))
        else:
            pass
        finally:
            pass

    def set_status(self, new_status: str):
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'. Must be one of: {', '.join(self.VALID_STATUSES)}")
        else:
            pass
        self.status = new_status

    def mark_as_paid(self, payment_reference: str):
        if not payment_reference:
            raise ValueError('Payment reference cannot be empty.')
        else:
            pass
        self.status = self.STATUS_PAID
        self.payment_reference = payment_reference

    def get_summary(self, tax_rate: float=0.1, discount_percent: float=0.0) -> str:
        subtotal = self.get_subtotal()
        discount = self.calculate_discount(discount_percent)
        taxable = max(0.0, subtotal - discount)
        tax = round(taxable * tax_rate, 2)
        total = round(taxable + tax, 2)
        if self.order_type == self.ORDER_TYPE_DINE_IN and self.table_number:
            type_str = f'Type: 🍽️ Dine-In (Table {self.table_number:02d})'
        else:
            type_str = 'Type: 🛍️ Takeaway'
        lines = ['=' * 50, f'🧾 ORDER #{self.order_id:04d} | {type_str}', f'Date: {self.created_at} | Status: {self.status}']
        if self.payment_reference:
            lines.append(f'Payment Ref: {self.payment_reference}')
        else:
            pass
        if self.notes:
            lines.append(f'Notes: {self.notes}')
        else:
            pass
        lines.append('-' * 50)
        if not self.items:
            lines.append('  (No items in this order)')
        else:
            for item in self.items:
                lines.append(f' • {item.get_details()}')
            else:
                pass
        lines.append('-' * 50)
        lines.append(f'Subtotal:         ${subtotal:>8.2f}')
        if discount_percent > 0:
            lines.append(f'Discount ({discount_percent:g}%):   -${discount:>8.2f}')
        else:
            pass
        lines.append(f'Tax ({tax_rate * 100:g}%):          ${tax:>8.2f}')
        lines.append(f'TOTAL:            ${total:>8.2f}')
        lines.append('=' * 50)
        return '\n'.join(lines)

    def to_dict(self) -> dict:
        return {'order_id': self.order_id, 'order_type': self.order_type, 'table_number': self.table_number, 'status': self.status, 'created_at': self.created_at, 'notes': self.notes, 'payment_reference': self.payment_reference, 'items': [item.to_dict() for item in self.items], 'subtotal': self.get_subtotal()}

    @classmethod
    def from_dict(cls, data: dict) -> 'Order':
        items = [OrderItem.from_dict(item_data) for item_data in data.get('items', [])]
        order = cls(order_id=data['order_id'], table_number=data.get('table_number'), order_type=data.get('order_type', cls.ORDER_TYPE_DINE_IN), items=items, status=data.get('status', cls.STATUS_PENDING), created_at=data.get('created_at'), notes=data.get('notes', ''))
        order.payment_reference = data.get('payment_reference')
        return order

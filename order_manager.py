# ==============================================================================
# AUTHOR: Kim Sorng (Group 2, Gen 6)
# MODULE: Order Manager (Service Layer)
# DESCRIPTION: Core functions for staff to create, modify, view, and validate
#              customer orders for Dine-In and Takeaway operations.
# ==============================================================================

from typing import List, Optional, Union
from models.menu import MenuItem
from models.table import Table
from models.order import Order, OrderItem
import itertools

# Internal order ID generator for session management
_order_id_counter = itertools.count(1001)


def generate_order_id() -> int:
    """Generates a sequential order ID starting from 1001."""
    return next(_order_id_counter)


def start_new_order(
    order_type: str = Order.ORDER_TYPE_DINE_IN,
    table_number: Optional[int] = None,
    notes: str = "",
    tables_list: Optional[List[Table]] = None,
    order_id: Optional[int] = None
) -> Order:
    """Starts a new customer order for either Dine-In or Takeaway.
    
    Args:
        order_type: 'Dine-In' or 'Takeaway'.
        table_number: Table number required if Dine-In; optional/ignored for Takeaway.
        notes: Optional staff or customer notes.
        tables_list: Optional list of Table objects to validate availability and occupy.
        order_id: Optional explicit order ID. If None, auto-generated.
        
    Returns:
        Order: The newly created Order instance.
        
    Raises:
        ValueError: If order_type is invalid, if table is missing or occupied for Dine-In.
    """
    clean_type = order_type.strip().title()
    if clean_type in ["Dine-In", "Dine In", "Dine_In"]:
        resolved_type = Order.ORDER_TYPE_DINE_IN
    elif clean_type in ["Takeaway", "Take Away", "Take-Away", "Togo", "To Go"]:
        resolved_type = Order.ORDER_TYPE_TAKEAWAY
    else:
        raise ValueError(
            f"Invalid order type '{order_type}'. Must be 'Dine-In' or 'Takeaway'."
        )

    # Validate Table for Dine-In
    target_table: Optional[Table] = None
    if resolved_type == Order.ORDER_TYPE_DINE_IN:
        if table_number is None or table_number <= 0:
            raise ValueError("Dine-In orders require a valid positive table number.")

        if tables_list is not None:
            matching_tables = [t for t in tables_list if t.table_number == table_number]
            if not matching_tables:
                raise ValueError(f"Table {table_number} does not exist in restaurant layout.")
            target_table = matching_tables[0]
            if not target_table.is_available:
                raise ValueError(f"Table {table_number:02d} is currently occupied.")

    assigned_id = order_id if order_id is not None else generate_order_id()

    # Create Order
    new_order = Order(
        order_id=assigned_id,
        table_number=table_number if resolved_type == Order.ORDER_TYPE_DINE_IN else None,
        order_type=resolved_type,
        notes=notes
    )

    # Occupy table if dine-in
    if target_table is not None:
        target_table.occupy()

    return new_order


def add_menu_item_to_order(
    order: Order,
    item: Union[MenuItem, int],
    quantity: int = 1,
    special_notes: str = "",
    menu_list: Optional[List[MenuItem]] = None
) -> OrderItem:
    """Adds a menu item to the order by MenuItem instance or by item_id.
    
    Args:
        order: The target Order instance.
        item: MenuItem object or integer item_id.
        quantity: Positive number of items to add.
        special_notes: Special preparation instructions (e.g. 'Extra spicy').
        menu_list: Required if item is passed as integer item_id to look up the item.
        
    Returns:
        OrderItem: The created or updated OrderItem.
        
    Raises:
        ValueError: If item is not found, quantity <= 0, or order is closed.
    """
    if isinstance(item, int):
        if not menu_list:
            raise ValueError("A menu_list must be provided when adding items by item_id.")
        matching = [m for m in menu_list if m.item_id == item]
        if not matching:
            raise ValueError(f"Menu item with ID [{item}] not found in menu.")
        menu_item = matching[0]
    elif isinstance(item, MenuItem):
        menu_item = item
    elif isinstance(item, OrderItem):
        return order.add_item(item)
    else:
        raise TypeError("Item must be an instance of MenuItem, OrderItem, or integer item_id.")

    return order.add_item(menu_item, quantity=quantity, special_notes=special_notes)


def remove_item_from_order(order: Order, item_id: int) -> bool:
    """Removes all line items matching item_id from the order.
    
    Args:
        order: The target Order instance.
        item_id: ID of the menu item to remove.
        
    Returns:
        bool: True if item was removed, False if not found.
    """
    return order.remove_item(item_id)


def update_item_quantity(order: Order, item_id: int, new_quantity: int) -> bool:
    """Updates the quantity of an item in the order.
    
    If new_quantity is 0, the item is removed from the order.
    
    Args:
        order: The target Order instance.
        item_id: ID of the item to update.
        new_quantity: New quantity (>= 0).
        
    Returns:
        bool: True if updated or removed, False if item was not found.
        
    Raises:
        ValueError: If new_quantity < 0 or order is already paid/cancelled.
    """
    return order.update_item_quantity(item_id, new_quantity)


def calculate_subtotal(order: Order) -> float:
    """Calculates and returns the subtotal of the order."""
    return order.get_subtotal()


def display_order_summary(
    order: Order,
    tax_rate: float = 0.10,
    discount_percent: float = 0.0
) -> str:
    """Displays and returns the formatted order summary receipt.
    
    Args:
        order: The target Order instance.
        tax_rate: Tax rate percentage as decimal (default 0.10 = 10%).
        discount_percent: Discount percentage (0-100).
        
    Returns:
        str: The formatted summary string.
    """
    summary = order.get_summary(tax_rate=tax_rate, discount_percent=discount_percent)
    print(summary)
    return summary


def validate_order_for_checkout(order: Order) -> bool:
    """Validates that an order contains at least one item before checkout.
    
    Args:
        order: The Order instance to validate.
        
    Returns:
        bool: True if valid.
        
    Raises:
        ValueError: If the order contains no items or has invalid quantities.
    """
    return order.validate_for_checkout()


class OrderManager:
    """High-level service class managing orders, tables, and menu integration."""

    def __init__(
        self,
        menu_list: Optional[List[MenuItem]] = None,
        tables_list: Optional[List[Table]] = None
    ):
        self.menu_list: List[MenuItem] = menu_list if menu_list is not None else []
        self.tables_list: List[Table] = tables_list if tables_list is not None else []
        self.active_orders: List[Order] = []

    def start_order(
        self,
        order_type: str = Order.ORDER_TYPE_DINE_IN,
        table_number: Optional[int] = None,
        notes: str = ""
    ) -> Order:
        """Starts and registers a new order in the manager."""
        order = start_new_order(
            order_type=order_type,
            table_number=table_number,
            notes=notes,
            tables_list=self.tables_list
        )
        self.active_orders.append(order)
        return order

    def add_item(
        self,
        order: Order,
        item: Union[MenuItem, int],
        quantity: int = 1,
        special_notes: str = ""
    ) -> OrderItem:
        """Adds an item to an order."""
        return add_menu_item_to_order(
            order=order,
            item=item,
            quantity=quantity,
            special_notes=special_notes,
            menu_list=self.menu_list
        )

    def remove_item(self, order: Order, item_id: int) -> bool:
        """Removes an item from an order."""
        return remove_item_from_order(order, item_id)

    def update_quantity(self, order: Order, item_id: int, new_quantity: int) -> bool:
        """Updates quantity of an item in an order."""
        return update_item_quantity(order, item_id, new_quantity)

    def get_subtotal(self, order: Order) -> float:
        """Calculates subtotal of an order."""
        return calculate_subtotal(order)

    def print_summary(
        self,
        order: Order,
        tax_rate: float = 0.10,
        discount_percent: float = 0.0
    ) -> str:
        """Prints and returns order summary."""
        return display_order_summary(order, tax_rate, discount_percent)

    def validate_checkout(self, order: Order) -> bool:
        """Validates order has items before checkout."""
        return validate_order_for_checkout(order)

    def release_table_for_order(self, order: Order) -> bool:
        """Releases the dining table associated with an order."""
        if order.table_number and self.tables_list:
            for t in self.tables_list:
                if t.table_number == order.table_number:
                    t.release()
                    return True
        return False


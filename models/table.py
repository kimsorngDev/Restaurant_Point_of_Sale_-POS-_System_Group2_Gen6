"""
models/table.py
Defines the Table model, tracking table number, seating capacity, availability,
and the currently assigned order ID to prevent double-booking occupied tables.
"""


class Table:
    # Initializes a floor table and validates its number and seat capacity
    def __init__(self, table_number: int, capacity: int, is_available: bool = True, active_order_id: str | None = None):
        if table_number <= 0:
            raise ValueError("Table number must be positive.")
        if capacity <= 0:
            raise ValueError("Capacity must be at least 1.")

        self.table_number = int(table_number)
        self.capacity = int(capacity)
        self.is_available = bool(is_available)
        self.active_order_id = active_order_id

    # Locks the table to a dine-in order and blocks duplicate assignments
    def assign_order(self, order_id: str) -> None:
        if not self.is_available or self.active_order_id is not None:
            raise ValueError(
                f"Table {self.table_number} is already occupied (Order: {self.active_order_id})."
            )
        self.is_available = False
        self.active_order_id = order_id

    # Clears the active order and makes the table available again after checkout
    def complete_order(self) -> str | None:
        finished_order = self.active_order_id
        self.is_available = True
        self.active_order_id = None
        return finished_order

    # Serializes table state into a dictionary for JSON storage
    def to_dict(self) -> dict:
        return {
            "table_number": self.table_number,
            "capacity": self.capacity,
            "is_available": self.is_available,
            "active_order_id": self.active_order_id,
        }

    # Formats table number, seat count, and occupancy status for terminal display
    def __str__(self) -> str:
        state = "Available" if self.is_available else f"Occupied (Order: {self.active_order_id})"
        return f"Table {self.table_number:02d} | Seats: {self.capacity} | {state}"
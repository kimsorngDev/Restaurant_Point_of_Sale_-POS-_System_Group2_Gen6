class Table:

 def __init__(self, table_number: int, capacity: int, is_available: bool=True, active_order_id: str | None=None):
  if table_number <= 0:
   raise ValueError('Table number must be positive.')
  if capacity <= 0:
   raise ValueError('Capacity must be at least 1.')
  self.table_number = int(table_number)
  self.capacity = int(capacity)
  self.is_available = bool(is_available)
  self.active_order_id = active_order_id

 def occupy(self, order_id: str | None=None) -> None:
  self.is_available = False
  if order_id is not None:
   self.active_order_id = str(order_id)

 def release(self) -> str | None:
  return self.complete_order()

 def assign_order(self, order_id: str) -> None:
  if not self.is_available or self.active_order_id is not None:
   raise ValueError(f'Table {self.table_number} is already occupied (Order: {self.active_order_id}).')
  self.is_available = False
  self.active_order_id = str(order_id)

 def complete_order(self) -> str | None:
  finished_order = self.active_order_id
  self.is_available = True
  self.active_order_id = None
  return finished_order

 def get_status(self) -> str:
  state = 'Available' if self.is_available else f' Occupied (Order: {self.active_order_id or "Active"})'
  return f'Table {self.table_number:02d} | Seats: {self.capacity} | Status: {state}'

 def to_dict(self) -> dict:
  return {'table_number': self.table_number, 'capacity': self.capacity, 'is_available': self.is_available, 'active_order_id': self.active_order_id}

 def __str__(self) -> str:
  state = 'Available' if self.is_available else f'Occupied (Order: {self.active_order_id})'
  return f'Table {self.table_number:02d} | Seats: {self.capacity} | {state}'

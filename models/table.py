# ==============================================================================
# AUTHOR: Ra Daro
# MODULE: Table Management System (Models)
# DESCRIPTION: Contains the Table class to track seat capacity and status.
# ==============================================================================

class Table:
    """Class representing a dining table in the restaurant."""
    
    def __init__(self, table_number: int, capacity: int, is_available: bool = True):
        if capacity <= 0:
            raise ValueError("Table capacity must be greater than zero.")
        self.table_number = table_number
        self.capacity = capacity
        self.is_available = is_available

    def occupy(self):
        """Marks table as occupied."""
        self.is_available = False

    def release(self):
        """Marks table as available/vacant."""
        self.is_available = True

    def get_status(self) -> str:
        """Returns formatted string displaying table status."""
        status = "🟢 Available" if self.is_available else "🔴 Occupied"
        return f"Table {self.table_number:02d} | Seats: {self.capacity} | Status: {status}"

    def to_dict(self) -> dict:
        """Converts Table object to dictionary for JSON serialization."""
        return {
            "table_number": self.table_number,
            "capacity": self.capacity,
            "is_available": self.is_available
        }


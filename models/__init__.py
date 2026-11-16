"""
models/__init__.py
Exposes the core domain models (MenuItem, Food, Drink, Table) so other modules
can import them directly from the `models` package.
"""

from .menu import MenuItem, Food, Drink
from .table import Table

__all__ = ["MenuItem", "Food", "Drink", "Table"]
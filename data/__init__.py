"""
data/__init__.py
Exposes starter menu and table data seed functions for the service layer.
"""

from .sample_data import get_sample_menu, get_sample_tables

__all__ = ["get_sample_menu", "get_sample_tables"]
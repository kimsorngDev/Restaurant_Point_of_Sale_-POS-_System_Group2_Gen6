class MenuItem:
    """Base class representing a restaurant menu item with stock tracking."""

    def __init__(self, item_id: str | int, name: str, price: float, category: str, is_available: bool = True, stock: int = 10):
        # Validate required fields and prevent negative price or stock
        raw_id = str(item_id).strip() if item_id is not None else ''
        if not raw_id:
            raise ValueError('Item ID is required.')
        if not name or not str(name).strip():
            raise ValueError('Item name is required.')
        if price < 0:
            raise ValueError('Price cannot be negative.')
        if int(stock) < 0:
            raise ValueError('Stock cannot be negative.')

        # Normalize and store item attributes
        self.item_id = raw_id.upper()
        self.name = str(name).strip()
        self.price = round(float(price), 2)
        self.category = str(category).strip()
        self.stock = int(stock)
        # Item is only available if flagged active AND stock is greater than 0
        self.is_available = bool(is_available) and self.stock > 0

    def update_price(self, new_price: float) -> None:
        """Update item price while rejecting negative values."""
        if new_price < 0:
            raise ValueError('Price cannot be negative.')
        self.price = round(float(new_price), 2)

    def set_availability(self, available: bool, stock: int | None = None) -> None:
        """Toggle item availability and optionally update stock quantity."""
        if stock is not None:
            if int(stock) < 0:
                raise ValueError('Stock cannot be negative.')
            self.stock = int(stock)
        elif available and self.stock == 0:
            # Default to 10 units if re-enabled while stock is empty
            self.stock = 10
        self.is_available = bool(available) and self.stock > 0

    def to_dict(self) -> dict:
        """Serialize menu item attributes to a dictionary for JSON storage."""
        return {
            'item_id': self.item_id,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'is_available': self.is_available,
            'stock': self.stock
        }

    def __str__(self) -> str:
        """Format menu item display string with current stock count."""
        status = f'Available: {self.stock}' if (self.is_available and self.stock > 0) else 'Inactive / Out of Stock'
        return f'[{self.item_id}] {self.name:<22} ${self.price:>6.2f} ({status})'


class Food(MenuItem):
    """Represents a food item with an optional spicy indicator."""

    def __init__(self, item_id: str | int, name: str, price: float, is_spicy: bool = False, is_available: bool = True, stock: int = 10):
        super().__init__(item_id=item_id, name=name, price=price, category='Food', is_available=is_available, stock=stock)
        self.is_spicy = bool(is_spicy)

    def to_dict(self) -> dict:
        """Include spicy status in serialized food data."""
        data = super().to_dict()
        data['is_spicy'] = self.is_spicy
        return data

    def __str__(self) -> str:
        """Append [Spicy] tag if applicable."""
        spicy_tag = ' [Spicy]' if self.is_spicy else ''
        return f'{super().__str__()}{spicy_tag}'


class Drink(MenuItem):
    """Represents a beverage item with a serving size."""

    def __init__(self, item_id: str | int, name: str, price: float, size: str = 'Regular', is_available: bool = True, stock: int = 10):
        super().__init__(item_id=item_id, name=name, price=price, category='Drink', is_available=is_available, stock=stock)
        self.size = str(size).strip() if size else 'Regular'

    def to_dict(self) -> dict:
        """Include drink size in serialized drink data."""
        data = super().to_dict()
        data['size'] = self.size
        return data

    def __str__(self) -> str:
        """Append drink size tag to display output."""
        return f'{super().__str__()} [{self.size}]'


# Aliases for backward compatibility across modules
FoodItem = Food
DrinkItem = Drink
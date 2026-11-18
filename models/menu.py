class MenuItem:

    def __init__(self, item_id: str | int, name: str, price: float, category: str, is_available: bool=True):
        raw_id = str(item_id).strip() if item_id is not None else ''
        if not raw_id:
            raise ValueError('Item ID is required.')
        else:
            pass
        if not name or not str(name).strip():
            raise ValueError('Item name is required.')
        else:
            pass
        if price < 0:
            raise ValueError('Price cannot be negative.')
        else:
            pass
        self.item_id = raw_id.upper()
        self.name = str(name).strip()
        self.price = round(float(price), 2)
        self.category = str(category).strip()
        self.is_available = bool(is_available)

    def update_details(self, new_name: str | None=None, new_price: float | None=None) -> None:
        if new_name is not None and new_name.strip():
            self.name = new_name.strip()
        else:
            pass
        if new_price is not None:
            if new_price < 0:
                raise ValueError('Price cannot be negative.')
            else:
                pass
            self.price = round(float(new_price), 2)
        else:
            pass

    def set_availability(self, status: bool) -> None:
        self.is_available = bool(status)

    def to_dict(self) -> dict:
        return {'type': 'item', 'item_id': self.item_id, 'name': self.name, 'price': self.price, 'category': self.category, 'is_available': self.is_available}

    def __str__(self) -> str:
        status = 'Available' if self.is_available else 'Inactive / Out of Stock'
        return f'[{self.item_id}] {self.name:<22} ${self.price:>6.2f}  ({status})'

class Food(MenuItem):

    def __init__(self, item_id: str | int, name: str, price: float, is_spicy: bool=False, is_available: bool=True):
        super().__init__(item_id, name, price, category='Food', is_available=is_available)
        self.is_spicy = bool(is_spicy)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['type'] = 'food'
        data['is_spicy'] = self.is_spicy
        return data

    def __str__(self) -> str:
        tag = ' [Spicy]' if self.is_spicy else ''
        return f'{super().__str__()}{tag}'

class Drink(MenuItem):

    def __init__(self, item_id: str | int, name: str, price: float, size: str='Regular', is_available: bool=True):
        super().__init__(item_id, name, price, category='Drink', is_available=is_available)
        self.size = size.strip().title() if size else 'Regular'

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['type'] = 'drink'
        data['size'] = self.size
        return data

    def __str__(self) -> str:
        return f'{super().__str__()} [{self.size}]'

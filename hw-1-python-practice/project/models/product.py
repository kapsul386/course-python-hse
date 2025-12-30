from __future__ import annotations

from typing import Union

Number = Union[int, float]


class Product:
    def __init__(self, name: str, category: str, price: Number) -> None:
        self.name: str = name
        self.category: str = category
        self.price: Number = price
        self.sale: int = 0

    def edit_category(self, new_category: str) -> None:
        self.category = new_category

    def edit_price(self, new_price: Number) -> None:
        self.price = new_price

    def set_sale(self, sale: int) -> None:
        self.sale = sale

    def cancel_sale(self) -> None:
        self.sale = 0

    def get_price(self) -> float:
        return float(self.price) * (100 - self.sale) / 100

    def __repr__(self) -> str:
        return f"Product(name={self.name!r}, category={self.category!r}, price={self.price!r}, sale={self.sale!r})"

from __future__ import annotations

from typing import Sequence
from models.product import Product


def get_ordered_products_by_price(products: Sequence[Product]) -> list[Product]:
    return sorted(products, key=lambda p: p.price, reverse=True)

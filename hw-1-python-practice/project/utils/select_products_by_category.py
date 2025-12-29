from __future__ import annotations

from typing import Sequence
from models.product import Product


def select_products_by_category(products: Sequence[Product], category: str) -> list[Product]:
    return [p for p in products if p.category == category]

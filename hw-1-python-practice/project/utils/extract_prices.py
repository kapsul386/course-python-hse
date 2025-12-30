from __future__ import annotations

from typing import Sequence, Union
from models.product import Product

Number = Union[int, float]


def extract_prices(products: Sequence[Product]) -> list[Number]:
    return [p.price for p in products]

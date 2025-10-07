from dataclasses import dataclass
from food_delivery.models.money import Money


@dataclass(frozen=True)
class OrderItem:
    menu_item_id: int
    price: Money

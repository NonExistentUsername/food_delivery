from typing import Protocol, List
from food_delivery.models.order import Order


class OrderRepository(Protocol):
    def get(self, order_id: str) -> Order: ...
    def save(self, order: Order) -> None: ...
    def find_by_state(self, state: str) -> List[Order]: ...


class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self.orders: dict[str, Order] = {}

    def get(self, order_id: str) -> Order:
        return self.orders[order_id]

    def save(self, order: Order) -> None:
        self.orders[order.id] = order

    def find_by_state(self, state: str) -> List[Order]:
        return [o for o in self.orders.values() if o.state == state]

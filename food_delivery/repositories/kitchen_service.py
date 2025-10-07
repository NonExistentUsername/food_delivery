from food_delivery.repositories.order_repository import OrderRepository
from food_delivery.services.event_bus import EventBus
from datetime import datetime


class KitchenService:
    def __init__(self, orders: OrderRepository, bus: EventBus):
        self.orders, self.bus = orders, bus

    def accept_order(self, order_id: str, prep_time: int, now: datetime) -> None:
        o = self.orders.get(order_id)
        evt = o.accept(prep_time, now)
        self.orders.save(o)
        self.bus.publish(evt)

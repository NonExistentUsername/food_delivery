from datetime import datetime
from food_delivery.models.order import Order
from food_delivery.repositories.order_repository import OrderRepository
from food_delivery.services.event_bus import EventBus
from food_delivery.models.order_item import OrderItem
from food_delivery.models.address import Address


class OrderingService:
    def __init__(
        self,
        orders: OrderRepository,
        event_bus: EventBus,
    ):
        self.orders, self.event_bus = orders, event_bus

    def place_order(
        self,
        order_id: str,
        restaurant_id: str,
        items: list[OrderItem],
        address: Address,
        menu: set[int],
        promised_by: datetime,
    ) -> str:
        o = Order(order_id, restaurant_id, [], address, "Draft", promised_by)

        for it in items:
            o.add_item(it, menu)

        evt = o.place()
        self.orders.save(o)
        self.event_bus.publish(evt)

        return o.id

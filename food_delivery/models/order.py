from dataclasses import dataclass, field
from typing import List, Optional, Literal

from food_delivery.models.address import Address
from datetime import datetime, timedelta
from food_delivery.models.order_item import OrderItem
from food_delivery.models.menu import menu
from food_delivery import events
from food_delivery.models.prep_time import PrepTime


class Order:
    def __init__(
        self,
        id: str,
        restaurant_id: str,
        items: List[OrderItem] | None = None,
        address: Address | None = None,
        state: Literal[
            "Draft", "Placed", "Accepted", "Dispatched", "Delivered", "Cancelled"
        ] = "Draft",
        promised_by: Optional[datetime] = None,
    ):
        self._id = id
        self._restaurant_id = restaurant_id
        self._items = items if items is not None else []
        self._address = address
        self._state = state
        self._promised_by = promised_by

    @property
    def id(self) -> str:
        return self._id

    @property
    def restaurant_id(self) -> str:
        return self._restaurant_id

    @property
    def items(self) -> List[OrderItem]:
        return self._items

    @property
    def address(self) -> Optional[Address]:
        return self._address

    @property
    def state(
        self,
    ) -> Literal["Draft", "Placed", "Accepted", "Dispatched", "Delivered", "Cancelled"]:
        return self._state

    @property
    def promised_by(self) -> Optional[datetime]:
        return self._promised_by

    def add_item(self, item: OrderItem, menu: set[int]) -> None:
        assert self.state == "Draft", "Can only add items in Draft"
        assert item.menu_item_id in menu, "Item not served by restaurant"
        self.items.append(item)

    def place(self) -> events.OrderPlaced:
        assert self.state == "Draft" and self.items, "Must have items"
        self.state = "Placed"
        return events.OrderPlaced(order_id=self.id, placed_at=datetime.now())

    def accept(self, prep_time: PrepTime) -> events.OrderAccepted:
        assert self.state == "Placed", "Accept only after placed"
        ready_at = datetime.now() + prep_time.to_delta()
        self.state = "Accepted"
        return events.OrderAccepted(order_id=self.id, ready_at=ready_at)

    def can_dispatch(self, route_eta: timedelta) -> bool:
        if self.state == "Canceled" or self.promised_by is None:
            return False

        return (datetime.now() + route_eta) <= self.promised_by

    def dispatch(self, courier_id: str) -> events.CourierAssigned:
        assert self.state in {"Placed", "Accepted"}, "Invalid state"
        self._state = "Dispatched"
        return events.CourierAssigned(
            order_id=self.id,
            courier_id=courier_id,
            assigned_at=datetime.now(),
        )

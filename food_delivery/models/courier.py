from datetime import datetime
from typing import Literal
from food_delivery.models.geo_point import GeoPoint


class Courier:
    def __init__(
        self,
        id: str,
        location: GeoPoint,
        state: Literal["Available", "Delivering"] = "Available",
        order_id: str | None = None,
    ):
        self._id = id
        self._location = location
        self._state = state
        self._order_id = order_id

    @property
    def id(self) -> str:
        return self._id

    @property
    def location(self) -> GeoPoint:
        return self._location

    @property
    def state(self) -> Literal["Available", "Delivering"]:
        return self._state

    @property
    def order_id(self) -> str | None:
        return self._order_id

    @property
    def is_available(self) -> bool:
        return self.state == "Available"

    def take_order(self, order_id: str, eta: datetime) -> None:
        assert self.state == "Available", "Courier not available"
        self._state = "Delivering"
        self._order_id = order_id

    def complete_order(self) -> None:
        assert self.state == "Delivering", "Courier not delivering"
        self._state = "Available"
        self._order_id = None

    def update_location(self, location: GeoPoint) -> None:
        self._location = location

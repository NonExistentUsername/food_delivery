from typing import Protocol, List
from food_delivery.models.courier import Courier
from food_delivery.models.service_area import ServiceArea


class CourierRepository(Protocol):
    def get(self, courier_id: str) -> Courier: ...
    def save(self, courier: Courier) -> None: ...
    def find_available_in_area(self, service_area: ServiceArea) -> List[Courier]: ...


class InMemoryCourierRepository(CourierRepository):
    def __init__(self):
        self.couriers: dict[str, Courier] = {}

    def get(self, courier_id: str) -> Courier:
        return self.couriers.get(courier_id)

    def save(self, courier: Courier) -> None:
        self.couriers[courier.id] = courier

    def find_available_in_area(self, service_area: ServiceArea) -> List[Courier]:
        return [
            c
            for c in self.couriers.values()
            if c.is_available and service_area.contains(c.location)
        ]

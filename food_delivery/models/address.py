from dataclasses import dataclass
from food_delivery.models.geo_point import GeoPoint


@dataclass(frozen=True)
class Address:
    street: str
    geo: GeoPoint

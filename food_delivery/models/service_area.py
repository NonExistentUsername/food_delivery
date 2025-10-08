from dataclasses import dataclass
from food_delivery.models.geo_point import GeoPoint
from food_delivery.services.utils import haversine


@dataclass(frozen=True)
class ServiceArea:
    radius_km: float
    restaurant_location: GeoPoint

    def contains(self, point: GeoPoint) -> bool:
        distance = haversine(
            self.restaurant_location.lat,
            self.restaurant_location.lon,
            point.lat,
            point.lon,
        )
        return distance <= self.radius_km

from dataclasses import dataclass
from food_delivery.models.geo_point import GeoPoint
from food_delivery.services.utils import haversine


@dataclass(frozen=True)
class ServiceArea:
    radius_km: float
    center: GeoPoint

    def contains(self, point: GeoPoint) -> bool:
        distance = haversine(self.center.lat, self.center.lon, point.lat, point.lon)
        return distance <= self.radius_km

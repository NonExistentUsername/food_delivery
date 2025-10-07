from datetime import timedelta
from food_delivery.models.geo_point import GeoPoint
from food_delivery.services.utils import haversine

from functools import lru_cache


class RouteEstimator:
    def estimate_eta(
        self,
        restaurant_loc: GeoPoint,
        customer_loc: GeoPoint,
    ) -> timedelta:
        km = self.distance_km(restaurant_loc, customer_loc)  # pure calc
        minutes = int((km / 25.0) * 60)  # ~25 km/h city speed
        return timedelta(minutes=max(1, minutes))

    def distance_km(self, a: GeoPoint, b: GeoPoint) -> float:
        return haversine(
            a.lat, a.lon, b.lat, b.lon
        )  # Just straight line distance on sphere


class CachedRouteEstimator(RouteEstimator):
    @lru_cache(maxsize=2000)
    def distance_km(self, a: GeoPoint, b: GeoPoint) -> float:
        return super().distance_km(a, b)

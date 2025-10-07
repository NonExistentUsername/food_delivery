from dataclasses import dataclass


@dataclass(frozen=True)
class GeoPoint:
    lat: float
    lon: float

    def __post_init__(self):
        assert -90 <= self.lat <= 90 and -180 <= self.lon <= 180

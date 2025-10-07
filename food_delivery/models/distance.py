from dataclasses import dataclass


@dataclass(frozen=True)
class DistanceKm:
    km: float

    def post_init(self):
        assert self.km >= 0.0

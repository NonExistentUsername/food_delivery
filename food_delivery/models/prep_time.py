from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class PrepTime:
    minutes: int

    def post_init(self):
        assert self.minutes >= 0

    def to_delta(self):
        return timedelta(minutes=self.minutes)

from datetime import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class OrderAccepted:
    order_id: str
    accepted_at: datetime

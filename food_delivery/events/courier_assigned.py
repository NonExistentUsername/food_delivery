from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CourierAssigned:
    order_id: str
    courier_id: str
    assigned_at: datetime

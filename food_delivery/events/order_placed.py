from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class OrderPlaced:
    order_id: str
    ready_at: datetime

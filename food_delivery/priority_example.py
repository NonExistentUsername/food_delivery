from typing import Literal
from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class Priority:
    level: Literal["normal", "priority"] = "normal"


def latest_allowed(promised_by, priority: Priority):
    return promised_by - (
        timedelta(minutes=10) if priority.level == "priority" else timedelta()
    )

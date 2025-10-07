from typing import Protocol


class EventBus(Protocol):
    def publish(self, event: object) -> None: ...


class SimpleEventBus(EventBus):
    def __init__(self) -> None:
        self.published_events = []

    def publish(self, event: object) -> None:
        self.published_events.append(event)

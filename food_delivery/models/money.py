from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: int  # cents
    currency: str = "USD"

    def add(self, other: "Money") -> "Money":
        assert self.currency == other.currency
        return Money(self.amount + other.amount, self.currency)

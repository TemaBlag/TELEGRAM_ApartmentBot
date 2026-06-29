from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Listing:
    id: str
    price: str
    url: str

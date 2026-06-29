from __future__ import annotations

import abc
from typing import Sequence

from models import Listing


class BaseParser(abc.ABC):
    @abc.abstractmethod
    async def fetch_listings(self) -> Sequence[Listing]:
        raise NotImplementedError

    @abc.abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        return f"<Parser {self.name()}>"

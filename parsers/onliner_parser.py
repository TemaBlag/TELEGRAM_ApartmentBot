from __future__ import annotations

import json
from typing import Any, List

import config
from models import Listing
from parsers.base_parser import BaseParser
from parsers.http_utils import fetch_text


class OnlinerParser(BaseParser):
    def name(self) -> str:
        return "Onliner"

    async def fetch_listings(self) -> List[Listing]:
        json_code = await fetch_text(config.ONLINER_URL, self.name(), expect_json=True)
        if not json_code:
            return []

        try:
            data: dict[str, Any] = json.loads(json_code)
        except json.JSONDecodeError:
            return []

        apartments = data.get("apartments", [])
        listings: List[Listing] = []

        for apartment in apartments:
            apartment_id = apartment.get("id")
            price_amount = (
                apartment.get("price", {})
                .get("converted", {})
                .get("BYN", {})
                .get("amount")
            )
            if not apartment_id or not price_amount:
                continue

            full_url = f"https://r.onliner.by/ak/apartments/{apartment_id}"
            price_text = str(price_amount).replace(" ", "")
            listings.append(Listing(id=full_url, price=price_text, url=full_url))

        return listings

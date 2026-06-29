from __future__ import annotations

from typing import List

from bs4 import BeautifulSoup

import config
from models import Listing
from parsers.base_parser import BaseParser
from parsers.http_utils import fetch_text


class DomovitaParser(BaseParser):
    def name(self) -> str:
        return "Domovita"

    async def fetch_listings(self) -> List[Listing]:
        html = await fetch_text(config.DOMOVITA_URL, self.name())
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select('div.found_full:has(a[href])')
        row_cards = list(soup.select('a.found_item'))
        anchors = [card.select_one("a.title") for card in cards] + row_cards
        all_cards = list(cards) + row_cards

        listings: List[Listing] = []
        for card, anchor in zip(all_cards, anchors):
            if anchor is None:
                continue

            href = anchor.get("href", "").strip()
            if not href:
                continue

            price_tag = card.select_one("div.dropdown-toggle")
            if price_tag:
                raw_price = price_tag.get_text(strip=True)
                separator_index = raw_price.find("./")
                price_text = raw_price[: separator_index - 2].replace(" ", "") if separator_index > 1 else raw_price
            else:
                price_text = "—"

            listings.append(Listing(id=href, price=price_text, url=href))

        return listings[:3]

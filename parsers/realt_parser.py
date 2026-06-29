from __future__ import annotations

from typing import List

from bs4 import BeautifulSoup

import config
from models import Listing
from parsers.base_parser import BaseParser
from parsers.http_utils import fetch_text


class RealtParser(BaseParser):
    def name(self) -> str:
        return "Realt"

    async def fetch_listings(self) -> List[Listing]:
        html = await fetch_text(config.REALT_URL, self.name())
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select('div:has(a[href^="/rent-flat-for-long/object/"])')

        listings: List[Listing] = []
        for card in cards:
            anchor = card.select_one('a[href^="/rent-flat-for-long/object/"]')
            if not anchor:
                continue

            href = anchor.get("href", "").strip()
            if not href:
                continue

            full_url = href if href.startswith("http") else f"https://realt.by{href}"
            price_tag = card.select_one("span.text-title")
            price_text = price_tag.get_text(strip=True)[:-7].replace(" ", "") if price_tag else "—"

            listings.append(Listing(id=full_url, price=price_text, url=full_url))

        return listings

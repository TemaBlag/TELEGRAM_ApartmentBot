from __future__ import annotations

from typing import List
from urllib.parse import urlsplit, urlunsplit

from bs4 import BeautifulSoup

import config
from models import Listing
from parsers.base_parser import BaseParser
from parsers.http_utils import fetch_text


def _normalize_url(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


class KufarParser(BaseParser):
    def name(self) -> str:
        return "Kufar"

    async def fetch_listings(self) -> List[Listing]:
        html = await fetch_text(config.KUFAR_URL, self.name())
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select('a[data-testid^="kufar-realty-card-"]') or soup.select('a.styles_wrapper__Q06m9')

        listings: List[Listing] = []
        for anchor in cards:
            href = anchor.get("href", "").strip()
            if not href:
                continue

            full_url = href if href.startswith("http") else f"https://re.kufar.by{href}"
            normalized_url = _normalize_url(full_url)

            price_tag = anchor.select_one("div.styles_price__gpHWH span.styles_price__byr__lLSfd")
            price_text = price_tag.get_text(strip=True)[:-2].replace(" ", "") if price_tag else "—"

            listings.append(Listing(id=normalized_url, price=price_text, url=full_url))

        return listings

from __future__ import annotations

import asyncio
import logging
from typing import Sequence

import config
from bot import send_new_listing
from parsers.base_parser import BaseParser
from parsers.domovita_parser import DomovitaParser
from parsers.kufar_parser import KufarParser
from parsers.onliner_parser import OnlinerParser
from parsers.realt_parser import RealtParser
from storage.storage import add_seen, is_seen

logger = logging.getLogger(__name__)

PARSERS: Sequence[BaseParser] = (
    KufarParser(),
    RealtParser(),
    OnlinerParser(),
    DomovitaParser(),
)


async def check_all_sites(app) -> None:
    for parser in PARSERS:
        try:
            listings = await parser.fetch_listings()
        except Exception:
            logger.exception("%s failed during fetch_listings", parser.name())
            continue

        for listing in listings:
            if is_seen(listing.id):
                continue

            await send_new_listing(listing, app)
            add_seen(listing.id)


async def scheduler_loop(app) -> None:
    while True:
        await check_all_sites(app)
        await asyncio.sleep(config.CHECK_INTERVAL_SECONDS)

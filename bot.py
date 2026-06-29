from __future__ import annotations

import asyncio
import logging

from pyrogram.client import Client

from config import API_HASH, API_ID, BOT_TOKEN, TARGET_USERS
from models import Listing

logger = logging.getLogger(__name__)

app = Client("apt_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


async def send_new_listing(listing: Listing, client: Client) -> None:
    text = f"[{listing.price} BYN]({listing.url})"
    for user in TARGET_USERS:
        try:
            await client.send_message(chat_id=user, text=text)
        except Exception:
            logger.exception("Failed to send listing to user %s", user)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    await app.start()
    logger.info("Bot client started")

    from scheduler import scheduler_loop

    asyncio.create_task(scheduler_loop(app))
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())

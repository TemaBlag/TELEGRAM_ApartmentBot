from __future__ import annotations

import logging
import ssl
from typing import Optional

import aiohttp

import config

logger = logging.getLogger(__name__)


def _build_ssl_context(verify: bool) -> ssl.SSLContext:
    if verify:
        return ssl.create_default_context()

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context


async def fetch_text(url: str, parser_name: str, *, expect_json: bool = False) -> Optional[str]:
    ssl_errors = (
        aiohttp.ClientConnectorCertificateError,
        aiohttp.ClientSSLError,
        ssl.SSLCertVerificationError,
    )

    for verify in (True, False):
        ssl_context = _build_ssl_context(verify)
        connector = aiohttp.TCPConnector(ssl=ssl_context)

        try:
            async with aiohttp.ClientSession(
                headers=config.HTTP_HEADERS,
                connector=connector,
            ) as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        logger.warning("%s returned HTTP %s", parser_name, response.status)
                        return None

                    if not verify:
                        logger.warning(
                            "%s requested with disabled SSL verification after certificate validation failure",
                            parser_name,
                        )

                    return await response.text()
        except ssl_errors:
            if verify:
                logger.warning("%s SSL verification failed, retrying without verification", parser_name)
                continue

            logger.exception("%s request failed without SSL verification", parser_name)
            return None
        except Exception:
            logger.exception("%s request failed", parser_name)
            return None

    return None

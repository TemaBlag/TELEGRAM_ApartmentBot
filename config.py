from __future__ import annotations

import os
from typing import Final


def _get_env(name: str, *, required: bool = True, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if required and not value:
        raise RuntimeError(f"Environment variable {name} is required")
    return value or ""


def _get_env_int(name: str, *, required: bool = True, default: int | None = None) -> int:
    raw_default = str(default) if default is not None else None
    value = _get_env(name, required=required, default=raw_default)
    try:
        return int(value)
    except ValueError as error:
        raise RuntimeError(f"Environment variable {name} must be an integer") from error


API_ID: Final[int] = _get_env_int("API_ID")
API_HASH: Final[str] = _get_env("API_HASH")
BOT_TOKEN: Final[str] = _get_env("BOT_TOKEN")

TARGET_USERS: Final[list[str]] = [
    user.strip()
    for user in _get_env("TARGET_USERS").split(",")
    if user.strip()
]

CHECK_INTERVAL_SECONDS: Final[int] = _get_env_int("CHECK_INTERVAL_SECONDS", default=60)

KUFAR_URL: Final[str] = (
    "https://re.kufar.by/l/minsk/snyat/kvartiru/bez-posrednikov?cur=BYR&fkn=v.and%3A1&oph=1&prc=r%3A60000%2C110000&rms=v.or%3A2%2C1"
)

REALT_URL: Final[str] = (
    "https://realt.by/rent/flat-for-long/?addressV2=%5B%7B%22townUuid%22%3A%224cb07174-7b00-11eb-8943-0cc47adabd66%22%7D%5D&page=1&priceFrom=600&priceTo=1100&priceType=933&rooms=1&rooms=2&seller=true&sortType=createdAt"
)

ONLINER_URL: Final[str] = (
    "https://r.onliner.by/sdapi/ak.api/search/apartments?rent_type%5B%5D=1_room&rent_type%5B%5D=2_rooms&price%5Bmin%5D=600&price%5Bmax%5D=1100&currency=byn&only_owner=true&order=created_at%3Adesc&page=1&bounds%5Blb%5D%5Blat%5D=53.651963867253315&bounds%5Blb%5D%5Blong%5D=27.210388183593754&bounds%5Brt%5D%5Blat%5D=54.12945489870697&bounds%5Brt%5D%5Blong%5D=27.897033691406254&v=0.3819675990546686"
)

DOMOVITA_URL: Final[str] = (
    "https://domovita.by/minsk/flats/rent?rooms=1%2C2&price%5Bmin%5D=600&price%5Bmax%5D=1100&individual=yes&price_type=all_byn&order=-date_revision"
)

HTTP_HEADERS: Final[dict[str, str]] = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

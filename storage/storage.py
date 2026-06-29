from __future__ import annotations

import json
from pathlib import Path
from typing import Set

SEEN_FILE = Path(__file__).with_name("seen_links.json")


def load_seen() -> Set[str]:
    if not SEEN_FILE.exists():
        return set()

    try:
        data = json.loads(SEEN_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return set()

    return set(data) if isinstance(data, list) else set()


def save_seen(seen: Set[str]) -> None:
    ordered_seen = sorted(seen)
    SEEN_FILE.write_text(
        json.dumps(ordered_seen, ensure_ascii=False, indent=4),
        encoding="utf-8",
    )


def is_seen(link_id: str) -> bool:
    return link_id in load_seen()


def add_seen(link_id: str) -> None:
    seen = load_seen()
    if link_id not in seen:
        seen.add(link_id)
        save_seen(seen)

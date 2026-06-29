# Apartment Parser Bot

Telegram bot for monitoring apartment rental listings in Minsk and sending new offers to selected users.

## Features

- Collects listings from:
  - Kufar
  - Realt
  - Onliner
  - Domovita
- Filters duplicates using local storage in [`storage/seen_links.json`](storage/seen_links.json)
- Sends new listings to Telegram users through a bot
- Uses async HTTP requests for periodic polling
- Reads sensitive settings from environment variables instead of hardcoded secrets

## Project structure

- [`bot.py`](bot.py) — entrypoint and Telegram message delivery
- [`scheduler.py`](scheduler.py) — periodic parser execution loop
- [`config.py`](config.py) — environment-based configuration
- [`models.py`](models.py) — shared data models
- [`parsers/`](parsers) — site-specific parsers and HTTP helpers
- [`storage/storage.py`](storage/storage.py) — seen links persistence

## Requirements

- Python 3.11+
- Telegram application credentials
- Telegram bot token

Recommended Python packages:

```bash
pip install pyrogram tgcrypto aiohttp beautifulsoup4
```

## Configuration

Set these environment variables before запуском:

```bash
export API_ID=123456
export API_HASH=your_api_hash
export BOT_TOKEN=your_bot_token
export TARGET_USERS=user1,user2
export CHECK_INTERVAL_SECONDS=60
```

### Variables

- `API_ID` — Telegram API ID
- `API_HASH` — Telegram API hash
- `BOT_TOKEN` — Telegram bot token
- `TARGET_USERS` — comma-separated Telegram usernames or chat IDs
- `CHECK_INTERVAL_SECONDS` — polling interval in seconds, default `60`

## Run

```bash
python bot.py
```

## Publication readiness improvements made

- Removed hardcoded secrets from [`config.py`](config.py)
- Added typed configuration helpers and stricter validation in [`config.py`](config.py)
- Improved logging in [`bot.py`](bot.py), [`scheduler.py`](scheduler.py), [`parsers/http_utils.py`](parsers/http_utils.py)
- Simplified and hardened parser logic in [`parsers/*.py`](parsers)
- Improved [`Listing`](models.py) model immutability with dataclass slots
- Made storage handling cleaner in [`storage/storage.py`](storage/storage.py)

## Recommended files for Git

Add a [`.gitignore`](.gitignore) with at least:

```gitignore
__pycache__/
*.pyc
.venv/
.env
```

Also avoid committing real production values into [`config.py`](config.py) or [`storage/seen_links.json`](storage/seen_links.json).

## How to publish to Git

Example commands:

```bash
git init
git add .
git commit -m "Initial commit"
```

If you want to push to GitHub:

```bash
git remote add origin <repo-url>
git branch -M main
git push -u origin main
```

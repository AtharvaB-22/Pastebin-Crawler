# Pastebin Keyword Crawler

A Python script to scrape Pastebin's public archive for pastes containing crypto-related keywords or Telegram links.

## Setup
1. Create and activate a virtual environment:
   Command:
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

2. Install dependencies:
   Command: pip install -r requirements.txt

3. Run the script:
    Command: python crawler.py

## Output:
- Results are saved to keyword_matches.jsonl.
- Logs are saved to crawler.log.

## Features:
- Scrapes Pastebin archive for paste IDs.
- Fetches raw paste content asynchronously.
- Detects keywords: crypto, bitcoin, ethereum, blockchain, t.me.
- Implements rate-limiting and proxy rotation (optional).
- Logs all activities and errors.
- This will be updated as we implement more features.
- Archive Scraper: Extracts up to 30 paste IDs from https://pastebin.com/archive using `requests` and `BeautifulSoup`.

## Configuration
All constants are defined in `config.py`, including:
- Archive URL: `https://pastebin.com/archive`
- Raw URL template: `https://pastebin.com/raw/{paste_id}`
- Keywords: `crypto`, `bitcoin`, `ethereum`, `blockchain`, `t.me`
- Output file: `keyword_matches.jsonl`
- Rate-limiting delay: 1.5 seconds (adjustable)
- Maximum pastes to scrape: 30
- Proxy settings: Disabled by default (configurable in `config.py`)
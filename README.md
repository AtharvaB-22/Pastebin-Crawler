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
Results are saved to keyword_matches.jsonl.
Logs are saved to crawler.log.

## Features:
Scrapes Pastebin archive for paste IDs.
Fetches raw paste content asynchronously.
Detects keywords: crypto, bitcoin, ethereum, blockchain, t.me.
Implements rate-limiting and proxy rotation (optional).
Logs all activities and errors.
This will be updated as we implement more features.


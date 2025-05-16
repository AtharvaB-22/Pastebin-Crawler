# test_keyword_detector.py

import asyncio
from scraper import scrape_paste_ids
from fetcher import fetch_all_pastes
from keyword_detector import detect_keywords

async def main():
    paste_ids = scrape_paste_ids()
    if not paste_ids:
        print("No paste IDs to fetch")
        return
    
    paste_contents = await fetch_all_pastes(paste_ids)
    print(f"Analyzing {len(paste_contents)} pastes for keywords:")
    for paste_id, content in paste_contents:
        keywords = detect_keywords(paste_id, content)
        status = "Matched" if keywords else "No matches"
        print(f"Paste {paste_id}: {status}")
        if keywords:
            print(f"Keywords found: {keywords}")

if __name__ == "__main__":
    asyncio.run(main())
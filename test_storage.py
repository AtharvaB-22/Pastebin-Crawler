# test_storage.py

import asyncio
from scraper import scrape_paste_ids
from fetcher import fetch_all_pastes
from keyword_detector import detect_keywords
from storage import save_paste

async def main():
    paste_ids = scrape_paste_ids()
    if not paste_ids:
        print("No paste IDs to fetch")
        return
    
    paste_contents = await fetch_all_pastes(paste_ids)
    print(f"Processing {len(paste_contents)} pastes for keyword detection and storage:")
    
    for paste_id, content in paste_contents:
        keywords = detect_keywords(paste_id, content)
        saved = save_paste(paste_id, content, keywords)
        status = "Saved" if saved else "Not saved (no keywords or error)"
        print(f"Paste {paste_id}: {status}")
        if saved:
            print(f"Keywords: {keywords}")

if __name__ == "__main__":
    asyncio.run(main())
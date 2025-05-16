# test_fetcher.py

import asyncio
from scraper import scrape_paste_ids
from fetcher import fetch_all_pastes

async def main():
    paste_ids = scrape_paste_ids()
    if not paste_ids:
        print("No paste IDs to fetch")
        return
    results = await fetch_all_pastes(paste_ids)
    print(f"Fetched content for {len(results)} paste IDs:")
    for paste_id, content in results:
        status = "Success" if content else "Failed"
        print(f"Paste {paste_id}: {status}")
        if content:
            print(f"Content preview: {content[:100]}...")

if __name__ == "__main__":
    asyncio.run(main())
# test_scraper.py

from scraper import scrape_paste_ids

def main():
    paste_ids = scrape_paste_ids()
    print(f"Extracted {len(paste_ids)} paste IDs:")
    for pid in paste_ids:
        print(pid)

if __name__ == "__main__":
    main()
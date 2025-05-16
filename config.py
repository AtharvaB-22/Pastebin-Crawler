# config.py

# URL for Pastebin's public archive page
ARCHIVE_URL = "https://pastebin.com/archive"

# URL template for fetching raw paste content, with placeholder for paste ID
RAW_URL_TEMPLATE = "https://pastebin.com/raw/{}"

# List of keywords to search for in paste content
KEYWORDS = ["crypto", "bitcoin", "ethereum", "blockchain", "t.me"]

# Path to the output JSONL file for storing matching pastes
OUTPUT_FILE = "keyword_matches.jsonl"

# Delay between requests in seconds to avoid rate-limiting
RATE_LIMIT_DELAY = 1.5

# Maximum number of paste IDs to scrape from the archive
MAX_PASTES = 30

# List of proxy URLs for rotation (empty by default)
PROXIES = []

# Flag to enable/disable proxy rotation
USE_PROXIES = False
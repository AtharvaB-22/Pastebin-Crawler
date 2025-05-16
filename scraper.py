# scraper.py

import logging
import requests
from bs4 import BeautifulSoup
from config import ARCHIVE_URL, MAX_PASTES

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Log to console
    ]
)
logger = logging.getLogger(__name__)

def scrape_paste_ids():
    """
    Scrape the Pastebin archive page to extract up to MAX_PASTES paste IDs.
    Returns a list of paste IDs (e.g., ['abc123', 'xyz456']).
    """
    try:
        # Set headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        logger.info("Fetching Pastebin archive from %s", ARCHIVE_URL)
        
        # Send GET request to archive page
        response = requests.get(ARCHIVE_URL, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table containing paste links (class 'maintable')
        paste_table = soup.find('table', class_='maintable')
        if not paste_table:
            logger.error("Could not find paste table on archive page")
            return []
        
        # Extract paste IDs from <a> tags in the table
        paste_ids = []
        for row in paste_table.find_all('tr')[:MAX_PASTES]:
            link = row.find('a', href=True)
            if link and link['href'].startswith('/'):
                paste_id = link['href'][1:]  # Remove leading '/'
                paste_ids.append(paste_id)
        
        logger.info("Extracted %d paste IDs", len(paste_ids))
        return paste_ids[:MAX_PASTES]  # Ensure no more than MAX_PASTES
        
    except requests.exceptions.RequestException as e:
        logger.error("Failed to fetch archive page: %s", e)
        return []
    except Exception as e:
        logger.error("Unexpected error while scraping archive: %s", e)
        return []
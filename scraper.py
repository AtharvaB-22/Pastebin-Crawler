import requests
from bs4 import BeautifulSoup
from logger import get_logger

logger = get_logger(__name__)

def scrape_paste_ids():
    """
    Scrape paste IDs from Pastebin archive page.
    Returns:
        list: List of paste IDs (e.g., ['abc123', 'xyz789']).
    """
    url = "https://pastebin.com/archive"
    logger.info("Fetching Pastebin archive from %s", url)
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='maintable')
        paste_ids = []
        
        if table:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip header row
                link = row.find('a')
                if link and link['href'].startswith('/'):
                    paste_id = link['href'][1:]  # Remove leading '/'
                    paste_ids.append(paste_id)
        
        logger.info("Extracted %d paste IDs", len(paste_ids))
        return paste_ids
    
    except requests.RequestException as e:
        logger.error("Failed to fetch archive: %s", e)
        return []
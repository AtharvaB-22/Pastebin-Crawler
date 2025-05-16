# fetcher.py

import aiohttp
import asyncio
import logging
from config import RAW_URL_TEMPLATE, RATE_LIMIT_DELAY, USE_PROXIES, PROXIES

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Log to console
    ]
)
logger = logging.getLogger(__name__)

async def fetch_paste_content(session, paste_id, retries=3):
    """
    Fetch raw content for a single paste ID with retry logic.
    Args:
        session: aiohttp.ClientSession for making requests.
        paste_id: str, the paste ID (e.g., 'abc123').
        retries: int, number of retry attempts for failed requests.
    Returns:
        tuple: (paste_id, content) or (paste_id, None) if failed.
    """
    url = RAW_URL_TEMPLATE.format(paste_id)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    proxy = PROXIES[0] if USE_PROXIES and PROXIES else None

    for attempt in range(retries):
        try:
            logger.info("Fetching paste %s (attempt %d/%d)", paste_id, attempt + 1, retries)
            async with session.get(url, headers=headers, proxy=proxy, timeout=10) as response:
                if response.status == 200:
                    content = await response.text()
                    logger.info("Successfully fetched paste %s", paste_id)
                    return paste_id, content
                elif response.status == 429:
                    logger.warning("Rate limit hit for paste %s, retrying after delay", paste_id)
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error("Failed to fetch paste %s: HTTP %d", paste_id, response.status)
                    return paste_id, None
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logger.error("Error fetching paste %s (attempt %d/%d): %s", paste_id, attempt + 1, retries, e)
            if attempt < retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            continue
    logger.error("Failed to fetch paste %s after %d attempts", paste_id, retries)
    return paste_id, None

async def fetch_all_pastes(paste_ids, batch_size=5):
    """
    Fetch content for a list of paste IDs in batches.
    Args:
        paste_ids: list, paste IDs to fetch.
        batch_size: int, number of concurrent requests.
    Returns:
        list: [(paste_id, content), ...], content is None for failed fetches.
    """
    logger.info("Starting to fetch content for %d paste IDs", len(paste_ids))
    results = []
    
    async with aiohttp.ClientSession() as session:
        for i in range(0, len(paste_ids), batch_size):
            batch = paste_ids[i:i + batch_size]
            logger.info("Processing batch of %d paste IDs", len(batch))
            tasks = [fetch_paste_content(session, paste_id) for paste_id in batch]
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            results.extend(batch_results)
            if i + batch_size < len(paste_ids):
                logger.info("Waiting %s seconds before next batch", RATE_LIMIT_DELAY)
                await asyncio.sleep(RATE_LIMIT_DELAY)
    
    logger.info("Completed fetching %d paste IDs", len(paste_ids))
    return results
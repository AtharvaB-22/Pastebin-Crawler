import aiohttp
import asyncio
from config import RATE_LIMIT_DELAY
from logger import get_logger

logger = get_logger(__name__)

async def fetch_paste(session, paste_id, max_retries=3):
    """
    Fetch raw content of a single paste from Pastebin.
    Args:
        session: aiohttp.ClientSession, the HTTP session.
        paste_id: str, the paste ID (e.g., 'abc123').
        max_retries: int, maximum number of retry attempts.
    Returns:
        tuple: (paste_id, content) where content is str or None if failed.
    """
    url = f"https://pastebin.com/raw/{paste_id}"
    for attempt in range(1, max_retries + 1):
        logger.info("Fetching paste %s (attempt %d/%d)", paste_id, attempt, max_retries)
        try:
            async with session.get(url, timeout=10) as response:
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
            logger.error("Error fetching paste %s: %s", paste_id, e)
            if attempt == max_retries:
                return paste_id, None
            await asyncio.sleep(2 ** attempt)
    return paste_id, None

async def fetch_all_pastes(paste_ids, batch_size=5):
    """
    Fetch content for multiple paste IDs in batches.
    Args:
        paste_ids: list, list of paste IDs.
        batch_size: int, number of concurrent requests per batch.
    Returns:
        list: List of (paste_id, content) tuples.
    """
    logger.info("Starting to fetch content for %d paste IDs", len(paste_ids))
    results = []
    async with aiohttp.ClientSession() as session:
        for i in range(0, len(paste_ids), batch_size):
            batch = paste_ids[i:i + batch_size]
            logger.info("Processing batch of %d paste IDs", len(batch))
            tasks = [fetch_paste(session, paste_id) for paste_id in batch]
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            results.extend(batch_results)
            if i + batch_size < len(paste_ids):
                logger.info("Waiting %.1f seconds before next batch", RATE_LIMIT_DELAY)
                await asyncio.sleep(RATE_LIMIT_DELAY)
    logger.info("Completed fetching %d paste IDs", len(paste_ids))
    return results
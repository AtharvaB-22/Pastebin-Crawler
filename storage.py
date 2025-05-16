# storage.py

import json
import logging
from datetime import datetime
from config import OUTPUT_FILE

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Log to console
    ]
)
logger = logging.getLogger(__name__)

def save_paste(paste_id, content, keywords):
    """
    Save paste data to keyword_matches.jsonl if keywords are found.
    Args:
        paste_id: str, the paste ID (e.g., 'abc123').
        content: str or None, the paste content.
        keywords: list, matched keywords (e.g., ['crypto', 't.me']).
    Returns:
        bool: True if saved, False if not (no keywords or error).
    """
    if not keywords:
        logger.info("No keywords for paste %s, skipping storage", paste_id)
        return False

    try:
        # Format paste data into JSON structure
        paste_data = {
            "source": "pastebin",
            "context": f"Found crypto-related content in Pastebin paste ID {paste_id}",
            "paste_id": paste_id,
            "url": f"https://pastebin.com/raw/{paste_id}",
            "discovered_at": datetime.utcnow().isoformat() + "Z",
            "keywords_found": keywords,
            "status": "pending"
        }

        # Write JSON object as a line to keyword_matches.jsonl
        with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
            json.dump(paste_data, f, ensure_ascii=False)
            f.write('\n')  # Add newline for JSONL format

        logger.info("Saved paste %s with keywords %s to %s", paste_id, keywords, OUTPUT_FILE)
        return True

    except Exception as e:
        logger.error("Failed to save paste %s: %s", paste_id, e)
        return False
# keyword_detector.py

import logging
from config import KEYWORDS

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Log to console
    ]
)
logger = logging.getLogger(__name__)

def detect_keywords(paste_id, content):
    """
    Detect specified keywords in paste content.
    Args:
        paste_id: str, the paste ID (e.g., 'abc123').
        content: str or None, the paste content to analyze.
    Returns:
        list: List of matched keywords (e.g., ['crypto', 't.me']).
    """
    if content is None:
        logger.info("No content for paste %s, skipping keyword detection", paste_id)
        return []
    
    matched_keywords = []
    content_lower = content.lower()  # Case-insensitive matching
    logger.info("Detecting keywords in paste %s", paste_id)
    
    for keyword in KEYWORDS:
        if keyword.lower() in content_lower:
            matched_keywords.append(keyword)
            logger.info("Found keyword '%s' in paste %s", keyword, paste_id)
    
    if not matched_keywords:
        logger.info("No keywords found in paste %s", paste_id)
    
    return matched_keywords
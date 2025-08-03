import threading
import random
import string
from datetime import datetime, timezone
from urllib.parse import urlparse

# In-memory store for short_code → metadata
url_store = {}
lock = threading.Lock()

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def is_valid_url(url):
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])

def save_url_mapping(original_url):
    with lock:
        short_code = generate_short_code()
        while short_code in url_store:
            short_code = generate_short_code()

        url_store[short_code] = {
            "url": original_url,
            "clicks": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        return short_code

def get_original_url(short_code):
    with lock:
        if short_code in url_store:
            url_store[short_code]["clicks"] += 1
            return url_store[short_code]["url"]
        return None 

def get_url_stats(short_code):
    with lock:
        return url_store.get(short_code, None)

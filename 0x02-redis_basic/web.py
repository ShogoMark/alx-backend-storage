import requests
import time
from functools import lru_cache

# Dictionary to keep track of URL access count
url_access_count = {}


def update_access_count(url):
    """Helper function to update URL access count."""
    url_access_count[url] = url_access_count.get(url, 0) + 1


def get_page(url):
    """Fetches the HTML content of a URL and caches the result for 10 seconds."""
    update_access_count(url)

    # Use lru_cache to cache the result with an expiration time of 10 seconds
    @lru_cache(maxsize=None, typed=False)
    def fetch_page(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to fetch URL: {url}")

    return fetch_page(url)

#!/usr/bin/env python3
"""
Module for fetching web pages with caching and access counting.
"""

import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    """
    Decorator to cache the result of a function and track how many times it's called.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        The wrapper function for caching the output and tracking access.
        """
        redis_store.incr(f'count:{url}')
        
        cached_result = redis_store.get(f'result:{url}')
        if cached_result:
            return cached_result.decode('utf-8')
        
        result = method(url)
        
        redis_store.setex(f'result:{url}', 10, result)
        
        return result
    return wrapper


@data_cacher
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a particular URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    return requests.get(url).text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"
    
    print("Fetching page for the first time (should be slow):")
    content = get_page(url)
    print(f"Content length: {len(content)}")
    
    print("\nFetching page for the second time (should be fast, cached):")
    content = get_page(url)
    print(f"Content length: {len(content)}")
    
    count = redis_store.get(f"count:{url}")
    print(f"\nThe URL was accessed {count.decode('utf-8')} times.")

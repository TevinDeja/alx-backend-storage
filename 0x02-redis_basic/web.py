#!/usr/bin/env python3
"""
Module for fetching web pages with caching and access counting.
"""

import redis
import requests
from functools import wraps
from typing import Callable

# Module-level Redis instance
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
        # Increment the access count
        redis_store.incr(f'count:{url}')
        
        # Check if the result is cached
        cached_result = redis_store.get(f'result:{url}')
        if cached_result:
            return cached_result.decode('utf-8')
        
        # If not cached, call the original function
        result = method(url)
        
        # Cache the result with expiration time of 10 seconds
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
    # Example usage
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"
    
    print("Fetching page for the first time (should be slow):")
    content = get_page(url)
    print(f"Content length: {len(content)}")
    
    print("\nFetching page for the second time (should be fast, cached):")
    content = get_page(url)
    print(f"Content length: {len(content)}")
    
    # Display the access count
    count = redis_store.get(f"count:{url}")
    print(f"\nThe URL was accessed {count.decode('utf-8')} times.")

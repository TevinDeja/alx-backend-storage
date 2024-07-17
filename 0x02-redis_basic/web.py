#!/usr/bin/env python3
"""
Module for fetching web pages with caching and access counting.
"""

import redis
import requests
from functools import wraps
from typing import Callable


def cache_and_track(expiration_time: int = 10) -> Callable:
    """
    Decorator to cache the result of a function and track how many times it's called.

    Args:
        expiration_time (int): The expiration time for the cache in seconds.

    Returns:
        Callable: The decorated function.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            redis_client = redis.Redis()
            
            # Create keys for caching and counting
            cache_key = f"cache:{url}"
            count_key = f"count:{url}"
            
            # Increment the access count
            redis_client.incr(count_key)
            
            # Check if the result is cached
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return cached_result.decode('utf-8')
            
            # If not cached, call the original function
            result = func(url)
            
            # Cache the result with expiration time
            redis_client.setex(cache_key, expiration_time, result)
            
            return result
        return wrapper
    return decorator


@cache_and_track()
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a particular URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text


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
    redis_client = redis.Redis()
    count = redis_client.get(f"count:{url}")
    print(f"\nThe URL was accessed {count.decode('utf-8')} times.")

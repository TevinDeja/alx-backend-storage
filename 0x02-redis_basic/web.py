#!/usr/bin/env python3
"""
Module for fetching web pages with caching and access counting.
"""

import redis
import requests
from functools import wraps

redis_store = redis.Redis()


def data_cacher(method)
    """
    Decorator to cache the result of a function and track how many times it's called.
    """
    @wraps(method)
    def wrapper(url)
        """
        The wrapper function for caching the output and tracking access.
        """
        cached_key = "cached:" + url
        cached_result = redis_store.get(cached_key)
        
        if cached_result:
            return cached_result.decode('utf-8')
        
        count_key = "count:" + url
        result = method(url)

        redis_store.incr(count_key)
        redis_store.set(cached_key, result)
        redis_store.expire(cached_key, 10)
        
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

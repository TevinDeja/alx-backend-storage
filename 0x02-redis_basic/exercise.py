#!/usr/bin/env python3
"""
Module containing the Cache class for Redis operations and related functions.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the call count and calls the original method.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a particular function.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that stores input and output history and calls the original method.
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        
        # Store input arguments
        self._redis.rpush(input_key, str(args))
        
        # Execute the wrapped function
        output = method(self, *args, **kwargs)
        
        # Store output
        self._redis.rpush(output_key, str(output))
        
        return output
    return wrapper


class Cache:
    """
    A class that provides caching functionality using Redis.
    """

    def __init__(self):
        """
        Initialize the Cache instance with a Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key and return the key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored in Redis.

        Returns:
            str: The randomly generated key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis using the given key and optionally apply a conversion function.

        Args:
            key (str): The key to retrieve data from Redis.
            fn (Optional[Callable]): A function to convert the retrieved data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data, possibly converted, or None if the key doesn't exist.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve a string value from Redis using the given key.

        Args:
            key (str): The key to retrieve data from Redis.

        Returns:
            Union[str, None]: The retrieved string data or None if the key doesn't exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve an integer value from Redis using the given key.

        Args:
            key (str): The key to retrieve data from Redis.

        Returns:
            Union[int, None]: The retrieved integer data or None if the key doesn't exist.
        """
        return self.get(key, fn=int)


def replay(method: Callable):
    """
    Display the history of calls of a particular function.

    Args:
        method (Callable): The method to replay.
    """
    redis_instance = redis.Redis()
    method_name = method.__qualname__
    inputs = redis_instance.lrange(f"{method_name}:inputs", 0, -1)
    outputs = redis_instance.lrange(f"{method_name}:outputs", 0, -1)
    
    print(f"{method_name} was called {len(inputs)} times:")
    
    for input_args, output in zip(inputs, outputs):
        input_str = input_args.decode('utf-8')
        output_str = output.decode('utf-8')
        print(f"{method_name}(*{input_str}) -> {output_str}")


if __name__ == "__main__":
    cache = Cache()
    
    cache.store("foo")
    cache.store("bar")
    cache.store(42)
    
    replay(cache.store)

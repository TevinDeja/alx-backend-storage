#!/usr/bin/env python3
"""
Module containing the Cache class for Redis operations and related functions.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    # ... (previous implementation remains the same)

def call_history(method: Callable) -> Callable:
    # ... (previous implementation remains the same)

class Cache:
    # ... (previous implementation remains the same)

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

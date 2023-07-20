#!/usr/bin/env python3
"""a class Cache and method store that takes in data argument"""

import redis
import uuid
from typing import Union, Callable
from functools import wraps

def count_calls(fn: Callable) -> Callable:
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(fn.__qualname__)
        return fn(self, *args, **kwargs)

    return wrapper

class Cache:
    """class Cache initiating _redis with redis.Redis()"""
    call_count = {}

    def __init__(self):
        """__init__ function for class Cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """takes in data as argument and return key as strings"""
        key = str(uuid.uuid4())
        self._redis.setex(key, 3600, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """takes in key as string and callable function"""
        if fn is None:
            return self._redis.get(key)

        data = self._redis.get(key)
        if data:
            data = data.decode()
            return fn(data)

        return None

    def get_str(self, key: str) -> Union[str, None]:
        """takes in key and returns the respective format"""
        return self.get(key, fn=str)

    def get_int(self, key: str) -> Union[int, None]:
        """takes in key and return its respective format"""
        return self.get(key, fn=int)

    @classmethod
    def get_call_count(cls, method_name: str) -> int:
        """returns the call count for the specified method"""
        return int(cls.call_count.get(method_name) or 0)

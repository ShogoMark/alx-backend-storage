#!/usr/bin/env python3
"""a class Cache and method store that takes in data argument"""

import redis
import uuid


class Cache:
    """class Cache initiating _redis with redis.Redis()"""

    def __init__(self):
        """__init__ function for class Cache"""
        self._redis = redis.Redis()

        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """takes in data as argument and return key as strings"""
        key = str(uuid.uuid4())
        self._redis.setex(key, 3600, data)

        return key

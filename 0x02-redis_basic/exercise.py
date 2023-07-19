#!/usr/bin/env python3
"""a class Cache and method store that takes in data argument"""

import redis
import uuid


class Cache:
    def __init__(self):
        self._redis = redis.Redis()

        self._redis.flushdb()

    def store(self, data) -> str:
        """takes in data as argument and return key as strings"""
        key = str(uuid.uuid4())
        self._redis.setex(key, 3600, data)

        return key

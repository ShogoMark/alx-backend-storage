#!/usr/bin/env python3

import redis
import uuid


class Cache:
    def __init__(self):
        self._redis = redis.Redis()

        self._redis.flushdb()

    def store(self, data) -> str:
        key = str(uuid.uuid4())
        self._redis.setex(key, 3600, data)

        return key
#!/usr/bin/env python3
"""A class Cache and method store that takes in data argument"""

import redis
import uuid
from typing import Union, Callable
from functools import wraps


def replay(self, method: Callable) -> Callable:
    """Display the history of calls for a particular function"""
    inputs_key = "{}:inputs".format(method.__qualname__)
    outputs_key = "{}:outputs".format(method.__qualname__)

    inputs = self._redis.lrange(inputs_key, 0, -1)
    outputs = self._redis.lrange(outputs_key, 0, -1)

    for input_data, output_data in zip(inputs, outputs):
        input_args = eval(input_data.decode())
        output_res = eval(output_data.decode())
        print("{}{} -> {}".format(method.__qualname__, input_args, output_res))


def call_history(method: Callable) -> Callable:
    @wraps(method)
    def wrapper1(self, *args):
        inputs_key = "{}:inputs".format(method.__qualname__)
        outputs_key = "{}:outputs".format(method.__qualname__)

        # Store the input arguments in the Redis list
        self._redis.rpush(inputs_key, str(args))

        # Retrieve output and store it in the outputs list
        res = method(self, *args)
        self._redis.rpush(outputs_key, str(res))

        return res

    return wrapper1


def count_calls(fn: Callable) -> Callable:
    """counts the times calls are made to function"""
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(fn.__qualname__)
        return fn(self, *args, **kwargs)

    return wrapper


class Cache:
    """Class Cache initializing _redis with redis.Redis()"""
    call_count = {}

    def __init__(self):
        """__init__ function for class Cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Takes in data as an argument and returns the key as strings"""
        key = str(uuid.uuid4())
        self._redis.setex(key, 3600, data)
        return key

    def get(
        self,
        key: str,
        fn: Callable = None
    ) -> Union[str, bytes, int, float, None]:
        """Takes in key as a string and a callable function"""
        if fn is None:
            return self._redis.get(key)

        data = self._redis.get(key)
        if data:
            data = data.decode()
            return fn(data)

        return None

    def get_str(self, key: str) -> Union[str, None]:
        """Takes in key and returns the respective format"""
        return self.get(key, fn=str)

    def get_int(self, key: str) -> Union[int, None]:
        """Takes in key and returns its respective format"""
        return self.get(key, fn=int)

    @classmethod
    def get_call_count(cls, method_name: str) -> int:
        """Returns the call count for the specified method"""
        return int(cls.call_count.get(method_name) or 0)

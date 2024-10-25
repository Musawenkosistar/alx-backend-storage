#!/usr/bin/python3
""" web task """

import requests
import time
import redis
from functools import wraps

cache = redis.Redis()
cache.flushdb()

def cache_page(expiration=10):
    def decorator(func):
        @wraps(func)
        def wrapper(url: str):
            cache_key = f"count:{url}"
            cached_content = cache.get(url)
            if cached_content:
                cache.incr(cache_key)
                return cached_content.decode('utf-8')

            response = func(url)
            cache.set(url, response, ex=expiration)
            cache.set(cache_key, 1)
            return response
        return wrapper
    return decorator

@cache_page(expiration=10)
def get_page(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text

if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk"
    print(get_page(test_url))
    print(get_page(test_url))
    time.sleep(11)
    print(get_page(test_url))

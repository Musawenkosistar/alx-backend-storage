#!/usr/bin/env python3
"""A module with tools for request caching and tracking"""

import requests
import time
from functools import wraps

cache = {}

def cache_result(expiration=10):
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            current_time = time.time()
            cache_key = f"count:{url}"
            if url in cache and (current_time - cache[url]['time'] < expiration):
                cache[cache_key] += 1
                return cache[url]['content']
            else:
                response = func(url)
                cache[url] = {'content': response, 'time': current_time}
                cache[cache_key] = 1
                return response
        return wrapper
    return decorator

@cache_result(expiration=10)
def get_page(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://example.com"
    print(get_page(url))
    print(get_page(url))
    time.sleep(11)
    print(get_page(url))

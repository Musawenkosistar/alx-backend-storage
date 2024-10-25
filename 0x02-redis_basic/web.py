#!/usr/bin/env python3

import redis
import requests
from functools import wraps

r = redis.Redis()

def url_access_count(method):
    @wraps(method)
    def wrapper(url):
        key = "cached:" + url
        cached_value = r.get(key)
        if cached_value:
            return cached_value.decode("utf-8")

        key_count = "count:" + url
        html_content = method(url)

        r.incr(key_count)
        r.set(key, html_content, ex=10)
        return html_content
    return wrapper

@url_access_count
def get_page(url: str) -> str:
    results = requests.get(url)
    return results.text

if __name__ == "__main__":
    print(get_page('http://slowwly.robertomurray.co.uk/delay/1000/url/http://example.com'))

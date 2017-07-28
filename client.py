#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json

from tumblr_token import load_oauth


api_url_prefix = "http://api.tumblr.com/v2/"


def json_to_dict(post):
    tags = post["tags"]
    post_url = post["post_url"]
    timestamp = post["liked_timestamp"]

    return {"tags": tags, "post_url": post_url, "timestamp": timestamp}


def retrieve_like_page(oauth, timestamp):
    if timestamp is not None:
        params = {"before": timestamp}
    else:
        params = {}
    r = requests.get(api_url_prefix + "user/likes", auth=oauth1, params=params)
    posts = json.loads(r.content)["response"]["liked_posts"]
    return [json_to_dict(x) for x in posts]


if __name__ == "__main__":
    oauth1 = load_oauth()

    n = 0
    last_timestamp = None
    while True:
        page = retrieve_like_page(oauth1, last_timestamp)

        if len(page) == 0:
            break

        for p in page:
            n += 1
            print(str(n), end=":")
            print(", ".join(p["tags"]), end=" => ")
            print(p["post_url"])
            last_timestamp = p["timestamp"]

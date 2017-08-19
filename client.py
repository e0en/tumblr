#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json

from tumblr_token import load_oauth


api_url_prefix = "http://api.tumblr.com/v2/"


def retrieve_like_page(oauth, timestamp):
    if timestamp is not None:
        params = {"before": timestamp}
    else:
        params = {}
    r = requests.get(api_url_prefix + "user/likes", auth=oauth1, params=params)
    posts = json.loads(r.content)["response"]["liked_posts"]
    return posts


def retrieve_post(client_id, post_url):
    no_http = post_url.split("//")[1]
    blog_and_post = no_http.split("/")
    blog_id = blog_and_post[0]
    post_id = blog_and_post[2]

    url = api_url_prefix + "blog/" + blog_id + "/posts"
    params = {"api_key": client_id, "id": post_id}
    r = requests.get(url, params)
    post = json.loads(r.content)

    if r.status_code == 200:
        return post['response']['posts'][0]
    else:
        return None


def unlike_post(post, oauth):
    url = api_url_prefix + "user/unlike"
    params = {'id': post['id'], 'reblog_key': post['reblog_key']}
    r = requests.post(url, params, auth=oauth)


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
            last_timestamp = p["liked_timestamp"]

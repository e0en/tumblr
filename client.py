#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

from tumblr_token import load_oauth


if __name__ == "__main__":
    api_url_prefix = "http://api.tumblr.com/v2/"

    oauth1 = load_oauth()
    r = requests.get(api_url_prefix + "user/likes", auth=oauth1)
    print(r.content)

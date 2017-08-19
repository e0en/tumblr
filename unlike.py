#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import client

url = sys.argv[1]
oauth = client.load_oauth()
post = client.retrieve_post(oauth.client.client_key, url)
if post is not None:
    client.unlike_post(post, oauth)

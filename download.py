#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

import requests

import client


def make_filename(post, photo_url):
    tags = '_'.join(post['tags'])
    postfix = "_".join(photo_url.split('/')[-2:])
    components =\
        [post['blog_name'], str(post['id']), post['slug'], tags, postfix]

    filename = "_".join(components)
    if len(filename) > 255:
        components =\
            [post['blog_name'], str(post['id']), post['slug'], postfix]
        filename = "_".join(components)

    return filename


pattern = sys.argv[1].lower()
post_url = sys.argv[2]
dirname = sys.argv[3]

if not os.path.exists(dirname):
    os.mkdir(dirname)

new_list = []
oauth = client.load_oauth()

if pattern in post_url:
    post = client.retrieve_post(post_url)
    if post is not None and 'photos' in post:
        photo_metadata = post['photos']
        for photo in photo_metadata:
            photo_url = photo['original_size']['url']
            filename = make_filename(post, photo_url)
            filepath = os.path.join(dirname, filename)
            if not os.path.exists(filepath):
                with open(filepath, 'wb') as fp:
                    fp.write(requests.get(photo_url).content)

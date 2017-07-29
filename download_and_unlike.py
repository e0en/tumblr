#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import client


TAG = sys.argv[1]


with open("secrets/filtered_list.txt") as fp:
    for line in fp:
        items = line.split("=>")
        tags = items[0]
        if TAG in tags:
            url = items[1].strip()
            post = client.retrieve_post(url)
            if 'photos' in post:
                photo_metadata = post['photos']
                for photo in photo_metadata:
                    print(photo['original_size'])
            break

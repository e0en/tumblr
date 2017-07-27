#!/usr/bin/env python
# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session, OAuth1
import requests
import pickle
import os
from secrets import CLIENT_ID, CLIENT_SECRET, OAUTH_FILE_NAME


def oauth_url(name):
    return "https://www.tumblr.com/oauth/" + name


request_token_url = oauth_url("request_token")
authorize_base_url = oauth_url("authorize")
access_token_url = oauth_url("access_token")


def get_oauth_tokens(client_id, client_secret):
    tumblr = OAuth1Session(client_id, client_secret=client_secret)
    tumblr.fetch_request_token(request_token_url)

    authorization_url = tumblr.authorization_url(authorize_base_url)
    print("Please go here and authorize.", authorization_url)

    redirect_response = input("Pase the full redirect url:")
    tumblr.parse_authorization_response(redirect_response)

    oauth_tokens = tumblr.fetch_access_token(access_token_url)

    resource_owner_key = oauth_tokens.get("oauth_token")
    resource_owner_secret = oauth_tokens.get("oauth_token_secret")

    tumblr.close()

    return OAuth1(client_id,
                  client_secret=client_secret,
                  resource_owner_key=resource_owner_key,
                  resource_owner_secret=resource_owner_secret)


if os.path.exists(OAUTH_FILE_NAME):
    with open(OAUTH_FILE_NAME, "rb") as fp:
        oauth1 = pickle.load(fp)
else:
    oauth1 = get_oauth_tokens(CLIENT_ID, CLIENT_SECRET)
    with open(OAUTH_FILE_NAME, "wb") as fp:
        pickle.dump(oauth1, fp)

api_url_prefix = "http://api.tumblr.com/v2/"

r = requests.get(api_url_prefix + "user/likes", auth=oauth1)
print(r.content)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session, OAuth1
from secrets import client_id, client_secret


def oauth_url(name):
    return "https://www.tumblr.com/oauth/" + name


request_token_url = oauth_url("request_token")
authorize_base_url = oauth_url("authorize")
access_token_url = oauth_url("access_token")


tumblr = OAuth1Session(client_id, client_secret=client_secret)
tumblr.fetch_request_token(request_token_url)

authorization_url = tumblr.authorization_url(authorize_base_url)
print("Please go here and authorize.", authorization_url)

redirect_response = input("Pase the full redirect url:")
tumblr.parse_authorization_response(redirect_response)

oauth_tokens = tumblr.fetch_access_token(access_token_url)

resource_owner_key = oauth_tokens.get("oauth_token")
resource_owner_secret = oauth_tokens.get("oauth_token_secret")

oauth = OAuth1(client_id,
               client_secret=client_secret,
               resource_owner_key=resource_owner_key,
               resource_owner_secret=resource_owner_secret)

api_url_prefix = "http://api.tumblr.com/v2/"

r = tumblr.get(api_url_prefix + "user/likes")
print(r.content)

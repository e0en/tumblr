#!/usr/bin/env python
# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session, OAuth1
from secrets import client_id, client_secret


request_token_url = "https://www.tumblr.com/oauth/request_token"
authorize_base_url = "https://www.tumblr.com/oauth/authorize"
access_token_url = "https://www.tumblr.com/oauth/access_token"

api_url_base = "http://api.tumblr.com/v2/"


tumblr = OAuth1Session(client_id, client_secret=client_secret)
tumblr.fetch_request_token(request_token_url)

authorization_url = tumblr.authorization_url(authorize_base_url)
print("Please go here and authorize.", authorization_url)

redirect_response = input("Pase the full redirect url:")
tumblr.parse_authorization_response(redirect_response)

tumblr.fetch_access_token(access_token_url)

r = tumblr.get(api_url_base + "user/likes")
print(r.content)

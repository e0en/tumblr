#!/usr/bin/env python
# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session, OAuth1
import pickle
import os
import webbrowser


def retrieve_oauth_tokens(
        client_id,
        client_secret,
        request_token_url,
        authorize_url,
        access_token_url,
        ):
    session = OAuth1Session(client_id, client_secret=client_secret)
    session.fetch_request_token(request_token_url)

    authorization_url = session.authorization_url(authorize_url)
    webbrowser.open(authorization_url)

    redirect_response = input("Paste the full redirect url:")
    session.parse_authorization_response(redirect_response)

    oauth_tokens = session.fetch_access_token(access_token_url)

    resource_owner_key = oauth_tokens.get("oauth_token")
    resource_owner_secret = oauth_tokens.get("oauth_token_secret")

    session.close()

    return OAuth1(client_id,
                  client_secret=client_secret,
                  resource_owner_key=resource_owner_key,
                  resource_owner_secret=resource_owner_secret)


def load_oauth(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as fp:
            oauth1 = pickle.load(fp)
    return oauth1


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print(f"usage: python {__file__} [file_name]")
        exit()

    filename = sys.argv[1]

    client_id = input("client id: ")
    client_secret = input("client secret: ")
    request_token_url = input("request token url: ")
    authorize_url = input("authorize url: ")
    access_token_url = input("access token url: ")

    oauth1 = retrieve_oauth_tokens(
        client_id,
        client_secret,
        request_token_url,
        authorize_url,
        access_token_url,
        )

    with open(filename, "wb") as fp:
            pickle.dump(oauth1, fp)

#!/usr/bin/env python3

import requests
import hashlib
import secrets
import string
import sys

# use Selenium to then click the button 

with open("client_credentials.txt") as file:
    client_id = file.readline()
    client_secret = file.readline()

state = "".join(secrets.choice(string.ascii_letters + string.digits) for i in range(20))
scope = "" # need to add these
code_verifier = "".join(secrets.choice(string.ascii_letters + string.digits) for i in range(secrets.randbelow(128 - 43 + 1) + 43))
hashed_code_verifier = hashlib.sha256(code_verifier.encode("utf-8")).hexdigest()

payload = {
    "client_id" : client_id,
    "response_type" : "code",
    "redirect_uri"  : "http://localhost:8080",
    "state" : state,
    "scope" : scope,
    "code_challenge_method" : "S256",
    "code_challenge" : hashed_code_verifier
}

response = requests.get("https://accounts.spotify.com/authorize", params = payload)
# open response.url with Selenium here to click the button
#if response[1] != state:
#    sys.exit("Mismatched state parameter")

# need to proceed here, but will try logging in first


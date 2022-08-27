#!/usr/bin/env python3

import hashlib
import secrets
import string

with open("client_credentials.txt") as file:
    client_id = file.readline()

state = "".join(secrets.choice(string.ascii_letters + string.digits) for i in range(20))
scope = "" # need to add these
code_verifier = "".join(secrets.choice(string.ascii_letters + string.digits) for i in range(secrets.randbelow(128 - 43 + 1) + 43))
hashed_code_verifier = hashlib.sha256(code_verifier.encode("ascii")).hexdigest()

with open("get_request_params.txt", "w") as file:
    file.write(state + "\n")
    file.write(code_verifier + "\n")

payload = {
    "client_id" : client_id,
    "response_type" : "code",
    "redirect_uri"  : "http://localhost:8080",
    "state" : state,
    "scope" : scope,
    "code_challenge_method" : "S256",
    "code_challenge" : hashed_code_verifier
}

url = "https://accounts.spotify.com/authorize?"
for key, value in payload.items():
    url += key + "=" + value + "&"

print(url)


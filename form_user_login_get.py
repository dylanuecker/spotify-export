#!/usr/bin/env python3

import secrets
import string
import webbrowser

with open("authentication/client_credentials.txt") as file:
    client_id = file.readline()

state = "".join(secrets.choice(string.ascii_letters + string.digits) for i in range(20))
scope = "playlist-read-private user-library-read playlist-read-collaborative"

with open("authentication/state.txt", "w") as file:
    file.write(state + "\n")

payload = {
    "client_id" : client_id,
    "response_type" : "code",
    "redirect_uri"  : "http://localhost:8080",
    "state" : state,
    "scope" : scope,
}

url = "https://accounts.spotify.com/authorize?"
for key, value in payload.items():
    url += key + "=" + value + "&"

webbrowser.open(url)


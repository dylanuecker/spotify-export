#!/usr/bin/env python3

import requests

with open("access_token.txt") as file:
    access_token = file.readline()

base_url = "https://api.spotify.com/v1"

headers = {
    "Authorization" : "Bearer " + access_token,
    "Content-Type" : "application/json"
}

saved_tracks = requests.get(base_url + "/me/tracks", headers = headers)
print(saved_tracks.json())


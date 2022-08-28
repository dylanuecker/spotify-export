#!/usr/bin/env python3

import requests

with open("access_token.txt") as file:
    access_token = file.readline()

base_url = "https://api.spotify.com/v1"

headers = {
    "Authorization" : "Bearer " + access_token,
    "Content-Type" : "application/json"
}

# saved tracks first (saved local files are not counted, see Spotify Local Music for these if so desired)
total = requests.get(base_url + "/me/tracks", headers = headers).json()["total"]

with open("saved_tracks.txt", "w") as file:
    for i in range(0, total, 50):
        payload = {
            "limit" : 50,
            "offset" : i
        }

        for saved_track in requests.get(base_url + "/me/tracks", headers = headers, params = payload).json()["items"]:
            print(saved_track)
            #file.write(saved_track + "\n")


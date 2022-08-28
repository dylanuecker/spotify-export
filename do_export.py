#!/usr/bin/env python3

import requests
import json

with open("authentication/access_token.txt") as file:
    access_token = file.readline()

base_url = "https://api.spotify.com/v1"

headers = {
    "Authorization" : "Bearer " + access_token,
    "Content-Type" : "application/json"
}

def write_raw(song, output):
    output.write(json.dumps(song) + "\n\n")

def strip_and_write_song(song, output):
    print(song["added_at"])
    for elem in song["track"]:
        print(elem)
    print(song["track"]["artists"][0]["name"])
    print(song["track"]["id"])

# saved tracks first (saved local files are not counted, see Spotify Local Music for these if so desired)
total = requests.get(base_url + "/me/tracks", headers = headers).json()["total"]
per_get = 1 
raw_file = open("exports/saved_tracks_raw.txt", "w")
formatted_file = open("exports/saved_tracks.csv", "w")
formatted_file.write("name,artist(s),album,added_at,duration_ms,explicit")
# using commas as delimiter, not worrying about commas in data

for offset in range(0, 1, per_get):
    payload = {
        "limit" : per_get,
        "offset" : offset
    }

    for saved_track in requests.get(base_url + "/me/tracks", headers = headers, params = payload).json()["items"]:
        write_raw(saved_track, raw_file)
        strip_and_write_song(saved_track, formatted_file)

raw_file.close()
formatted_file.close()


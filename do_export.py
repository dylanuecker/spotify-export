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

def ms_to_min_and_sec(ms):
    mi, se = divmod(ms / 1000, 60)
    ro_se = int(round(se))
    return str(int(mi)) + ":" + ("0" if ro_se < 10 else "") + str(ro_se)

def strip_and_write_song(song, output):
    row = "\n" + song["track"]["name"] + ","
    first = True
    for artist in song["track"]["artists"]:
        if first:
            first = False
        else:
            row += " "
        row += artist["name"]
    row += "," + song["track"]["album"]["name"]
    row += "," + song["added_at"]
    row += "," + ms_to_min_and_sec(song["track"]["duration_ms"])
    row += "," + ("yes" if song["track"]["explicit"] else "no")
    output.write(row)

def export_saved_tracks():
    total = requests.get(base_url + "/me/tracks", headers = headers).json()["total"]
    per_get = 50 
    st_raw_file = open("exports/saved_tracks_raw.txt", "w")
    st_file = open("exports/saved_tracks.csv", "w")
    st_file.write("name,artist(s),album,added_at,duration,explicit")
    # using commas as delimiter, not worrying about commas in data

    for offset in range(0, total, per_get):
        payload = {
            "limit" : per_get,
            "offset" : offset
        }

        for saved_track in requests.get(base_url + "/me/tracks", headers = headers, params = payload).json()["items"]:
            write_raw(saved_track, st_raw_file)
            strip_and_write_song(saved_track, st_file)

    st_raw_file.close()
    st_file.close()

def export_albums():
    return

def export_playlists():
    return

export_saved_tracks()
#export_albums()
#export_playlists()


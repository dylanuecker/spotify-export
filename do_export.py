#!/usr/bin/env python3

import requests
import json
import sys

usage = "Usage ./do_export.py <y/n for saved tracks> <y/n for saved albums> <y/n for playlists>"

if len(sys.argv) != 4:
    sys.exit(usage)

if sys.argv[1] == "y" or sys.argv[1] == "Y":
    do_export_saved_tracks = True
elif sys.argv[1] == "n" or sys.argv[1] == "N":
    do_export_saved_tracks = False
else:
    sys.exit(usage)

if sys.argv[2] == "y" or sys.argv[2] == "Y":
    do_export_saved_albums = True
elif sys.argv[2] == "n" or sys.argv[2] == "N":
    do_export_saved_albums = False
else:
    sys.exit(usage)

if sys.argv[3] == "y" or sys.argv[3] == "Y":
    do_export_playlists = True
elif sys.argv[3] == "n" or sys.argv[3] == "N":
    do_export_playlists = False
else:
    sys.exit(usage)

with open("authentication/access_token.txt") as file:
    access_token = file.readline()

base_url = "https://api.spotify.com/v1"

headers = {
    "Authorization" : "Bearer " + access_token,
    "Content-Type" : "application/json"
}

def write_raw(raw, output):
    output.write(json.dumps(raw) + "\n\n")

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

def strip_and_write_album(album, output):
    row = "\n" + album["album"]["name"] + ","
    first = True
    for artist in album["album"]["artists"]:
        if first:
            first = False
        else:
            row += " "
        row += artist["name"]
    row += "," + album["added_at"]
    output.write(row)

def export_saved_tracks():
    total = requests.get(base_url + "/me/tracks", headers = headers).json()["total"]
    per_get = 50 
    st_raw_file = open("exports/saved_tracks_raw.txt", "w")
    st_file = open("exports/saved_tracks.csv", "w")
    st_file.write("name,artist(s),album,added_at,duration,explicit")

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

def export_saved_albums():
    total = requests.get(base_url + "/me/albums", headers = headers).json()["total"]
    per_get = 50 
    sa_raw_file = open("exports/saved_albums_raw.txt", "w")
    sa_file = open("exports/saved_albums.csv", "w")
    sa_file.write("name,artist(s),added_at")

    for offset in range(0, total, per_get):
        payload = {
            "limit" : per_get,
            "offset" : offset
        }

        for album in requests.get(base_url + "/me/albums", headers = headers, params = payload).json()["items"]:
            write_raw(album, sa_raw_file)
            strip_and_write_album(album, sa_file)

    sa_raw_file.close()
    sa_file.close()

def export_playlists():
    return

if do_export_saved_tracks:
    export_saved_tracks()
    print("Exported saved tracks")

if do_export_saved_albums:
    export_saved_albums()
    print("Exported saved albums")

if do_export_playlists:
    export_playlists()
    print("Exported playlists")


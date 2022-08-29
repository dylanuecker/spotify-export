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
per_get = 50

headers = {
    "Authorization" : "Bearer " + access_token,
    "Content-Type" : "application/json"
}

width = 30
lotta_spaces = " " * width + "\r"

def write_raw(raw, output):
    output.write(json.dumps(raw) + "\n\n")

def ms_to_min_and_sec(ms):
    mi, se = divmod(ms / 1000, 60)
    ro_se = int(round(se))
    return str(int(mi)) + ":" + ("0" if ro_se < 10 else "") + str(ro_se)

def strip_and_write_track(track, output, from_playlist):
    row = "\n" + track["track"]["name"]
    first = True
    for artist in track["track"]["artists"]:
        if first:
            row += ","
            first = False
        else:
            row += " "
        row += artist["name"]
    row += "," + track["track"]["album"]["name"]
    row += "," + track["added_at"]
    if from_playlist:
        first = True
        row += "," + track["added_by"]["id"]
        row += "," + ("yes" if track["is_local"] else "no")
    row += "," + ms_to_min_and_sec(track["track"]["duration_ms"])
    row += "," + ("yes" if track["track"]["explicit"] else "no")
    output.write(row)

def strip_and_write_album(album, output):
    row = "\n" + album["album"]["name"]
    first = True
    for artist in album["album"]["artists"]:
        if first:
            row += ","
            first = False
        else:
            row += " "
        row += artist["name"]
    row += "," + album["added_at"]
    output.write(row)
# Could really do a much job writing these methods and reduce redundant code, but who cares
def strip_and_write_playlist_metadata(playlist, output):
    row = "\n" + playlist["name"]
    row += "," + playlist["owner"]["id"]
    row += "," + ("yes" if playlist["collaborative"] else "no")
    row += "," + ("public" if playlist["public"] else "private")
    row += ',"' + playlist["description"] + '"' # high probability of " in description
    output.write(row)

def export_saved_tracks():
    total = requests.get(base_url + "/me/tracks", headers = headers).json()["total"]
    print("Number of saved tracks: " + str(total))
    st_raw_file = open("exports/saved_tracks_raw.txt", "w")
    st_file = open("exports/saved_tracks.csv", "w")
    st_file.write("name,artist(s),album,added_at,duration,explicit")

    for offset in range(0, total, per_get):
        payload = {
            "limit" : per_get,
            "offset" : offset
        }

        for saved_track in requests.get(base_url + "/me/tracks", headers = headers, params = payload).json()["items"]:
            print(lotta_spaces, end = "")
            print("Exporting " + saved_track["track"]["name"][:width - 10] + "\r", end = "")
            write_raw(saved_track, st_raw_file)
            strip_and_write_track(saved_track, st_file, False)

    st_raw_file.close()
    st_file.close()

def export_saved_albums():
    total = requests.get(base_url + "/me/albums", headers = headers).json()["total"]
    print("Number of saved albums: " + str(total))
    sa_raw_file = open("exports/saved_albums_raw.txt", "w")
    sa_file = open("exports/saved_albums.csv", "w")
    sa_file.write("name,artist(s),added_at")

    for offset in range(0, total, per_get):
        payload = {
            "limit" : per_get,
            "offset" : offset
        }

        for album in requests.get(base_url + "/me/albums", headers = headers, params = payload).json()["items"]:
            print(lotta_spaces, end = "")
            print("Exporting " + album["album"]["name"][:width - 10] + "\r", end = "")
            write_raw(album, sa_raw_file)
            strip_and_write_album(album, sa_file)

    sa_raw_file.close()
    sa_file.close()

def export_playlists():
    total = requests.get(base_url + "/me/playlists", headers = headers).json()["total"]
    print("Number of playlists: " + str(total))
    ap_raw_file = open("exports/all_playlists_raw.txt", "w")
    ap_file = open("exports/all_playlists.csv", "w")
    ap_file.write("name,owner,collaborative,public,description")
    # handling local files here correctly?

    for offset in range(0, total, per_get):
        payload = {
            "limit" : per_get,
            "offset" : offset
        }

        for playlist_link in requests.get(base_url + "/me/playlists", headers = headers, params = payload).json()["items"]:
            playlist = requests.get(base_url + "/playlists/" + playlist_link["id"], headers = headers, params = payload).json()
            write_raw(playlist, ap_raw_file)
            strip_and_write_playlist_metadata(playlist, ap_file)

            name = playlist["name"]
            print(lotta_spaces, end = "")
            print("Exporting " + name[:width - 10] + "\r", end = "")
            name = name.replace("/", "") # don't screw up directories

            p_raw_file = open("exports/playlists/" + name + "_raw.txt", "w")
            write_raw(playlist, p_raw_file)
            p_raw_file.close()

            p_file = open("exports/playlists/" + name + ".csv", "w")
            p_file.write("name,artist(s),album,added_at,added_by,is_local,duration,explicit")
            for track in playlist["tracks"]["items"]:
                strip_and_write_track(track, p_file, True)
            p_file.close()

    ap_raw_file.close()
    ap_file.close()

if do_export_saved_tracks:
    print("Starting saved tracks export")
    export_saved_tracks()
    print(lotta_spaces, end = "")
    print("Exported saved tracks\n")

if do_export_saved_albums:
    print("Starting saved albums export")
    export_saved_albums()
    print(lotta_spaces, end = "")
    print("Exported saved albums\n")

if do_export_playlists:
    print("Starting playlists export")
    export_playlists()
    print(lotta_spaces, end = "")
    print("Exported playlists")


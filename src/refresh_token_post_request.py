#!/usr/bin/env python3

from relative_paths import AUTHENTICATION_PATH
import requests
import base64

with open(AUTHENTICATION_PATH + "client_credentials.txt") as file:
    client_id = file.readline().strip()
    client_secret = file.readline().strip()

with open(AUTHENTICATION_PATH + "refresh_token.txt") as file:
    refresh_token = file.readline()

base64_encoding = base64.b64encode((client_id + ":" + client_secret).encode("ascii"))

headers = {
    "Authorization" : "Basic " + base64_encoding.decode("ascii"),
    "Content-Type" : "application/x-www-form-urlencoded"
}

payload = {
    "grant_type" : "refresh_token",
    "refresh_token" : refresh_token
}

response = requests.post("https://accounts.spotify.com/api/token", params = payload, headers = headers)

with open(AUTHENTICATION_PATH + "access_token.txt", "w") as file:
    file.write(response.json()["access_token"])
    print("Successfully received and wrote access token")

if "refresh_token" in response.json():
    with open(AUTHENTICATION_PATH + "refresh_token.txt", "w") as file:
        file.write(response.json()["refresh_token"])
        print("Wrote a new refresh token as well")


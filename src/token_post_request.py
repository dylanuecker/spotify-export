#!/usr/bin/env python3

from relative_paths import AUTHENTICATION_PATH
import requests
import base64
import sys

uri = input("Copy and paste the localhost uri you were directed to after authentication:\n\n")
print()
params = uri[23:].split("&")

first_param = params[0].split("=")
if first_param[0] != "code":
    sys.exit("Error with logging in user")

code = first_param[1]

with open(AUTHENTICATION_PATH + "/state.txt") as file:
    state = file.readline().strip()

if params[1].split("=")[1] != state:
    sys.exit("State does not match")

with open(AUTHENTICATION_PATH + "client_credentials.txt") as file:
    client_id = file.readline().strip()
    client_secret = file.readline().strip()

base64_encoding = base64.b64encode((client_id + ":" + client_secret).encode("ascii"))

headers = {
    "Authorization" : "Basic " + base64_encoding.decode("ascii"),
    "Content-Type" : "application/x-www-form-urlencoded"
}

payload = {
    "grant_type" : "authorization_code",
    "code" : code,
    "redirect_uri" : "http://localhost:8080",
}

response = requests.post("https://accounts.spotify.com/api/token", params = payload, headers = headers)

with open(AUTHENTICATION_PATH + "access_token.txt", "w") as file:
    file.write(response.json()["access_token"])

with open(AUTHENTICATION_PATH + "refresh_token.txt", "w") as file:
    file.write(response.json()["refresh_token"])

print("Successfully received and wrote access token + refresh token\n")


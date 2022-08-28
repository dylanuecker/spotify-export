#!/usr/bin/env python3

import requests
import base64

uri = input("Enter redirected uri: ")
print()
params = uri[23:].split("&")

first_param = params[0].split("=")
if first_param[0] != "code":
    print("Error with logging in user")
    exit()

code = first_param[1]

with open("authentication/state.txt") as file:
    state = file.readline().strip()

if params[1].split("=")[1] != state:
    print("State does not match")
    exit()

with open("authentication/client_credentials.txt") as file:
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

access_token = response.json()["access_token"] # other returned params, but don't need

with open("authentication/access_token.txt", "w") as file:
    file.write(access_token)

print("Successfully received and wrote access token")

# Not implementing requesting a refreshed access token (just reauthenticate)


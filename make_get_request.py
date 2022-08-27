#!/usr/bin/env python3

import requests
import hashlib
import secrets
import string
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()

with open("client_credentials.txt") as file:
    client_id = file.readline()
    client_secret = file.readline()

with open("user_credentials.txt") as file:
    username = file.readline()
    password = file.readline()

state = "".join(secrets.choice(string.ascii_letters + string.digits) for i in range(20))
scope = "" # need to add these
code_verifier = "".join(secrets.choice(string.ascii_letters + string.digits) for i in range(secrets.randbelow(128 - 43 + 1) + 43))
hashed_code_verifier = hashlib.sha256(code_verifier.encode("utf-8")).hexdigest()

payload = {
    "client_id" : client_id,
    "response_type" : "code",
    "redirect_uri"  : "http://localhost:8080",
    "state" : state,
    "scope" : scope,
    "code_challenge_method" : "S256",
    "code_challenge" : hashed_code_verifier
}

response = requests.get("https://accounts.spotify.com/authorize", params = payload)
print(response.url)
driver.get(response.url)
driver.find_element(By.ID, "login-username").send_keys(username)
driver.find_element(By.ID, "login-password").send_keys(password)
driver.find_element(By.ID, "login-button").click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Agree']"))).click()

# open response.url with Selenium here to click the button
#if response[1] != state:
#    sys.exit("Mismatched state parameter")

# need to proceed here, but will try logging in first
driver.quit()


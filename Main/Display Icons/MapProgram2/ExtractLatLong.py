"""
A python program that extracts latitude and longitude from an address.
"""
from urllib.parse import urlencode
import requests
import pandas as pd

with open("google_api_key.txt", "r") as api_file:
    API_KEY = api_file.read().strip()

def extract_lat_lng(address, data_type = "json"):
    global API_KEY
    endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
    params = {"address": address, "key": API_KEY}
    url_params = urlencode(params)
    url = f"{endpoint}?{url_params}" 
    r = requests.get(url)
    if r.status_code not in range(200, 299):
        return {}
    latlng = {}
    try:
        latlng = r.json()["results"][0]["geometry"]["location"]
    except:
        print("Latitude and longitude not found.")
    return latlng.get("lat"), latlng.get("lng")     

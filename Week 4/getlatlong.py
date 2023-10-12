"""
A python program that extracts latitude and longitude from an address.
"""
from urllib.parse import urlencode, urlparse, parse_qsl
import requests
import gmaps
import gmaps.datasets
import pandas as pd

API_KEY = "***REMOVED***"
gmaps.configure(api_key=API_KEY)

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

def get_road_suburb():
    data = pd.read_csv("data.csv")
    ## declaring stores for latitude and longitude
    location_name = []
    latslongs = []
    ## extracting relevant data from data.csv
    for index, row in data.iterrows():
        road = row["ROAD"]
        suburb = row["SUBURB"]
        location_name.append(road + ", " + suburb)
    for location in location_name:
        # address = location_name.index(location)
        lat, lng = extract_lat_lng(location)
        latslongs.append((lat, lng))
        #print(f"Address: {address}, Latitude: {lat}, Longitude: {lng}"
    return latslongs
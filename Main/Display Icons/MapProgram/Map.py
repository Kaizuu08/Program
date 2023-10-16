from flask import Flask, render_template, request, jsonify
import folium
import folium.plugins
import pandas as pd
import openrouteservice as ors
from ExtractLatLong import extract_lat_lng

# Read in OpenRouteService API key from text file
with open("ors_api_key.txt", "r") as api_file:
    api_key = api_file.read().strip()

# Creates client object for ORS API
client = ors.Client(key=api_key)

# Initialise Flask App
app = Flask(__name__)

# Create Map with start location, zoom and tile config
m = folium.Map(location=[-27.189539, 152.9694482], tiles="cartodbpositron", zoom_start=12)

# Reads in dataset
data = pd.read_csv("UpdatedData.csv")

# Directory for icon image
#icon_directory = r"Icon/Directory"    

@app.route('/')
def show_map():
    # Displaying road closure icons using latitude and longitude
    for index, row in data.iterrows():
        latitude = row["LATITUDE"]
        longitude = row["LONGITUDE"]

        closure_icon = folium.CustomIcon(icon_image="road_closure_icon.png",icon_size=(25, 25))
        marker = folium.Marker(location=[latitude, longitude], icon=closure_icon, popup = row["ADDRESS"].replace("Queensland, Australia", "") + "\nFlooded on:\n(" + str(row["TIME"]) + ")")
        marker.add_to(m)

    # Adding additional functionality
    folium.LayerControl().add_to(m)
    folium.plugins.Fullscreen().add_to(m)

    # Render the map
    return m.get_root().render()

""" Not in use right now, needs to add options for user to add end and start position"""
# Function to provide navigatation between two locations
def navigation():
    start_position = request.form.get('start_location')
    end_position = request.form.get('end_location')

    try:
        start_lat, start_lng = extract_lat_lng(start_position)
        end_lat, end_lng = extract_lat_lng(end_position)
    except:
        print("Latitude and Longitude not found.")
    start_position = [start_lng, start_lat]
    end_position = [end_lng, end_lat]

    # Calculates route given locations and method of transport
    route = client.directions(coordinates=[start_position, end_position], profile="driving-car", format="geojson")
    # Adds start and end markers
    start_marker = folium.Marker(location=start_position, popup = start_position, color="green")
    end_marker = folium.Marker(location=end_position, popup = end_position, color="green")
    start_marker.add_to(m)
    end_marker.add_to(m)

    # Gets each coordinate within the route and puts into list
    coordinate_list = [list(reversed(coord)) for coord in route["features"][0]["geometry"]["coordinates"]]

    # Adds a polyLine with the coordinates to the map
    folium.PolyLine(locations=coordinate_list, color="blue").add_to(m)   

if __name__ == '__main__':
    app.run(debug=True)

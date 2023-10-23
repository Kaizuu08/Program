# Import required modules
from flask import Flask, render_template, request
import folium
import pandas as pd
import openrouteservice as ors
from ExtractLatLong import extract_lat_lng
import fiona as fn
from shapely.geometry import Polygon, mapping, MultiPolygon, LineString, Point
import pyproj

# Read in OpenRouteService API key from a text file
with open("ors_api_key.txt", "r") as api_file:
    api_key = api_file.read().strip()

# Creates a client object for ORS API
client = ors.Client(key=api_key)

# Initialize Flask App
app = Flask(__name__)

# Read in datasets and establish directory
data = pd.read_csv("UpdatedData.csv")
rainfall = pd.read_csv("Rainfall_Data.csv")
icon_directory = r"C:\Users\Ainsley\OneDrive - University of the Sunshine Coast\CSC100\Program\Main\Display Icons\MapProgram2"

nav_marked = False

# Function to create a folium map
def create_map(lat=-27.189539, lng=152.9694482):
    global current_map
    current_map = folium.Map(location=[lat, lng], tiles="cartodbpositron", zoom_start=12)
# Create a map when the program is run
create_map()

# Function to render the map within the webpage
@app.route('/map')
def show_map():
    return current_map.get_root().render(), 200, {'Content-Type': 'text/html'}

# Function to render html file
@app.route('/')
def index():
    return render_template('index.html', map_url="/map")

# Function to add road closure markers to map
def add_markers():
    global flooded
    flooded =[]
    for index, row in filtered_data.iterrows():
        latitude = row["LATITUDE"]
        longitude = row["LONGITUDE"]
        closure_icon = folium.CustomIcon(icon_image="road_closure_icon.png", icon_size=(25, 25))
        marker = folium.Marker(location=[latitude, longitude], icon=closure_icon, popup=row["ADDRESS"].replace(", Queensland, Australia", "") + "\nFlooded:\n(" + str(row["TIME"]) + ")")
        marker.add_to(current_map)
        flood = create_buffer_polygon([latitude, longitude],resolution=2, radius=20)
        flooded.append(flood)

# Function to handle rainfall user input
@app.route('/submit', methods=["GET", "POST"])
def button_submit():
    global filtered_data
    if request.method == 'POST':
        try:
            rainfall_limit = request.form.get("rainfallAmount")
            rainfall_limit = float(rainfall_limit)  # Convert to a numeric type
            filtered_data = rainfall[(rainfall["RAINFALL"] < rainfall_limit) & (rainfall["RAINFALL"] > 30)]
            filtered_data = data[data["TIME"].isin(filtered_data["TIME"])]
            update_map()
        except Exception as e:
            print("An error has occured.")
    return render_template('index.html', map_url="/map")

# Function to update map when new rainfall or navigation inputs are submitted
def update_map():
    if nav_marked == True:
        create_map()
        add_markers()
        calculate_route()
    else:
        create_map()
        add_markers()

# Function to calculate route and add markers
def calculate_route():
    global coordinates, start_position, end_position
    avoided_coords = [] 
    route_directions = create_route(avoided_coords, [coordinates[0][::-1], coordinates[1][::-1]]) 
    buffered_route = create_buffer(route_directions) 
    for site_poly in flooded:
        poly = Polygon([list(reversed(coord)) for coord in site_poly])
        if poly.within(buffered_route):
            avoided_coords.append(poly)
            route_directions = create_route(avoided_coords, [coordinates[0][::-1], coordinates[1][::-1]]) 
            buffered_route = create_buffer(route_directions)  

    # Extract coordinates from the route response
    coordinate_list = [list(reversed(coord)) for coord in route_directions["features"][0]["geometry"]["coordinates"]]

    # Add a polyline with the coordinates to the map
    line = folium.PolyLine(locations=coordinate_list, color="blue")
    line.add_to(current_map)
    # Add location markers to the map
    start_marker = folium.Marker(location=list(coordinates[0]), popup=start_position, color="green")
    end_marker = folium.Marker(location=list(coordinates[1]), popup=end_position, color="green")
    start_marker.add_to(current_map)
    end_marker.add_to(current_map) 
             
# Function to handle navigation user input
@app.route('/navigation', methods=["GET", "POST"])
def navigation():
    global nav_marked, coordinates, start_position, end_position
    if request.method == 'POST':
        try:
            start_position = request.form.get('startAddress')
            end_position = request.form.get('endAddress')
            # Extract latitude and longitude and initialize default lat & lng between locations
            coordinates = [extract_lat_lng(start_position), extract_lat_lng(end_position)]
            midpoint_lat = (coordinates[0][0] + coordinates[1][0]) / 2
            midpoint_lng = (coordinates[0][1] + coordinates[1][1]) / 2
            
            if nav_marked == True:
                current_map = create_map(midpoint_lat, midpoint_lng)
                add_markers(filtered_data, current_map)
            calculate_route()
            nav_marked = True
        except Exception as e:
            print(f"Unable to navigate. Error: {str(e)}")
    return render_template('index.html', map_url="/map")

# Function to create a buffer around each road closure coordinate
def create_buffer_polygon(point_in, resolution=2, radius=20):
    # Converting between different coordinate systems
    convert = pyproj.Transformer.from_crs("epsg:4326", 'epsg:32632')
    convert_back = pyproj.Transformer.from_crs('epsg:32632', "epsg:4326")
    point_in_proj = convert.transform(*point_in)
    point_buffer_proj = Point(point_in_proj).buffer(radius, resolution=resolution) 
    poly_wgs = []
    for point in point_buffer_proj.exterior.coords:
        poly_wgs.append(convert_back.transform(*point))  # Transform back to WGS84
    return poly_wgs

# Function to create route that avoids road closures using ORS API
def create_route(avoided_point_list, coordinates):
    route = {
        'coordinates': coordinates,
        'profile': 'driving-car',
        'format': 'geojson',
        'preference': 'shortest',
        'options': {
            'avoid_polygons': mapping(MultiPolygon(avoided_point_list))
        }
    }
    route_directions = client.directions(**route)
    return route_directions


# Function to create a buffer around the route
def create_buffer(route):
    line_tup = []
    for line in route['features'][0]['geometry']['coordinates']:
        tup_format = tuple(line)
        line_tup.append(tup_format)

    new_linestring = LineString(line_tup)
    buffered_route = new_linestring.buffer(0.001)
    return buffered_route


if __name__ == '__main__':
    app.run(debug=False)

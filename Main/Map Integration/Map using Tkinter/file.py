import tkinter
from tkintermapview import TkinterMapView
import pandas as pd
import googlemaps

## google api
api_key = "***REMOVED***" 
gmaps = googlemaps.Client(key = api_key)

## function to return distance between two points
def calculate_distance():
    origin = origin_var.get()
    destination = destination_var.get()
    pass

## function to zoom into selected location
def zoom_to_location():
    selected_location = location_var.get()
    for index, row in enumerate(locations):
        latitude = row[0]
        longitude = row[1]
        name = row[2]
        if name == selected_location:
            map_widget.set_position(latitude, longitude)
            map_widget.set_zoom(15)
            break

## loadingg data as data
data = pd.read_csv("data.csv")

## declaring stores for latitude and longitude
locations = []

## extracting relevant data from data.csv
for index, row in data.iterrows():
    location_name = row["Location Name"]
    latitude = row["Latitude"]
    longitude = row["Longitude"]
    locations.append((latitude, longitude,location_name))

## intialising the tkinter window
root_tk = tkinter.Tk()
root_tk.geometry("800x600")
root_tk.title("Google Maps")

## drop down to select location & search button
location_label = tkinter.Label(root_tk, text="Select Location:")
location_label.pack()
location_var = tkinter.StringVar()
location_dropdown = tkinter.OptionMenu(root_tk, location_var, *set(location[2] for location in locations))
location_dropdown.pack()
search_button = tkinter.Button(root_tk, text="Search", command=zoom_to_location)
search_button.pack()

## Buttons for determining location distances
origin_label = tkinter.Label(root_tk, text="Select Origin:")
origin_label.pack()
origin_var = tkinter.StringVar()
origin_dropdown = tkinter.OptionMenu(root_tk, origin_var, *set(location[2] for location in locations))
origin_dropdown.pack()

destination_label = tkinter.Label(root_tk, text="Select Destination:")
destination_label.pack()
destination_var = tkinter.StringVar()
destination_dropdown = tkinter.OptionMenu(root_tk, destination_var, *set(location[2] for location in locations))
destination_dropdown.pack()

calculate_button = tkinter.Button(root_tk, text="Calculate Distance", command=calculate_distance)
calculate_button.pack()

## displaying the tkintermap widgets
map_widget = TkinterMapView(root_tk, width = 600, height=400, corner_radius=0)
map_widget.pack(fill="both",expand = True)

## importing the data as markers
markers = {}  # Create an empty dictionary to store markers
for index, row in enumerate(locations):
    latitude = row[0]
    longitude = row[1]
    name = row[2]
    
    marker_name = f"marker_{index}"  # Generate a unique marker variable name
    markers[marker_name] = map_widget.set_marker(latitude, longitude, text=name)

root_tk.mainloop()
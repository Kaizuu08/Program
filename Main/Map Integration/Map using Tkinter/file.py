import tkinter
from tkintermapview import TkinterMapView
import pandas as pd

## loadingg data as data
data = pd.read_csv("data.csv")

## declaring stores for latitude and longitude
locations = []

## extracting relevant data from data.csv
for index, row in data.iterrows():
    name = row["Location Name"]
    latitude = row["Latitude"]
    longitude = row["Longitude"]
    locations.append((latitude, longitude,name))

## intialising the tkinter window
root_tk = tkinter.Tk()
root_tk.geometry("500x500")
root_tk.title("Google Maps")

## displaying the tkintermap widgets
map_widget = TkinterMapView(root_tk, width = 600, height=400, corner_radius=0)
map_widget.pack(fill="both",expand = True)

## set current widget position and zoom
map_widget.set_position(locations[0][0], locations[0][1])  # the first station position
map_widget.set_zoom(15)

## importing the data as markers
markers = {}  # Create an empty dictionary to store markers
for index, row in enumerate(locations):
    latitude = row[0]
    longitude = row[1]
    name = row[2]
    
    marker_name = f"marker_{index}"  # Generate a unique marker variable name
    markers[marker_name] = map_widget.set_marker(latitude, longitude, text=name)

root_tk.mainloop()
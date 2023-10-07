import tkinter
from tkintermapview import TkinterMapView
import pandas as pd

## loadingg data as data
data = pd.read_csv("data.csv")

## declaring stores for latitude and longitude
locations = []

## extracting relevant data from data.csv
for index, row in data.iterrows():
    latitude = row["Latitude"]
    longitude = row["Longitude"]
    locations.append((latitude, longitude))

print (locations[0][0])
## intialising the tkinter window
root_tk = tkinter.Tk()
root_tk.geometry("500x500")
root_tk.title("Google Maps")

## displaying the tkintermap widgets
map_widget = TkinterMapView(root_tk, width = 600, heigh=400, corner_radius=0)
map_widget.pack(fill="both",expand = True)

## importing google resources
map_widget.set_position(locations[0][0], locations[0][1])

root_tk.mainloop()
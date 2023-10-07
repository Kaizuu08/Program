import tkinter
from tkintermapview import TkinterMapView
import pandas as pd

# Load the data from the CSV file
data = pd.read_csv("data.csv")

# Now, you can extract latitude and longitude columns
latitudes = data["Latitude"]
longitudes = data["Longitude"]

# Example: Printing the first few rows to verify data loading
print(data.head())

## intialising the tkinter window
root_tk = tkinter.Tk()
root_tk.geometry("500x500")
root_tk.title("Google Maps")

## displaying the tkintermap widgets
map_widget = TkinterMapView(root_tk, width = 600, heigh=400, corner_radius=0)
map_widget.pack(fill="both",expand = True)

## importing google resources
#map_widget.set_position()

root_tk.mainloop()
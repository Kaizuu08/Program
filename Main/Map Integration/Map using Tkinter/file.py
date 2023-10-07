import tkinter
from tkintermapview import TkinterMapView

## intialising the tkinter window
root_tk = tkinter.Tk()
root_tk.geometry("500x500")
root_tk.title("Google Maps")

## displaying the tkintermap widgets
map_widget = TkinterMapView(root_tk, width = 600, heigh=400, corner_radius=0)
map_widget.pack(fill="both",expand = True)

root_tk.mainloop()
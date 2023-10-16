# using the googlemaps module, tis program gets the latitude and longitde of the inserted address
import googlemaps

#Store API key for usage
gmaps = googlemaps.Client(key="AIzaSyCqubcCK_1D3asTroRdtQPVrvV3VzmYwgY")

# Perform geocoding inserting address
geocode_result = gmaps.geocode('90 Sippy Downs Dr, Sippy Downs, QLD')

# Print the latitude and longitude
location = geocode_result[0]['geometry']['location']
print(f"Latitude: {location['lat']}, Longitude: {location['lng']}")


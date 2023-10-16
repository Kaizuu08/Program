"""
A python program that cleans existing dataset and saves to a new csv file
"""
import pandas as pd
from ExtractLatLong import extract_lat_lng

# Reads in dataset
data = pd.read_csv("data.csv")
new_dataset = []

# Loop through each row and assign to variables
for index, row in data.iterrows():
    road = row["ROAD"]
    suburb = row["SUBURB"]
    location = str(road) + ", " + str(suburb) + ", Queensland, Australia"
    reason = row["REASON"]
    update_time = row["UPDATETIME"]

    # Call function to extract latitude and longitude from address
    lat, lng = extract_lat_lng(location)

    # Check if flooded and if information is missing
    if lat is not None and lng is not None and update_time is not None and reason == "Flooded":
        new_data = {
            "LATITUDE": lat,
            "LONGITUDE": lng,
            "ADDRESS": location,
            "REASON": reason,
            "TIME": update_time
            }
        new_dataset.append(new_data)

# Turn dictionary into dataframe
new_dataset = pd.DataFrame(new_dataset)
# Save the new dataset to a CSV file
new_dataset.to_csv("UpdatedData.csv", index=False)
print("New Dataset Created Successfully")

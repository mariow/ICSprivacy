import os
from filter_ics import filter_private_events

# Load the ICS file data
with open("tmp/source.ics", "r") as f:
    ics_data = f.read()

# Call the filter_private_events function
filtered_ics_data = filter_private_events(ics_data)

# Save the filtered ICS data to a file
with open("tmp/filtered.ics", "w") as f:
    f.write(filtered_ics_data)

# Print the filtered ICS data to the console
print("Filtered ICS data:")
print(filtered_ics_data)


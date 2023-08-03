import pandas as pd
import matplotlib.pyplot as plt

# List of CSV files
csv_files = ['world.csv', 'camatim_short.csv']

# Initialize empty lists for average locations
average_locations_x = []
average_locations_y = []

# Iterate over each CSV file
for file in csv_files:
    first_row = pd.read_csv(file, nrows=1).to_string(index=False)
    size = first_row[first_row.find(":") + 2:first_row.find("\n")]
    frame_width = int(size[:size.find("x")])
    frame_height = int(size[size.find("x") + 1:])

    # Step 3: Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file, skiprows=2)

    # Step 4: Extract the face location data
    face_data = df[['x1', 'y1', 'x2', 'y2']]

    # Step 5: Scale the face coordinates based on the frame size

    face_data['x1'] = face_data['x1'] / frame_width
    face_data['y1'] = face_data['y1'] / frame_height
    face_data['x2'] = face_data['x2'] / frame_width
    face_data['y2'] = face_data['y2'] / frame_height

    # Step 6: Calculate the average location for each file
    average_location = face_data.mean()

    # Append average locations to lists
    average_locations_x.append(average_location['x1'])
    average_locations_y.append(average_location['y1'])

# Plot the average locations for all files
plt.figure(figsize=(6, 6))
plt.scatter(average_locations_x, average_locations_y, c='red', marker='o')
plt.xlabel('X (Normalized)')
plt.ylabel('Y (Normalized)')
plt.title('Average Location of Faces')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.gca().invert_yaxis()
plt.show()

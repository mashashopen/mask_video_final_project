import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('world.csv', skiprows=2)

first_row = pd.read_csv('world.csv', nrows=1).to_string(index=False)

# Step 4: Extract the frame size
size = first_row[first_row.find(":") + 2:first_row.find("\n")]
frame_width = int(size[:size.find("x")])
frame_height = int(size[size.find("x") + 1:])

# Step 5: Initialize an empty heatmap
heatmap = np.zeros((frame_height, frame_width))

# Step 6: Update the heatmap based on face locations
for index, row in df.iterrows():
    x1, y1, x2, y2 = row['x1'], row['y1'], row['x2'], row['y2']
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    heatmap[y1:y2, x1:x2] += 1

# Step 7: Plot the heatmap
plt.imshow(heatmap, cmap='hot')
plt.colorbar(label='Frequency')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Heatmap of Face Locations')
plt.show()



face_data = df[['x1', 'y1', 'x2', 'y2']]

# Step 5: Scale the face coordinates based on the frame size
face_data['x1'] = face_data['x1'] / frame_width
face_data['y1'] = face_data['y1'] / frame_height
face_data['x2'] = face_data['x2'] / frame_width
face_data['y2'] = face_data['y2'] / frame_height

# Step 6: Calculate the average location of the faces
average_location = face_data.mean()

# Step 7: Plot the average location
plt.figure(figsize=(6, 6))
plt.scatter(average_location['x1'], average_location['y1'], c='red', marker='o')
plt.xlabel('X (Normalized)')
plt.ylabel('Y (Normalized)')
plt.title('Average Location of Faces (Normalized)')
plt.xlim(0, 1)  # Set the X-axis limits to match the normalized coordinates
plt.ylim(0, 1)  # Set the Y-axis limits to match the normalized coordinates
plt.gca().invert_yaxis()  # Invert the Y-axis to match the video frame
plt.show()
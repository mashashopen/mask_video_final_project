import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys


def main():
    csv_file = sys.argv[1]

    # Step 1: Read csv file

    df = pd.read_csv(csv_file, skiprows=2)

    first_row = pd.read_csv(csv_file, nrows=1).to_string(index=False)

    # Step 2: Extract the frame size
    size = first_row[first_row.find(":") + 2:first_row.find("\n")]
    frame_width = int(size[:size.find("x")])
    frame_height = int(size[size.find("x") + 1:])

    # Step 3: Initialize an empty heatmap
    heatmap = np.zeros((frame_height, frame_width))

    # Step 4: Update the heatmap based on face locations
    for index, row in df.iterrows():
        x1, y1, x2, y2 = row['x1'], row['y1'], row['x2'], row['y2']
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        heatmap[y1:y2, x1:x2] += 1

    # Step 5: Plot the heatmap
    plt.imshow(heatmap, cmap='hot')
    plt.colorbar(label='Frequency')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Heatmap of Face Locations')
    plt.show()


if __name__ == "__main__":
    main()

import csv

import cv2
import os
from extract_frames import ExtractFrames
from mask_frame import MaskFrame
from tqdm import tqdm
from tkinter import Tk, Label, Entry, Button, filedialog


class MaskVideo:
    def __init__(self, video_file: str, kernel_size: tuple, epsilon: float):
        self.extract_frames_manager = ExtractFrames(video_file)
        self.video_file_name = video_file
        self.kernel_size = kernel_size
        self.epsilon = epsilon

        self.fps = self.extract_frames_manager.extract_frames_and_get_fps()

        # Create a VideoWriter object to write the frames to a video file
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video = cv2.VideoWriter(self.video_file_name[:-4] + '-masked.mp4', self.fourcc, self.fps,
                                      self._get_width_height())

    def _get_width_height(self) -> tuple:
        dir_name = self.extract_frames_manager.get_unmasked_dir_name()
        frame = cv2.imread(os.path.join(dir_name, self._get_unmasked_sorted_frames()[0]))
        height, width, layers = frame.shape
        return width, height

    def _get_unmasked_sorted_frames(self) -> list:
        return self.extract_frames_manager.sorted_frames_files()

    def extract_data_to_csv_file(self, data, unmasked_frames):
        # Specify the field names (column names) for the CSV file
        fieldnames = ["number_of_frame", "x1", "y1", "x2", "y2"]

        filename_without_extension = self.video_file_name[:-4]
        # Specify the file name for the CSV file
        filename = filename_without_extension + ".csv"

        # Open the CSV file in write mode
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Add comments or metadata to the CSV file
            csvfile.write(self.extract_frames_manager.get_video_dimensions() + "\n")
            csvfile.write("Number of frames:" + str(len(unmasked_frames)) + "\n")
            # Write the header (field names)
            writer.writeheader()
            # Write the data rows
            for row in data:
                writer.writerow(row)
            writer.writerow(row)
        print("CSV file exported successfully.")

    def mask_video_flow(self):
        unmasked_frames = self._get_unmasked_sorted_frames()
        rows = []

        with tqdm(total=len(unmasked_frames), desc="Progress", unit="frame") as pbar:
            for i, frame in enumerate(unmasked_frames):
                full_path = self.extract_frames_manager.get_unmasked_dir_name() + "/" + frame
                mask_frame_manager = MaskFrame(full_path)
                for face in mask_frame_manager.get_all_faces_locations():
                    row = {"number_of_frame": i, "x1": face[0], "y1": face[1], "x2": face[2], "y2": face[3]}
                    rows.append(row)
                masked_frame = mask_frame_manager.mask_frame(self.kernel_size, self.epsilon)
                self.video.write(masked_frame)
                pbar.update(1)
        self.video.release()

        self.extract_data_to_csv_file(rows, unmasked_frames)




root = Tk()
root.title("Mask Video")
root.geometry("400x150")

entry_video_file = Entry(root, width=40)
entry_video_file.pack()


def browse_video_file():
    filename = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])
    entry_video_file.delete(0, "end")
    entry_video_file.insert(0, filename)

def process_video():
    video_file = entry_video_file.get()
    mask_video = MaskVideo(video_file, (5, 5), 10)
    mask_video.mask_video_flow()


label_video_file = Label(root, text="Video File:")
label_video_file.pack()

entry_video_file = Entry(root, width=40)
entry_video_file.pack()

button_browse = Button(root, text="Browse", command=browse_video_file)
button_browse.pack()

button_process = Button(root, text="Process Video", command=process_video)
button_process.pack()

root.mainloop()

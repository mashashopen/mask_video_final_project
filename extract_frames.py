from datetime import timedelta
import cv2
import numpy as np
import os
import retina
import sys
import time

UNMASKED_FRAMES_DIR = "-unmasked_frames"
SAVING_FRAMES_PER_SECOND = 30


class ExtractFrames:

    def __init__(self, video_file_name: str):
        self.video_file_name = video_file_name
        self.unmasked_dir_name = self.get_unmasked_dir_name()
        self.create_dir(self.unmasked_dir_name)

    def get_unmasked_dir_name(self) -> str:
        video_name = os.path.splitext(self.video_file_name)
        dir_name = video_name[0] + UNMASKED_FRAMES_DIR
        return dir_name

    @staticmethod
    def _format_timedelta(td) -> str:
        result = str(td)
        try:
            result, ms = result.split(".")
        except ValueError:
            return (result + ".00").replace(":", "-")
        ms = int(ms)
        ms = round(ms / 1e4)
        return f"{result}.{ms:02}".replace(":", "-")

    @staticmethod
    def _get_saving_frames_durations(cap, saving_fps) -> list:
        """A function that returns the list of durations where to save the frames"""
        s = []
        # get the clip duration by dividing number of frames by the number of frames per second
        clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
        # use np.arange() to make floating-point steps
        for i in np.arange(0, clip_duration, 1 / saving_fps):
            s.append(i)
        return s

    def create_dir(self, dir_name):
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)

    def extract_frames_and_get_fps(self):
        # read the video file
        cap = cv2.VideoCapture(self.video_file_name)
        # get the FPS of the video
        fps = cap.get(cv2.CAP_PROP_FPS)
        # if the SAVING_FRAMES_PER_SECOND is above video FPS, then set it to FPS (as maximum)
        saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
        # get the list of duration spots to save
        saving_frames_durations = self._get_saving_frames_durations(cap, saving_frames_per_second)
        # start the loop
        count = 0
        while True:
            is_read, frame = cap.read()
            if not is_read:
                # break out of the loop if there are no frames to read
                break
            # get the duration by dividing the frame count by the FPS
            frame_duration = count / fps
            try:
                # get the earliest duration to save
                closest_duration = saving_frames_durations[0]
            except IndexError:
                # the list is empty, all duration frames were saved
                break
            if frame_duration >= closest_duration:
                # if closest duration is less than or equals the frame duration,
                # then save the frame
                frame_duration_formatted = self._format_timedelta(timedelta(seconds=frame_duration))
                cv2.imwrite(os.path.join(self.unmasked_dir_name, f"frame{frame_duration_formatted}.png"), frame)
                # drop the duration spot from the list, since this duration spot is already saved
                try:
                    saving_frames_durations.pop(0)
                except IndexError:
                    pass
            # increment the frame count
            count += 1
        return fps

    def sorted_frames_files(self):
        return sorted(filter(lambda x: os.path.isfile(os.path.join(self.unmasked_dir_name, x)),
                             os.listdir(self.unmasked_dir_name)))

    def get_video_dimensions(self) -> str:

        files = os.listdir(self.unmasked_dir_name)

        # Filter for image files
        image_files = [file for file in files if file.lower().endswith((".jpg", ".jpeg", ".png", ".gif"))]

        # Get the path of the first image file
        if image_files:
            first_image_path = os.path.join(self.unmasked_dir_name, image_files[0])
            print("Path of the first image file:", first_image_path)

        image = Image.open(first_image_path)

        # Get the dimensions (height and width) of the image
        width, height = image.size

        # Print the retrieved dimensions
        return "Frame Dimensions: {}x{}".format(width, height)


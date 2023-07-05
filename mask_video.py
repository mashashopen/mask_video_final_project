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
        self.video = cv2.VideoWriter(self.video_file_name + '-masked.mp4', self.fourcc, self.fps,
                                      self._get_width_height())

    def _get_width_height(self) -> tuple:
        dir_name = self.extract_frames_manager.get_unmasked_dir_name()
        frame = cv2.imread(os.path.join(dir_name, self._get_unmasked_sorted_frames()[0]))
        height, width, layers = frame.shape
        return width, height

    def _get_unmasked_sorted_frames(self) -> list:
        return self.extract_frames_manager.sorted_frames_files()

    def mask_video_flow(self):
        unmasked_frames = self._get_unmasked_sorted_frames()
        with tqdm(total=len(unmasked_frames), desc="Progress", unit="frame") as pbar:
            for i, frame in enumerate(unmasked_frames):
                full_path = self.extract_frames_manager.get_unmasked_dir_name() + "/" + frame
                mask_frame_manager = MaskFrame(full_path)
                masked_frame = mask_frame_manager.mask_frame(self.kernel_size, self.epsilon)
                self.video.write(masked_frame)
                pbar.update(1)
        self.video.release()


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

button_process = Button(root, text="Mask Video", command=process_video)
button_process.pack()

root.mainloop()

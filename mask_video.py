import cv2
import os
import shutil
from PIL import Image, ImageTk
from tkinter import Tk, Label, Entry, Button, filedialog, ttk, Scale, HORIZONTAL
from extract_frames import ExtractFrames
from mask_frame import MaskFrame
from tqdm import tqdm

class MaskVideo:
    def __init__(self, video_file: str, kernel_size: tuple, epsilon: float, destination_folder: str = None):
        self.extract_frames_manager = ExtractFrames(video_file)
        self.video_file_name = os.path.basename(video_file)  # Use the video file name without path
        self.kernel_size = kernel_size
        self.epsilon = epsilon

        self.fps = self.extract_frames_manager.extract_frames_and_get_fps()

        if destination_folder:
            # Use the chosen destination folder path if provided
            self.output_video_path = os.path.join(destination_folder, self.video_file_name + '-masked.mp4')
        else:
            # If destination_folder is not provided, use Downloads folder
            self.output_video_path = os.path.join(os.path.expanduser("~"), "Downloads", self.video_file_name + '-masked.mp4')

        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video = cv2.VideoWriter(self.output_video_path, self.fourcc, self.fps, self._get_width_height())

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
                # Update the progress bar
                pbar.update(1)
                progress_bar['value'] = i + 1
                root.update_idletasks()
        self.video.release()
        # Remove the unmasked frames directory
        unmasked_dir = self.extract_frames_manager.get_unmasked_dir_name()
        shutil.rmtree(unmasked_dir)


root = Tk()
root.title("Mask Video")
root.geometry("650x650")

# Load the image
image_path = "people.jpg"
image = Image.open(image_path)

# Calculate the new size to fit the GUI while maintaining the aspect ratio
desired_width = 300
aspect_ratio = desired_width / image.width
desired_height = int(image.height * aspect_ratio)

# Resize the image
image = image.resize((desired_width, desired_height), Image.ANTIALIAS)

# Convert the image to a format compatible with tkinter
photo = ImageTk.PhotoImage(image)

# Create the label to display the original image
label_image = Label(root, image=photo)
label_image.grid(row=0, column=0, padx=10, pady=10)

def update_masked_image():
    global blur_level, coverage_level

    # Load the original image
    original_image = Image.open(image_path)

    # Create a MaskFrame object to apply the mask
    mask_frame_manager = MaskFrame(image_path)
    masked_frame = mask_frame_manager.mask_frame((blur_level, blur_level), coverage_level)

    # Convert the masked_frame to RGB format
    masked_frame_rgb = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2RGB)

    # Resize the masked image to the same size as the original image
    masked_image = Image.fromarray(masked_frame_rgb)
    masked_image = masked_image.resize((desired_width, desired_height), Image.ANTIALIAS)

    # Convert the masked image to PhotoImage and update the displayed image
    masked_photo = ImageTk.PhotoImage(masked_image)
    label_masked_image.configure(image=masked_photo)
    label_masked_image.image = masked_photo  # Keep a reference to prevent image garbage collection

    # Convert the masked image to PhotoImage and update the displayed image
    masked_photo = ImageTk.PhotoImage(masked_image)
    label_masked_image.configure(image=masked_photo)
    label_masked_image.image = masked_photo  # Keep a reference to prevent image garbage collection

# Create the label to display the masked image
label_masked_image = Label(root, image=photo)  # Initialize with the original image
label_masked_image.grid(row=0, column=1, padx=10, pady=10)

# Create a variable to store the blur level selected by the slider
blur_level = 10  # Initial default blur level

# Create the slider widget for blur level
slider_blur = Scale(root, from_=1, to=50, orient=HORIZONTAL, length=300, label="Blur Level:")
slider_blur.set(blur_level)  # Set the initial value of the slider
slider_blur.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

# Create a variable to store the coverage level selected by the slider
coverage_level = 10  # Initial default coverage level

# Create the slider widget for coverage level
slider_coverage = Scale(root, from_=1, to=50, orient=HORIZONTAL, length=300, label="Mask size:")
slider_coverage.set(coverage_level)  # Set the initial value of the slider
slider_coverage.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

def update_parameters():
    global blur_level, coverage_level
    blur_level = slider_blur.get()
    coverage_level = slider_coverage.get()
    update_masked_image()  # Update the masked image when parameters change

def browse_video_file():
    filename = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])
    entry_video_file.delete(0, "end")
    entry_video_file.insert(0, filename)

def choose_destination_folder():
    folder_path = filedialog.askdirectory()
    entry_destination_folder.delete(0, "end")
    entry_destination_folder.insert(0, folder_path)

# Create a label for displaying the status message
label_status_message = Label(root, text="", fg="green")
label_status_message.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

# Update the process_video function to include the destination folder
def process_video():
    if not blur_level or not coverage_level:
        print("Please update the parameters first.")
        return

    video_file = entry_video_file.get()
    destination_folder = entry_destination_folder.get()  # Get the chosen destination folder

    mask_video = MaskVideo(video_file, (blur_level, blur_level), coverage_level, destination_folder)
    mask_video.mask_video_flow()

    # Display the status message after the masking and downloading process is finished
    label_status_message.config(text="Masking finished, the masked video was downloaded to: {}".format(mask_video.output_video_path))


button_update_params = Button(root, text="Update Parameters", command=update_parameters)
button_update_params.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

entry_video_file = Entry(root, width=40)
entry_video_file.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

button_browse = Button(root, text="Browse video file", command=browse_video_file)
button_browse.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

# Create a label and entry widget for the destination folder
label_destination_folder = Label(root, text="Destination Dir:")
label_destination_folder.grid(row=6, column=0, padx=0, pady=5)  # Move the label to row 5

entry_destination_folder = Entry(root, width=40)
entry_destination_folder.grid(row=6, column=0,columnspan=2, padx=10, pady=5)  # Move the entry to row 5

# Create a button to browse and select the destination folder
button_browse_destination = Button(root, text="Browse Destination", command=choose_destination_folder)
button_browse_destination.grid(row=7, column=0,columnspan=2, padx=10, pady=5)  # Move the button to row 5

button_process = Button(root, text="Mask Video", command=process_video)
button_process.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

progress_bar = ttk.Progressbar(root, orient='horizontal', length=200, mode='determinate')
progress_bar.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()

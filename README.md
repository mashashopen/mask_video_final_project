# mask faces in video final project

Dr. Sharon Gilai Dotan's laboratory houses a valuable collection of global videos. The goal is to share these videos online while safeguarding the privacy of individuals featured in them. To achieve this, we've created a specialized tool as part of our project. This tool enables users to view these worldwide videos and compile a database of videos with faces that the laboratory is comfortable sharing openly, free from privacy concerns.

Our developed tool takes a video and various parameters as input and then generates the same video with human faces blurred to varying degrees, depending on the selected parameters. To accomplish this, we harnessed the power of RetinaFace, a renowned deep learning model for facial recognition:  https://github.com/serengil/retinaface   


## run this project locally:  
   
Clone the repo and run: python mask_video.py   

Or you can find the executable file in this website: https://www.gilaie-dotan-lab.com/depth-judgements   
and you can simply download it and follow the instruction below.  

## How to Use the Mask Video GUI

1. Update Parameters: Adjust the blur level and mask size parameters using the sliders. Click 'Update Parameters' to apply the changes to the preview and video.

2. Browse Video File: Click 'Browse video file' to select the video you want to mask.

3. Browse Destination: Click 'Browse Destination' to choose the output folder for the masked video. If no destination is chosen, the masked video will be saved in the "Downloads" directory by default.

4. Mask Video: Click 'Mask Video' to start the masking process.

5. Progress Bar: The progress bar shows the percentage of frames that have been masked.

6. Masking Finished: Once the masking process is complete, a pop-up message will display the path to the masked video. The saved format will be in the following pattern: "random_number-video_name-blur_level-mask_size".

Note: The 'Blur Level' controls the amount of blur applied to the video frames, while the 'Mask size' controls the size of the masked region.
Pay attention, the process run time is approximately 1 minute run per 1 second of the video. So for example, a video of duration 30 second, will be ready after 30 minutes. 


## run analysis scripts:

1. single video analysis:  
   run analysis.py <csv_file_path>  
   * the file path should not contain spaces.  
   the output is a graph that puts a red dot in the average location of the detected faces.

2. multi videos analysis:  
   run multi_analysis.py <csv_file_path_1> <csv_file_path_2> <csv_file_path_3> ...<csv_file_path_n>  
   * the file paths should not contain spaces.  
   the output is a heat map that colors the map according to the frequency of detected faces in every pixel. areas with high frequency of detected faces will be colored with bright color, areas with low frequency of detected faces will be colored with dark color.


## the program:  

the program includes 3 files:  
1. mask_frame.py -> responsible for masking only one frame, running the retinaface itself, blurs the frame according to the given parameters.
2. extract_frames.py -> processes the input video file, meaning extracts the frames, saves them on a separate directory.
3. mask_video.py -> the main program which connects the other 2 classes, loops all the frames, creates the GUI, creates the output video file and the csv file.
   




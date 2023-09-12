# mask_video_final_project

This project masks human faces in video the program gets as an input. It was created for the Gilaie-Dotan lab.    
The face detection algorithm that was used here, is RetinaFace, based on this project:  https://github.com/serengil/retinaface   

# run this project locally:  
   
Clone the repo and run: python mask_video.py   

1. Choose parameters which with you want to mask the entire video and click on Update Parameters.
2. Click on Browse video file and choose the video you want to mask from your files browser.
3. Click on Browse Destination and select the directory you want to download the video to (the default is your current directory).
4. Click on Mask Video and wait for the video to be ready. It will be downloaded automatically in the end of the proccess. You can see how to process progresses looking on the displayed progress bar. Pay attention, the process run time is approximately 1 minute run per 1 second of the video. So for example, a video of duration 30 second, will be ready after 30 minutes.    


The executable file can be found in this website: https://www.gilaie-dotan-lab.com/experiments  
and you can simply download it and follow the instruction above.  



# run analysis scripts:

1. single video analysis:
   run analysis.py <csv_file_path>  
   * the file path should not contain spaces.  
   the output is a graph that puts a red dot in the average location of the detected faces.

2. multi videos analysis:
   run multi_analysis.py <csv_file_path_1> <csv_file_path_2> <csv_file_path_3> ...<csv_file_path_n>
   * the file paths should not contain spaces.
   the output is a heat map that colors the map according to the frequency of detected faces in every pixel. areas with high frequency of detected faces will be colored with bright color, areas with low frequency of detected faces will be colored with dark color.   


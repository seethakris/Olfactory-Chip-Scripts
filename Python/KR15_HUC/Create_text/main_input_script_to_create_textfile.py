# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 13:35:15 2015
@author: seetha

For Olfactory Chip data analysis
Take user input in this file and call other routines
"""

## Enter Main Folder containing stimulus folders to create text files

Exp_Folder ='/Volumes/Seagate/Microfluidic_Chip/Data/HUC-KR15/Fish27_Kr153aHUC_8dpf/Tiff/Cropped/Registered/Thresholded_OB/Registered_Stimulus/'
filename_save_prefix = 'ThresholdedOB_T129'

#Rewrite text files. 1- Yes
rewrite_flag = 0

#Experiment parameters
img_size_x = 200 #X and Y resolution - if there are images that dont have this resolution, they will be resized
img_size_y = 350
img_size_crop_x1 = 0 #How many pixels to crop on x and y axis. If none say 0
img_size_crop_x2 = 0
img_size_crop_y1 = 0 #How many pixels to crop on x and y axis. If none say 0
img_size_crop_y2 = 0

# Time period within which to do the analysis
time_start = 0
time_end = 129

#Stimulus on and off time
stimulus_pulse = 1
if stimulus_pulse == 1:
    stimulus_on_time = [11,29,48,66,84,102]
    stimulus_off_time = [14,32,51,69,87,105]
    color_mat = ['#00FFFF','#0000A0','#800080','#FF00FF', '#800000','#A52A2A']

#Set if you want to use raw images or delta f/f. If delta f/f is needed, specify baseline time points
f_f_flag = 0 #0-raw data, 1-delta f/f
dff_start = 10
dff_end = 20

## Median filter - threshold
median_filter_threshold = 1
######################################################################


######################################################################
########################## Run Scripts ###############################

# Go into the main function that takes thunder data and 
from main_file_for_textfiles_for_thunder import initial_function

initial_function(Exp_Folder, filename_save_prefix, img_size_x, img_size_y, img_size_crop_x1, img_size_crop_x2, img_size_crop_y1, img_size_crop_y2, \
stimulus_on_time, stimulus_off_time, time_start,time_end, f_f_flag, dff_start, dff_end, median_filter_threshold, rewrite_flag)

import pickle

with open(Exp_Folder+filename_save_prefix+'_save_input_variables', 'w') as f:
    pickle.dump([img_size_x,img_size_y,img_size_crop_x1, img_size_crop_x2, img_size_crop_y1, img_size_crop_y2,\
    time_start,time_end,stimulus_pulse, stimulus_on_time, stimulus_off_time], f)



# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 13:35:15 2015
@author: seetha

For Olfactory Chip data analysis
Take user input in this file and call other routines
"""

## Enter Main Folder containing stimulus folders. Ensure the data in the stimulus folders are registered
## and are multitiffs in Z

Exp_Folder = '/media/seetha/Se/Microfluidic Chip_Data/Data/Fish1_5dpf/Tiff/Registered/Registered_Stimulus/'

#Prefix using which all text files, figures, matfiles and numpy array for this run of thunder will be saved.
#If text file with prefixed name already exists, the script will go straight to running PCA
filename_save_prefix = 'test1'

#Experiment parameters
img_size_x = 128 #X and Y resolution - if there are images that dont have this resolution, they will be resized
img_size_y = 256
img_size_crop_x = 10 #How many pixels to crop on x and y axis. If none say 0
img_size_crop_y = 10
num_time = 30 #Total Number of time points in experiment

#Only time points specified in these two variables will be used
#for creating text files and further analysis
time_start = 1 #Starting time point
time_end = 30 #Ending time point

#Stimulus on and off time
stim_start = 10 #Stimulus Starting time point
stim_end = 15 #Stimulus Ending time point

#Set if you want to use raw images or delta f/f. If delta f/f is needed, specify baseline time points
f_f_flag = 0 #0-raw data, 1-delta f/f
dff_start = 10
dff_end = 20

#PCA parameters
pca_components = 3 #Number of pca components to detect from files
num_pca_colors = 150 #Number of colors on the pca maps
num_samples = 3000 #number of random samples to select to do PCA reconstruction
thresh_pca = 0.0001 #Threshold above which to plot the pca components
color_map = 'polar' #Colormap for plotting principle components
######################################################################



######################################################################
########################## Run Scripts ###############################

# Go into the main function that creates text files and runs analysis
from thunder_main import initial_function

initial_function(Exp_Folder, filename_save_prefix, img_size_x, img_size_y, img_size_crop_x, img_size_crop_y, num_time, \
time_start, time_end, stim_start, stim_end, f_f_flag, dff_start, dff_end, \
pca_components, num_pca_colors, num_samples, thresh_pca, color_map)





# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 13:35:15 2015
@author: seetha

For Olfactory Chip data analysis
Take user input in this file and call other routines
"""

## Enter Main Folder containing stimulus folders. 

Exp_Folder = '/media/seetha/Se/Microfluidic Chip_Data/Data/Fish1_5dpf/Tiff/Registered/Registered_Stimulus/'

#Prefix using which all text files, figures, matfiles and numpy array for this run of thunder will be saved.
#If text file with prefixed name already exists, the script will go straight to running PCA
filename_save_prefix = 'test4'

#Experiment parameters
img_size_x = 128 #X and Y resolution - if there are images that dont have this resolution, they will be resized
img_size_y = 256
img_size_crop_x = 10 #How many pixels to crop on x and y axis. If none say 0
img_size_crop_y = 10

# Time period within which to do the analysis
time_start = 0
time_end = 30

#Stimulus on and off time
stim_start = 15 #Stimulus Starting time point
stim_end = 20 #Stimulus Ending time point

#Set if you want to use raw images or delta f/f. If delta f/f is needed, specify baseline time points
f_f_flag = 0 #0-raw data, 1-delta f/f
dff_start = 10
dff_end = 20

#PCA parameters
pca_components = 3 #Number of pca components to detect from files
num_pca_colors = 50 #Number of colors on the pca maps
num_samples = 100 #number of random samples to select to do PCA reconstruction
thresh_pca = 0.0001 #Threshold above which to plot the pca components
color_map = 'polar' #Colormap for plotting principle components
######################################################################



######################################################################
########################## Run Scripts ###############################

# Go into the main function that takes thunder data and 
from main_file_for_textfiles_for_thunder import initial_function

initial_function(Exp_Folder, filename_save_prefix, img_size_x, img_size_y, \
img_size_crop_x, img_size_crop_y, stim_start, stim_end, time_start,time_end, f_f_flag, dff_start, dff_end)


from main_file_for_thunder_analysis import run_analysis_initial_function

run_analysis_initial_function(Exp_Folder, filename_save_prefix, pca_components, num_pca_colors,\
num_samples, thresh_pca, color_map)


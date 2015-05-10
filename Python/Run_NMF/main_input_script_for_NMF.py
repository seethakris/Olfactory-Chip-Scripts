# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 17:07:18 2015
# Inputs for doing NMF
@author: seetha
"""



## Enter Main Folder containing stimulus folders to create text files
Exp_Folder ='/Users/seetha/Desktop/KCTD/Fish14_KCTDHUC_5dpf/Tiff/Cropped/Registered/Thresholded_OB/Registered_Stimulus/'
filename_save_prefix = 'ThresholdedOB_T81'

#Which files to do NMF on
files_to_do_NMF = [0,0,1] #Individual NMF, Each_exp NMF, All_exp NMF

#Use existing parameters from pickle dump -1  or use new paprameters -0?
use_existing_parameters = 0

#Redo NMF - 1
redo_NMF = 0
remake_colormap = 1

colors_NMF = ['LightYellow','aqua','Orange','Fuchsia','LimeGreen']

#NMF parameters for individual trial NMF
NMF_components_ind = 5 #Number of NMF components to detect from files
num_NMF_colors_ind = 5 #Number of colors on the NMF maps
max_iterations_ind = 20
tolerence_level_ind = 0.001
color_map_ind = 'indexed' #Colormap for plotting NMF components


#NMF parameters for each exp NMF
NMF_components_eachexp = 4 #Number of NMF components to detect from files
num_NMF_colors_eachexp = 4 #Number of colors on the NMF maps
max_iterations_eachexp = 30
tolerence_level_eachexp = 0.001
color_map_eachexp = 'indexed' #Colormap for plotting principle components


#NMF parameters for all exp NMF
NMF_components_allexp = 4 #Number of NMF components to detect from files
num_NMF_colors_allexp = 5 #Number of colors on the NMF maps
max_iterations_allexp = 15
tolerence_level_allexp = 0.01
color_map_allexp= 'indexed' #Colormap for plotting principle components

#Stimulus on and off time
stimulus_pulse = 1
if stimulus_pulse == 1:
    stimulus_on_time = [10,29,49,68]
    stimulus_off_time = [14,33,53,72]

    
elif stimulus_pulse == 2:
    stimulus_on_time = [10,29,48,67,86,105]
    stimulus_off_time = [13,32,51,70,89,108]

## How long is the baseline?
time_baseline = 10
######################################################################
########################## Run Scripts ###############################

# Load imput parameters that were saved from creating text file. 
import pickle

with open(Exp_Folder+filename_save_prefix +'_save_input_variables') as f:
    img_size_x,img_size_y,img_size_crop_x1, img_size_crop_x2, img_size_crop_y1, img_size_crop_y2,\
    time_start,time_end,stimulus_pulse, stimulus_on_time, stimulus_off_time = pickle.load(f)
    
    
if use_existing_parameters == 1:
    with open(Exp_Folder+filename_save_prefix +'_save_NMF_variables') as f:
        NMF_components_ind, num_NMF_colors_ind, color_map_ind,max_iterations_ind, tolerence_level_ind,\
        NMF_components_eachexp, num_NMF_colors_eachexp, color_map_eachexp,max_iterations_eachexp, tolerence_level_eachexp,\
        NMF_components_allexp, num_NMF_colors_allexp, color_map_allexp,max_iterations_allexp, tolerence_level_allexp,colors_NMF = pickle.load(f)


# Go into the main function that does NMF for indiviudal trials
from NMF_thunder_analysis import run_analysis_individualodors
from NMF_thunder_analysis import run_analysis_eachodor
from NMF_thunder_analysis import run_analysis_allodor

from thunder import ThunderContext

print 'Starting Thunder Now. Check console for details'
tsc = ThunderContext.start(appName="thunderNMF")

if files_to_do_NMF[0]== 1:
    run_analysis_individualodors(Exp_Folder, filename_save_prefix,  NMF_components_ind, num_NMF_colors_ind, color_map_ind,\
    tsc,redo_NMF,  stimulus_on_time, stimulus_off_time, time_baseline,colors_NMF,max_iterations_ind, tolerence_level_ind,remake_colormap)
    
if files_to_do_NMF[1]== 1:
    run_analysis_eachodor(Exp_Folder, filename_save_prefix,  NMF_components_eachexp, num_NMF_colors_eachexp, color_map_eachexp,\
    tsc,redo_NMF,  stimulus_on_time, stimulus_off_time, time_baseline,colors_NMF, max_iterations_eachexp, tolerence_level_eachexp,remake_colormap)

if files_to_do_NMF[2]== 1:
    run_analysis_allodor(Exp_Folder, filename_save_prefix, NMF_components_allexp, num_NMF_colors_allexp, color_map_allexp,\
    tsc,redo_NMF,  stimulus_on_time, stimulus_off_time, time_baseline,colors_NMF, max_iterations_allexp, tolerence_level_allexp,remake_colormap)
    
############# Save all imput parameters
with open(Exp_Folder+filename_save_prefix+'_save_NMF_variables', 'w') as f:
    pickle.dump([ NMF_components_ind, num_NMF_colors_ind, color_map_ind,max_iterations_ind, tolerence_level_ind,\
        NMF_components_eachexp, num_NMF_colors_eachexp, color_map_eachexp,max_iterations_eachexp, tolerence_level_eachexp,\
        NMF_components_allexp, num_NMF_colors_allexp, color_map_allexp,max_iterations_allexp, tolerence_level_allexp,colors_NMF], f)

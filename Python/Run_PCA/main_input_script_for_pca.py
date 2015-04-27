# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 17:07:18 2015
# Inputs for doing PCA
@author: seetha
"""



## Enter Main Folder containing stimulus folders to create text files
Exp_Folder ='/Users/seetha/Desktop/KCTD/Fish19_KCTDHUC_8dpf/Tiff/Cropped/Registered/Thresholded_OB/Registered_Stimulus/'
filename_save_prefix_forPCA = 'ThresholdedOB_T128_1and2PC'
filename_save_prefix_for_textfile = 'ThresholdedOB_T128'
#Which files to do PCA on
files_to_do_PCA = [0,0,1] #Individual PCA, Each_odor PCA, All_odor PCA

#Use existing parameters from pickle dump -1  or use new paprameters -0?
use_existing_parameters = 0

#Redo pca - 1
redo_pca = 1

# Required pcs from what was received previously
required_pcs = [1,2]

#PCA parameters for individual trial pca
pca_components_ind = 4 #Number of pca components to detect from files
num_pca_colors_ind = 100 #Number of colors on the pca maps
num_samples_ind = 10000 #number of random samples to select to do PCA reconstruction
thresh_pca_ind = 0.00001 #Threshold above which to plot the pca components
color_map_ind = 'polar' #Colormap for plotting principle components

#PCA parameters for each odor pca
pca_components_eachodor = 4 #Number of pca components to detect from files
num_pca_colors_eachodor = 150 #Number of colors on the pca maps
num_samples_eachodor = 10000 #number of random samples to select to do PCA reconstruction
thresh_pca_eachodor = 0.00001 #Threshold above which to plot the pca components
color_map_eachodor = 'polar' #Colormap for plotting principle components

#PCA parameters for all odor pca
pca_components_allodor = 4 #Number of pca components to detect from files
num_pca_colors_allodor = 100 #Number of colors on the pca maps
num_samples_allodor = 100000 #number of random samples to select to do PCA reconstruction
thresh_pca_allodor = 0.000001 #Threshold above which to plot the pca components
color_map_allodor= 'polar' #Colormap for plotting principle components


#Stimulus on and off time
stimulus_pulse = 2 ##Whether a single pulse or a train of pulses were given
stim_start = 10 #Stimulus Starting time point
stim_end = 14 #Stimulus Ending time point

######################################################################
########################## Run Scripts ###############################

# Load imput parameters that were saved from creating text file. 
import pickle

with open(Exp_Folder+filename_save_prefix_for_textfile +'_save_input_variables') as f:
    img_size_x,img_size_y,img_size_crop_x1, img_size_crop_x2, img_size_crop_y1, img_size_crop_y2,\
    time_start,time_end,stim_start,stim_end,f_f_flag,dff_start,dff_end,stimulus_pulse = pickle.load(f)
    
#Stimulus on and off time
stimulus_pulse = 2 ##Whether a single pulse or a train of pulses were given
stim_start = 10 #Stimulus Starting time point
stim_end = 14 #Stimulus Ending time point
    
if use_existing_parameters == 1:
    with open(Exp_Folder+filename_save_prefix_forPCA+'_save_pca_variables') as f:
        pca_components_ind, num_pca_colors_ind, num_samples_ind, thresh_pca_ind, color_map_ind,\
        pca_components_eachodor, num_pca_colors_eachodor, num_samples_eachodor, thresh_pca_eachodor, color_map_eachodor,\
        pca_components_allodor, num_pca_colors_allodor, num_samples_allodor, thresh_pca_allodor, color_map_allodor,required_pcs  = pickle.load(f)


# Go into the main function that does pca for indiviudal trials
from pca_thunder_analysis import run_analysis_individualodors
from pca_thunder_analysis import run_analysis_eachodor
from pca_thunder_analysis import run_analysis_allodor

from thunder import ThunderContext

print 'Starting Thunder Now. Check console for details'
tsc = ThunderContext.start(appName="thunderpca")

if files_to_do_PCA[0]== 1:
    run_analysis_individualodors(Exp_Folder, filename_save_prefix_forPCA, filename_save_prefix_for_textfile, pca_components_ind, num_pca_colors_ind, num_samples_ind, thresh_pca_ind, color_map_ind,\
    stim_start-time_start, stim_end-time_start, tsc,redo_pca,stimulus_pulse,required_pcs )
    
if files_to_do_PCA[1]== 1:
    run_analysis_eachodor(Exp_Folder, filename_save_prefix_forPCA, filename_save_prefix_for_textfile, pca_components_eachodor, num_pca_colors_eachodor, num_samples_eachodor, thresh_pca_eachodor, color_map_eachodor,\
    stim_start-time_start, stim_end-time_start, tsc,redo_pca,stimulus_pulse,required_pcs )

if files_to_do_PCA[2]== 1:
    run_analysis_allodor(Exp_Folder, filename_save_prefix_forPCA, filename_save_prefix_for_textfile, pca_components_allodor, num_pca_colors_allodor, num_samples_allodor, thresh_pca_allodor, color_map_allodor,\
    stim_start-time_start, stim_end-time_start, tsc,redo_pca,stimulus_pulse,required_pcs )
    
############# Save all imput parameters
with open(Exp_Folder+filename_save_prefix_forPCA+'_save_pca_variables', 'w') as f:
    pickle.dump([pca_components_ind, num_pca_colors_ind, num_samples_ind, thresh_pca_ind, color_map_ind,\
        pca_components_eachodor, num_pca_colors_eachodor, num_samples_eachodor, thresh_pca_eachodor, color_map_eachodor,\
        pca_components_allodor, num_pca_colors_allodor, num_samples_allodor, thresh_pca_allodor, color_map_allodor, required_pcs ], f)

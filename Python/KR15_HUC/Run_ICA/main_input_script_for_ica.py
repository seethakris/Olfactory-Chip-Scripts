# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 17:07:18 2015
# Inputs for doing ica
@author: seetha
"""



## Enter Main Folder containing stimulus folders to create text files
Exp_Folder ='/Users/seetha/Desktop/KCTD/Fish14_KCTDHUC_5dpf/Tiff/Cropped/Registered/Thresholded_OB/Registered_Stimulus/'
filename_save_prefix = 'ThresholdedOB_T81'

#Which files to do ica on
files_to_do_ica = [0,0,1] #Individual ica, Each_odor ica, All_odor ica

#Use existing parameters from pickle dump -1  or use new paprameters -0?
use_existing_parameters = 0

# redo ica - 1
redo_ica = 0

colors_ica = ['hotpink','aqua','gold','mediumpurple']

#ica parameters for individual trial ica
number_principle_components_ind = 3 #Number of principle components to use
ica_components_ind = 3 #Number of ica components to detect from files
color_map_ind = 'indexed' #Colormap for plotting ica components
num_ica_colors_ind = 100 # number of colors in colormap

#ica parameters for each odor ica
number_principle_components_eachodor = 3 #Number of principle components to use
ica_components_eachodor = 3 #Number of ica components to detect from files
color_map_eachodor = 'indexed' #Colormap for plotting ica components
num_ica_colors_eachodor = 100 # number of colors in colormap

#ica parameters for all odor ica
number_principle_components_allodor = 10 #Number of principle components to use
ica_components_allodor = 4 #Number of ica components to detect from files
color_map_allodor = 'indexed' #Colormap for plotting ica components
num_ica_colors_allodor = 4 # number of colors in colormap

time_baseline = 10

#Stimulus on and off time
stimulus_pulse = 1
if stimulus_pulse == 1:
    stimulus_on_time = [10,30,48,67]
    stimulus_off_time = [14,34,52,71]

    
elif stimulus_pulse == 2:
    stimulus_on_time = [10,29,48,67,86,105]
    stimulus_off_time = [13,32,51,70,89,108]

######################################################################
########################## Run Scripts ###############################

# Load imput parameters that were saved from creating text file. 
import pickle

with open(Exp_Folder+filename_save_prefix +'_save_input_variables') as f:
    img_size_x,img_size_y,img_size_crop_x1, img_size_crop_x2, img_size_crop_y1, img_size_crop_y2,\
    time_start,time_end,stimulus_pulse, stimulus_on_time, stimulus_off_time = pickle.load(f)
    
if use_existing_parameters == 1:
    with open(Exp_Folder+filename_save_prefix+'_save_ica_variables') as f:
        number_principle_components_ind, ica_components_ind, color_map_ind,num_ica_colors_ind,\
        number_principle_components_eachodor, ica_components_eachodor, color_map_eachodor,num_ica_colors_eachodor,\
        number_principle_components_allodor, ica_components_allodor, color_map_allodor, num_ica_colors_allodor, \
        colors_ica,time_baseline = pickle.load(f)


# Go into the main function that does ica for indiviudal trials
from ica_thunder_analysis import run_analysis_individualodors
from ica_thunder_analysis import run_analysis_eachodor
from ica_thunder_analysis import run_analysis_allodor

from thunder import ThunderContext

print 'Starting Thunder Now. Check console for details'
tsc = ThunderContext.start(appName="thunderica")

if files_to_do_ica[0]== 1:
    run_analysis_individualodors(Exp_Folder, filename_save_prefix, number_principle_components_ind, ica_components_ind, num_ica_colors_ind, color_map_ind,colors_ica[0:ica_components_ind],\
    stimulus_on_time, stimulus_off_time, tsc,redo_ica,time_baseline)
    
if files_to_do_ica[1]== 1:
    run_analysis_eachodor(Exp_Folder, filename_save_prefix, number_principle_components_eachodor, ica_components_eachodor, num_ica_colors_eachodor, color_map_eachodor,colors_ica[0:ica_components_ind],\
    stimulus_on_time, stimulus_off_time, tsc,redo_ica,time_baseline)

if files_to_do_ica[2]== 1:
    run_analysis_allodor(Exp_Folder, filename_save_prefix, number_principle_components_allodor, ica_components_allodor, num_ica_colors_allodor, color_map_allodor,colors_ica[0:ica_components_ind],\
    stimulus_on_time, stimulus_off_time, tsc,redo_ica,time_baseline)
    
############# Save all imput parameters
with open(Exp_Folder+filename_save_prefix+'_save_ica_variables', 'w') as f:
    pickle.dump([number_principle_components_ind, ica_components_ind, color_map_ind,num_ica_colors_ind,\
        number_principle_components_eachodor, ica_components_eachodor, color_map_ind,num_ica_colors_eachodor,\
        number_principle_components_allodor, ica_components_allodor, color_map_allodor, num_ica_colors_allodor, \
        colors_ica,time_baseline],f)
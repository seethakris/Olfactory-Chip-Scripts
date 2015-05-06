# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 17:07:18 2015
# Inputs for doing kmeans
@author: seetha
"""



## Enter Main Folder containing stimulus folders to create text files
Exp_Folder ='/Users/seetha/Desktop/KCTD/Fish14_KCTDHUC_5dpf/Tiff/Cropped/Registered/Thresholded_OB/Registered_Stimulus/'
filename_save_prefix = 'ThresholdedOB_T81'

#Which files to do kmeans on
files_to_do_kmeans = [1,0,1] #Individual kmeans, Each_odor kmeans, All_odor kmeans

#Use existing parameters from pickle dump -1  or use new paprameters -0?
use_existing_parameters = 0

#Redo kmeans - 1
redo_kmeans = 1

#kmeans parameters for individual trial kmeans
kmeans_clusters_ind = 12 #Number of kmeans clusters to detect from files


#kmeans parameters for each odor kmeans
kmeans_clusters_eachodor = 12 #Number of kmeans clusters  to detect from files


#kmeans parameters for all odor kmeans
kmeans_clusters_allodor = 12 #Number of kmeans clusters to detect from files


######################################################################
########################## Run Scripts ###############################

# Load imput parameters that were saved from creating text file. 
import pickle

with open(Exp_Folder+filename_save_prefix +'_save_input_variables') as f:
    img_size_x,img_size_y,img_size_crop_x1, img_size_crop_x2, img_size_crop_y1, img_size_crop_y2,\
    time_start,time_end,stim_start,stim_end,f_f_flag,dff_start,dff_end,stimulus_pulse = pickle.load(f)
    
#Stimulus on and off time
stimulus_pulse = 1 ##Whether a single pulse or a train of pulses were given
stim_start = 10 #Stimulus Starting time point
stim_end = 14 #Stimulus Ending time point

    
if use_existing_parameters == 1:
    with open(Exp_Folder+filename_save_prefix+'_save_kmeans_variables') as f:
        kmeans_clusters_ind, kmeans_clusters_eachodor, kmeans_clusters_allodor = pickle.load(f)


# Go into the main function that does kmeans for indiviudal trials
from kmeans_thunder_analysis import run_analysis_individualodors
from kmeans_thunder_analysis import run_analysis_eachodor
from kmeans_thunder_analysis import run_analysis_allodor

from thunder import ThunderContext

print 'Starting Thunder Now. Check console for details'
tsc = ThunderContext.start(appName="thunderkmeans")

if files_to_do_kmeans[0]== 1:
    run_analysis_individualodors(Exp_Folder, filename_save_prefix, kmeans_clusters_ind,\
    stim_start-time_start, stim_end-time_start, tsc,redo_kmeans,stimulus_pulse)
    
if files_to_do_kmeans[1]== 1:
    run_analysis_eachodor(Exp_Folder, filename_save_prefix, kmeans_clusters_eachodor, \
    stim_start-time_start, stim_end-time_start, tsc,redo_kmeans,stimulus_pulse)

if files_to_do_kmeans[2]== 1:
    run_analysis_allodor(Exp_Folder, filename_save_prefix, kmeans_clusters_allodor, \
    stim_start-time_start, stim_end-time_start, tsc,redo_kmeans,stimulus_pulse)
    
############# Save all imput parameters
with open(Exp_Folder+filename_save_prefix+'_save_kmeans_variables', 'w') as f:
    pickle.dump([kmeans_clusters_ind, kmeans_clusters_eachodor, kmeans_clusters_allodor], f)

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 17:07:18 2015
# Inputs for doing kmeans
@author: seetha
"""



## Enter Main Folder containing stimulus folders to create text files
Exp_Folder ='/Users/seetha/Desktop/HUC-KR15/Fish33_HUC_5dpf/Tiff/Cropped/Registered/Thresholded_OB/Registered_Stimulus/'
filename_save_prefix_forkmeanswithPCA = 'ThresholdedOB_23and4PCT129'
filename_save_prefix = 'ThresholdedOB_T129'

#Which files to do kmeans on
files_to_do_kmeans = [0,0,1] #Individual kmeans, Each_odor kmeans, All_odor kmeans

#Use existing parameters from pickle dump -1  or use new paprameters -0?
use_existing_parameters = 0

#Redo kmeans - 1
redo_kmeans = 0
redo_kmeans_colormap = 1

## Ignore any clusters that dont represent data. If 0, dont remove anything
ignore_clusters = [1,2,3]

#kmeans parameters for individual trial kmeans
kmeans_clusters_ind = 12 #Number of kmeans clusters to detect from files


#kmeans parameters for each odor kmeans
kmeans_clusters_eachodor = 12 #Number of kmeans clusters  to detect from files


#kmeans parameters for all odor kmeans
kmeans_clusters_allodor = 6 #Number of kmeans clusters to detect from files

time_baseline = 10 #Baseline over which ot normalizes

######################################################################
########################## Run Scripts ###############################

# Load imput parameters that were saved from creating text file. 
import pickle


#Stimulus on and off time
stimulus_pulse = 1
if stimulus_pulse == 1:
    stimulus_on_time = [10,28,47,65,83,101]
    stimulus_off_time = [14,32,51,69,87,105]
    color_mat = ['#00FFFF','#0000A0','#800080','#FF00FF', '#800000','#A52A2A']
    
if use_existing_parameters == 1:
    with open(Exp_Folder+filename_save_prefix+'_save_kmeans_variables') as f:
        kmeans_clusters_ind, kmeans_clusters_eachodor, kmeans_clusters_allodor, time_baseline,ignore_clusters = pickle.load(f)


# Go into the main function that does kmeans for indiviudal trials
from kmeans_thunder_analysis import run_analysis_individualodors
from kmeans_thunder_analysis import run_analysis_eachodor
from kmeans_thunder_analysis import run_analysis_allodor

from thunder import ThunderContext

print 'Starting Thunder Now. Check console for details'
tsc = ThunderContext.start(appName="thunderkmeans")

if files_to_do_kmeans[0]== 1:
    run_analysis_individualodors(Exp_Folder, filename_save_prefix, filename_save_prefix_forkmeanswithPCA, kmeans_clusters_ind,\
    stimulus_on_time, stimulus_off_time, tsc,redo_kmeans,time_baseline,redo_kmeans_colormap,ignore_clusters)
    
if files_to_do_kmeans[1]== 1:
    run_analysis_eachodor(Exp_Folder, filename_save_prefix, filename_save_prefix_forkmeanswithPCA, kmeans_clusters_eachodor, \
    stimulus_on_time, stimulus_off_time, tsc,redo_kmeans,time_baseline,redo_kmeans_colormap,ignore_clusters)

if files_to_do_kmeans[2]== 1:
    run_analysis_allodor(Exp_Folder, filename_save_prefix, filename_save_prefix_forkmeanswithPCA, kmeans_clusters_allodor, \
    stimulus_on_time, stimulus_off_time, tsc,redo_kmeans, time_baseline,redo_kmeans_colormap,ignore_clusters)
    
############# Save all imput parameters
with open(Exp_Folder+filename_save_prefix+'_save_kmeans_variables', 'w') as f:
    pickle.dump([kmeans_clusters_ind, kmeans_clusters_eachodor, kmeans_clusters_allodor, time_baseline, ignore_clusters], f)

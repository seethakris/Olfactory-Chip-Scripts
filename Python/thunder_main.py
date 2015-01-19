# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 17:16:26 2015
@author: seetha

"""

######################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~ Importing Libraries ~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#Import some python libraries
import os
filesep = os.path.sep
import time
import scipy
#Import thunder libraries
from thunder import ThunderContext
#Import user defined libraries
from create_textfile_for_thunder_individual import create_textfile_individual
#from create_textfile_for_thunder_stacks import create_textfile_stacks
#from thunder_analysis import run_pca
#from thunder_analysis import make_pca_maps
#from thunder_plots import plot_pca_maps
#from thunder_plots_stacks import plot_pca_maps_for_stacks
######################################################################


def  initial_function(Exp_Folder, filename_save_prefix, img_size_x, img_size_y, img_size_crop_x, img_size_crop_y, num_time, \
time_start, time_end, stim_start, stim_end, f_f_flag, dff_start, dff_end, \
pca_components, num_pca_colors, num_samples, thresh_pca, color_map):
    
    ##Create different types of text files and run analysis on them
    #1.Use each odor seperately
    #2.Use different odors as stacks
    
    ############### STEP 1 ######################
    #Create text file for each odor seperately
    #Check appropriate folders if combine = 0 or 1
    #Find Stimulus folder
    
    Stimulus_Folders = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f)) and f.find('Figures')<0]
        
    #Check if text file already exists in each stimulus folder, else create it
    for ii in range(0, len(Stimulus_Folders)):
        txt_file = [f for f in os.listdir(os.path.join(Exp_Folder, Stimulus_Folders[ii])) \
        if (f.find(filename_save_prefix+'.txt')==0)]        
        if len(txt_file)==0:
            start_time = time.time()
            
            print 'Saving images individually to text on '+Stimulus_Folders[ii]
            Working_Directory = os.path.join(Exp_Folder, Stimulus_Folders[ii])
            
            Matfile_for_thunder = create_textfile_individual(Working_Directory, filename_save_prefix, img_size_x, img_size_y,\
            img_size_crop_x, img_size_crop_y,num_time, time_start, time_end,\
            stim_start, stim_end, f_f_flag, dff_start, dff_end) #Create text file
            
            print 'Saving to text file took '+ str(int(time.time()-start_time)) +' seconds'

    
    
    
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 17:00:39 2015
Main function to load data and start thunder analysis
@author: chad
"""
import os
filesep = os.path.sep

import time
import numpy as np

from thunder_pca import run_pca
from thunder_pca import make_pca_maps

from thunder import ThunderContext

print 'Starting Thunder Now. Check console for details'
tsc = ThunderContext.start(appName="thunderpca")

def run_analysis_initial_function(Exp_Folder, filename_save_prefix, pca_components, num_pca_colors, num_samples, thresh_pca, color_map):
    
    # Different Working directories to load different datas
    
    # 1. Main Directory for all odors and all trials
    
    if flag_directory == 1 or flag_directory == 0:
        Working_Directory = Exp_Folder
        
        name_for_saving_files = 'All_odors_'+ filename_save_prefix+'_eachodor.txt'
        txt_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files)==0)]            
        
        if len(txt_file)>0:
            #Load data        
            data = tsc.loadSeries(Working_Directory+name_for_saving_files, inputformat='text', nkeys=3)
            data.center()
            data = data.cache()
            run_pca_thunder(Working_Directory, data, pca_components, num_pca_colors, num_samples, thresh_pca, color_map)
        
    
    #2. For each odor
    if flag_directory == 2 or flag_directory == 0:
        Stimulus_Directories = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f)) and f.find('Figures')<0]
            
        for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):
            Working_Directory = os.path.join(Exp_Folder, Stimulus_Directories[ii])+filesep     
            name_for_saving_files = Stimulus_Directories[ii] + '_'+ filename_save_prefix+'_eachodor.txt'
            txt_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files)==0)]            
            
            if len(txt_file)>0:
                #Load data        
                data = tsc.loadSeries(Working_Directory+name_for_saving_files, inputformat='text', nkeys=3)
                data.center()
                data = data.cache()
                run_pca_thunder(Working_Directory, data, pca_components, num_pca_colors, num_samples, thresh_pca, color_map)
            
    #3. For each trial
    if flag_directory == 3 or flag_directory == 0:
    
                    
def run_pca_thunder(Working_Directory, data, pca_components, num_pca_colors, num_samples, thresh_pca, color_map):
    
    #Run PCA
    start_time = time.time()
    text_file = open(Working_Directory + "pcalog.txt", "w")
    text_file.write("Running pca in %s \n" % Working_Directory)
    print 'Running pca for all files...in '+ Working_Directory
    pca, imgs_pca = run_pca(data,pca_components)
    print 'Running PCA took '+ str(int(time.time()-start_time)) +' seconds' 
    text_file.write("Running pca took took %s seconds \n" %  str(int(time.time()-start_time)))
    
    
    #Create PCA maps
    start_time = time.time()
    text_file.write("Making pca color maps in %s \n" % Working_Directory)
    print 'Making pca color maps for all files...in '+ Working_Directory
    img_size_x = np.size(imgs_pca,1)
    img_size_y = np.size(imgs_pca,2)
    maps, pts, clrs, recon, unique_clrs, matched_pixels, matched_signals, mean_signal, sem_signal = make_pca_maps(pca, imgs_pca, img_size_x,\
    img_size_y, num_pca_colors, num_samples, thresh_pca, color_map)
    print 'Making pca color maps '+ str(int(time.time()-start_time)) +' seconds' 
    text_file.write("Making pca color maps took took %s seconds \n" %  str(int(time.time()-start_time)))
    
    # Plot PCA
    
    
    
    

        
        


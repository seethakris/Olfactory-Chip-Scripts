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
import matplotlib.pyplot as plt 
import pickle

from thunder_ica import run_ica
from thunder_ica import make_ica_maps
from thunder_ica_plots import plot_ica_maps


## ica on individual odors
def run_analysis_individualodors(Exp_Folder, filename_save_prefix, number_principle_components, ica_components, num_ica_colors, color_map, colors_ica, stim_start, stim_end, tsc,redo_ica,stimulus_pulse):


    Stimulus_Directories = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f)) and f.find('Figures')<0]
    
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):
        Trial_Directories = [f for f in os.listdir(os.path.join(Exp_Folder, Stimulus_Directories[ii]))\
        if os.path.isdir(os.path.join(Exp_Folder, Stimulus_Directories[ii], f)) and f.find('Figures')<0] #Get only directories
        
        for jj in xrange(0, np.size(Trial_Directories, axis = 0)):
            Working_Directory = os.path.join(Exp_Folder, Stimulus_Directories[ii], Trial_Directories[jj], 'C=1')+filesep        
                    
            name_for_saving_figures = Stimulus_Directories[ii] + ' ' + Trial_Directories[jj]        

            ## Check if textfile exists to do ica            
            name_for_saving_files = Stimulus_Directories[ii] + '_' + Trial_Directories[jj] + filename_save_prefix+'_individualtrial'
            txt_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files+'.txt')==0)]    
            
            if len(txt_file)>0:
                                
                #Load data        
                data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputformat='text', nkeys=3)
                data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputformat='text', nkeys=3)
                             
                data_filtered.center()
                data_filtered.zscore()
                data_filtered.cache()
                
                flag = 0
                run_ica_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files, redo_ica, data_filtered,\
                data_background, number_principle_components, ica_components, num_ica_colors, color_map, colors_ica, stim_start, stim_end,  flag,stimulus_pulse)
                
    
def run_analysis_eachodor(Exp_Folder, filename_save_prefix, number_principle_components, ica_components, num_ica_colors, color_map,\
colors_ica, stim_start, stim_end,tsc,redo_ica,stimulus_pulse):
    
    Stimulus_Directories = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f)) and f.find('Figures')<0]            
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):
        Working_Directory = os.path.join(Exp_Folder, Stimulus_Directories[ii])+filesep     
        
        name_for_saving_files = Stimulus_Directories[ii] + '_'+ filename_save_prefix+'_eachodor'
        txt_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files)==0)]                    
        name_for_saving_figures = Stimulus_Directories[ii]       

        if len(txt_file)>0:
           #Load data                    
            data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputformat='text', nkeys=3)
            data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputformat='text', nkeys=3)
                        
            data_filtered.center()
            data_filtered.zscore()
            data_filtered.cache()
                
            flag = 1
            run_ica_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files,redo_ica, data_filtered,\
            data_background, number_principle_components, ica_components, num_ica_colors, color_map, colors_ica, stim_start, stim_end, flag,stimulus_pulse)
            
    
def run_analysis_allodor(Exp_Folder, filename_save_prefix, number_principle_components, ica_components, num_ica_colors, color_map,\
colors_ica, stim_start, stim_end, tsc,redo_ica,stimulus_pulse):
    
    Working_Directory = Exp_Folder
        
    name_for_saving_files = 'All_odors_'+ filename_save_prefix+'_eachodor'
    txt_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files)==0)]            
    
    if len(txt_file)>0:
       #Load data                    
        data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputformat='text', nkeys=3)
        data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputformat='text', nkeys=3)
                
        data_filtered.center()
        data_filtered.zscore()
        data_filtered.cache()
            
        name_for_saving_figures = Working_Directory
        flag = 2
        run_ica_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files, redo_ica,data_filtered,\
        data_background, number_principle_components, ica_components, num_ica_colors, color_map, colors_ica, stim_start, stim_end, flag,stimulus_pulse)

    
def run_ica_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files, redo_ica, data,data_background,\
number_principle_components, ica_components, num_ica_colors, color_map, colors_ica, stim_start, stim_end, flag,stimulus_pulse):
    
    
    ### If ica result files exists, then dont run any more ica, just do plotting, 
    ## Else run ica and save all outputs
    pickle_dump_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files+'_ica_results')==0)]    
        
    if len(pickle_dump_file)==0 or redo_ica==1:
        #Run ica
        start_time = time.time()
        text_file = open(Working_Directory + "log.txt", "a")
        text_file.write("Running ica in %s \n" % Working_Directory)
        print 'Running ica for all files...in '+ Working_Directory
        ica, imgs_ica = run_ica(data,number_principle_components, ica_components)
        print 'Running ica took '+ str(int(time.time()-start_time)) +' seconds' 
        text_file.write("Running ica took %s seconds \n" %  str(int(time.time()-start_time)))
        
        
        #Create ica maps
        start_time = time.time()
        text_file.write("Making ica color maps in %s \n" % Working_Directory)
        print 'Making ica color maps for all files...in '+ Working_Directory
        img_size_x = np.size(imgs_ica,1)
        img_size_y = np.size(imgs_ica,2)
        maps, matched_pixels = make_ica_maps(data_background, imgs_ica, img_size_x,\
        img_size_y, num_ica_colors, color_map, colors_ica)
        print 'Making ica color maps '+ str(int(time.time()-start_time)) +' seconds' 
        text_file.write("Making ica color maps took %s seconds \n" %  str(int(time.time()-start_time)))
       
        print 'Matched_Pixels........' + str(np.shape(matched_pixels))
        ica_components_plot = ica.a
        ## save input parameters
        ############# Save all imput parameters
        with open(Working_Directory+name_for_saving_files+'_ica_results', 'w') as f:
            pickle.dump([ica_components_plot, imgs_ica, maps, colors_ica, matched_pixels],f)
    
    else:        
        
        print 'Using existing pickled parameters....'
        text_file = open(Working_Directory + "log.txt", "a")
        text_file.write("Plotting Using existing pickled parameters....\n")
        with open(Working_Directory+name_for_saving_files+'_ica_results') as f:
            ica_components_plot, imgs_ica, maps, colors_ica, matched_pixels = pickle.load(f)
    
    
    start_time = time.time()
    text_file.write("Plotting ica in %s \n" % Working_Directory)
    print 'Plotting ica in for all files...in '+ Working_Directory
    plot_ica_maps(Working_Directory, name_for_saving_figures, name_for_saving_files, \
    ica_components_plot, maps, colors_ica, matched_pixels, stim_start, stim_end, flag,stimulus_pulse)
    print 'Plotting ica in '+ str(int(time.time()-start_time)) +' seconds' 
    text_file.write("Plotting ica in took %s seconds \n" %  str(int(time.time()-start_time)))
    
    
        


# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 17:00:39 2015
Main function to load data and start thunder analysis
@author: chad
"""
import os
filesep = os.path.sep
from copy import copy
import time
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import pickle

from thunder_NMF import run_NMF
from thunder_NMF import make_NMF_maps
from thunder_NMF_plots import plot_NMF_maps

from thunder import Colorize
image = Colorize.image

## NMF on individual exps
def run_analysis_individualodors(Exp_Folder, filename_save_prefix, NMF_components, num_NMF_colors, \
color_map, tsc,redo_NMF, stimulus_on_time, stimulus_off_time,time_baseline,colors_NMF,max_iterations, tolerence_level,remake_colormap):


    Stimulus_Directories = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f)) and f.find('Figures')<0]
    
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):
        Trial_Directories = [f for f in os.listdir(os.path.join(Exp_Folder, Stimulus_Directories[ii]))\
        if os.path.isdir(os.path.join(Exp_Folder, Stimulus_Directories[ii], f)) and f.find('Figures')<0] #Get only directories
        
        for jj in xrange(0, np.size(Trial_Directories, axis = 0)):
            Working_Directory = os.path.join(Exp_Folder, Stimulus_Directories[ii], Trial_Directories[jj],'C=1')+filesep        
                    
            name_for_saving_figures = Stimulus_Directories[ii] + ' ' + Trial_Directories[jj]        

            ## Check if textfile exists to do NMF            
            name_for_saving_files = Stimulus_Directories[ii] + '_' + Trial_Directories[jj] + filename_save_prefix+'_individualtrial'
            txt_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files+'.txt')==0)]    
            
            if len(txt_file)>0:
                #Load data        
                data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputFormat='text', nkeys=3).toTimeSeries().detrend(method='linear', order=10)
                data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputFormat='text', nkeys=3)
                                
                data_filtered.center()
                data_filtered.zscore(time_baseline)
                data_filtered.cache()
                
                flag = 0
                name_for_saving_files = Stimulus_Directories[ii] + '_' + Trial_Directories[jj] + filename_save_prefix+'_individualtrial'
                run_NMF_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files, redo_NMF, data_filtered,\
                data_background,NMF_components, num_NMF_colors, color_map,  flag, stimulus_on_time, stimulus_off_time, colors_NMF,\
                max_iterations, tolerence_level,remake_colormap)
                
    
def run_analysis_eachodor(Exp_Folder, filename_save_prefix, NMF_components, num_NMF_colors, color_map,\
tsc,redo_NMF, stimulus_on_time, stimulus_off_time, time_baseline,colors_NMF,max_iterations, tolerence_level,remake_colormap):
    
    Stimulus_Directories = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f)) and f.find('Figures')<0]            
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):
        Working_Directory = os.path.join(Exp_Folder, Stimulus_Directories[ii])+filesep     
        
        name_for_saving_files = Stimulus_Directories[ii] + '_'+ filename_save_prefix+'_eachodor'
        txt_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files)==0)]                    
        name_for_saving_figures = Stimulus_Directories[ii]       

        if len(txt_file)>0:
           #Load data                    
            data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputFormat='text', nkeys=3).toTimeSeries().detrend(method='linear', order=5)
            data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputFormat='text', nkeys=3)
            
            
            data_filtered.center()
            data_filtered.zscore(time_baseline)
            data_filtered.cache()
                
            flag = 1
            name_for_saving_files = Stimulus_Directories[ii] + '_'+ filename_save_prefix+'_eachodor'
            run_NMF_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files, redo_NMF, data_filtered,\
            data_background, NMF_components, num_NMF_colors, color_map, flag,\
            stimulus_on_time, stimulus_off_time,colors_NMF,max_iterations, tolerence_level,remake_colormap)
            
    
def run_analysis_allodor(Exp_Folder, filename_save_prefix, NMF_components, num_NMF_colors, color_map,\
 tsc,redo_NMF, stimulus_on_time, stimulus_off_time, time_baseline, colors_NMF,max_iterations, tolerence_level,remake_colormap):
    
    Working_Directory = Exp_Folder
        
    name_for_saving_files = 'All_odors_'+ filename_save_prefix+'_eachodor'
    txt_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files)==0)]            
    
    if len(txt_file)>0:
       #Load data                    
        data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputFormat='text', nkeys=3).toTimeSeries().detrend(method='linear', order=5)
        data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputFormat='text', nkeys=3)
                
        data_filtered.center()
#        data_filtered.zscore(time_baseline)
        data_filtered.cache()
            
        name_for_saving_figures = Working_Directory
        flag = 2
        name_for_saving_files = 'All_odors_'+ filename_save_prefix +'_eachodor'
        run_NMF_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files, redo_NMF, data_filtered,\
        data_background, NMF_components, num_NMF_colors, color_map, flag,\
        stimulus_on_time, stimulus_off_time,colors_NMF,max_iterations, tolerence_level,remake_colormap)

    
def run_NMF_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files, redo_NMF, data,data_background,\
NMF_components, num_NMF_colors, color_map,  flag, stimulus_on_time, stimulus_off_time,colors_NMF,max_iterations, tolerence_level,remake_colormap):
    
    
    ### If NMF result files exists, then dont run any more NMF, just do plotting, 
    ## Else run NMF and save all outputs
    pickle_dump_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files+'_NMF_results')==0)]    
    
    if len(pickle_dump_file)==0 or redo_NMF==1:
        #Run NMF
        start_time = time.time()
        text_file = open(Working_Directory + "log.txt", "a")
        text_file.write("Running NMF in %s \n" % Working_Directory)
        print 'Running NMF for all files...in '+ Working_Directory
        NMF, imgs_NMF = run_NMF(data,NMF_components,max_iterations, tolerence_level, Working_Directory)
        print 'Running NMF took '+ str(int(time.time()-start_time)) +' seconds' 
        text_file.write("Running NMF took %s seconds \n" %  str(int(time.time()-start_time)))
        
        
        #Create NMF maps
        start_time = time.time()
        text_file.write("Making NMF color maps in %s \n" % Working_Directory)
        print 'Making NMF color maps for all files...in '+ Working_Directory
        img_size_x = np.size(imgs_NMF,1)
        img_size_y = np.size(imgs_NMF,2)
        
        maps, matched_pixels, unique_clrs = make_NMF_maps(data_background,imgs_NMF, img_size_x,\
        img_size_y, num_NMF_colors, color_map, colors_NMF)

        print 'Making NMF color maps '+ str(int(time.time()-start_time)) +' seconds' 
        text_file.write("Making NMF color maps took %s seconds \n" %  str(int(time.time()-start_time)))
       
        print 'Matched_Pixels........' + str(np.shape(matched_pixels))
        NMF_components = NMF.h.T
        
        ## save input parameters
        ############# Save all imput parameters
        with open(Working_Directory+name_for_saving_files+'_NMF_results', 'wb') as f:
            pickle.dump([NMF_components, imgs_NMF, maps, matched_pixels,unique_clrs],f)
    
    else:        
        print 'Using existing pickled parameters....'
        text_file = open(Working_Directory + "log.txt", "a")
        text_file.write("Plotting Using existing pickled parameters....\n")
        with open(Working_Directory+name_for_saving_files+'_NMF_results','rb') as f:
            NMF_components, imgs_NMF,  maps, matched_pixels, unique_clrs = pickle.load(f)
        
        img_size_x = np.size(imgs_NMF,1)
        img_size_y = np.size(imgs_NMF,2)
        
        #Run colorization again
        if remake_colormap == 1:
            start_time = time.time()
            print 'Re-Making NMF color maps for all files...in '+ Working_Directory
            maps, matched_pixels, unique_clrs = make_NMF_maps(data_background,imgs_NMF, img_size_x,\
            img_size_y, num_NMF_colors, color_map, colors_NMF)
            print 'Re-Making NMF color maps '+ str(int(time.time()-start_time)) +' seconds' 
            with open(Working_Directory+name_for_saving_files+'_NMF_results', 'wb') as f:
                pickle.dump([NMF_components, imgs_NMF, maps, matched_pixels,unique_clrs],f)
# Plot NMF
    start_time = time.time()
    text_file.write("Plotting NMF in %s \n" % Working_Directory)
    print 'Plotting NMF in for all files...in '+ Working_Directory
   
    plot_NMF_maps(Working_Directory, name_for_saving_figures, name_for_saving_files, \
    NMF_components, maps, colors_NMF, matched_pixels, stimulus_on_time, stimulus_off_time, flag, unique_clrs)
    
    print 'Plotting NMF in '+ str(int(time.time()-start_time)) +' seconds' 
    text_file.write("Plotting NMF in took %s seconds \n" %  str(int(time.time()-start_time)))
    

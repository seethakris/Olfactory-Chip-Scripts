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
import pickle

from thunder_kmeans import run_kmeans
from thunder_kmeans import make_kmeans_maps
from thunder_kmeans_plots import plot_kmeans_maps


## kmeans on individual odors
def run_analysis_individualodors(Exp_Folder, filename_save_prefix, filename_save_prefix_forkmeanswithPCA, kmeans_clusters, \
    stimulus_on_time, stimulus_off_time, tsc, redo_kmeans,time_baseline,redo_kmeans_colormap,ignore_clusters):


    Stimulus_Directories = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f)) and f.find('Figures')<0 and f.find('DataFrames')<0]
    
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):
        Trial_Directories = [f for f in os.listdir(os.path.join(Exp_Folder, Stimulus_Directories[ii]))\
        if os.path.isdir(os.path.join(Exp_Folder, Stimulus_Directories[ii], f)) and f.find('Figures')<0 and f.find('DataFrames')<0] #Get only directories
        
        for jj in xrange(0, np.size(Trial_Directories, axis = 0)):
            Working_Directory = os.path.join(Exp_Folder, Stimulus_Directories[ii], Trial_Directories[jj], 'C=1')+filesep        

            name_for_saving_figures = Stimulus_Directories[ii] + ' ' + Trial_Directories[jj]        

            ## Check if textfile exists to do kmeans            
            name_for_saving_files = Stimulus_Directories[ii] + '_' + Trial_Directories[jj] + filename_save_prefix+'_individualtrial'
            txt_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files+'.txt')==0)]    
            
            if len(txt_file)>0:                                
                #Load data        
                if filename_save_prefix_forkmeanswithPCA == filename_save_prefix:
                    data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputFormat='text', nkeys=3).toTimeSeries().detrend(method='linear', order=8)
                    data_filtered.center()
                    data_filtered.zscore(time_baseline)
                else:
                    name_for_saving_files_kmeans = Stimulus_Directories[ii] + '_' + Trial_Directories[jj] + filename_save_prefix_forkmeanswithPCA+'_individualtrial'
                    data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files_kmeans+'_pca_recon.txt', inputFormat='text', nkeys=3)

                data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputFormat='text', nkeys=3)
                data_background.cache()
                data_filtered.cache()
                
                flag = 0
                run_kmeans_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files_kmeans, redo_kmeans, data_filtered,\
                data_background,kmeans_clusters, stimulus_on_time, stimulus_off_time,flag,redo_kmeans_colormap,ignore_clusters)
                
    
def run_analysis_eachodor(Exp_Folder, filename_save_prefix,filename_save_prefix_forkmeanswithPCA, kmeans_clusters, \
    stimulus_on_time, stimulus_off_time, tsc, redo_kmeans,time_baseline,redo_kmeans_colormap,ignore_clusters):
    
    Stimulus_Directories = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f)) and f.find('Figures')<0 and f.find('DataFrames')<0]            
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):
        Working_Directory = os.path.join(Exp_Folder, Stimulus_Directories[ii])+filesep     
        name_for_saving_files = Stimulus_Directories[ii] + '_'+ filename_save_prefix+'_eachodor'
        txt_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files)==0)]                    
        name_for_saving_figures = Stimulus_Directories[ii]       

        if len(txt_file)>0:
            #Load data        
            if filename_save_prefix_forkmeanswithPCA == filename_save_prefix:
                data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputFormat='text', nkeys=3).toTimeSeries().detrend(method='linear', order=8)
                data_filtered.center()
                data_filtered.zscore(time_baseline)
            else:
                name_for_saving_files_kmeans = Stimulus_Directories[ii] + '_'+ filename_save_prefix_forkmeanswithPCA+'_eachodor'
                data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files_kmeans+'_pca_recon.txt', inputFormat='text', nkeys=3).toTimeSeries().detrend(method='linear', order=8)
            
            data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputFormat='text', nkeys=3)
            data_background.cache()
            
            data_filtered.cache()
                
            flag = 1
            run_kmeans_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files_kmeans, redo_kmeans, data_filtered,\
            data_background, kmeans_clusters,stimulus_on_time, stimulus_off_time, flag,redo_kmeans_colormap,ignore_clusters)
            
    
def run_analysis_allodor(Exp_Folder, filename_save_prefix, filename_save_prefix_forkmeanswithPCA, kmeans_clusters, \
    stimulus_on_time, stimulus_off_time, tsc, redo_kmeans,time_baseline,redo_kmeans_colormap,ignore_clusters):
    
    Working_Directory = Exp_Folder

    name_for_saving_files = 'All_odors_'+ filename_save_prefix+'_eachodor'
    txt_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files)==0)]            
    
    if len(txt_file)>0:
       #Load data                    
        if filename_save_prefix_forkmeanswithPCA == filename_save_prefix:
            data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputFormat='text', nkeys=3).toTimeSeries().detrend(method='linear', order=8)
            data_filtered.center()
            data_filtered.zscore(time_baseline)
        else:
            name_for_saving_files_kmeans = 'All_odors_'+ filename_save_prefix_forkmeanswithPCA+'_eachodor'                    
            data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files_kmeans+'_pca_recon.txt', inputFormat='text', nkeys=3)
        
        data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputFormat='text', nkeys=3)
        data_background.cache()
        data_filtered.cache()


            
        name_for_saving_figures = Working_Directory
        flag = 2
        run_kmeans_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files_kmeans, redo_kmeans, data_filtered,\
        data_background, kmeans_clusters, stimulus_on_time, stimulus_off_time, flag,redo_kmeans_colormap,ignore_clusters)

    
def run_kmeans_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files, redo_kmeans, data,data_background,\
kmeans_clusters, stimulus_on_time, stimulus_off_time, flag,redo_kmeans_colormap,ignore_clusters):
    
    
    ### If kmeans result files exists, then dont run any more kmeans, just do plotting, 
    ## Else run kmeans and save all outputs
    pickle_dump_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files+'_kmeans_results')==0)]    
    
    if len(pickle_dump_file)==0 or redo_kmeans==1:
        #Run kmeans
        start_time = time.time()
        text_file = open(Working_Directory + "log.txt", "a")
        text_file.write("Running kmeans in %s \n" % Working_Directory)
        print 'Running kmeans for all files...in '+ Working_Directory
        kmeans_model, img_sim, img_labels = run_kmeans(data, kmeans_clusters)
        print 'Running kmeans took '+ str(int(time.time()-start_time)) +' seconds' 
        text_file.write("Running kmeans took %s seconds \n" %  str(int(time.time()-start_time)))
          
        #Create kmeans maps
        start_time = time.time()
        text_file.write("Making kmeans color maps in %s \n" % Working_Directory)
        print 'Making kmeans color maps for all files...in '+ Working_Directory
        
        img_size_x = np.size(img_sim,1)
        img_size_y = np.size(img_sim,2)
        brainmap, unique_clrs, newclrs_rgb, newclrs_brewer, matched_pixels, kmeans_clusters_updated = make_kmeans_maps(data_background, kmeans_model.centers.T, img_labels, img_sim, img_size_x, img_size_y,ignore_clusters)
        
        print 'Making kmeans color maps '+ str(int(time.time()-start_time)) +' seconds' 
        text_file.write("Making kmeans color maps took %s seconds \n" %  str(int(time.time()-start_time)))
       
        kmeans_clusters = kmeans_model.centers.T
        ## save input parameters
        ############# Save all imput parameters
        with open(Working_Directory+name_for_saving_files+'_kmeans_results', 'wb') as f:
            pickle.dump([kmeans_clusters,kmeans_clusters_updated, img_sim, img_labels, brainmap, unique_clrs, newclrs_rgb, newclrs_brewer, matched_pixels],f)
    
    else:        
        print 'Using existing pickled parameters....'
        text_file = open(Working_Directory + "log.txt", "a")
        text_file.write("Plotting Using existing pickled parameters....\n")
        with open(Working_Directory+name_for_saving_files+'_kmeans_results','rb') as f:
            kmeans_clusters,kmeans_clusters_updated, img_sim, img_labels, brainmap, unique_clrs, newclrs_rgb, newclrs_brewer, matched_pixels = pickle.load(f)
        
        if redo_kmeans_colormap == 1:
            start_time = time.time()
            img_size_x = np.size(img_sim,1)
            img_size_y = np.size(img_sim,2)            
            
            print 'Re-Making kmeans color maps for all files...in '+ Working_Directory
            brainmap, unique_clrs, newclrs_rgb, newclrs_brewer, matched_pixels, kmeans_clusters_updated = make_kmeans_maps(data_background,kmeans_clusters, img_labels, img_sim, img_size_x, img_size_y,ignore_clusters)
                        
            print 'Re-Making kmeans color maps '+ str(int(time.time()-start_time)) +' seconds' 
            #Resave            
            with open(Working_Directory+name_for_saving_files+'_kmeans_results', 'wb') as f:
                pickle.dump([kmeans_clusters,kmeans_clusters_updated, img_sim, img_labels, brainmap, unique_clrs, newclrs_rgb, newclrs_brewer, matched_pixels],f)
    
    
    # Plot kmeans
    start_time = time.time()
    text_file.write("Plotting kmeans in %s \n" % Working_Directory)
    print 'Plotting kmeans in for all files...in '+ Working_Directory
    plot_kmeans_maps(Working_Directory, name_for_saving_figures, name_for_saving_files, \
    kmeans_clusters_updated, img_sim, img_labels, brainmap, unique_clrs, newclrs_rgb, newclrs_brewer, matched_pixels, stimulus_on_time, stimulus_off_time, flag)
    print 'Plotting kmeans in '+ str(int(time.time()-start_time)) +' seconds' 
    text_file.write("Plotting kmeans in took %s seconds \n" %  str(int(time.time()-start_time)))
    

        


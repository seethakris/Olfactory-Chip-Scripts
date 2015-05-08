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
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import pickle

from thunder_pca import run_pca
from thunder_pca import make_pca_maps
from thunder_pca_plots import plot_pca_maps
from thunder_pca import create_data_in_pca_space

## PCA on individual odors
def run_analysis_individualodors(Exp_Folder, filename_save_prefix_forPCA, filename_save_prefix_for_textfile, pca_components, num_pca_colors, num_samples, thresh_pca,\
color_map, tsc,redo_pca,stimulus_on_time, stimulus_off_time, color_mat,required_pcs, time_baseline):


    Stimulus_Directories = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f)) and f.find('Figures')<0]
    
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):
        Trial_Directories = [f for f in os.listdir(os.path.join(Exp_Folder, Stimulus_Directories[ii]))\
        if os.path.isdir(os.path.join(Exp_Folder, Stimulus_Directories[ii], f)) and f.find('Figures')<0] #Get only directories
        
        for jj in xrange(0, np.size(Trial_Directories, axis = 0)):
            Working_Directory = os.path.join(Exp_Folder, Stimulus_Directories[ii], Trial_Directories[jj], 'C=1')+filesep        
                    
            name_for_saving_figures = Stimulus_Directories[ii] + ' ' + Trial_Directories[jj]        

            ## Check if textfile exists to do PCA            
            name_for_saving_files = Stimulus_Directories[ii] + '_' + Trial_Directories[jj] + filename_save_prefix_for_textfile+'_individualtrial'
            txt_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files+'.txt')==0)]    
            
            if len(txt_file)>0:
                #Load data        
                data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputFormat='text', nkeys=3).toTimeSeries().detrend(method='linear', order=5)
                data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputFormat='text', nkeys=3)
                
#                data_plotting = data_background
#                plot_preprocess_data(Working_Directory, name_for_saving_files, data_plotting, stimulus_on_time, stimulus_off_time)
                
                data_filtered.center()
                data_filtered.zscore(time_baseline)
                data_filtered.cache()
                
                flag = 0
                name_for_saving_files = Stimulus_Directories[ii] + '_' + Trial_Directories[jj] + filename_save_prefix_forPCA+'_individualtrial'
                run_pca_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files, redo_pca, data_filtered,\
                data_background,pca_components, num_pca_colors, num_samples, thresh_pca, color_map,  flag, stimulus_on_time, stimulus_off_time, color_mat,required_pcs)
                
    
def run_analysis_eachodor(Exp_Folder, filename_save_prefix_forPCA, filename_save_prefix_for_textfile, pca_components, num_pca_colors, num_samples, thresh_pca, color_map,\
tsc,redo_pca, stimulus_on_time, stimulus_off_time, color_mat,required_pcs, time_baseline):
    
    Stimulus_Directories = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f)) and f.find('Figures')<0]            
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):
        Working_Directory = os.path.join(Exp_Folder, Stimulus_Directories[ii])+filesep     
        
        name_for_saving_files = Stimulus_Directories[ii] + '_'+ filename_save_prefix_for_textfile+'_eachodor'
        txt_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files)==0)]                    
        name_for_saving_figures = Stimulus_Directories[ii]       

        if len(txt_file)>0:
           #Load data                    
            data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputFormat='text', nkeys=3).toTimeSeries().detrend(method='linear', order=5)
            data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputFormat='text', nkeys=3)
            
#            data_plotting = data_background
#            plot_preprocess_data(Working_Directory, name_for_saving_files, data_plotting, stimulus_on_time, stimulus_off_time)
            
            data_filtered.center()
            data_filtered.zscore(time_baseline)
            data_filtered.cache()
                
            flag = 1
            name_for_saving_files = Stimulus_Directories[ii] + '_'+ filename_save_prefix_forPCA+'_eachodor'
            run_pca_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files, redo_pca, data_filtered,\
            data_background, pca_components, num_pca_colors, num_samples, thresh_pca, color_map, flag, stimulus_on_time, stimulus_off_time, color_mat,required_pcs)
            
    
def run_analysis_allodor(Exp_Folder, filename_save_prefix_forPCA, filename_save_prefix_for_textfile, pca_components, num_pca_colors, num_samples, thresh_pca, color_map,\
 tsc,redo_pca, stimulus_on_time, stimulus_off_time, color_mat, required_pcs, time_baseline):
    
    Working_Directory = Exp_Folder
        
    name_for_saving_files = 'All_odors_'+ filename_save_prefix_for_textfile+'_eachodor'
    txt_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files)==0)]            
    
    if len(txt_file)>0:
       #Load data                    
        data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputFormat='text', nkeys=3).toTimeSeries().detrend(method='linear', order=5)
        data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputFormat='text', nkeys=3)
        
#        data_plotting = data_background
#        plot_preprocess_data(Working_Directory, name_for_saving_files, data_plotting, stimulus_on_time, stimulus_off_time)
        
        data_filtered.center()
        data_filtered.zscore(time_baseline)
        data_filtered.cache()
            
        name_for_saving_figures = Working_Directory
        flag = 2
        name_for_saving_files = 'All_odors_'+ filename_save_prefix_forPCA +'_eachodor'
        run_pca_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files, redo_pca, data_filtered,\
        data_background, pca_components, num_pca_colors, num_samples, thresh_pca, color_map, flag,stimulus_on_time, stimulus_off_time, color_mat, required_pcs)

    
def run_pca_thunder(Working_Directory, name_for_saving_figures, name_for_saving_files, redo_pca, data,data_background,\
pca_components, num_pca_colors, num_samples, thresh_pca, color_map,  flag, stimulus_on_time, stimulus_off_time, color_mat, required_pcs):
    
    
    ### If pca result files exists, then dont run any more pca, just do plotting, 
    ## Else run pca and save all outputs
    pickle_dump_file = [f for f in os.listdir(Working_Directory) if (f.find(name_for_saving_files+'_pca_results')==0)]    
    
    if len(pickle_dump_file)==0 or redo_pca==1:
        #Run PCA
        start_time = time.time()
        text_file = open(Working_Directory + "log.txt", "a")
        text_file.write("Running pca in %s \n" % Working_Directory)
        print 'Running pca for all files...in '+ Working_Directory
        pca, imgs_pca, new_imgs = run_pca(data,pca_components,required_pcs)
        print 'Running PCA took '+ str(int(time.time()-start_time)) +' seconds' 
        text_file.write("Running pca took %s seconds \n" %  str(int(time.time()-start_time)))
        
        
        #Create PCA maps
        start_time = time.time()
        text_file.write("Making pca color maps in %s \n" % Working_Directory)
        print 'Making pca color maps for all files...in '+ Working_Directory
        img_size_x = np.size(new_imgs,1)
        img_size_y = np.size(new_imgs,2)
        maps, pts, pts_nonblack, clrs, clrs_nonblack, recon, unique_clrs, matched_pixels, matched_signals, mean_signal, sem_signal = make_pca_maps(data_background,pca, new_imgs, required_pcs, img_size_x,\
        img_size_y, num_pca_colors, num_samples, thresh_pca, color_map)
        print 'Making pca color maps '+ str(int(time.time()-start_time)) +' seconds' 
        text_file.write("Making pca color maps took %s seconds \n" %  str(int(time.time()-start_time)))
       
        print 'Matched_Pixels........' + str(np.shape(matched_pixels))
        pca_components = pca.comps.T
        ## save input parameters
        ############# Save all imput parameters
        start_time = time.time()
        text_file.write("Saving PCA reconstructed data.. in %s \n" % Working_Directory)
        create_data_in_pca_space(imgs_pca, pca_components, required_pcs,0.003, Working_Directory, name_for_saving_files)
        print 'Saving PCA reconstructed data in '+ str(int(time.time()-start_time)) +' seconds' 
        text_file.write("Saving PCA reconstructed data took %s seconds \n" %  str(int(time.time()-start_time)))
            
        with open(Working_Directory+name_for_saving_files+'_pca_results', 'w') as f:
            pickle.dump([pca_components, imgs_pca,new_imgs, maps, pts, pts_nonblack, clrs, clrs_nonblack, recon, unique_clrs, matched_pixels, matched_signals, mean_signal, sem_signal],f)
    
    else:        
        print 'Using existing pickled parameters....'
        text_file = open(Working_Directory + "log.txt", "a")
        text_file.write("Plotting Using existing pickled parameters....\n")
        with open(Working_Directory+name_for_saving_files+'_pca_results') as f:
            pca_components, imgs_pca, new_imgs, maps, pts, pts_nonblack, clrs, clrs_nonblack, recon, unique_clrs, matched_pixels, matched_signals, mean_signal, sem_signal = pickle.load(f)
        
            start_time = time.time()
            text_file.write("Saving PCA reconstructed data.. in %s \n" % Working_Directory)
            create_data_in_pca_space(imgs_pca, pca_components, required_pcs,0.003, Working_Directory, name_for_saving_files)
            print 'Saving PCA reconstructed data in '+ str(int(time.time()-start_time)) +' seconds' 
            text_file.write("Saving PCA reconstructed data took %s seconds \n" %  str(int(time.time()-start_time)))
# Plot PCA
    start_time = time.time()
    text_file.write("Plotting pca in %s \n" % Working_Directory)
    print 'Plotting pca in for all files...in '+ Working_Directory
    plot_pca_maps(Working_Directory, name_for_saving_figures, name_for_saving_files, \
    pca_components, maps, pts, pts_nonblack, clrs, clrs_nonblack, recon, unique_clrs, matched_pixels, matched_signals, flag,stimulus_on_time, stimulus_off_time, color_mat,required_pcs)
    print 'Plotting pca in '+ str(int(time.time()-start_time)) +' seconds' 
    text_file.write("Plotting pca in took %s seconds \n" %  str(int(time.time()-start_time)))
    


def plot_preprocess_data(Working_Directory, name_for_saving_files, data, stimulus_on_time, stimulus_off_time):
    
    #### Plot subset of data to view ######## 
    
        # To save as pdf create file
    start_time = time.time()
    print 'Plotting centered data...in '+ Working_Directory
    text_file = open(Working_Directory + "log.txt", "a")
    text_file.write("Plotting centered data in %s \n" % Working_Directory)
    
    #Save some data wide statistics to text file
    
    print 'Data Statistics :'
    print 'Series Mean :' + str(data.seriesMean().first())
    text_file = open(Working_Directory + "log.txt", "a")
    text_file.write("Series Mean : %s \n" % str(data.seriesMean().first()))
    
    print 'Series Std :' + str(data.seriesStdev().first())
    text_file = open(Working_Directory + "log.txt", "a")
    text_file.write("Series Std : %s \n" % str(data.seriesStdev().first()))

    from numpy import random
    signal = random.randn(data.index.shape[0])
    print 'Series Corrrelation :' + str(data.correlate(signal).first())
    text_file = open(Working_Directory + "log.txt", "a")
    text_file.write("Series Corrrelation : %s \n" % str(data.correlate(signal).first()))

        
    ## Plot some data related figures
    Figure_PDFDirectory = Working_Directory+filesep+'Figures'+filesep
    if not os.path.exists(Figure_PDFDirectory):
        os.makedirs(Figure_PDFDirectory)           
    pp = PdfPages(Figure_PDFDirectory+name_for_saving_files+'_PreprocessedData.pdf')
    
        
    with sns.axes_style("darkgrid"):    
        fig2 = plt.figure()
        examples = data.center().subset(nsamples=100, thresh=0.5)
        if np.size(examples)!=0:        
            plt.plot(examples.T[:,:]);
            plot_vertical_lines_onset(stimulus_on_time)
            plot_vertical_lines_offset(stimulus_off_time)
            plt.tight_layout()
            fig2 = plt.gcf()
            pp.savefig(fig2)
        
    with sns.axes_style("darkgrid"):  
        fig3 = plt.figure()
        
        examples = data.zscore(10).subset(nsamples=100, thresh=2)
        if np.size(examples)!=0:
            plt.plot(examples.T[:,:])
            plot_vertical_lines_onset(stimulus_on_time)
            plot_vertical_lines_offset(stimulus_off_time)
            plt.tight_layout()
            fig2 = plt.gcf()
            pp.savefig(fig3)
    
        
        fig4 = plt.figure()
        plt.plot(data.center().max());
        plt.plot(data.center().mean());
        plt.plot(data.center().min());
        plot_vertical_lines_onset(stimulus_on_time)
        plot_vertical_lines_offset(stimulus_off_time)        
        plt.tight_layout()
        fig2 = plt.gcf()
        pp.savefig(fig4)
        
        plt.close()
        pp.close()
        
        print 'Plotting centered data took '+ str(int(time.time()-start_time)) +' seconds' 
        text_file.write("Plotting centered data took %s seconds \n" %  str(int(time.time()-start_time)))

def plot_vertical_lines_onset(stimulus_on_time):
    for ii in xrange(0,np.size(stimulus_on_time)):
        plt.axvline(x=stimulus_on_time[ii], linestyle='-', color='k', linewidth=1)

def plot_vertical_lines_offset(stimulus_off_time):
    for ii in xrange(0,np.size(stimulus_off_time)):
        plt.axvline(x=stimulus_off_time[ii], linestyle='--', color='k', linewidth=1)
        
    
    
        
        


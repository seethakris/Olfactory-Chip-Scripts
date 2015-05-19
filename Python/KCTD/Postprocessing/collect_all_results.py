# -*- coding: utf-8 -*-
"""
Created on Mon May 11 03:04:13 2015

@author: seetha
"""
import os
filesep = os.path.sep

import pandas as pd
from numpy import size, logical_and,array
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns #For creating nice plots

Start_Folder = '/Users/seetha/Desktop/KCTD/'
Classified_Folder = Start_Folder+'Classified_Results/'

Save_DataFrames_Directory = Start_Folder+'DataFrames'+filesep
if not os.path.exists(Save_DataFrames_Directory):
    os.makedirs(Save_DataFrames_Directory)  
    
Figure_PDFDirectory = Classified_Folder   
name_file = 'Compile_Results_All'    
pp = PdfPages(Figure_PDFDirectory+name_file+'.pdf')          
sns.set_context("poster")  

Stimulus_Directories = [f[:-5] for f in os.listdir(Classified_Folder) if f.endswith('.xlsx')]
count_start = 0
count_file = 0

index_hets = array([19,17,20,23, 24])-14
index_wildtype = array([14,16,15,21,22,25])-14
index_mutants = array([18])-14

Stimulus_Directories_Hets = [ii for ii in Stimulus_Directories if (Stimulus_Directories.index(ii)==index_hets).any()]
Stimulus_Directories_Wildtype = [ii for ii in Stimulus_Directories if (Stimulus_Directories.index(ii)==index_wildtype).any()]
Stimulus_Directories_Mutants = [ii for ii in Stimulus_Directories if (Stimulus_Directories.index(ii)==index_mutants).any()]

for ii in Stimulus_Directories:
    
    if ii == 'Fish18_KCTDHUC_7dpf':
        Find_Folder = os.path.join(Start_Folder, ii, 'Tiff/Cropped/Registered/Thresholded_OB/Registered_Stimulus/Only_GCDA/DataFrames/')
    else:
        Find_Folder = os.path.join(Start_Folder, ii, 'Tiff/Cropped/Registered/Thresholded_OB/Registered_Stimulus/DataFrames/')
        
    ## Load data frames using pickle
    all_df = pd.read_pickle(Find_Folder+'all_df')
    df_for_plotting = pd.read_pickle(Find_Folder+'df_for_plotting') 
    df_pixels = pd.read_pickle(Find_Folder+'df_pixels')
    df_duration = pd.read_pickle(Find_Folder+'df_duration')
    
    ## Get a new dataframe with index for stimulus having maximum pixel 
    A = df_pixels.set_index([range(size(all_df,0))])
    B = pd.DataFrame({'Max':A.idxmax(axis=1)})
    
    if count_file == 0: 
        df_max = pd.concat((B,df_duration), axis=1)
        df_max_all = pd.concat((B,df_duration), axis=1)
        df_for_plotting_all = df_for_plotting 
    else:
        print count_file
        df_max = pd.concat((B,df_duration), axis=1)
        df_max_all = df_max_all.append(df_max)
        df_for_plotting_all = df_for_plotting_all.append(df_for_plotting,ignore_index=True)

    for jj in xrange(0, size(df_max,0)):
        if count_start == 0:
            df_max_stimlabels = df_for_plotting[logical_and(df_for_plotting['Original_Stim']==df_max['Max'][jj],\
            df_for_plotting['Stimulus_Type']==df_max['Stimulus_Type'][jj])]
            
        else:
            print jj
            df_max_stimlabels = df_max_stimlabels.append(df_for_plotting[logical_and(df_for_plotting['Original_Stim']==df_max['Max'][jj],\
            df_for_plotting['Stimulus_Type']==df_max['Stimulus_Type'][jj])])
        
        count_start = count_start +1
    
    ## Concetenate to get dataframe with max for plotting
    df_max_all = df_max_all.set_index([range(size(df_max_all,0))]) 
    df_max_stimlabels = df_max_stimlabels.set_index([range(size(df_max_stimlabels,0))])
    
    df_max_for_plotting = pd.merge(df_max_all, df_max_stimlabels, left_index=True, right_index=True, how='outer')
    df_max_for_plotting['Stimulus_Type_label'] = df_max_for_plotting.Stimulus_Type_x.str.contains('ON')   
    df_max_for_plotting['Stimulus_Type_label'] = df_max_for_plotting.Stimulus_Type_label.map({True:'ON', False:'OFF'})
    
    df_for_plotting_all['Stimulus_Type_label'] = df_for_plotting_all.Stimulus_Type.str.contains('ON')   
    df_for_plotting_all['Stimulus_Type_label'] = df_for_plotting_all.Stimulus_Type_label.map({True:'ON', False:'OFF'})
    ##Remove pixels that are 0
    df_for_plotting_all = df_for_plotting_all[(df_for_plotting_all.Pixels >= 10)]

    #Save
    df_max_for_plotting.to_pickle(Save_DataFrames_Directory+'df_max_compiled_for_plotting')
    
    
    count_file = count_file+1
    


    
## Plot compiled duration
sns.set_context('poster')
with sns.axes_style("darkgrid"):
    fig1 = plt.figure(figsize=(5,5))
    g = sns.lmplot('Label_stimulus', 'TDuration', df_max_for_plotting, \
    x_jitter=.15, hue='Stimulus_Type_label', markers=["x", "o"], size=5)
    g.set_axis_labels("Stimulus", "Duration of Activity (s)");
    g.set(xticks=[1,2,3], ylim=(5, 22))
    g.set_xticklabels(['GCDA100nM', 'GCDA10uM', 'GCDA1mM'], fontsize=12)
    fig1 = plt.gcf()
    pp.savefig(fig1)
    plt.close()
    
## Plot compiled number of cells
sns.set_context('poster')
with sns.axes_style("darkgrid"):
    fig1 = plt.figure(figsize=(5,5))
    g = sns.lmplot('Label_stimulus', 'Pixels', df_for_plotting_all, \
    x_jitter=.15, hue='Stimulus_Type_label', markers=["x", "o"], size=5)
    g.set_axis_labels("Stimulus", "Duration of Activity (s)");
    g.set(xticks=[1,2,3])
    g.set_xticklabels(['GCDA100nM', 'GCDA10uM', 'GCDA1mM'], fontsize=12)
    fig1 = plt.gcf()
    pp.savefig(fig1)
    plt.close()
    
pp.close()
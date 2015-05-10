# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 08:50:59 2014
Plot NMF components and maps for OB data 
@author: seetha
"""

#Import python libraries
import os
filesep = os.path.sep

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns #For creating nice plots
from mpl_toolkits.mplot3d import axes3d

from libtiff import TIFF

from thunder import Colorize
image = Colorize.image

z_direction = 'z'

def plot_NMF_maps(Working_Directory, name_for_saving_figures, name_for_saving_files, \
    NMF_components, maps, colors_NMF, matched_pixels, stimulus_on_time, stimulus_off_time, flag, unique_clrs):
    

    # To save as pdf create file
    Figure_PDFDirectory = Working_Directory+filesep+'Figures'+filesep
    if not os.path.exists(Figure_PDFDirectory):
        os.makedirs(Figure_PDFDirectory)           
    pp = PdfPages(Figure_PDFDirectory+name_for_saving_files+'_NMF.pdf')
               
    sns.set_context("poster")  
    
    ########### Plot components ##################
    fig2 = plt.figure()
    sns.set_context("talk", font_scale=1.25)
    with sns.axes_style("darkgrid"):
        ax1 = plt.subplot(221)
        plot_NMF_components(NMF_components,ax1,stimulus_on_time, stimulus_off_time, colors_NMF)
    
    #Plot mean projection   
    with sns.axes_style("white"):  
        fig2 = plt.subplot(223)        
        if len(maps.shape)==3:
            plt.imshow(maps)
        else:
            image(np.amax(maps,2))
            
        plt.axis('off')
        plt.title('Max projection')
    
    
    ########### Plot Boxplot of number of pixels ##################        
    with sns.axes_style("white"):
        fig2 = plt.subplot(222)
        fig2 = plot_boxplot(fig2, matched_pixels, colors_NMF[0:np.size(NMF_components,1)])
    
    plt.tight_layout()
    fig2 = plt.gcf()
    pp.savefig(fig2)
    plt.close()
    
    ################  Plot color maps individually #######################
    if flag == 0:
        plot_colormaps_ind(maps, Working_Directory, name_for_saving_figures, pp)
    elif flag == 1:
        plot_colormaps_each(maps, Working_Directory, name_for_saving_figures, pp,matched_pixels,colors_NMF[0:np.size(NMF_components,1)])
    elif flag == 2:
        plot_colormaps_all( maps, Working_Directory, pp, matched_pixels, colors_NMF[0:np.size(NMF_components,1)])
        plot_colormaps_all_z_plane_wise(maps, Working_Directory, pp,matched_pixels, colors_NMF[0:np.size(NMF_components,1)])
    

    pp.close()
                
def plot_colormaps_ind(maps, Working_Directory, name_for_saving_figures, pp):
###########  Plot color maps individually #######################
    if len(np.shape(maps)) == 3:
        #Plot colored maps for each stack
        with sns.axes_style("white"):
            fig1 = plt.figure()           
            plt.imshow(maps[:,:,:])
            plt.title(name_for_saving_figures + ' Z=1')
            plt.axis('off')                 
            fig1 = plt.gcf()
            pp.savefig(fig1)
            plt.close()
            
            
    else:
        with sns.axes_style("white"):
            for ii in range(0, np.size(maps,2)):
                fig1 = plt.imshow(maps[:,:,ii,:])
                plt.title(name_for_saving_figures + ' Z='+str(ii+1))
                plt.axis('off')
                fig1 = plt.gcf()
                pp.savefig(fig1)
                plt.close()

    
def plot_colormaps_each(maps, Working_Directory, name_for_saving_figures, pp, matched_pixels, unique_clrs):
    
    Trial_Directories = [f for f in os.listdir(os.path.join(Working_Directory)) if os.path.isdir(os.path.join(Working_Directory, f)) and f.find('Figures')<0] #Get only directories
    
    ## To find num z planes in each trial directory
    num_z_planes = np.zeros((np.size(Trial_Directories)), dtype=np.int)
    for jj in xrange(0, np.size(Trial_Directories, axis = 0)):
        Image_Directory = os.path.join(Working_Directory, Trial_Directories[jj],'C=1')+filesep    
        tif = TIFF.open(Image_Directory +'T=1.tif', mode='r') #Open multitiff 
        count = 1        
        for image in tif.iter_images():
            num_z_planes[jj] = count
            count = count+1
    
    count = 0     
    count_trial1 = 0
    for ii in xrange(0, np.size(Trial_Directories, axis = 0)):       
        count_subplot = 1
        for jj in xrange(0, num_z_planes[ii]):
            name_for_saving_figures1 = name_for_saving_figures + ' ' + Trial_Directories[ii] + ' Z=' + str(jj+1)
            with sns.axes_style("darkgrid"):           
                fig2 = plt.subplot(2,2,count_subplot)
                plt.imshow(maps[:,:,count,:])
                plt.title(name_for_saving_figures1)
                plt.axis('off')
            count = count+1
            count_subplot = count_subplot + 1
            
            # If there are more than 6 panel, save and start new figure
            if count_subplot == 5:
                fig2 = plt.gcf()
                pp.savefig(fig2)
                plt.close()
                count_subplot = 1
                    
        #Plot boxplots for each trial
        if count_subplot <= 4:
            with sns.axes_style("darkgrid"):
                fig2 = plt.subplot(2,2,count_subplot)
                fig2 = plot_boxplot(fig2, matched_pixels[:,count_trial1:count_trial1+num_z_planes[ii]], unique_clrs)
#                plt.tight_layout()            
                fig2 = plt.gcf()
                pp.savefig(fig2)
                plt.close()
            count_trial1 = count_trial1 + num_z_planes[ii]
            
        else:
            with sns.axes_style("darkgrid"):
                fig3 = plt.figure()
                fig3 = plot_boxplot(fig3, matched_pixels[:,count_trial1:count_trial1+num_z_planes[ii]], unique_clrs)
#                plt.tight_layout()            
                fig3 = plt.gcf()
                pp.savefig(fig3)
                plt.close()
            count_trial1 = count_trial1 + num_z_planes[ii]

        

    
def  plot_colormaps_all(maps, Working_Directory, pp, matched_pixels, unique_clrs):
    
    Stimulus_Directories = [f for f in os.listdir(Working_Directory) if os.path.isdir(os.path.join(Working_Directory, f)) and f.find('Figures')<0]
    
    ## To find num z planes in each trial directory
    num_z_planes = []
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):
        Trial_Directories = [f for f in os.listdir(os.path.join(Working_Directory, Stimulus_Directories[ii]))\
        if os.path.isdir(os.path.join(Working_Directory, Stimulus_Directories[ii], f)) and f.find('Figures')<0] #Get only directories        
        temp_num_z_planes = np.zeros((np.size(Trial_Directories)), dtype=np.int)    
        
        for jj in xrange(0, np.size(Trial_Directories, axis = 0)):
            Image_Directory = os.path.join(Working_Directory, Stimulus_Directories[ii], Trial_Directories[jj],'C=1')+filesep    
            tif = TIFF.open(Image_Directory +'T=1.tif', mode='r') #Open multitiff 
            count = 1        
            for image in tif.iter_images():
                temp_num_z_planes[jj] = count
                count = count+1
        
        num_z_planes.append(temp_num_z_planes)
                
    ### Plot maps - each stimulus in one page            
    count = 0
    count_exp1 = 0
    
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):
        count_subplot = 1
        
        Trial_Directories = [f for f in os.listdir(os.path.join(Working_Directory, Stimulus_Directories[ii]))\
        if os.path.isdir(os.path.join(Working_Directory, Stimulus_Directories[ii], f)) and f.find('Figures')<0] #Get only directories        
        
        for jj in xrange(0, np.size(Trial_Directories, axis = 0)):
            for kk in xrange(0, num_z_planes[ii][jj]):
                name_for_saving_figures1 = Stimulus_Directories[ii] + ' ' + Trial_Directories[jj] + ' Z=' + str(kk+1)                
                with sns.axes_style("darkgrid"):
                    fig2 = plt.subplot(2,2,count_subplot)
                    plt.imshow(maps[:,:,count,:])
                    plt.title(name_for_saving_figures1)
                    plt.axis('off')
                    
                count = count+1
                count_subplot = count_subplot+1
                

                # If there are more than 6 panel, save and start new figure
                if count_subplot == 5:
                    fig2 = plt.gcf()
                    pp.savefig(fig2)
                    plt.close()
                    count_subplot = 1
                    
        #Plot boxplots for each exp        
        if count_subplot <= 4:
            with sns.axes_style("darkgrid"):
                fig2 = plt.subplot(2,2,count_subplot)
                fig2 = plot_boxplot(fig2, matched_pixels[:,count_exp1:count_exp1+\
                np.sum(num_z_planes[ii])], unique_clrs)
                plt.tight_layout()            
                fig2 = plt.gcf()
                pp.savefig(fig2)
                plt.close()
            count_exp1 = count_exp1+np.sum(num_z_planes[ii])
            
        else:
            with sns.axes_style("darkgrid"):
                fig3 = plt.figure()
                fig2 = plot_boxplot(fig3, matched_pixels[:,count_exp1:count_exp1+\
                num_z_planes[ii][jj]], unique_clrs)
                plt.tight_layout()            
                fig3 = plt.gcf()
                pp.savefig(fig3)
                plt.close()
            count_exp1 = count_exp1+np.sum(num_z_planes[ii])



## Plot maps - each plane in one slide                  
def plot_colormaps_all_z_plane_wise(maps, Working_Directory, pp, matched_pixels, unique_clrs):
    
    
    Stimulus_Directories = [f for f in os.listdir(Working_Directory) if os.path.isdir(os.path.join(Working_Directory, f)) and f.find('Figures')<0]
    
    ## To find num z planes in each trial directory
    num_z_planes = []
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):
        Trial_Directories = [f for f in os.listdir(os.path.join(Working_Directory, Stimulus_Directories[ii]))\
        if os.path.isdir(os.path.join(Working_Directory, Stimulus_Directories[ii], f)) and f.find('Figures')<0] #Get only directories        
        temp_num_z_planes = np.zeros((np.size(Trial_Directories)), dtype=np.int)    
        
        for jj in xrange(0, np.size(Trial_Directories, axis = 0)):
            Image_Directory = os.path.join(Working_Directory, Stimulus_Directories[ii], Trial_Directories[jj],'C=1')+filesep    
            tif = TIFF.open(Image_Directory +'T=1.tif', mode='r') #Open multitiff 
            count = 1        
            for image in tif.iter_images():
                temp_num_z_planes[jj] = count
                count = count+1       
        num_z_planes.append(temp_num_z_planes)
        
        
    
    ## First rearrange maps according to planes instead of stimulus
    ## 1. Name the figures in maps one by one and then select those that are of a particular z
    name_for_saving_figures1 = []
    count = 0
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):        
        Trial_Directories = [f for f in os.listdir(os.path.join(Working_Directory, Stimulus_Directories[ii]))\
        if os.path.isdir(os.path.join(Working_Directory, Stimulus_Directories[ii], f)) and f.find('Figures')<0] #Get only directories                
        for jj in xrange(0, np.size(Trial_Directories, axis = 0)):
            for kk in xrange(0, num_z_planes[ii][jj]):
                name_for_saving_figures1.append(Stimulus_Directories[ii] + ' ' + Trial_Directories[jj] + ' Z=' + str(kk+1))        
                
    ### Plot maps - each z-plane one page          
    ## FInd maximum z planes
    Max_z = max(max(num_z_planes, key=lambda x:np.max(x)))
    for ii in xrange(1, Max_z+1):
        Matching_file_index = [name_for_saving_figures1.index(s) for s in name_for_saving_figures1 if "Z="+str(ii) in s]
        Matching_file_names = [s for s in name_for_saving_figures1 if "Z="+str(ii) in s]        
        temp_maps = maps[:,:,Matching_file_index,:]    
        temp_matched_pixels = matched_pixels[:,Matching_file_index]
        count_subplot=1        
        for jj in xrange(0,np.size(temp_maps,2)):
            with sns.axes_style("darkgrid"):
                fig2 = plt.subplot(2,3,count_subplot)
                plt.imshow(temp_maps[:,:,jj,:])
                plt.title(Matching_file_names[jj],fontsize=11)
                plt.axis('off')
            
            count_subplot = count_subplot+1
    
            if count_subplot == 7:
                fig2 = plt.gcf()
                pp.savefig(fig2)
                plt.close()
                count_subplot = 1
                
        #Plot boxplots for each exp        
        if count_subplot <= 6:
            with sns.axes_style("darkgrid"):
                fig2 = plt.subplot(2,3,count_subplot)
                fig2 = plot_boxplot(fig2, temp_matched_pixels, unique_clrs)
                plt.tight_layout()            
                fig2 = plt.gcf()
                pp.savefig(fig2)
                plt.close()
            
        else:
            with sns.axes_style("darkgrid"):
                fig3 = plt.figure()
                fig2 = plot_boxplot(fig3, temp_matched_pixels, unique_clrs)
                plt.tight_layout()            
                fig3 = plt.gcf()
                pp.savefig(fig3)
                plt.close()
        
        
    
def plot_NMF_components(NMF_components,ax1,stimulus_on_time, stimulus_off_time, colors_NMF):
########### Plot components ##################    
    for ii in range(np.size(NMF_components,1)):
        plt.plot(NMF_components[:,ii], color=colors_NMF[ii])
    
    plt.locator_params(axis = 'y', nbins = 4)
    sns.axlabel("Time (seconds)","a.u")
    
    A = []
    for ii in xrange(0,np.size(NMF_components, 1)):
        A = np.append(A, [str(ii)])
        
    ax1.legend(A, loc=4)
    plt.axhline(y=0, linestyle='-', color='k', linewidth=1)
    plot_vertical_lines_onset(stimulus_on_time)
    plot_vertical_lines_offset(stimulus_off_time)
        
    

def plot_boxplot(fig2, matched_pixels, unique_clrs):
#### Plot Boxplot of number of pixels
    ## Dont plot boxplot if there is only one Z
    if np.size(matched_pixels,1) == 1:
        with sns.axes_style("darkgrid"):
            for ii in xrange(0,np.size(matched_pixels,0)):
                fig2 = plt.plot(ii+1,np.transpose(matched_pixels[ii,:]),'o', color=unique_clrs[ii])
                plt.xlim([0,np.size(matched_pixels,0)+1])
    else:
        fig2 = sns.boxplot(np.transpose(matched_pixels),linewidth=3, widths=.5, color=unique_clrs)
        
    for ii in range(0,np.size(unique_clrs,0)):
        fig2 = plt.plot(np.repeat(ii+1,np.size(matched_pixels,1)), np.transpose(matched_pixels[ii,:]),'s', \
        color=unique_clrs[ii], markersize=5, markeredgecolor='k', markeredgewidth=2) 
    
    plt.locator_params(axis = 'y', nbins = 2)
    sns.axlabel("Colors", "Number of Pixels")
    sns.despine(offset=10, trim=True)
    return fig2
    
    
def plot_axis_labels_byzdir(ax1,z_direction,required_pcs):
    
    if z_direction == 'y':
        ax1.set_xlabel('PC'+str(required_pcs[0]), linespacing=10, labelpad = 50)
        ax1.set_ylabel('PC'+str(required_pcs[2]), linespacing=10, labelpad = 50)
        
        ax1.zaxis.set_rotate_label(False)  # disable automatic rotation
        ax1.set_zlabel('PC'+str(required_pcs[1]), rotation=90, linespacing=10, labelpad = 10)

    elif z_direction == 'z':
        ax1.set_xlabel('PC'+str(required_pcs[0]), linespacing=10, labelpad = 50)
        ax1.set_ylabel('PC'+str(required_pcs[1]), linespacing=10, labelpad = 50)
        
        ax1.zaxis.set_rotate_label(False)  # disable automatic rotation
        ax1.set_zlabel('PC'+str(required_pcs[2]), rotation=90, linespacing=10, labelpad = 10)
    
    elif z_direction == 'x':
        ax1.set_xlabel('PC'+str(required_pcs[1]), linespacing=10, labelpad = 50)
        ax1.set_ylabel('PC'+str(required_pcs[2]), linespacing=10, labelpad = 50)
        
        ax1.zaxis.set_rotate_label(False)  # disable automatic rotation
        ax1.set_zlabel('PC'+str(required_pcs[0]), rotation=90, linespacing=10, labelpad = 10)
    
    ax1.locator_params(axis = 'x',  pad=50)
    ax1.locator_params(axis = 'y', pad=50)
    ax1.locator_params(axis = 'z',  pad=50)
         

def plot_vertical_lines_onset(stimulus_on_time):
    for ii in xrange(0,np.size(stimulus_on_time)):
        plt.axvline(x=stimulus_on_time[ii], linestyle='-', color='k', linewidth=1)

def plot_vertical_lines_offset(stimulus_off_time):
    for ii in xrange(0,np.size(stimulus_off_time)):
        plt.axvline(x=stimulus_off_time[ii], linestyle='--', color='k', linewidth=1)
                
    

    

        
        


# -*- coding: utf-8 -*-
"""
Created on Fri May  8 16:54:52 2015
Postprocessing to find glomeruli 
@author: seetha
"""
from numpy import zeros, size, corrcoef,all, append, array, where, logical_and, less,\
argmin, greater, isnan, squeeze, mean, int, float16, hstack,tile, reshape, repeat, argmax

import pickle
import matplotlib.pyplot as plt
import os
filesep = os.path.sep
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns #For creating nice plots
from scipy.signal import argrelextrema
from pandas import DataFrame, concat, ExcelWriter
from libtiff import TIFF
import os
filesep = os.path.sep

Label_Odor = {'GCDA100NM':1,'GCDA10UM':2, 'GCDA1MM':3}
Label_Odor_reverse = {1:'GCDA100NM',2:'GCDA10UM', 3:'GCDA1MM'}
######################### Inputs ######################################
## Enter Main Folder containing stimulus folders to create text files

Exp_Folder ='/Users/seetha/Desktop/KCTD/Fish14_KCTDHUC_5dpf/Tiff/Cropped/Registered/Thresholded_OB/Registered_Stimulus/'
filename_save_prefix_forkmeanswithPCA = 'ThresholdedOB_1and2PC_T81'
Result_Directory = '/Users/seetha/Desktop/KCTD/'

#Stimulus on and off time
stimulus_pulse = 1
if stimulus_pulse == 1:
    stimulus_on_time = [10,29,49,68]
    stimulus_off_time = [14,33,53,72]

    
elif stimulus_pulse == 2:
    stimulus_on_time = [10,28,47,65,84,101]
    stimulus_off_time = [13,31,52,68,87,104]

elif stimulus_pulse == 3: #Fish 21 onwards
    stimulus_on_time = [10,29,48,66,85,103]
    stimulus_off_time = [13,32,53,69,88,106]
    color_mat = ['#00FFFF','#0000A0','#800080','#FF00FF', '#800000','#A52A2A']

elif stimulus_pulse == 4: #Fish 23 onwards
    stimulus_on_time = [10,28,46,65,83,102]
    stimulus_off_time = [13,31,51,70,86,105]
    color_mat = ['#00FFFF','#0000A0','#800080','#FF00FF', '#800000','#A52A2A']
elif stimulus_pulse == 5: #Only Fish 24 alone
    stimulus_on_time = [10,29,46,66,84,104]
    stimulus_off_time = [13,32,51,69,87,107]
    color_mat = ['#00FFFF','#0000A0','#800080','#FF00FF', '#800000','#A52A2A']

#Create may directoriess
Save_Directory = Result_Directory+'Classified_Results'+filesep
if not os.path.exists(Save_Directory):
    os.makedirs(Save_Directory)  

Save_DataFrames_Directory = Exp_Folder+'DataFrames'+filesep
if not os.path.exists(Save_DataFrames_Directory):
    os.makedirs(Save_DataFrames_Directory)  
    
Figure_PDFDirectory = Save_Directory    
name_file = Exp_Folder[len(Result_Directory):len(Result_Directory)+\
Exp_Folder[len(Result_Directory):].find(filesep)]      
pp = PdfPages(Figure_PDFDirectory+name_file+'.pdf')
           
sns.set_context("poster")  


#######################################################################
def Main_function(Exp_Folder, name_file, filename_save_prefix_forkmeanswithPCA, stimulus_on_time, stimulus_off_time):
    #For kmeans
    name_for_saving_files_kmeans = 'All_odors_'+ filename_save_prefix_forkmeanswithPCA+'_eachodor'
    
    #OPen kmeans outputs
    with open(Exp_Folder+name_for_saving_files_kmeans+'_kmeans_results') as f:
        kmeans_clusters,kmeans_clusters_updated, img_sim, img_labels, brainmap_kmeans, unique_clrs_kmeans, newclrs_rgb, newclrs_brewer, matched_pixels_kmeans = pickle.load(f)
    
    ## Create a sinusoid for stimulus and correlate with kmeans to find on and off traces
    Stim_on_trace = zeros((size(kmeans_clusters_updated,0),1))
    for ii in xrange(0, len(stimulus_on_time)):
        Stim_on_trace[stimulus_on_time[ii]+1:stimulus_off_time[ii]+8] = 0.005
        
    corr_coef = zeros((size(kmeans_clusters_updated,1),1))
    for ii in xrange(0, size(kmeans_clusters_updated,1)):
        corr_coef[ii] = corrcoef(Stim_on_trace[:,0], kmeans_clusters_updated[:,ii])[0,1]
    
    #On clusters
    On_clusters_index = array(where(corr_coef[:,0]>0))
    Off_clusters_index = array(where(corr_coef[:,0]<0))

    ## Find duration of signal, amplitude of signal and number of pixels using kmeans. Sort by stimuli
    Duration_ON = get_duration_for_ON(On_clusters_index, kmeans_clusters_updated, stimulus_on_time, stimulus_off_time)
    Duration_OFF =  get_duration_for_OFF(Off_clusters_index, kmeans_clusters_updated, stimulus_on_time, stimulus_off_time)
      
    ##Sort matched pixel matrix by rgb color for the clusters
    if size(On_clusters_index,1)>1:
        newclrs_rgb_ON = squeeze(newclrs_rgb.colors[On_clusters_index]).tolist()
        Num_pixels_ON = get_pixels_ON(matched_pixels_kmeans, newclrs_rgb_ON, unique_clrs_kmeans.tolist())
    elif size(On_clusters_index,1) == 1:
        newclrs_rgb_ON = newclrs_rgb.colors[On_clusters_index].tolist()
        newclrs_rgb_ON = [j for i in newclrs_rgb_ON for j in i]
        Num_pixels_ON = get_pixels_ON(matched_pixels_kmeans, newclrs_rgb_ON, unique_clrs_kmeans.tolist())
    else: 
        Num_pixels_ON = []
    
    if size(Off_clusters_index,1)>1:    
        newclrs_rgb_OFF = squeeze(newclrs_rgb.colors[Off_clusters_index]).tolist()    
        Num_pixels_OFF = get_pixels_OFF(matched_pixels_kmeans,newclrs_rgb_OFF, unique_clrs_kmeans.tolist())
    elif size(Off_clusters_index,1) == 1:
        newclrs_rgb_OFF = newclrs_rgb.colors[Off_clusters_index].tolist()    
        newclrs_rgb_OFF = [j for i in newclrs_rgb_OFF for j in i]

        Num_pixels_OFF = get_pixels_OFF(matched_pixels_kmeans,newclrs_rgb_OFF, unique_clrs_kmeans.tolist())
    else:
        Num_pixels_OFF = []
    ## Accumalate data for all fish
    all_df, df_duration, df_pixels,df_for_plotting = save_data(Exp_Folder, Result_Directory, name_file, Duration_ON, Duration_OFF, Num_pixels_ON, Num_pixels_OFF)    
    all_df.to_pickle(Save_DataFrames_Directory+'all_df')
    df_duration.to_pickle(Save_DataFrames_Directory+'df_duration')
    df_pixels.to_pickle(Save_DataFrames_Directory+'df_pixels')
    df_for_plotting.to_pickle(Save_DataFrames_Directory+'df_for_plotting')
    
    ## Get localtion of each NMF component and 
    ## plot the kmeans selected by correlation
    plot_selected_traces(pp, kmeans_clusters_updated, corr_coef, On_clusters_index, Off_clusters_index, \
    Stim_on_trace, stimulus_on_time, stimulus_off_time)
    
    # Plot raw data
    kmeans = squeeze(kmeans_clusters_updated[:,[hstack((On_clusters_index, Off_clusters_index))]])
    raw_data_heatmaps(kmeans, df_pixels, df_for_plotting)
        
    pp.close()
    
    return corr_coef, all_df, df_duration, df_pixels , df_for_plotting 

## Save data
def save_data(Working_Directory, Result_Directory, name_file, Duration_ON, Duration_OFF, Num_pixels_ON, Num_pixels_OFF):
    ## Excel data
    #Save duration 
    Duration = list()
    Stimulus_Type = list()
    Matched_Pixels = list()
    Stimulus_Index = list()
    count=0
    for ii in xrange(size(Duration_ON,0)):
        Duration.append(mean(Duration_ON[ii,:]))
        Matched_Pixels.append(Num_pixels_ON[ii,:])
        Stimulus_Type.append(str(count+1)+'ON')
        Stimulus_Index.append(count)
        count=count+1
    for ii in xrange(size(Duration_OFF,0)):
        Duration.append(mean(Duration_OFF[ii,:]))
        Matched_Pixels.append(Num_pixels_OFF[ii,:])
        Stimulus_Type.append(str(count+1)+'OFF')   
        Stimulus_Index.append(count)
        count=count+1
    
    ## For fish 23, change OFF to ON and save
#    Stimulus_Type[2] = '3ON'
        
    #Save matched_pixels 
    Name_stimulus = get_list_of_stimulus_name(Working_Directory)
    Label_plane, Label_stimulus = label_stimulus(Name_stimulus,Stimulus_Type)
    Stim_type_all = repeat(Stimulus_Type, size(Matched_Pixels,1))
    Matched_Pixels_all = reshape(Matched_Pixels, (size(Matched_Pixels)))
    Name_stimulus_all = tile(Name_stimulus, size(Matched_Pixels,0))
    # Some data frames
    df1 = DataFrame({'Stimulus_Type':Stimulus_Type,'TDuration':Duration}) #Only duration
    df2 = DataFrame(index=Stimulus_Index, columns=Name_stimulus) # pixels to concatenate with duration
    df3 = DataFrame(index=Stimulus_Type, columns=Name_stimulus) #pixels tandalone
    df4 = DataFrame({'Stimulus_Type':Stim_type_all, 'Pixels':Matched_Pixels_all,\
    'Label_plane':Label_plane, 'Label_stimulus':Label_stimulus, 'Original_Stim':Name_stimulus_all}) #label pixels with stimulus and z plane
    df4["Stimulus"] = df4.Label_stimulus.map(Label_Odor_reverse)
    
    for ii in xrange(0,size(Stimulus_Index)):
        df2.ix[ii] = Matched_Pixels[ii]
        df3.ix[ii] = Matched_Pixels[ii]
    df = concat([df1,df2], join='inner', axis=1)
    #Save to excel
    writer = ExcelWriter(Result_Directory+ filesep+'Classified_Results'+filesep+name_file+ '.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='sheet1')
    writer.close()
    
    return df, df1, df3, df4
    
#Create Labels for the stimulus
def label_stimulus(Name_stimulus, Stimulus_Type):
    label_stim = list()
    label_plane = list()
    for index, value in enumerate(Name_stimulus):
        stim = value[:value.find(' ')]
        Z = value[value.find('Z=')+2:value.find('Z=')+3]
        label_stim.append(Label_Odor[stim.upper()])
        print stim.upper()
        label_plane.append(int(Z))
    
    label_stim = tile(label_stim, size(Stimulus_Type,0))
    label_plane = tile(label_plane, size(Stimulus_Type,0))
        
    return label_plane, label_stim
#Get stimlus names
def get_list_of_stimulus_name(Working_Directory):
    ## To find num z planes in each trial directory
    num_z_planes = []
    Name_stimulus = list()
    
    Stimulus_Directories = [f for f in os.listdir(Working_Directory) if os.path.isdir(os.path.join(Working_Directory, f)) and f.find('Figures')<0]

    for ii in xrange(0, size(Stimulus_Directories, axis = 0)):
        Trial_Directories = [f for f in os.listdir(os.path.join(Working_Directory, Stimulus_Directories[ii]))\
        if os.path.isdir(os.path.join(Working_Directory, Stimulus_Directories[ii], f)) and f.find('Figures')<0] #Get only directories        
        temp_num_z_planes = zeros((size(Trial_Directories)), dtype=int)    
        
        for jj in xrange(0, size(Trial_Directories, axis = 0)):
            Image_Directory = os.path.join(Working_Directory, Stimulus_Directories[ii], Trial_Directories[jj], 'C=1')+filesep    
            tif = TIFF.open(Image_Directory +'T=1.tif', mode='r') #Open multitiff 
            count = 1        
            for image in tif.iter_images():
                temp_num_z_planes[jj] = count
                count = count+1
        
        num_z_planes.append(temp_num_z_planes)
                  
    for ii in xrange(0, size(Stimulus_Directories, axis = 0)):        
        Trial_Directories = [f for f in os.listdir(os.path.join(Working_Directory, Stimulus_Directories[ii]))\
        if os.path.isdir(os.path.join(Working_Directory, Stimulus_Directories[ii], f)) and f.find('Figures')<0] #Get only directories                
        for jj in xrange(0, size(Trial_Directories, axis = 0)):
            for kk in xrange(0, num_z_planes[ii][jj]):
                name_for_saving_figures = Stimulus_Directories[ii] + ' ' + Trial_Directories[jj] + ' Z=' + str(kk+1)       
                Name_stimulus.append(name_for_saving_figures)
    
    return Name_stimulus
                
def get_duration_for_ON(On_clusters_index, kmeans_clusters_updated, stimulus_on_time, stimulus_off_time):    
    #Loop through the picked clusters and find mean duration
    kmeans_clusters_ON = kmeans_clusters_updated[:,On_clusters_index[0]]    
    Duration = zeros((size(kmeans_clusters_ON,1),size(stimulus_on_time)-1), dtype=float16)
    
    for ii in xrange(0,size(kmeans_clusters_ON,1)):
        for jj in xrange(0,size(stimulus_on_time)-1):
            A1 = kmeans_clusters_ON[stimulus_on_time[jj]:stimulus_off_time[jj+1],ii]
            offset_A1 = A1[stimulus_off_time[jj]+3-stimulus_on_time[jj]:]
            #Find minima
            minimum_pts = argrelextrema(offset_A1, less)
            if size(minimum_pts)==0:
                    print ii, jj
                    Duration[ii,jj] = argmin(offset_A1)+ stimulus_off_time[jj]+3-stimulus_on_time[jj]
            elif (offset_A1[minimum_pts] < A1[0]).any():               
                offset_duration = minimum_pts[0][where(offset_A1[minimum_pts] < A1[0])[0][0]]
                Duration[ii,jj] = offset_duration + stimulus_off_time[jj]+3-stimulus_on_time[jj]
            else:
                Duration[ii,jj] = minimum_pts[0][argmin(offset_A1[minimum_pts])] + stimulus_off_time[jj]+3-stimulus_on_time[jj]
            
    return Duration
    
def get_duration_for_OFF(Off_clusters_index, kmeans_clusters_updated, stimulus_on_time, stimulus_off_time):
    
    #Loop through the picked clusters and find mean duration
    kmeans_clusters_OFF = kmeans_clusters_updated[:,Off_clusters_index[0]]    
    Duration = zeros((size(kmeans_clusters_OFF,1),size(stimulus_on_time)-1), dtype=float16)

    for ii in xrange(0,size(kmeans_clusters_OFF,1)):
        for jj in xrange(0,size(stimulus_on_time)-1):
            A1 = kmeans_clusters_OFF[stimulus_on_time[jj]:stimulus_off_time[jj+1],ii]
            offset_A1 = A1[stimulus_off_time[jj]+3-stimulus_on_time[jj]:]
            print ii, jj
            #Find maxima
            maximum_pts = argrelextrema(offset_A1, greater)
            if size(maximum_pts)==0:
                Duration[ii,jj] = argmax(offset_A1)+ stimulus_off_time[jj]+3-stimulus_on_time[jj]
            elif (A1[maximum_pts] > A1[0]).any():
                offset_duration = maximum_pts[0][where(offset_A1[maximum_pts] > A1[0])[0][0]]
                Duration[ii,jj] = offset_duration + stimulus_off_time[jj]+3-stimulus_on_time[jj]
            else:
                Duration[ii,jj] =  maximum_pts[0][argmax(offset_A1[maximum_pts])] + stimulus_off_time[jj]+3-stimulus_on_time[jj]
    
    return Duration
    
def get_pixels_ON(matched_pixels_kmeans, newclrs_rgb_ON, unique_clrs_kmeans):
    matched_pixels_ON = zeros((size(newclrs_rgb_ON), size(matched_pixels_kmeans,1)))
    for ii in xrange(0,size(newclrs_rgb_ON,0)):
        index = unique_clrs_kmeans.index(newclrs_rgb_ON[ii])
        print index, newclrs_rgb_ON[ii]
        matched_pixels_ON[ii,:] = matched_pixels_kmeans[index,:]
    return matched_pixels_ON
 
def get_pixels_OFF(matched_pixels_kmeans, newclrs_rgb_OFF, unique_clrs_kmeans):
    matched_pixels_OFF = zeros((size(newclrs_rgb_OFF), size(matched_pixels_kmeans,1)))
    for ii in xrange(0,size(newclrs_rgb_OFF,0)):
        index = unique_clrs_kmeans.index(newclrs_rgb_OFF[ii])
        print index, newclrs_rgb_OFF[ii]
        matched_pixels_OFF[ii,:] = matched_pixels_kmeans[index,:]
    return matched_pixels_OFF

    
def plot_selected_traces(pp, kmeans_clusters_updated, corr_coef, On_clusters_index, \
Off_clusters_index, Stim_on_trace, stimulus_on_time, stimulus_off_time):
    
    fig1 = plt.figure(1)
    
    plt.subplot(2,2,1)
    plt.plot(kmeans_clusters_updated)
    plot_vertical_lines_onset(stimulus_on_time)
    plot_vertical_lines_offset(stimulus_off_time)
    
    A = []
    for ii in xrange(0,size(kmeans_clusters_updated, 1)):
        A = append(A, [str(ii)])
        
    plt.legend(A, loc=4)
    
    plt.subplot(2,2,2)
    plt.plot(kmeans_clusters_updated[:,all(corr_coef>0, axis=1)])
    plt.plot(Stim_on_trace, color='k')
    plot_vertical_lines_onset(stimulus_on_time)
    plot_vertical_lines_offset(stimulus_off_time)
    
    A = []
    for ii in xrange(0,size(On_clusters_index[0])):
        A = append(A, [str(On_clusters_index[0][ii])])
        
    plt.legend(A, loc=4)
    
    
    plt.subplot(2,2,4)
    plt.plot(kmeans_clusters_updated[:,all(corr_coef<0, axis=1)])
    plt.plot(-Stim_on_trace, color='k')
    plot_vertical_lines_onset(stimulus_on_time)
    plot_vertical_lines_offset(stimulus_off_time)
    
    A = []
    for ii in xrange(0,size(Off_clusters_index[0])):
        A = append(A, [str(Off_clusters_index[0][ii])])
        
    plt.legend(A, loc=4)
    
    fig1 = plt.gcf()
    pp.savefig(fig1)
    plt.close()
    
def raw_data_heatmaps(kmeans, df_pixels,df_for_plotting):
    fig1 = plt.figure(figsize=(14, 15))
    gs = plt.GridSpec(4+(size(kmeans,1)*2)+2, 6)
    
    #Historgram
    hist_ax = fig1.add_subplot(gs[:3,:3])
    pixels = df_pixels.sum(axis=0)
    hist_ax.bar(range(size(df_pixels,1)), pixels, 1, ec="w", lw=2, color=".3")
    hist_ax.set(xticks=[], ylabel="pixels")
    
    ## Plot mean number of pixels
    barplot_ax = fig1.add_subplot(gs[:3,4:])
    sns.barplot("Stimulus", "Pixels", "Stimulus_Type", data=df_for_plotting,\
    ax=barplot_ax,palette="Pastel1");
    box = barplot_ax.get_position()
    barplot_ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    # Put a legend to the right of the current axis
    barplot_ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    #Plot traces
    count = 4
    for ii in xrange(0,size(kmeans,1)):
        with sns.axes_style("white"):
            plot_ax = fig1.add_subplot(gs[count:count+2,3:])
            plot_ax.plot(kmeans[:,ii], linewidth=3)
            plot_ax.axhline(y=0, linestyle='-', color='k', linewidth=1)
            plot_ax.axis('off')
            plot_vertical_lines_onset(stimulus_on_time)
            plot_vertical_lines_offset(stimulus_off_time)
        count=count+2
        
    #Colormap
    map_ax = fig1.add_subplot(gs[3:-1,:3])
    bar_ax = fig1.add_subplot(gs[-1,3:])
    sns.heatmap(df_pixels, cmap="OrRd", ax=map_ax,
                cbar_ax=bar_ax, cbar_kws={"orientation": "horizontal"})
    bar_ax.set(xlabel="pixels")
    
    fig1 = plt.gcf()
    pp.savefig(fig1)
    plt.close()
    
      
def plot_vertical_lines_onset(stimulus_on_time):
    for ii in xrange(0,size(stimulus_on_time)):
        plt.axvline(x=stimulus_on_time[ii], linestyle='-', color='k', linewidth=1)

def plot_vertical_lines_offset(stimulus_off_time):
    for ii in xrange(0,size(stimulus_off_time)):
        plt.axvline(x=stimulus_off_time[ii], linestyle='--', color='k', linewidth=1)
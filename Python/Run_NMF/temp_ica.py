Exp_Folder ='/Users/seetha/Desktop/Ruey_Habenula/Habenula/Short_Stimulus/Fish104_Block2_Blue&UV1c/'
filename_save_prefix = 'Test1'


from thunder import ThunderContext

print 'Starting Thunder Now. Check console for details'
tsc = ThunderContext.start(appName="thunderNMF")
import os
filesep = os.path.sep

import matplotlib.pyplot as plt 

import numpy as np
from thunder_NMF import run_NMF
from thunder_NMF import make_NMF_maps
from thunder_NMF_plots import plot_NMF_maps

from thunder import Colorize
image = Colorize.image

Stimulus_Directories = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f)) and f.find('Figures')<0]
#Stimulus_Directories
ii = 0
Trial_Directories = [f for f in os.listdir(os.path.join(Exp_Folder, Stimulus_Directories[ii]))\
if os.path.isdir(os.path.join(Exp_Folder, Stimulus_Directories[ii], f)) and f.find('Figures')<0]
Trial_Directories
jj = 0

stim_start = 10 #Stimulus Starting time point
stim_end = 14 #Stimulus Ending time point

flag = 0

name_for_saving_figures = Stimulus_Directories[ii] + ' ' + Trial_Directories[jj]        
Working_Directory = os.path.join(Exp_Folder, Stimulus_Directories[ii], Trial_Directories[jj])+filesep       
name_for_saving_files = Stimulus_Directories[ii] + '_' + Trial_Directories[jj] + filename_save_prefix+'_individualtrial'
#Working_Directory = os.path.join(Exp_Folder, Stimulus_Directories[ii])+filesep     
#name_for_saving_files = Stimulus_Directories[ii] + '_'+ filename_save_prefix+'_eachodor'
#name_for_saving_figures = Stimulus_Directories[ii]       

#Working_Directory = Exp_Folder
#name_for_saving_files = 'All_odors_'+ filename_save_prefix+'_eachodor'
#name_for_saving_figures = Working_Directory

data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputFormat='text', nkeys=3).toTimeSeries().detrend(method='linear', order=10)
data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputFormat='text', nkeys=3)
data_background.cache()
#plot_preprocess_data(Working_Directory, name_for_saving_files, data_filtered, stim_start, stim_end)
                
data_filtered.center()
data_filtered.zscore(30)
data_filtered.cache()

NMF, imgs_NMF = run_NMF(data_filtered,4)
NMF_components = NMF.h.T
colors_NMF = ['mediumpurple','hotpink','red','aqua']

for ii in range(np.size(NMF_components,1)):
    plt.plot(NMF_components[:,ii], color=colors_NMF[ii])##

img_size_x = np.size(imgs_NMF,1)
img_size_y = np.size(imgs_NMF,2)
#
maps,matched_pixels,unique_clrs = make_NMF_maps(data_background,NMF, imgs_NMF, img_size_x, img_size_y, 5, 'indexed', colors_NMF)
stimulus_on_time = [46,98,142,194]
stimulus_off_time = [65,117,161,213]
plot_NMF_maps(Working_Directory, name_for_saving_figures, name_for_saving_files, \
    NMF_components, maps, colors_NMF, matched_pixels, stimulus_on_time, stimulus_off_time, flag, unique_clrs)
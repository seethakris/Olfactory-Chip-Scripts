Exp_Folder = '/media/seetha/Se/Microfluidic Chip_Data_mac/Data/Fish3_7dpf/Tiff/Registered/Registered_Stimulus/'
filename_save_prefix = 'test1_T40'
from thunder import ThunderContext

print 'Starting Thunder Now. Check console for details'
tsc = ThunderContext.start(appName="thunderica")
import os
filesep = os.path.sep

import time
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

from thunder_ica import run_ica
from thunder_ica import make_ica_maps
from thunder_ica_plots import plot_ica_maps
#from ica_thunder_analysis import plot_preprocess_data

Stimulus_Directories = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f)) and f.find('Figures')<0]
#Stimulus_Directories
ii = 0
Trial_Directories = [f for f in os.listdir(os.path.join(Exp_Folder, Stimulus_Directories[ii]))\
if os.path.isdir(os.path.join(Exp_Folder, Stimulus_Directories[ii], f)) and f.find('Figures')<0]
jj = 0

stim_start = 10 #Stimulus Starting time point
stim_end = 15 #Stimulus Ending time point

flag = 0

name_for_saving_figures = Stimulus_Directories[ii] + ' ' + Trial_Directories[jj]        
Working_Directory = os.path.join(Exp_Folder, Stimulus_Directories[ii], Trial_Directories[jj], 'C=1')+filesep       
## Check if textfile exists, else create a new one
name_for_saving_files = Stimulus_Directories[ii] + '_' + Trial_Directories[jj] + filename_save_prefix+'_individualtrial'
#Working_Directory = os.path.join(Exp_Folder, Stimulus_Directories[ii])+filesep     
#name_for_saving_files = Stimulus_Directories[ii] + '_'+ filename_save_prefix+'_eachodor'
#name_for_saving_figures = Stimulus_Directories[ii]       

#Working_Directory = Exp_Folder
#name_for_saving_files = 'All_odors_'+ filename_save_prefix+'_eachodor'
#name_for_saving_figures = Working_Directory

data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputformat='text', nkeys=3)
data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputformat='text', nkeys=3)
data_background.cache()
#plot_preprocess_data(Working_Directory, name_for_saving_files, data_filtered, stim_start, stim_end)
                
data_filtered.center()
data_filtered.zscore()
data_filtered.cache()

colors_ica = ['red','blue','lime','hotpink','gold','mediumpurple']

ica, imgs_ica = run_ica(data_filtered,4,3)
for ii in xrange(0, np.size(ica.a, 1)):
    plt.plot(ica.a[:,ii], color=colors_ica[ii])


img_size_x = np.size(imgs_ica,1)
img_size_y = np.size(imgs_ica,2)


#ica parameters for individual trial ica
color_map = 'indexed' #Colormap for plotting ica components
num_ica_colors = 5 # number of colors in colormap

maps, matched_pixels = make_ica_maps(data_background,ica, imgs_ica, img_size_x,\
img_size_y, num_ica_colors, color_map, colors_ica[0:3])
#
plot_ica_maps(Working_Directory, name_for_saving_figures, name_for_saving_files, \
ica.a, maps, colors_ica[0:3], matched_pixels, stim_start, stim_end, flag)
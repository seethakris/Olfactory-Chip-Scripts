Exp_Folder ='/Users/seetha/Desktop/KCTD/Fish14_KCTDHUC_5dpf/Tiff/Cropped/Registered/Thresholded_OB/Registered_Stimulus/'
filename_save_prefix = 'ThresholdedOB_T81'
from thunder import ThunderContext

print 'Starting Thunder Now. Check console for details'
tsc = ThunderContext.start(appName="thunderpca")
import os
filesep = os.path.sep

import time
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

from thunder import KMeans
from thunder import Colorize

from thunder_kmeans_plots import plot_kmeans_maps
from thunder_kmeans import make_kmeans_maps

from kmeans_thunder_analysis import run_kmeans_thunder

#Stimulus_Directories = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f)) and f.find('Figures')<0]
##Stimulus_Directories
#ii = 1
#Trial_Directories = [f for f in os.listdir(os.path.join(Exp_Folder, Stimulus_Directories[ii]))\
#if os.path.isdir(os.path.join(Exp_Folder, Stimulus_Directories[ii], f)) and f.find('Figures')<0]
#Trial_Directories
#jj = 0

stim_start = 10 #Stimulus Starting time point
stim_end = 15 #Stimulus Ending time point

flag = 0

#name_for_saving_figures = Stimulus_Directories[ii] + ' ' + Trial_Directories[jj]        
#Working_Directory = os.path.join(Exp_Folder, Stimulus_Directories[ii], Trial_Directories[jj], 'C=1')+filesep       
#name_for_saving_files = Stimulus_Directories[ii] + '_' + Trial_Directories[jj] + filename_save_prefix+'_individualtrial'

Working_Directory = Exp_Folder
name_for_saving_files = 'All_odors_'+ filename_save_prefix+'_eachodor'
name_for_saving_figures = Working_Directory

data_filtered = tsc.loadSeries(Working_Directory+name_for_saving_files+'_filtered.txt', inputFormat='text', nkeys=3)
data_background = tsc.loadSeries(Working_Directory+name_for_saving_files+'.txt', inputFormat='text', nkeys=3)
data_background.cache()
               
data_filtered.center()
data_filtered.zscore()
data_filtered.cache()


std_map = data_filtered.seriesStdev().pack()

filtered = data_filtered.filterOnValues(lambda x: np.std(x) > np.mean(std_map[1:10,1:10,:])+0.1)
model = KMeans(k=10).fit(data_filtered)

#Kmean labels 
img_labels = model.predict(data_filtered).pack()

#For masking
sim = model.similarity(data_filtered)
img_sim = sim.pack()
img_size_y = np.size(img_sim,2)
img_size_x = np.size(img_sim,1)

brainmap, unique_clrs, newclrs_rgb, newclrs_brewer, matched_pixels, kmeans_clusters_updated = make_kmeans_maps(data_background, model.centers, img_labels, img_sim, img_size_x, img_size_y)
#
stimulus_pulse = 1
#
plot_kmeans_maps(Working_Directory, name_for_saving_figures, name_for_saving_files, \
    model.centers.T, img_sim, img_labels, brainmap, unique_clrs, newclrs_rgb, newclrs_brewer, matched_pixels, stim_start, stim_end, flag,stimulus_pulse)
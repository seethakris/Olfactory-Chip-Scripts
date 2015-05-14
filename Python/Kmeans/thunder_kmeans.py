# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 17:05:40 2015
Run Kmeans and get colormaps
@author: seetha
"""

#Import python libraries
import numpy as np

#Import thunder libraries
from thunder import KMeans
from thunder import Colorize
from copy import copy
import seaborn as sns
from matplotlib.colors import ListedColormap
import palettable

def run_kmeans(data,kmeans_clusters):
    
    ## Find threshold for filtering by finding the standard deviation
#    std_map = data.seriesStdev().pack()
#    max_map = data.seriesMax().pack()

#    filtered = data.filterOnValues(lambda x: np.std(x) > np.mean(std_map[1:10,1:10,:])+0.1)
    model = KMeans(k=kmeans_clusters).fit(data)
    
    #Kmean labels 
    img_labels = model.predict(data).pack()

    #For masking
    sim = model.similarity(data)
    img_sim = sim.pack()
        
    return model, img_sim, img_labels
    
#Make maps and scatter plots of the pca scores with colormaps for plotting 
def make_kmeans_maps(data, kmeans_cluster_centers, img_labels, img_sim, img_size_x, img_size_y,ignore_clusters):
    
    reference = data.seriesMean().pack()
    
    #Only plot those clusters where the standard deviation is greater than 0.1 - thus getting rid of noisy clusters
    
    interesting_clusters = np.array(np.where(np.logical_and(np.std(kmeans_cluster_centers,0)>0.0001,\
    np.max(kmeans_cluster_centers,0)>0.00001)))

    if ignore_clusters !=0:
        for ii in ignore_clusters:
            index = np.where(np.squeeze(interesting_clusters)==ii)[0]
            interesting_clusters = np.delete(interesting_clusters,index)
#    newclrs_rgb, newclrs_brewer = Colorize.optimize(kmeans_cluster_centers.T, asCmap=True)
    
    #Brewer colors
    string_cmap = 'Set1_'+str(np.size(kmeans_cluster_centers,1))
    newclrs_brewer = eval('palettable.colorbrewer.qualitative.' + string_cmap +'.mpl_colors')
    newclrs_brewer = ListedColormap(newclrs_brewer, name='from_list')
    newclrs_updated_brewer =  update_colors(newclrs_brewer, interesting_clusters)
    
    #RGB colors
    newclrs_rgb = ListedColormap(sns.color_palette("bright", np.size(kmeans_cluster_centers,1)), name='from_list')   
    newclrs_updated_rgb =  update_colors(newclrs_rgb, interesting_clusters)
    newclrs_updated_rgb.colors = np.round(newclrs_updated_rgb.colors)
     
    #Update kmeans clusters with those with higher standard deviation
    kmeans_cluster_centers_updated = np.zeros((np.shape(kmeans_cluster_centers)))
    kmeans_cluster_centers_updated[:,interesting_clusters] = kmeans_cluster_centers[:,interesting_clusters]
    
    #Create maps
    brainmap = Colorize(cmap=newclrs_updated_brewer).transform(img_labels, mask=img_sim, background=reference, mixing=1.0)
    brainmap_for_finding_pixels = Colorize(cmap=newclrs_updated_rgb).transform(img_labels, mask=img_sim)

    #Count number of unique colors in the images
    #Get number of planes based on map dimesnions
    if len(brainmap.shape)==3:
        num_planes = 1
    else:
        num_planes = np.size(brainmap,2)
    
    #Get specific color matches across animals and get mean and standard deviation       
    round_clrs= np.round(newclrs_updated_rgb.colors)
    new_array = [tuple(row) for row in round_clrs] 
    unique_clrs = (list(set(new_array)))   #Get unique combination of colors   

    ## remove black color if it exists
    elem = (0,0,0)
    X = unique_clrs.index(elem) if elem in unique_clrs else -1
    if X!=-1:
        unique_clrs.remove(elem)
        unique_clrs = np.round(unique_clrs)

    #From maps get number of pixel matches with color for each plane
    matched_pixels = np.zeros((np.size(unique_clrs,0),num_planes))
#    while sum(matched_pixels) == 0 :
    array_maps = brainmap_for_finding_pixels
    matched_pixels = np.zeros((np.size(unique_clrs,0),num_planes))
    if len(brainmap.shape) == 3:
        array_maps_plane = np.reshape(array_maps, (np.size(array_maps,0)*np.size(array_maps,1),3))
        matched_pixels[:,0] = [np.size(np.where((np.array(np.round(array_maps_plane)) == match).all(axis=1))) for match in unique_clrs]
    else:     
        for ii in xrange(0,num_planes):
            array_maps_plane = np.reshape(array_maps[:,:,ii,:], (np.size(array_maps,0)*np.size(array_maps,1),3))
            matched_pixels[:,ii] = [np.size(np.where((np.array(np.round(array_maps_plane)) == match).all(axis=1))) for match in unique_clrs]


    
    return brainmap, unique_clrs, newclrs_updated_rgb, newclrs_updated_brewer, matched_pixels, kmeans_cluster_centers_updated
    

def update_colors(newclrs, interesting_clusters):
    newclrs_updated = copy(newclrs)
    newclrs_updated.colors = np.zeros(np.shape(newclrs_updated.colors), dtype=np.float64)
    newclrs.colors = np.array(newclrs.colors)
    newclrs_updated.colors[interesting_clusters,:] = newclrs.colors[interesting_clusters,:]
   
    return newclrs_updated


# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 17:05:40 2015
Run ica and get colormaps
@author: seetha
"""

#Import python libraries
import numpy as np
import webcolors

#Import thunder libraries
from thunder import ICA
from thunder import Colorize


def run_ica(data,number_principle_components,ica_components):
    model = ICA(k=number_principle_components,c=ica_components).fit(data)
    imgs = model.sigs.pack()

    return model, imgs
    
#Make maps and scatter plots of the ica scores with colormaps for plotting 
def make_ica_maps(data, imgs, img_size_x, img_size_y, num_ica_colors, color_map, colors_ica):
    
    reference = data.seriesMean().pack()
    maps = Colorize(cmap=color_map, colors = colors_ica[0:np.size(imgs,0)], scale=num_ica_colors).transform(abs(imgs),background=reference, mixing=1.5)
        
    #Count number of unique colors in the images
    #Get number of planes based on map dimesnions
    if len(maps.shape)==3:
        num_planes = 1
    else:
        num_planes = np.size(maps,2)
        
    unique_clrs = []
    for ii in xrange(0, np.size(colors_ica[0:np.size(imgs,0)])):
        unique_clrs.append( np.round(np.array(webcolors.name_to_rgb(colors_ica[ii]), dtype=np.float)/255))
    
    #From maps get number of pixel matches with color for each plane
    matched_pixels = np.zeros((np.size(unique_clrs,0),num_planes))
    array_maps = np.round(maps.astype(np.float16))
    matched_pixels = np.zeros((np.size(unique_clrs,0),num_planes))
    if len(maps.shape) == 3:
        array_maps_plane = np.reshape(array_maps, (np.size(array_maps,0)*np.size(array_maps,1),3))
        matched_pixels[:,0] = [np.size(np.where((np.array(array_maps_plane) == match).all(axis=1))) for match in unique_clrs]
    else:     
        for ii in xrange(0,num_planes):
            array_maps_plane = np.reshape(array_maps[:,:,ii,:], (np.size(array_maps,0)*np.size(array_maps,1),3))
            matched_pixels[:,ii] = [np.size(np.where((np.array(array_maps_plane) == match).all(axis=1))) for match in unique_clrs]
                 
    
    return maps, matched_pixels
    
class structtype():
    pass




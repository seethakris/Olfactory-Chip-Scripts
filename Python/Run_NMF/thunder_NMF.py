# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 17:05:40 2015
Run NMF and get colormaps
@author: seetha
"""

#Import python libraries
from numpy import newaxis, squeeze, size, where, array, mean, zeros, round, reshape, float16, delete
from scipy import stats
from numpy import asarray
import webcolors


#Import thunder libraries
from thunder import NMF
from thunder import Colorize


def run_NMF(data,NMF_components, max_iterations, tolerence_level, Folder):
    model = NMF(k=NMF_components, maxIter=max_iterations, tol=tolerence_level, verbose='True', Working_Directory=Folder).fit(data)
    imgs = model.w.pack()
    

    return model, imgs
    
#Make maps and scatter plots of the NMF scores with colormaps for plotting 
def make_NMF_maps(data, imgs, img_size_x, img_size_y,  num_NMF_colors, color_map, colors_NMF):
    
    reference = data.seriesMean().pack()
    maps = Colorize(cmap=color_map, colors = colors_NMF[0:size(imgs,0)], scale=num_NMF_colors).transform(imgs,background=reference, mixing=0.1)
       
    #Count number of unique colors in the images
    #Get number of planes based on map dimesnions
    if len(maps.shape)==3:
        num_planes = 1
    else:
        num_planes = size(maps,2)
    
    
    unique_clrs = []
    for ii in xrange(0, size(colors_NMF[0:size(imgs,0)])):
        unique_clrs.append( round(array(webcolors.name_to_rgb(colors_NMF[ii]), dtype=float)/255))
        
    #From maps get number of pixel matches with color for each plane
    matched_pixels = zeros((size(unique_clrs,0),num_planes))
    array_maps = round(maps.astype(float16))
    matched_pixels = zeros((size(unique_clrs,0),num_planes))
    if len(maps.shape) == 3:
        array_maps_plane = reshape(array_maps, (size(array_maps,0)*size(array_maps,1),3))
        matched_pixels[:,0] = [size(where((array(array_maps_plane) == match).all(axis=1))) for match in unique_clrs]
    else:     
        for ii in xrange(0,num_planes):
            array_maps_plane = reshape(array_maps[:,:,ii,:], (size(array_maps,0)*size(array_maps,1),3))
            matched_pixels[:,ii] = [size(where((array(array_maps_plane) == match).all(axis=1))) for match in unique_clrs]


    
    return maps, matched_pixels, unique_clrs
class structtype():
    pass




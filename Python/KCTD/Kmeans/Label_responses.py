# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 10:54:33 2015

@author: seetha
"""
import webcolors as wb
import numpy as np 


def create_stats_for_responses(unique_clrs, matched_pixels):
    List_of_colors = (unique_clrs*255).tolist()
    List_of_pixels = matched_pixels.tolist()
    Response_type = ["on","]
#    Response_type = get_user_input_for_color_label(List_of_colors)
    Labels_and_numpixels = zip([wb.rgb_to_name(i) for i in List_of_colors], List_of_pixels) #Combine Number of pixels and List of colors


from Tkinter import *
import tkSimpleDialog

def get_user_input_for_color_label(List_of_colors):
#    root = Tk()
#    w = Label(root, text="Enter type of response for color")
#    w.pack()
    response_type = list()
    for ii in xrange(0, np.size(List_of_colors,0)):
        temp = tkSimpleDialog.askstring("Color", wb.rgb_to_name(List_of_colors[ii]))        
        response_type.append(temp)
        
    return response_type
        

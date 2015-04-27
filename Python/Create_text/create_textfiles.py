# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 15:16:53 2015
Create a variety of text file according to input
@author: chad
"""

#Import relevant libraries
import numpy as np #for numerical operations on arrays
import PIL as pil # for image resizing

import os
filesep = os.path.sep

import matplotlib.pyplot as plt #for plotting
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
from libtiff import TIFF #for reading multiTiffs
from scipy import ndimage

#Custom libraries
from smooth import smooth
smooth_window = 0

def create_textfile_individual(Working_Directory, name_for_saving_files, name_for_saving_figures, \
img_size_x, img_size_y, img_size_crop_x1, img_size_crop_x2, img_size_crop_y1, img_size_crop_y2, stim_start, stim_end, \
time_start,time_end, f_f_flag, dff_start, dff_end, median_filter_threshold, text_file,stimulus_pulse):

    pp = create_pdf(Working_Directory, name_for_saving_files) #To save as pdf
    
    #Send the file paths to get tiff files and convert them to mat and crop or resize appropriately
    [data_mat, data_filtered_mat, num_z_planes] = convert_tiff_to_mat(Working_Directory, img_size_x, img_size_y,\
    img_size_crop_x1, img_size_crop_x2, img_size_crop_y1, img_size_crop_y2, median_filter_threshold, text_file)    
    z_planes = range(1,num_z_planes+1)
    
    #Plot figures
    plot_pdf(data_mat, name_for_saving_figures, pp)    
    plot_pdf(data_filtered_mat, name_for_saving_figures+' Filtered', pp) 
    
    #Create proper matrix for textfile
    numpy_array_for_thunder = get_matrix_for_textfile(data_mat, name_for_saving_figures, z_planes, 0, np.size(data_mat,3) ,\
    f_f_flag, dff_start, dff_end, stim_start, stim_end, smooth_window, pp,stimulus_pulse)
    
    numpy_array_for_thunder_filtered = get_matrix_for_textfile(data_filtered_mat, name_for_saving_figures, z_planes, 0, np.size(data_mat,3) ,\
    f_f_flag, dff_start, dff_end, stim_start, stim_end, smooth_window, pp,stimulus_pulse)
    
    #Save as textfile
    pp.close()        
    print 'Saving all the data in the text file '            
    np.savetxt(Working_Directory+name_for_saving_files+'.txt', numpy_array_for_thunder, fmt='%i')#Save as text file
    np.savetxt(Working_Directory+name_for_saving_files+'_filtered.txt', numpy_array_for_thunder_filtered, fmt='%i')#Save as text file

def create_textfile_eachodor(Working_Directory, name_for_saving_files, name_for_saving_figures, \
img_size_x, img_size_y, img_size_crop_x1, img_size_crop_x2, img_size_crop_y1, img_size_crop_y2, stim_start, stim_end, \
time_start,time_end, f_f_flag, dff_start, dff_end, median_filter_threshold, text_file,stimulus_pulse):
    
    pp = create_pdf(Working_Directory, name_for_saving_files) #To save as pdf
    
    ## Get trial directories and convert to tiff files
    Trial_Directories = [f for f in os.listdir(os.path.join(Working_Directory)) if os.path.isdir(os.path.join(Working_Directory, f)) and f.find('Figures')<0] #Get only directories
    numpy_array_for_thunder = None
    numpy_array_for_thunder_filtered = None
    
    z_planes = [0]
    for jj in xrange(0, np.size(Trial_Directories, axis = 0)):
       
        Working_Directory1 = os.path.join(Working_Directory, Trial_Directories[jj], 'C=1')+filesep        
        ## Check if textfile exists, else create a new one
        name_for_saving_figures1 = name_for_saving_figures + ' ' + Trial_Directories[jj]
        
        #Send the file paths to get tiff files and convert them to mat and crop or resize appropriately
        [data_mat,  data_filtered_mat, num_z_planes] = convert_tiff_to_mat(Working_Directory1, img_size_x, img_size_y,\
        img_size_crop_x1, img_size_crop_x2, img_size_crop_y1, img_size_crop_y2, median_filter_threshold, text_file)    
        print num_z_planes        
        z_planes = range(z_planes[-1]+1,z_planes[-1]+num_z_planes+1)
        
        #Plot figures
        plot_pdf(data_mat, name_for_saving_figures1, pp)    
        plot_pdf(data_filtered_mat, name_for_saving_figures1+' Filtered', pp) 

        #Create proper matrix for textfile
        temp_numpy_array_for_thunder = get_matrix_for_textfile(data_mat, name_for_saving_figures1, z_planes, time_start, time_end, f_f_flag, dff_start, dff_end, stim_start, stim_end, smooth_window, pp,stimulus_pulse)
        temp_numpy_array_for_thunder_filtered = get_matrix_for_textfile(data_filtered_mat, name_for_saving_figures1, z_planes, time_start, time_end, f_f_flag, dff_start, dff_end, stim_start, stim_end, smooth_window, pp,stimulus_pulse)

        
                #Append each tiff files data to a bigger matrix
        if numpy_array_for_thunder is None:
            numpy_array_for_thunder = temp_numpy_array_for_thunder
        else:
            numpy_array_for_thunder = np.append(numpy_array_for_thunder,temp_numpy_array_for_thunder, axis=0)
    
        if numpy_array_for_thunder_filtered is None:
            numpy_array_for_thunder_filtered = temp_numpy_array_for_thunder_filtered
        else:
            numpy_array_for_thunder_filtered = np.append(numpy_array_for_thunder_filtered,temp_numpy_array_for_thunder_filtered, axis=0)
    #Save as textfile
    pp.close()        
    print 'Saving all the data in the text file '
    np.savetxt(Working_Directory+name_for_saving_files+'.txt', numpy_array_for_thunder, fmt='%i')#Save as text file
    np.savetxt(Working_Directory+name_for_saving_files+'_filtered.txt', numpy_array_for_thunder, fmt='%i')#Save as text file


def create_textfile_allodors(Working_Directory, name_for_saving_files, \
img_size_x, img_size_y, img_size_crop_x1, img_size_crop_x2, img_size_crop_y1, img_size_crop_y2, stim_start, stim_end, \
time_start,time_end, f_f_flag, dff_start, dff_end, median_filter_threshold, text_file,stimulus_pulse):
    
    pp = create_pdf(Working_Directory, name_for_saving_files) #To save as pdf
    
    Stimulus_Directories = [f for f in os.listdir(Working_Directory) if os.path.isdir(os.path.join(Working_Directory, f)) and f.find('Figures')<0]
    
    numpy_array_for_thunder = None
    numpy_array_for_thunder_filtered = None

    z_planes = [0]
    
    for ii in xrange(0, np.size(Stimulus_Directories, axis = 0)):
        Trial_Directories = [f for f in os.listdir(os.path.join(Working_Directory, Stimulus_Directories[ii]))\
        if os.path.isdir(os.path.join(Working_Directory, Stimulus_Directories[ii], f)) and f.find('Figures')<0] #Get only directories
        
        for jj in xrange(0, np.size(Trial_Directories, axis = 0)):
            Working_Directory1 = os.path.join(Working_Directory, Stimulus_Directories[ii], Trial_Directories[jj], 'C=1')+filesep        
            name_for_saving_figures1 = Stimulus_Directories[ii] + ' ' + Trial_Directories[jj]
            
            #Send the file paths to get tiff files and convert them to mat and crop or resize appropriately
            [data_mat,data_filtered_mat,num_z_planes] = convert_tiff_to_mat(Working_Directory1, img_size_x, img_size_y,\
            img_size_crop_x1, img_size_crop_x2, img_size_crop_y1, img_size_crop_y2, median_filter_threshold, text_file)    
            z_planes = range(z_planes[-1]+1,z_planes[-1]+num_z_planes+1)
            
            #Plot figures
            plot_pdf(data_mat, name_for_saving_figures1, pp)    
            plot_pdf(data_filtered_mat, name_for_saving_figures1+' Filtered', pp) 

            #Create proper matrix for textfile
            temp_numpy_array_for_thunder = get_matrix_for_textfile(data_mat, name_for_saving_figures1, z_planes, time_start, time_end, f_f_flag, dff_start, dff_end, stim_start, stim_end, smooth_window, pp,stimulus_pulse)
            temp_numpy_array_for_thunder_filtered = get_matrix_for_textfile(data_filtered_mat, name_for_saving_figures1, z_planes, time_start, time_end, f_f_flag, dff_start, dff_end, stim_start, stim_end, smooth_window, pp,stimulus_pulse)

                    #Append each tiff files data to a bigger matrix
            if numpy_array_for_thunder is None:
                numpy_array_for_thunder = temp_numpy_array_for_thunder
            else:
                numpy_array_for_thunder = np.append(numpy_array_for_thunder,temp_numpy_array_for_thunder, axis=0)
            
            if numpy_array_for_thunder_filtered is None:
                numpy_array_for_thunder_filtered = temp_numpy_array_for_thunder_filtered
            else:
                numpy_array_for_thunder_filtered = np.append(numpy_array_for_thunder_filtered,temp_numpy_array_for_thunder_filtered, axis=0)
    #Save as textfile
    pp.close()        
    print 'Saving all the data in the text file '
    np.savetxt(Working_Directory+name_for_saving_files+'.txt', numpy_array_for_thunder, fmt='%i')#Save as text file
    np.savetxt(Working_Directory+name_for_saving_files+'_filtered.txt', numpy_array_for_thunder, fmt='%i')#Save as text file

    
############################ Converts tiff files to numpy arrays and resizes and crops image if required
def convert_tiff_to_mat(Working_Directory, img_size_x, img_size_y, img_size_crop_x1,img_size_crop_x2, img_size_crop_y1, img_size_crop_y2,\
median_filter_threshold, text_file):
    #Get names of all tiff files in the directory
    onlyfiles = [ f for f in os.listdir(Working_Directory)\
    if (os.path.isfile(os.path.join(Working_Directory, f)) and f.find('.tif')>0 and f.find('T=')>=0)]
    
    Working_Directory2 = Working_Directory.replace('/Thresholded_OB','')        
    
    
    for lst in xrange(1,np.size(onlyfiles, axis=0)+1):
        tif1 = TIFF.open(Working_Directory+'T='+str(lst)+'.tif', mode='r') #Open multitiff 
        tif2 = TIFF.open(Working_Directory2+'T='+str(lst)+'.tif', mode='r')   #Open non thresholded image for template
         #Initialize data matrix based on number of planes in the multitiff        
        if lst==1:            
            count_z = 0
            for image in tif1.iter_images():
                count_z = count_z + 1           
            data_filtered = np.zeros((img_size_x-(img_size_crop_x1+img_size_crop_x2), img_size_y-(img_size_crop_y1+img_size_crop_y2), count_z,np.size(onlyfiles,0)), dtype=np.uint8)
            data = np.zeros((img_size_x-(img_size_crop_x1+img_size_crop_x2), img_size_y-(img_size_crop_y1+img_size_crop_y2), count_z,np.size(onlyfiles,0)), dtype=np.uint8)

        
        data_filtered, count_z = get_tif_images_filtered(data_filtered, lst, onlyfiles, text_file, tif1, \
        img_size_x, img_size_y, img_size_crop_x1,img_size_crop_x2, img_size_crop_y1, \
        img_size_crop_y2,median_filter_threshold)
        
        data = get_tif_images_raw(data, lst, onlyfiles, text_file, tif2, \
        img_size_x, img_size_y, img_size_crop_x1,img_size_crop_x2, img_size_crop_y1, \
        img_size_crop_y2)
        
    return data, data_filtered, count_z
     

def get_tif_images_filtered(data_filtered, lst, onlyfiles, text_file, tif, \
img_size_x, img_size_y, img_size_crop_x1,img_size_crop_x2, img_size_crop_y1, \
img_size_crop_y2,median_filter_threshold): 
        
    count_z = 0
    #Store tiff in numpy array data
    for image in tif.iter_images():
        if image.dtype == 'uint16':
            if lst==1 and count_z==0:
                print "Converting to uint8..."
                text_file.write("Converting to uint8...\n")
            image = np.uint8(image/255)
        ##Resizing if required
        if np.size(image,1)!=img_size_y or np.size(image,0)!=img_size_x:
            if lst==1 and count_z==0:
                print "Resizing image..."
                text_file.write("Resizing image...\n")
            temp_image = pil.Image.fromarray(image)
            temp_image1 = np.array(temp_image.resize((img_size_y, img_size_x), pil.Image.NEAREST)) 
            temp_image1.transpose()
        else:
            temp_image1 = image
        
        #Cropping unwanted pixels if required
        if img_size_crop_x1!= 0 and img_size_crop_y1!=0:
            if lst==1 and count_z==0:
                print "Cropping x and y pixels.."
                text_file.write("Cropping x and y pixels.. \n")
            temp_image2 = temp_image1[img_size_crop_x1:-img_size_crop_x2, img_size_crop_y1:-img_size_crop_y2]
        elif img_size_crop_x1!=0 and img_size_crop_y1==0:
            if lst==1 and count_z==0:
                print "Cropping only x pixels.."
                text_file.write("Cropping only x pixels..\n")
            temp_image2 = temp_image1[img_size_crop_x1:-img_size_crop_x2, :]
        elif img_size_crop_x1==0 and img_size_crop_y1!=0:
            if lst==1 and count_z==0:                
                print "Cropping only x pixels.."
                text_file.write("Cropping only x pixels..\n")
            temp_image2 = temp_image1[:, img_size_crop_y1:-img_size_crop_y2]
        else:
            temp_image2 = temp_image1        
        data_filtered[:,:,count_z, lst-1] = ndimage.median_filter(temp_image2, median_filter_threshold)
        
        count_z=count_z+1
        
    return data_filtered, count_z
         
def get_tif_images_raw(data, lst, onlyfiles, text_file, tif, \
img_size_x, img_size_y, img_size_crop_x1,img_size_crop_x2, img_size_crop_y1, \
img_size_crop_y2):
    
        
    count_z = 0
    
    #Store tiff in numpy array data
    for image in tif.iter_images():
        if image.dtype == 'uint16':
            if lst==1 and count_z==0:
                print "Converting to uint8..."
                text_file.write("Converting to uint8...\n")
            image = np.uint8(image/255)
        ##Resizing if required
        if np.size(image,1)!=img_size_y or np.size(image,0)!=img_size_x:
            if lst==1 and count_z==0:
                print "Resizing image..."
                text_file.write("Resizing image...\n")
            temp_image = pil.Image.fromarray(image)
            temp_image1 = np.array(temp_image.resize((img_size_y, img_size_x), pil.Image.NEAREST)) 
            temp_image1.transpose()
        else:
            temp_image1 = image
        
        #Cropping unwanted pixels if required
        if img_size_crop_x1!= 0 and img_size_crop_y1!=0:
            if lst==1 and count_z==0:
                print "Cropping x and y pixels.."
                text_file.write("Cropping x and y pixels.. \n")
            temp_image2 = temp_image1[img_size_crop_x1:-img_size_crop_x2, img_size_crop_y1:-img_size_crop_y2]
        elif img_size_crop_x1!=0 and img_size_crop_y1==0:
            if lst==1 and count_z==0:
                print "Cropping only x pixels.."
                text_file.write("Cropping only x pixels..\n")
            temp_image2 = temp_image1[img_size_crop_x1:-img_size_crop_x2, :]
        elif img_size_crop_x1==0 and img_size_crop_y1!=0:
            if lst==1 and count_z==0:                
                print "Cropping only x pixels.."
                text_file.write("Cropping only x pixels..\n")
            temp_image2 = temp_image1[:, img_size_crop_y1:-img_size_crop_y2]
        else:
            temp_image2 = temp_image1
        
        data[:,:,count_z, lst-1] = temp_image2
        
        count_z=count_z+1
        
    return data
    
### Create backend Pdf pages for saving
def create_pdf(Working_Directory, name_for_saving_files):
    
    filesep = os.path.sep #Get fileseperator according to operating system
    
    # To plot as PDF create directory
    Figure_PDFDirectory = Working_Directory+'Figures'+filesep
    if not os.path.exists(Figure_PDFDirectory):
        os.makedirs(Figure_PDFDirectory) 
    pp = PdfPages(Figure_PDFDirectory+name_for_saving_files+'_CheckRawData.pdf')
    return pp
    
        
        
def plot_pdf(data, name_for_saving_figures, pp):
    #Plot average data over time for reviewingin grayscale      
    with sns.axes_style("white"):
        for ii in xrange(0,np.size(data,2)): 
            fig1 = plt.imshow(np.mean(data[:,:,ii,:], axis=2), cmap='gray')
            plt.title(name_for_saving_figures+' Z='+str(ii+1))
            plt.axis('off')
            fig1 = plt.gcf()
            pp.savefig(fig1)
            plt.close()
            
#Create numpy arrays to save as textfiles 
def get_matrix_for_textfile(data_mat, name_for_saving_files, num_z_planes, time_start,time_end, f_f_flag, dff_start, dff_end, stim_start, stim_end, smooth_window, pp,stimulus_pulse):
    
    #Save as numpy array
    print 'Creating array from stack for ' + name_for_saving_files
    if smooth_window!=0:                
        temp_numpy_array_for_thunder = np.zeros([np.size(data_mat, axis=0)*np.size(data_mat, axis=1)*np.size(data_mat,axis=2),3+(time_end-time_start+1)+smooth_window-2], dtype=np.int)
    else:
        temp_numpy_array_for_thunder = np.zeros([np.size(data_mat, axis=0)*np.size(data_mat, axis=1)*np.size(data_mat,axis=2),3+(time_end-time_start)], dtype=np.int)

    print np.shape(temp_numpy_array_for_thunder)    
    count = 0  
    count1 = 0 
    for zz in xrange(0,np.size(num_z_planes,axis=0)):
        for yy in xrange(0,np.size(data_mat, axis=1)):
            for xx in xrange(0,np.size(data_mat, axis=0)): 
                temp_numpy_array_for_thunder[count,0] = xx+1;
                temp_numpy_array_for_thunder[count,1] = yy+1;
                temp_numpy_array_for_thunder[count,2] = num_z_planes[zz];
                # Create delta f/f values if necessary
                if smooth_window!=0:                
                    if f_f_flag==0:
                        temp_numpy_array_for_thunder[count,3:] = smooth(data_mat[xx,yy,zz,time_start:time_end],smooth_window,'hanning')
                    else:
                        temp_numpy_array_for_thunder[count,3:] = smooth(((data_mat[xx,yy,zz,time_start:time_end]-np.mean(data_mat[xx,yy,zz,dff_start:dff_end]))/np.std(data_mat[xx,yy,zz,dff_start:dff_end])),smooth_window,'hanning')
                else:
                    if f_f_flag==0:
                        temp_numpy_array_for_thunder[count,3:] = data_mat[xx,yy,zz,time_start:time_end]
                    else:
                        temp_numpy_array_for_thunder[count,3:] = ((data_mat[xx,yy,zz,time_start:time_end]-np.mean(data_mat[xx,yy,zz,dff_start:dff_end]))/np.std(data_mat[xx,yy,zz,dff_start:dff_end]))
                count = count+1 
                
        #Plot heatmap for validation    
        with sns.axes_style("white"):
            A = temp_numpy_array_for_thunder[count1:count-1,3:]
            count1 = count-1
            B = np.argsort(np.mean(A, axis=1))  
            C = A[B,:]
            if f_f_flag == 1: #Plot with correct clim if dff is true
                fig2 = plt.imshow(C[-1000:,:],aspect='auto', cmap='jet',vmin=-5, vmax=5)
            else:
                fig2 = plt.imshow(C[-1000:,:],aspect='auto', cmap='jet')
            
            plot_vertical_lines(stim_start,stim_end,stimulus_pulse)
            plt.title(name_for_saving_files +' Z='+ str(zz+1))
            plt.colorbar()
            fig2 = plt.gcf()
            pp.savefig(fig2)
            plt.close()


    return temp_numpy_array_for_thunder
    
def plot_vertical_lines(stim_start,stim_end, stimulus_pulse):
    if stimulus_pulse == 2:
        plt.axvline(x=stim_start, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=stim_end, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=stim_start+18, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=stim_end+18, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=stim_start+37, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=stim_end+37, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=stim_start+56, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=stim_end+56, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=stim_start+74, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=stim_end+74, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=stim_start+92, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=stim_end+92, linestyle='--', color='k', linewidth=1)
    
    elif stimulus_pulse == 1:
        
        plt.axvline(x=stim_start, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=stim_end, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=stim_start+18, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=stim_end+18, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=stim_start+37, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=stim_end+37, linestyle='--', color='k', linewidth=1)
        plt.axvline(x=stim_start+56, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=stim_end+56, linestyle='--', color='k', linewidth=1)

    else:
        plt.axvline(x=stim_start, linestyle='-', color='k', linewidth=1)
        plt.axvline(x=stim_end, linestyle='--', color='k', linewidth=1)
    
        
    
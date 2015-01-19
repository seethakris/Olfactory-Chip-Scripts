function main_function_for_matlabpreprocessing

%% Few preprocessing techniques in Matlab can be run using this script
% 1. Convert nd2 files to tiff using BioFormats reader for Matlab
% 2. Register images
% 3. Sort into stimulus folders for thunderization

Directory_Name = '/media/seetha/Se/Microfluidic Chip_Data/Data/Fish3_7dpf/';

% 1. Convert nd2 files to tiff using BioFormats reader for Matlab
disp('Converting nd2 files to tiff....')
save_nd2files_as_tiff(Directory_Name)

% 2. Register images
disp('Registering images....')
Tiff_Folder = [Directory_Name, 'Tiff/'];
image_register(Tiff_Folder)

% 3. Sort into stimulus folders for thunderization
disp('Sorting sitmulus folders....')
Registered_Folder = [Directory_Name,'Tiff/Registered/'];
transfer_to_individual_stim_folders(Registered_Folder)


 

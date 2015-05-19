function main_function_for_matlabpreprocessing

%% Few preprocessing techniques in Matlab can be run using this script
% 1. Convert nd2 files to tiff using BioFormats reader for Matlab
% 2. Register images
% 3. Sort into stimulus folders for thunderization

%User imput
%Get main directory and sort subfolders by order of fish number
Main_Directory_Name = '~/Desktop/HUC-KR15/';


subfolders = dir(Main_Directory_Name);
subfolders = subfolders([subfolders.isdir]);
foldernames = struct2cell(subfolders);
foldernames = foldernames(1,:);
[sorted_foldernames, ~] = sort(foldernames);


for ii = 11:11%length(sorted_foldernames)
    if  ~strcmpi(sorted_foldernames{ii}, '.') && ~strcmpi(sorted_foldernames{ii}, '..')
        Directory_Name = [Main_Directory_Name, sorted_foldernames{ii}, filesep];
        
        %                 if exist([Directory_Name, 'Tiff', filesep], 'dir')~=7
        
        % 1. Convert nd2 files to tiff using BioFormats reader for Matlab
        disp(['Converting nd2 files to tiff....for ', Directory_Name])
%         save_nd2files_as_tiff(Directory_Name)
        
        %%2. Crop images if user requires
        disp(['Cropping images....for ', Directory_Name,'..Require User Input'])
        Tiff_Folder = [Directory_Name,'Tiff/'];
        crop_pixel_outsideOB(Tiff_Folder)
        
        % 3. Register images
        disp(['Registering images....for ', Directory_Name])
        Cropped_Folder = [Directory_Name, 'Tiff/Cropped/'];
        image_register(Cropped_Folder)
        
        % 4. Threshold OB
        disp(['Sorting sitmulus folders....for ', Directory_Name])
        Registered_Folder = [Directory_Name,'Tiff/Cropped/Registered/'];
        threshold_OB(Registered_Folder)
        
        %5. Sort into stimulus folders for thunderization
        disp(['Sorting sitmulus folders....for ', Directory_Name])
        Thresholded_Folder = [Directory_Name,'Tiff/Cropped/Registered/Thresholded_OB/'];
        transfer_to_individual_stim_folders(Thresholded_Folder,1)
        
        %5. Also sort non thresholded folders.
        disp(['Sorting sitmulus folders....for ', Directory_Name])
        Thresholded_Folder = [Directory_Name,'Tiff/Cropped/Registered/'];
        transfer_to_individual_stim_folders(Thresholded_Folder,2)
        
        
        %         else
        %             continue
        %         end
    end
end



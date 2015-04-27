function transfer_to_individual_stim_folders(Data_Folder, flag)

%% Sort tiff files by name and transfer to folders based on type of stimulus for easy thunderization

%Create a Registered folder to save all registered images
Result_Folder = [Data_Folder, 'Registered_Stimulus'];

if ~isdir(Result_Folder)
    mkdir(Result_Folder)
end

%Find files in the folder and remove those that start with . or are folders
files_present = dir([Data_Folder,filesep, '*.tif']);


%Now register all images using base. Save as multitiff
for ff = 1:length(files_present)
    
    %Find parameters of file from file name
    
    File_string = files_present(ff).name;
    find_underscore = strfind(File_string,'_');
    if flag == 1
        Odor_name = File_string(find_underscore(3)+1:find_underscore(4)-1);
    elseif flag == 2
        Odor_name = File_string(find_underscore(2)+1:find_underscore(3)-1);      
    end
    
    find_trial = strfind(File_string,'Trial');
    find_underscore = strfind(File_string(find_trial+5:end),'_');
    Trial_Number = File_string(find_trial:find_trial+5+find_underscore(1)-2);
    
    find_z = strfind(File_string, 'Z=');
    find_underscore = strfind(File_string(find_z+2:end),'_');
    Z_Plane = File_string(find_z:find_z+2+find_underscore(1)-2);
    
    find_c = strfind(File_string, 'C=');
    C_Channel = File_string(find_c:end-4);
    
    Odor_Folder = [Result_Folder, filesep, Odor_name, filesep, Trial_Number, filesep, C_Channel, filesep];
    
    if ~isdir(Odor_Folder)
        mkdir(Odor_Folder)
    end
    
    disp(['Moving Stimulus...', files_present(ff).name,' To ', Odor_Folder]);
    
    %Find number of time points in image to classify the image as time
    %points
    info = imfinfo([Data_Folder, filesep, files_present(ff).name]);
    num_t = numel(info);
    for tt = 1:num_t
        image = imread([Data_Folder, filesep, files_present(ff).name], tt);
        
        if ~isempty(strfind(Z_Plane, 'Z=1'))
            imwrite(image,[Odor_Folder, filesep,Odor_name(find_z:end-4), 'T=', int2str(tt), '.tif'],'tif');
        else
            imwrite(image,[Odor_Folder, filesep,Odor_name(find_z:end-4), 'T=', int2str(tt), '.tif'],'tif', 'WriteMode', 'append');
        end
    end
end
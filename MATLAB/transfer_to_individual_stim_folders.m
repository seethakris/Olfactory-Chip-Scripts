function transfer_to_individual_stim_folders(Data_Folder)

%% Sort tiff files by name and transfer to folders based on type of stimulus for easy thunderization

%Create a Registered folder to save all registered images
Result_Folder = [Data_Folder, filesep, 'Registered_Stimulus'];

if ~isdir(Result_Folder)
    mkdir(Result_Folder)
end

%Find files in the folder and remove those that start with . or are folders
files_present = dir([Data_Folder,filesep, '*.tif']);


%Now register all images using base. Save as multitiff
for ff = 1:length(files_present)
    
    File_string = files_present(ff).name;
    find_underscore = strfind(File_string,'_');
    Odor_name = File_string(find_underscore(1)+1:find_underscore(2)-1);
    
    Odor_Folder = [Result_Folder, filesep, Odor_name, filesep];
    
    if ~isdir(Odor_Folder)
        mkdir(Odor_Folder)
    end
    
    disp(['Moving Stimulus...', files_present(ff).name,' To ', Odor_Folder]);
    movefile([Data_Folder, files_present(ff).name], Odor_Folder);
end
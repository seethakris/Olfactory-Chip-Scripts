function threshold_OB(Directory_Name)
%% Threshold Olfactory Bulb and remove few pixels along periphery

addpath(genpath('/Users/seetha/Desktop/Olfactory_Chip_Scripts/MATLAB/export_fig/'))

tiff_files = dir([Directory_Name, '*.tif']);

Result_Folder = [Directory_Name, 'Thresholded_OB/'];
if ~isdir(Result_Folder)
    mkdir(Result_Folder)
end


if ~isdir([Result_Folder,'Figures/'])
    mkdir([Result_Folder,'Figures/'])
end

for ii = 1:length(tiff_files)
    
    File_string = tiff_files(ii).name;
    
    find_c = strfind(File_string, 'C=');
    C_Channel = File_string(find_c:end-4);
    
    if strcmp(C_Channel, 'C=1')
        disp(['Thresholding....', File_string]);
        
        info = imfinfo([Directory_Name, filesep, File_string]); %Get image info
        num_t = numel(info);
        
        
        %get all images and get their average
        A1 = load_tiff_images([Directory_Name, filesep, File_string]);
        mean_image_uint16 = mean(A1,3);
        
        image_threshold_slider_min = min(mean_image_uint16(:));
        image_threshold_slider_max = max(mean_image_uint16(:));
        
        offset = load([Directory_Name, 'Offsets/', File_string(12:end-4), '_offset.mat']);
        xoff = max(abs(offset.xoffsets));
        yoff = max(abs(offset.yoffsets));
        
        % If thresholding has already been done, skip GUI
        if ~isfield(offset, 'bw_image')
            waitfor(msgbox(['Xoff: ', int2str(xoff), ' and ', 'Yoff: ', int2str(yoff)], 'Run OB thresholding?'));
            
            [threshold,bw_boundary_original, bw_boundary_adjusted, bw_image] = guide_to_threshold_OB(mean_image_uint16, image_threshold_slider_min, image_threshold_slider_max,...
                xoff, yoff);
            
            save([Directory_Name, 'Offsets/', File_string(12:end-4), '_offset.mat'], 'threshold', 'bw_boundary_original', 'bw_boundary_adjusted', 'bw_image', '-append'); %Save threshold and boundaries
            
        else
            bw_boundary_original = offset.bw_boundary_original;
            bw_boundary_adjusted = offset.bw_boundary_adjusted;
            bw_image = offset.bw_image;
        end
        
        %%Remove pixels where adjustments were made
        boundary_distances = sqrt((bw_boundary_original(:,1)-bw_boundary_adjusted(:,1)).^2 + (bw_boundary_original(:,2)-bw_boundary_adjusted(:,2)).^2);
        ind = find(boundary_distances~=0);
        
        save_images(Result_Folder, File_string, A1, bw_image,bw_boundary_original,bw_boundary_adjusted,ind,num_t)
        %% Save C=2
        %% Check if there exists C=2, save it the same way.
        second_clr_channel = strrep(File_string, 'C=1', 'C=2');
        if exist([Directory_Name, filesep, second_clr_channel])
            A2 = load_tiff_images([Directory_Name, filesep, second_clr_channel]);
            save_images(Result_Folder, File_string, A1, bw_image,bw_boundary_original,bw_boundary_adjusted,ind,num_t)
        end
    end
end
end

function save_images(Result_Folder, File_string, Image, bw_image, bw_boundary_original, bw_boundary_adjusted, ind,num_t)
A1_adjusted = uint16([]);

for tt = 1:num_t
    A1_adjusted(:,:,tt) = Image(:,:,tt);
    A1_adjusted(:,:,tt) = immultiply(A1_adjusted(:,:,tt),bw_image);
    for kk = 1:length(ind)
        A1_adjusted(bw_boundary_original(ind(kk),1):bw_boundary_adjusted(ind(kk),1), bw_boundary_original(ind(kk),2):bw_boundary_adjusted(ind(kk),2),tt) = 0;
    end
    if tt == 1
        imwrite(A1_adjusted(:,:,tt),[Result_Folder, filesep,'OBAdjusted_', File_string],'tif');
    else
        imwrite(A1_adjusted(:,:,tt),[Result_Folder, filesep,'OBAdjusted_', File_string],'tif', 'WriteMode','append');
    end
end

plot_mean_for_verification(Result_Folder, mean(A1_adjusted,3), File_string)
end

function plot_mean_for_verification(Result_Folder, mean_cropped_image, File_string)
fs2 = figure(2);
set(fs2, 'color', 'white')
imshow(mean_cropped_image, [0 10000])
title(File_string, 'Interpreter', 'None')
export_fig(fs2, [Result_Folder, 'Figures/mean_obadjusted_images.pdf'], '-pdf','-append', '-nocrop')
end

function FinalImage = load_tiff_images(FileTif)

InfoImage=imfinfo(FileTif);
mImage=InfoImage(1).Width;
nImage=InfoImage(1).Height;
NumberImages=length(InfoImage);
FinalImage=zeros(nImage,mImage,NumberImages,'uint16');

TifLink = Tiff(FileTif, 'r');
for i=1:NumberImages
    TifLink.setDirectory(i);
    FinalImage(:,:,i)=TifLink.read();
end
TifLink.close();

end
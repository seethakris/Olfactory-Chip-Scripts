function varargout = guide_to_threshold_OB(varargin)
% GUIDE_TO_THRESHOLD_OB MATLAB code for guide_to_threshold_OB.fig
%      GUIDE_TO_THRESHOLD_OB, by itself, creates a new GUIDE_TO_THRESHOLD_OB or raises the existing
%      singleton*.
%
%      H = GUIDE_TO_THRESHOLD_OB returns the handle to a new GUIDE_TO_THRESHOLD_OB or the handle to
%      the existing singleton*.
%
%      GUIDE_TO_THRESHOLD_OB('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in GUIDE_TO_THRESHOLD_OB.M with the given input arguments.
%
%      GUIDE_TO_THRESHOLD_OB('Property','Value',...) creates a new GUIDE_TO_THRESHOLD_OB or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before guide_to_threshold_OB_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to guide_to_threshold_OB_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help guide_to_threshold_OB

% Last Modified by GUIDE v2.5 07-Apr-2015 16:04:23

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
    'gui_Singleton',  gui_Singleton, ...
    'gui_OpeningFcn', @guide_to_threshold_OB_OpeningFcn, ...
    'gui_OutputFcn',  @guide_to_threshold_OB_OutputFcn, ...
    'gui_LayoutFcn',  [] , ...
    'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end


% End initialization code - DO NOT EDIT


% --- Executes just before guide_to_threshold_OB is made visible.
function guide_to_threshold_OB_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to guide_to_threshold_OB (see VARARGIN)



% Set handles
handles.image_threshold_final = 0;
handles.mean_image_uint16 = varargin{1};
handles.image_threshold_slider_min = varargin{2};
handles.image_threshold_slider_max = varargin{3};
handles.xoffset = varargin{4};
handles.yoffset = varargin{5};
handles.boundary_image = 0;
handles.boundary_original = 0;
handles.boundary_adjusted = 0;
handles. bw_image = 0;

set(handles.image_threshold_slider, 'Min', handles.image_threshold_slider_min);
set(handles.image_threshold_slider, 'Max', handles.image_threshold_slider_max);
set(handles.image_threshold_slider, 'Value', (handles.image_threshold_slider_min+ handles.image_threshold_slider_max)/2);
set(handles.image_threshold_slider, 'SliderStep', [0.01,0.001]);
set(handles.text_slider, 'String', (handles.image_threshold_slider_min+ handles.image_threshold_slider_max)/2);
set(handles.figure1,'CloseRequestFcn',@close_gui_Callback);

%Draw mean OB image
axes(handles.image_plot);
imshow(handles.mean_image_uint16, [handles.image_threshold_slider_min, (handles.image_threshold_slider_min+ handles.image_threshold_slider_max)/2]);


% Update handles structure
guidata(hObject, handles);


% UIWAIT makes guide_to_threshold_OB wait for user response (see UIRESUME)
uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = guide_to_threshold_OB_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.image_threshold_final;
varargout{2} = handles.boundary_original ;
varargout{3} = handles.boundary_adjusted;
varargout{4} = handles. bw_image;
delete(handles.figure1)



% --- Executes on slider movement.
function image_threshold_slider_Callback(hObject, eventdata, handles)
% hObject    handle to image_threshold_slider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
set(handles.text_slider, 'String', get(hObject,'Value'));

mean_image = handles.mean_image_uint16;
bw_image = mean_image>get(hObject,'Value');

handles.bw_image = bw_image;

axes(handles.image_plot);
imshow(bw_image)

% Update handles structure
guidata(hObject, handles);


% --- Executes during object creation, after setting all properties.
function image_threshold_slider_CreateFcn(hObject, eventdata, handles)
% hObject    handle to image_threshold_slider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end



% --- Executes on button press in convert_to_peremeter.
function convert_to_peremeter_Callback(hObject, eventdata, handles)
% hObject    handle to convert_to_peremeter (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
%% Get connected components. Remove those that are small in size and draw outline
BW = handles.bw_image;
CC = bwconncomp(BW);
numPixels = cellfun(@numel,CC.PixelIdxList);
[idx] = find(numPixels<10000);
for ii = 1:length(idx)
    BW(CC.PixelIdxList{idx(ii)})=0;
end

axes(handles.image_plot);
imshow(BW)
hold on

%Get boundary
B = bwboundaries(BW,'noholes');
%get largest boundary
if length(B)>1
    for k = 1:length(B)
        size_k(k) = size(B{k},1);
    end
    [~,idx] = max(size_k);
else
    idx = 1;
end

%Plot boundary
boundary = B{idx};
plot(boundary(:,2), boundary(:,1), 'b', 'LineWidth', 2)


%edit boundaries so you dont have any interior boundaries
A = boundary(:,1);
idx = find(A<size(BW,1)-5);
boundary1 = boundary(idx, :);
count = 1;
idx1 = [];
for ii = 1:length(boundary1)
    if (boundary1(ii,1)<100 || (boundary1(ii,2)<100 || boundary1(ii,2)>300))==1
        idx1(count) = ii;
        count = count+1;
    end
end
boundary2 = boundary1(idx1,:);

%Differentiate top, left nd right boundaries and plot
boundary_regions = zeros(length(boundary2),1);
boundary_adjusted = boundary2;

for ii = 1:length(boundary2)
    [~,idx]  = min([pdist2(boundary2(ii,:), [1,boundary2(ii,2)]),...
        pdist2(boundary2(ii,:), [boundary2(ii,1),1]),...
        pdist2(boundary2(ii,:), [boundary2(ii,1),size(BW,2)])]); %[top,left, right]
    
    switch idx
        
        case 1
            boundary_regions(ii) = 1;
            boundary_adjusted(ii,1) = boundary2(ii,1) + handles.yoffset;
            plot(boundary2(ii,2), boundary2(ii,1), 'm*', 'MarkerSize', 3)
        case 2
            boundary_regions(ii) = 2;
            boundary_adjusted(ii,2) = boundary2(ii,2) + handles.xoffset;
            
            plot(boundary2(ii,2), boundary2(ii,1), 'y*', 'MarkerSize', 3)
            
        case 3
            boundary_regions(ii) = 3;
            boundary_adjusted(ii,2) = boundary2(ii,2) - handles.xoffset;            
            plot(boundary2(ii,2), boundary2(ii,1), 'r*', 'MarkerSize', 3)
    end
end

% %Remove pixels where adjustments were made
% BW_adjusted = BW;
% boundary_distances = sqrt((boundary2(:,1)-boundary_adjusted(:,1)).^2 + (boundary2(:,2)-boundary_adjusted(:,2)).^2);
% ind = find(boundary_distances~=0);
% for ii = 1:length(ind)
%     BW_adjusted(boundary2(ind(ii),1):boundary_adjusted(ind(ii),1), boundary2(ind(ii),2):boundary_adjusted(ind(ii),2)) = 0;
% end

plot(boundary_adjusted(:,2), boundary_adjusted(:,1), 'g', 'LineWidth', 2)

handles.boundary_original = boundary2;
handles.boundary_adjusted = boundary_adjusted;
handles. bw_image = BW;

% Update handles structure
guidata(hObject, handles);

% --- Executes on button press in reset.
function reset_Callback(hObject, eventdata, handles)
% hObject    handle to reset (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
set(handles.image_threshold_slider, 'Min', handles.image_threshold_slider_min);
set(handles.image_threshold_slider, 'Max', handles.image_threshold_slider_max);
set(handles.image_threshold_slider, 'Value', (handles.image_threshold_slider_min+ handles.image_threshold_slider_max)/2);
set(handles.image_threshold_slider, 'SliderStep', [0.01,0.01]);
set(handles.text_slider, 'String', (handles.image_threshold_slider_min+ handles.image_threshold_slider_max)/2);

axes(handles.image_plot);
imshow(handles.mean_image_uint16, [handles.image_threshold_slider_min, (handles.image_threshold_slider_min+ handles.image_threshold_slider_max)/2]);


function text_slider_Callback(hObject, eventdata, handles)
% hObject    handle to yoffset (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of yoffset as text
%        str2double(get(hObject,'String')) returns contents of yoffset as a double
set(handles.image_threshold_slider, 'Value', str2double(get(handles.text_slider,'String')));

mean_image = handles.mean_image_uint16;
bw_image = mean_image>str2double(get(handles.text_slider,'String'));

handles.bw_image = bw_image;

axes(handles.image_plot);
imshow(bw_image)

% Update handles structure
guidata(hObject, handles);


% --- Executes on button press in close_gui.
function close_gui_Callback(hObject, eventdata, handles)
% hObject    handle to close_gui (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
selection = questdlg(['Would you like to use the following threshold? ', int2str(get(handles.image_threshold_slider,'Value'))],...
    'Close Request Function',...
    'Yes','No','Yes');
switch selection,
    case 'Yes',
        handles.image_threshold_final = get(handles.image_threshold_slider,'Value');
        uiresume(handles.figure1);
        guidata(hObject, handles);
    case 'No'
        return
end


% --- Executes during object creation, after setting all properties.
function text_slider_CreateFcn(hObject, eventdata, handles)
% hObject    handle to text_slider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

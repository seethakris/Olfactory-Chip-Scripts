count = 0
for ii = 1:length(boundary1)
    if boundary1(ii,1)<100
        if (boundary1(ii,2)<100 && boundary(ii,2)>300)
            idx1(count) = ii;
            count = count+1;
        end
    end
end




A = boundary(:,1);
idx = find(A<200);
boundary1 = boundary(idx, :);
count = 1;
idx1 = [];
for ii = 1:length(boundary1)
    if (boundary1(ii,1)<100 || (boundary1(ii,2)<100 || boundary1(ii,2)>300))==1
        idx1(count) = ii;
        count = count+1;
    end
end
for ii = 1:length(boundary2)
    plot(boundary2(ii,2), boundary2(ii,1), 'y*', 'LineWidth', 2)
end

figure; imshow(BW2)
hold on
boundary_regions = zeros(length(boundary2),1);
for ii = 1:length(boundary2)
    [~,idx]  = min([pdist2(boundary2(ii,:), [1,boundary2(ii,2)]),...
        pdist2(boundary2(ii,:), [boundary2(ii,1),1]),...
        pdist2(boundary2(ii,:), [boundary2(ii,1),size(BW,2)])]); %[top,left, right]

    switch idx
        case 1
            boundary_regions(ii) = 1;
            plot(boundary2(ii,2), boundary2(ii,1), 'm*')
        case 2
            boundary_regions(ii) = 2;
            plot(boundary2(ii,2), boundary2(ii,1), 'y*')
            
        case 3
            boundary_regions(ii) = 3;
            plot(boundary2(ii,2), boundary2(ii,1), 'r*')            
    end
end


A = sqrt((boundary2(:,1)-boundary_adjusted(:,1)).^2 + (boundary2(:,2)-boundary_adjusted(:,2)).^2);

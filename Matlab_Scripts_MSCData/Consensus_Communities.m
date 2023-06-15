function Con_D=Consensus_Communities(sub_networks)
%sub_networks must be in the workspace from Create_Parcellated_Connectomes.m
% Create consensus communities from Lancichetti et al. method

% order the networks from 1 to 1000 ascending
for rows=1:10
    for cols=2:5
        networks_sorted{rows,cols}=sortrows(sub_networks{rows,cols},1);
    end
end

% combine all thresholds for each subject
% columns 1 to 4 correspond to 2%, 3%, 4%, 5% thresholds and rows to parcels 1 to 1000
for subjects=1:10
    combined_networks{subjects}=[networks_sorted{subjects,2}(:,2) networks_sorted{subjects,3}(:,2) networks_sorted{subjects,4}(:,2) networks_sorted{subjects,5}(:,2)];
end

% preallocate consensus D matrix for speed
for subs=1:10
    Con_D{subs}=diag(ones(1000,1));
end

% for each parcel row how many times does it agree with thresholded columns
% Create consensus D matrix for each subject
tic
[r,c]=size(combined_networks{1});
count=0;
for subs=1:10
    for row=1:r
        for rows=1:r
            for column=1:c
                if combined_networks{subs}(row,column) == combined_networks{subs}(rows,column)
                    count=count+1;
                end
            end
            Con_D{subs}(row,rows)=count/4;
            count=0;
        end
    end
end
toc
%usually 10 seconds

% % threshold Consensus Matrix with anything below 0.25 and set to 0
for subs=1:10
    Con_D{subs}(Con_D{subs}<0.25)=0;
    Con_D{subs}=triu(Con_D{subs},1);
    con_indices{subs}=find(Con_D{subs});
end

% save consensus matrices as pajek file in order to run Infomap
for subs=1:10
    mat2pajek_byindex(Con_D{subs},con_indices{subs},sprintf('/Volumes/LaCie/consensus_matrices/Sub%d_Allthresh_ConsensusD',subs));
end




% %% Thresholds 2-10%
% 
% % order the networks from 1 to 1000 ascending
% for rows=1:10
%     for cols=1:9
%         networks_sorted{rows,cols}=sortrows(sub_networks{rows,cols},1);
%     end
% end
% 
% % combine all thresholds for each subject
% % columns 1 to 4 correspond to 2%, 3%, 4%, 5% thresholds and rows to parcels 1 to 1000
% for subjects=1:10
%     combined_networks{subjects}=[networks_sorted{subjects,1}(:,2) networks_sorted{subjects,2}(:,2) networks_sorted{subjects,3}(:,2) networks_sorted{subjects,4}(:,2) networks_sorted{subjects,5}(:,2) networks_sorted{subjects,6}(:,2) networks_sorted{subjects,7}(:,2) networks_sorted{subjects,8}(:,2) networks_sorted{subjects,9}(:,2)];
% end
% 
% % preallocate consensus D matrix for speed
% for subs=1:10
%     Con_D{subs}=diag(ones(1000,1));
% end
% 
% % for each parcel row how many times does it agree with thresholded columns
% % Create consensus D matrix for each subject
% tic
% [r,c]=size(combined_networks{1});
% count=0;
% for subs=1:10
%     for row=1:r
%         for rows=1:r
%             for column=1:c
%                 if combined_networks{subs}(row,column) == combined_networks{subs}(rows,column)
%                     count=count+1;
%                 end
%             end
%             Con_D{subs}(row,rows)=count/9;
%             count=0;
%         end
%     end
% end
% toc
% %usually 10 seconds
% 
% % % threshold Consensus Matrix with anything below 0.25 and set to 0
% for subs=1:10
%     Con_D{subs}(Con_D{subs}<0.25)=0;
%     Con_D{subs}=triu(Con_D{subs},1);
%     con_indices{subs}=find(Con_D{subs});
% end
% 
% % save consensus matrices as pajek file in order to run Infomap
% for subs=1:10
%     mat2pajek_byindex(Con_D{subs},con_indices{subs},sprintf('/Users/shefalirai/Desktop/consensus_matrices/Sub%d_2to10Thresh_ConsensusD',subs));
% end







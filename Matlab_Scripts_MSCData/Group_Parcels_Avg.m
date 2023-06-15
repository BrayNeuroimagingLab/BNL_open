%% Group Averaged
%Combine all sessions into 1 after running Create_Connectomes.m
for sub=1:10
    sub_alltimeseries{1,sub} = horzcat(task_meancent{1,sub}{1,1}, task_meancent{1,sub}{2,1}, task_meancent{1,sub}{3,1}, task_meancent{1,sub}{4,1}, task_meancent{1,sub}{5,1}, task_meancent{1,sub}{6,1}, task_meancent{1,sub}{7,1}, task_meancent{1,sub}{8,1}, task_meancent{1,sub}{9,1}, task_meancent{1,sub}{10,1});
end

%Exclude Subject MSC08 by excluding sub_alltimeseries{1,8} below
Z = zeros(91282,1705,9);
Z(:,1:width(sub_alltimeseries{1,1}),1) = sub_alltimeseries{1,1};
Z(:,1:width(sub_alltimeseries{1,2}),2) = sub_alltimeseries{1,2};
Z(:,1:width(sub_alltimeseries{1,3}),3) = sub_alltimeseries{1,3};
Z(:,1:width(sub_alltimeseries{1,4}),4) = sub_alltimeseries{1,4};
Z(:,1:width(sub_alltimeseries{1,5}),5) = sub_alltimeseries{1,5};
Z(:,1:width(sub_alltimeseries{1,6}),6) = sub_alltimeseries{1,6};
Z(:,1:width(sub_alltimeseries{1,7}),7) = sub_alltimeseries{1,7};
Z(:,1:width(sub_alltimeseries{1,8}),8) = sub_alltimeseries{1,8};
Z(:,1:width(sub_alltimeseries{1,9}),9) = sub_alltimeseries{1,9};
Z(:,1:width(sub_alltimeseries{1,10}),10) = sub_alltimeseries{1,10};
avg_sub_alltimeseries=mean(Z,3);

%Open ciftis and replace with sub_alltimeseries cdata
avgsub_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
avgsub_cifti.cdata=avg_sub_alltimeseries;

%Parcellate all sessions for each subject
ciftisavereset(avgsub_cifti,'/Volumes/LaCie/parcelled_subjects/AvgSubs_alltimeseries.dtseries.nii' , '/Applications/workbench/bin_macosx64/wb_command');
inputFile='/Volumes/LaCie/parcelled_subjects/AvgSubs_alltimeseries.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/parcelled_subjects/AvgSubs_1000parc_17nets.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
avgsub_parcelled=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
avgsub_parcelled=avgsub_parcelled.cdata;

%Create connectomes for parcellated Subject
avgsub_parcel_connectome=corr(avgsub_parcelled');
avgsub_parcel_connectome(isnan(avgsub_parcel_connectome))=0;


% Threshold 2%
thresh2percent_indices=matrix_thresholder_simple(avgsub_parcel_connectome, 0.02);
mat2pajek_byindex(avgsub_parcel_connectome,thresh2percent_indices,'/Volumes/LaCie/thresholded_connectomes/AvgSub_thresh2_1000parc_17nets_new');

% Threshold 3%
thresh3percent_indices=matrix_thresholder_simple(avgsub_parcel_connectome, 0.03);
mat2pajek_byindex(avgsub_parcel_connectome,thresh3percent_indices,'/Volumes/LaCie/thresholded_connectomes/AvgSub_thresh3_1000parc_17nets_new');


% Threshold 4%
thresh4percent_indices=matrix_thresholder_simple(avgsub_parcel_connectome, 0.04);
mat2pajek_byindex(avgsub_parcel_connectome,thresh4percent_indices,'/Volumes/LaCie/thresholded_connectomes/AvgSub_thresh4_1000parc_17nets_new');


% Threshold 5%
thresh5percent_indices=matrix_thresholder_simple(avgsub_parcel_connectome, 0.05);
mat2pajek_byindex(avgsub_parcel_connectome,thresh5percent_indices,'/Volumes/LaCie/thresholded_connectomes/AvgSub_thresh5_1000parc_17nets_new');

% Infomap run from Gordon paper: [infomapfolder '/Infomap-0.15.7/Infomap --clu -2 -N' num2str(reps) ' ' pajekfilename ' ' pathstr]);

% Thresholds 2-5% and run Infomap to create networks for each subject
for thresholds=2:5
        pajekfilename=sprintf('/Volumes/LaCie/thresholded_connectomes/AvgSub_thresh%g_1000parc_17nets_new',thresholds);
        pathstr='/Users/shefalirai/Desktop/Infomap_Out';
        reps=1000; 
        infomapfolder='/Users/shefalirai/Desktop/infomap-1.2.1';
        system([infomapfolder '/Infomap --clu -2 -N' num2str(reps) ' ' pajekfilename ' ' pathstr]); % not using -s random seed since it gives different results everytime 
end

% After running Infomap, open .clu network file for each subject across each threshold
for thresholds=2:5
        fid=fopen(sprintf('/Users/shefalirai/Desktop/Infomap_Out/AvgSub_thresh%g_1000parc_17nets_new.clu', thresholds));
        avgsub_networks{thresholds}= cell2mat(textscan(fid,'%f %f %f', 'headerlines', 9, 'delimiter', ' ')); 
        fclose(fid);
end


% order the networks from 1 to 1000 ascending
for cols=2:5
        avgnetworks_sorted{cols}=sortrows(avgsub_networks{cols},1);
end

% combine all thresholds for each subject
% columns 1 to 4 correspond to 2%, 3%, 4%, 5% thresholds and rows to parcels 1 to 1000
combined_avgnetworks=[avgnetworks_sorted{2}(:,2) avgnetworks_sorted{3}(:,2) avgnetworks_sorted{4}(:,2) avgnetworks_sorted{5}(:,2)];


% preallocate consensus D matrix for speed
Con_D=diag(ones(1000,1));


% for each parcel row how many times does it agree with thresholded columns
% Create consensus D matrix for each subject
tic
[r,c]=size(combined_avgnetworks);
count=0;
for row=1:r
        for rows=1:r
            for column=1:c
                if combined_avgnetworks(row,column) == combined_avgnetworks(rows,column)
                    count=count+1;
                end
            end
            Con_D(row,rows)=count/4;
            count=0;
        end
end
toc
%usually 10 seconds

% % threshold Consensus Matrix with anything below 0.25 and set to 0
Con_D(Con_D<0.25)=0;
Con_D=triu(Con_D,1);
con_avgindices=find(Con_D);


% save consensus matrices as pajek file in order to run Infomap
mat2pajek_byindex(Con_D,con_avgindices,'/Volumes/LaCie/consensus_matrices/AvgSubs_Allthresh_ConsensusD_new');


% Run Infomap on consensus matrix for each subject
pajekfilename='/Volumes/LaCie/consensus_matrices/AvgSubs_Allthresh_ConsensusD_new';
pathstr='/Volumes/LaCie/consensus_matrices';
reps=1000;
infomapfolder='/Users/shefalirai/Desktop/infomap-1.2.1';  
system([infomapfolder '/Infomap --clu -2 -N' num2str(reps) ' ' pajekfilename ' ' pathstr]);

% After running Infomap, open .clu network file for each subject across each threshold
fid=fopen('/Volumes/LaCie/consensus_matrices/AvgSubs_Allthresh_ConsensusD_new.clu');
avgsub_consensus_networks= cell2mat(textscan(fid,'%f %f %f', 'headerlines', 9, 'delimiter', ' '));
fclose(fid);

% Keep track of ambigious/changed parcels adjusted to fit 17 networks
[rows, columns] = find(avgsub_consensus_networks(:,2) > 17);
ambig_avgnetworks=avgsub_consensus_networks(rows,:);  

%Manually changed parcels belonging to network 18 to 2 and network 19 to 3

% visualize on the surface
avgconsensus_allthresh=ciftiopen('/Volumes/LaCie/parcelled_subjects/AvgSubs_1000parc_17nets.ptseries.nii', '/Applications/workbench/bin_macosx64/wb_command');
avgsub_consensus_networks=sortrows(avgsub_consensus_networks,1);
avgconsensus_allthresh.cdata=avgsub_consensus_networks(:,2);
ciftisavereset(avgconsensus_allthresh,'/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL_New2023.pscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');
























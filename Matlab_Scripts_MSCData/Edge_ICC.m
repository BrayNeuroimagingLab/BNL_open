%% Parcel wise ICC
% After running Create_Connectomes.m use this script
% First create firsthalf and lasthalf parcellated connectomes
% Load('allsessions_allsubjects_meancent.mat') from file or create
% meancentered variable

%combine all sessions into 1 matrix for each subject
for subjects=1:10
    sub_firsthalf_timeseries{subjects}=[allsessions_allsubjects_meancent{1,subjects}{1,1} allsessions_allsubjects_meancent{1,subjects}{2,1} allsessions_allsubjects_meancent{1,subjects}{3,1} allsessions_allsubjects_meancent{1,subjects}{4,1} allsessions_allsubjects_meancent{1,subjects}{5,1}];
    sub_lasthalf_timeseries{subjects}=[allsessions_allsubjects_meancent{1,subjects}{6,1} allsessions_allsubjects_meancent{1,subjects}{7,1} allsessions_allsubjects_meancent{1,subjects}{8,1} allsessions_allsubjects_meancent{1,subjects}{9,1} allsessions_allsubjects_meancent{1,subjects}{10,1}];
end

% Open ciftis and replace with firsthalf cdata
for subjects=1:10
    if subjects==10
        sub_firsthalf_cifti{subjects}=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC%d/sub-MSC%d/MNINonLinear/Results/task-rest_ses-func01_smoothed_midrefvolume/task-rest_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',subjects, subjects)),'/Applications/workbench/bin_macosx64/wb_command');
        sub_firsthalf_cifti{subjects}.cdata=sub_firsthalf_timeseries{subjects};
    else
        sub_firsthalf_cifti{subjects}=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC0%d/sub-MSC0%d/MNINonLinear/Results/task-rest_ses-func01_smoothed_midrefvolume/task-rest_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',subjects, subjects)),'/Applications/workbench/bin_macosx64/wb_command');
        sub_firsthalf_cifti{subjects}.cdata=sub_firsthalf_timeseries{subjects};
    end
end

% Open ciftis and replace with lasthalf cdata
for subjects=1:10
    if subjects==10
        sub_lasthalf_cifti{subjects}=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC%d/sub-MSC%d/MNINonLinear/Results/task-rest_ses-func01_smoothed_midrefvolume/task-rest_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',subjects, subjects)),'/Applications/workbench/bin_macosx64/wb_command');
        sub_lasthalf_cifti{subjects}.cdata=sub_lasthalf_timeseries{subjects};
    else
        sub_lasthalf_cifti{subjects}=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC0%d/sub-MSC0%d/MNINonLinear/Results/task-rest_ses-func01_smoothed_midrefvolume/task-rest_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',subjects, subjects)),'/Applications/workbench/bin_macosx64/wb_command');
        sub_lasthalf_cifti{subjects}.cdata=sub_lasthalf_timeseries{subjects};
    end
end


% Parcellate firsthalf for each subject
tic
for subjects=1:10
    ciftisavereset(sub_firsthalf_cifti{subjects},sprintf('/Volumes/LaCie/parcelled_subjects/sub%d_firsthalf_timeseries.dtseries.nii',subjects) , '/Applications/workbench/bin_macosx64/wb_command');
    inputFile=sprintf('/Volumes/LaCie/parcelled_subjects/sub%d_firsthalf_timeseries.dtseries.nii',subjects);
    parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
    parcelFile=sprintf('/Volumes/LaCie/parcelled_subjects/sub%d_firsthalf_1000parc17nets.ptseries.nii', subjects); 
    eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
    sub_firsthalf_parcelled{subjects}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
    sub_firsthalf_parcelled{subjects}=sub_firsthalf_parcelled{subjects}.cdata;
end
toc
% usually 112 seconds

% Parcellate lasthalf for each subject
tic
for subjects=1:10
    ciftisavereset(sub_lasthalf_cifti{subjects},sprintf('/Volumes/LaCie/parcelled_subjects/sub%d_lasthalf_timeseries.dtseries.nii',subjects) , '/Applications/workbench/bin_macosx64/wb_command');
    inputFile=sprintf('/Volumes/LaCie/parcelled_subjects/sub%d_lasthalf_timeseries.dtseries.nii',subjects);
    parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
    parcelFile=sprintf('/Volumes/LaCie/parcelled_subjects/sub%d_lasthalf_1000parc17nets.ptseries.nii', subjects); 
    eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
    sub_lasthalf_parcelled{subjects}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
    sub_lasthalf_parcelled{subjects}=sub_lasthalf_parcelled{subjects}.cdata;
end
toc
% usually 113 seconds

% Create connectomes for firsthalf parcellated Subject
for subjects=1:10
    sub_firsthalf_parcel_connectome{subjects}=corr(sub_firsthalf_parcelled{subjects}');
    sub_firsthalf_parcel_connectome{subjects}(isnan(sub_firsthalf_parcel_connectome{subjects}))=0;
end

% Create connectomes for lasthalf parcellated Subject
for subjects=1:10
    sub_lasthalf_parcel_connectome{subjects}=corr(sub_lasthalf_parcelled{subjects}');
    sub_lasthalf_parcel_connectome{subjects}(isnan(sub_lasthalf_parcel_connectome{subjects}))=0;
end

% Fischer transform the connectomes 
for subjects=1:10
    sub_firsthalf_parcel_connectome_Z{subjects}=atanh(sub_firsthalf_parcel_connectome{subjects});
    sub_lasthalf_parcel_connectome_Z{subjects}=atanh(sub_lasthalf_parcel_connectome{subjects});
end


% Create ICC input matrix, row is each subject and each column is the
% measure or firsthalf column 1 and lasthalf column 2
allsubs_ICC_matrix=[sub_firsthalf_parcel_connectome; sub_lasthalf_parcel_connectome]';

% Uses ICC.m matlab file to run ICC
tic
for r=1:1000
    for c=1:1000
        ICCM{r,c}=[allsubs_ICC_matrix{1,1}(r,c) allsubs_ICC_matrix{1,2}(r,c); allsubs_ICC_matrix{2,1}(r,c) allsubs_ICC_matrix{2,2}(r,c); allsubs_ICC_matrix{3,1}(r,c) allsubs_ICC_matrix{3,2}(r,c); allsubs_ICC_matrix{4,1}(r,c) allsubs_ICC_matrix{4,2}(r,c); allsubs_ICC_matrix{5,1}(r,c) allsubs_ICC_matrix{5,2}(r,c); allsubs_ICC_matrix{6,1}(r,c) allsubs_ICC_matrix{6,2}(r,c); allsubs_ICC_matrix{7,1}(r,c) allsubs_ICC_matrix{7,2}(r,c); allsubs_ICC_matrix{8,1}(r,c) allsubs_ICC_matrix{8,2}(r,c); allsubs_ICC_matrix{9,1}(r,c) allsubs_ICC_matrix{9,2}(r,c); allsubs_ICC_matrix{10,1}(r,c) allsubs_ICC_matrix{10,2}(r,c)];
        ICC21_FinalRC{r,c}=f_ICC(ICCM{r,c},0.05); %Using f_ICC.m file to calculate ICC(2,1) and ICC(3,1) absolute and consistency
    end
end
toc
% 634 seconds

for num=1:1000
    for nums =1:1000
    ICC21_RC(num,nums)=ICC21_FinalRC{num,nums}{1,2}.est;
    ICC21_Rms(num,nums)=ICC21_FinalRC{num,nums}{1,2}.rms;
    ICC21_Cms(num,nums)=ICC21_FinalRC{num,nums}{1,2}.cms;
%     ICC31_Final(num,nums)=ICC21_Final{num,nums}{1,3}.est;
    end
end


% Save ICC21 and ICC31 for each edge as a variable
save('ICC21_Final_ForEachEdge.mat','ICC21_Final');
save('ICC31_Final_ForEachEdge.mat','ICC31_Final');
save('ICC21.mat','ICC21_RC');
save('ICC21_RMS.mat','ICC21_Rms');
save('ICC21_CMS.mat','ICC21_Cms');

imagesc(ICC21_Rms);

% thresholding for only high ICC values (greater than 0.8)
ICC21_RC(isnan(ICC21_RC))=0;
% ICC31_Final(isnan(ICC31_Final))=0;
% ICC21_Final=triu(ICC21_Final,1);
% ICC21_indices=find(ICC21_Final);
% imagesc(ICC21_Final);

Parcel_ICC21Mean=mean(ICC21_RC,2);

% %convert 1000x1000 matrix as a pajek file
% mat2pajek_byindex(ICC21_Final,ICC21_indices,'/Volumes/LaCie/consensus_surface/ICC21_Final');

% Mapping ICC averages for each parcel on the surface 
AvgSub=ciftiopen('/Volumes/LaCie/parcelled_subjects/AvgSubs_1000parc_17nets.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub.cdata=Parcel_ICC21Mean;

ciftisavereset(AvgSub,'/Volumes/LaCie/AvgSub_ICC21.ptseries.nii' , '/Applications/workbench/bin_macosx64/wb_command');

% Mapping ICC averages for each network on the surface
AvgSub_Networks=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Networks=AvgSub_Networks.cdata;


Parcel_ICC21Mean(:,2)=AvgSub_Networks(:,1);


for num=1:17
    Parcel_ICC21Mean(Parcel_ICC21Mean(:,2)==num,3)=mean(Parcel_ICC21Mean((Parcel_ICC21Mean(:,2)==num),1));
end

AvgSub=ciftiopen('/Volumes/LaCie/parcelled_subjects/AvgSubs_1000parc_17nets.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub.cdata=Parcel_ICC21Mean(:,3);

ciftisavereset(AvgSub,'/Volumes/LaCie/AvgSub_ICC21Networks.ptseries.nii' , '/Applications/workbench/bin_macosx64/wb_command');
    





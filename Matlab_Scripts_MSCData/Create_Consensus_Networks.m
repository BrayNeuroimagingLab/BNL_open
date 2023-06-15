function [sub_parcel_connectome, sub_networks]=Create_Consensus_Networks(task_meancent, task)
%After running Create_Connectomes.m use this script
%task_meancent must be in the workspace for all runs
%task must be a string as written in the Ciftify folder i.e. 'rest'

%combine all sessions into 1 matrix for each subject
for subjects=1:10
    sub_alltimeseries{subjects}=[task_meancent{1,subjects}{1,1} task_meancent{1,subjects}{2,1} task_meancent{1,subjects}{3,1} task_meancent{1,subjects}{4,1} task_meancent{1,subjects}{5,1} task_meancent{1,subjects}{6,1} task_meancent{1,subjects}{7,1} task_meancent{1,subjects}{8,1} task_meancent{1,subjects}{9,1} task_meancent{1,subjects}{10,1}];
end

%Open ciftis and replace with sub_alltimeseries cdata
for subjects=1:10
    if subjects==10
        try
            sub_cifti{subjects}=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC%d/sub-MSC%d/MNINonLinear/Results/task-%s_ses-func01_smoothed_midrefvolume/task-%s_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',subjects, subjects,task,task)),'/Applications/workbench/bin_macosx64/wb_command');
            sub_cifti{subjects}.cdata=sub_alltimeseries{subjects};
        catch
            fprintf('error\n');
        end
    else
        try
            sub_cifti{subjects}=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC0%d/sub-MSC0%d/MNINonLinear/Results/task-%s_ses-func01_smoothed_midrefvolume/task-%s_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',subjects, subjects, task, task)),'/Applications/workbench/bin_macosx64/wb_command');
            sub_cifti{subjects}.cdata=sub_alltimeseries{subjects};
        catch
            fprintf('error\n');
        end
    end
end

%Parcellate all sessions for each subject
for subjects=1:10
    ciftisavereset(sub_cifti{subjects},sprintf('/Volumes/LaCie/parcelled_subjects/sub%d_alltimeseries.dtseries.nii',subjects) , '/Applications/workbench/bin_macosx64/wb_command');
    inputFile=sprintf('/Volumes/LaCie/parcelled_subjects/sub%d_alltimeseries.dtseries.nii',subjects);
    parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
    parcelFile=sprintf('/Volumes/LaCie/parcelled_subjects/sub%d_1000parc_17nets.ptseries.nii', subjects); 
    eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
    sub_parcelled{subjects}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
    sub_parcelled{subjects}=sub_parcelled{subjects}.cdata;
end
%usually 205 seconds

%Create connectomes for parcellated Subject
for subjects=1:10
    sub_parcel_connectome{subjects}=corr(sub_parcelled{subjects}');
    sub_parcel_connectome{subjects}(isnan(sub_parcel_connectome{subjects}))=0;
end


% Threshold Connectomes from top 2-5%
count=0;
for thresh=0.02:0.01:0.05
    threshold=2+count;
    for subjects=1:10
            thresh_indices{subjects}=matrix_thresholder_simple(sub_parcel_connectome{subjects}, thresh);
            mat2pajek_byindex(sub_parcel_connectome{subjects},thresh_indices{subjects},sprintf('/Volumes/LaCie/thresholded_connectomes/Sub%d_thresh%g_1000parc_17nets',subjects,threshold));
    end
    count=count+1;
end


% Run Infomap & Consensus Networks
% Infomap run from Gordon paper: [infomapfolder '/Infomap-0.15.7/Infomap --clu -2 -N' num2str(reps) ' ' pajekfilename ' ' pathstr]);

% Thresholds 2-5% and run Infomap to create networks for each subject
for thresholds=2:5
    for subjects=1:10
        pajekfilename=sprintf('/Volumes/LaCie/thresholded_connectomes/Sub%d_thresh%g_1000parc_17nets',subjects,thresholds);
        pathstr='/Users/shefalirai/Desktop/Infomap_Out';
        reps=1000; 
        infomapfolder='/Users/shefalirai/Desktop/infomap-1.2.1';
        system([infomapfolder '/Infomap --clu -2 -N' num2str(reps) ' ' pajekfilename ' ' pathstr]); % not using -s random seed since it gives different results everytime 
    end
end

% After running Infomap, open .clu network file for each subject across each threshold
for thresholds=2:5
    for subjects=1:10
        fid=fopen(sprintf('/Users/shefalirai/Desktop/Infomap_Out/Sub%d_thresh%g_1000parc_17nets.clu',subjects, thresholds));
        sub_networks{subjects,thresholds}= cell2mat(textscan(fid,'%f %f %f', 'headerlines', 9, 'delimiter', ' ')); 
        fclose(fid);
    end
end


   
    
    


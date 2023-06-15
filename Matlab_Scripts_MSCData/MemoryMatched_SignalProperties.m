%% Rest Signal Property Values

% %% REST_Motor_matched_all10subs %%
%  
% %STEP 1 open rest timeseries%%
%Run Open_CiftiTimeseries_REST.m

allsessions_allsubjects_rest=Open_CiftiTimeseries_REST('rest');

% %STEP 2%
rest_rm=Remove_Motion('msc_rest', allsessions_allsubjects_rest);
% 

rest_rm_mc=MeanCenter_Timeseries(rest_rm);

% %already calculated min size and minidx for all 10 subjects
minidx=[9,9,8,3,8,7,8,6,2,7]; 
minsize=[182,166,157,173,156,169,121,169,102,168];
% 
%  %STEP 3
for ses=1:10
    for sub=1:10
        rest_matched_mc{1,sub}{ses,1}=rest_rm_mc{1,sub}{ses,1}(:,1:minsize(ses));
    end
end

for ses=1:10
    for sub=1:10
        rest_matched_nomc{1,sub}{ses,1}=rest_rm{1,sub}{ses,1}(:,1:minsize(ses));
    end
end

%NOW ADD EMPTY COLUMN 8 !
rest_matched_mc{1,8}=[];
rest_matched_nomc{1,8}=[];

[Rest_Mean_Sub]=MeanSignal_Values_Jan2023(rest_matched_nomc);
[Rest_SD_Sub]=SD_Values_Jan2023(rest_matched_mc);
[Rest_tSNR_Sub]=tSNR_Values_Jan2023(Rest_Mean_Sub, Rest_SD_Sub);


% Save Avg_tSNR as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Rest_tSNR_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Rest_tSNR_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save Avg_SD as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Rest_SD_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Rest_SD_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save Avg_MeanSignal as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Rest_Mean_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Rest_MeanSignal_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

%parcellate TSNR
inputFile='/Users/shefalirai/Desktop/Rest_tSNR_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Rest_tSNR_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Rest_tSNR_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Rest_tSNR_Parc=Rest_tSNR_Parc.cdata;

%parcellate SD
inputFile='/Users/shefalirai/Desktop/Rest_SD_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Rest_SD_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Rest_SD_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Rest_SD_Parc=Rest_SD_Parc.cdata;

%parcellate MS
inputFile='/Users/shefalirai/Desktop/Rest_MeanSignal_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Rest_MeanSignal_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Rest_MeanSignal_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Rest_MeanSignal_Parc=Rest_MeanSignal_Parc.cdata;


%% Memory Signal Property Values NO REGRESSION

%STEP 1 open rest timeseries%%
allsessions_allsubjects_memorywords=Open_CiftiTimeseries('memorywords');
% 
% STEP 2%
words_rm=Remove_Motion('msc_memorywords', allsessions_allsubjects_memorywords);
%

%STEP 1 open rest timeseries%%
allsessions_allsubjects_memoryfaces=Open_CiftiTimeseries('memoryfaces');
% 
% STEP 2%
faces_rm=Remove_Motion('msc_memoryfaces', allsessions_allsubjects_memoryfaces);
%

%STEP 1 open rest timeseries%%
allsessions_allsubjects_memoryscenes=Open_CiftiTimeseries('memoryscenes');
% 
% STEP 2%
scenes_rm=Remove_Motion('msc_memoryscenes', allsessions_allsubjects_memoryscenes);


words_rm_mc=MeanCenter_Timeseries(words_rm);
scenes_rm_mc=MeanCenter_Timeseries(scenes_rm);
faces_rm_mc=MeanCenter_Timeseries(faces_rm);

% %already calculated min size and minidx for all 10 subjects
minidx=[9,9,8,3,8,7,8,6,2,7]; 
minsize=[182,166,157,173,156,169,121,169,102,168];
% 

%Do Steps 1-2 above first then the following
for j=1:10 %ses
    for k=1:10 %sub
        try
            memory_nomc{1,k}{j,1} = [words_rm{1,k}{j,1} scenes_rm{1,k}{j,1} faces_rm{1,k}{j,1}];
        catch
            fprintf('error\n')
        end
    end
end

%Do Steps 1-2 above first then the following
for j=1:10 %ses
    for k=1:10 %sub
        try
            memory_mc{1,k}{j,1} = [words_rm_mc{1,k}{j,1} scenes_rm_mc{1,k}{j,1} faces_rm_mc{1,k}{j,1}];
        catch
            fprintf('error\n')
        end
    end
end

%NOW ADD EMPTY COLUMN 8 !
memory_mc{1,8}=[];
memory_nomc{1,8}=[];

%  %STEP 3
for ses=1:10
    for sub=1:10
        try
            memory_matched_mc{1,sub}{ses,1}=memory_mc{1,sub}{ses,1}(:,1:minsize(ses));
        catch
            fprintf('error\n')
        end
    end
end

for ses=1:10
    for sub=1:10
        try
            memory_matched_nomc{1,sub}{ses,1}=memory_nomc{1,sub}{ses,1}(:,1:minsize(ses));
        catch
            fprintf('error\n')
        end
    end
end

[Memory_Mean_Sub]=MeanSignal_Values_Jan2023(memory_matched_nomc);
[Memory_SD_Sub]=SD_Values_Jan2023(memory_matched_mc);
[Memory_tSNR_Sub]=tSNR_Values_Jan2023(Memory_Mean_Sub, Memory_SD_Sub);

% Save tSNR as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Memory_tSNR_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Memory_tSNR_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save SD as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Memory_SD_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Memory_SD_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save MeanSignal as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Memory_Mean_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Memory_MeanSignal_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

%parcellate TSNR
inputFile='/Users/shefalirai/Desktop/Memory_tSNR_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Memory_tSNR_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Memory_tSNR_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Memory_tSNR_Parc=Memory_tSNR_Parc.cdata;

%parcellate SD
inputFile='/Users/shefalirai/Desktop/Memory_SD_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Memory_SD_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Memory_SD_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Memory_SD_Parc=Memory_SD_Parc.cdata;

%parcellate MS
inputFile='/Users/shefalirai/Desktop/Memory_MeanSignal_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Memory_MeanSignal_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Memory_MeanSignal_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Memory_MeanSignal_Parc=Memory_MeanSignal_Parc.cdata;




%% MEMORY - REST

%Open rest signal property files
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_MeanSignal_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_Mean_Sub=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_SD_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_SD_Sub=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_tSNR_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_tSNR_Sub=Avg_cifti.cdata;

Relative_Memory_Mean=Memory_Mean_Sub-Rest_Mean_Sub;
Relative_Memory_tSNR=Memory_tSNR_Sub-Rest_tSNR_Sub;
Relative_Memory_SD=Memory_SD_Sub-Rest_SD_Sub;

% Save Avg_tSNR as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Relative_Memory_tSNR;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/MemoryRelative_tSNR_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save Avg_SD as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Relative_Memory_SD;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/MemoryRelative_SD_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save Avg_MeanSignal as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Relative_Memory_Mean;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/MemoryRelative_MeanSignal_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

%parcellate TSNR
inputFile='/Users/shefalirai/Desktop/MemoryRelative_tSNR_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/MemoryRelative_tSNR_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
MemoryRelative_tSNR_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
MemoryRelative_tSNR_Parc=MemoryRelative_tSNR_Parc.cdata;

%parcellate SD
inputFile='/Users/shefalirai/Desktop/MemoryRelative_SD_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/MemoryRelative_SD_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
MemoryRelative_SD_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
MemoryRelative_SD_Parc=MemoryRelative_SD_Parc.cdata;

%parcellate MS
inputFile='/Users/shefalirai/Desktop/MemoryRelative_MeanSignal_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/MemoryRelative_MeanSignal_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
MemoryRelative_MeanSignal_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
MemoryRelative_MeanSignal_Parc=MemoryRelative_MeanSignal_Parc.cdata;

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
MemoryRelative_SD_Parc(:,2)=AvgSub_NETS;


%% Memory signal vs reli

% Save tSNR as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Memory_tSNR_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Memory_tSNR_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save SD as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Memory_SD_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Memory_SD_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save MeanSignal as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Memory_Mean_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Memory_MeanSignal_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

%parcellate TSNR
inputFile='/Users/shefalirai/Desktop/Memory_tSNR_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Memory_tSNR_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Memory_tSNR_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Memory_tSNR_Parc=Memory_tSNR_Parc.cdata;

%parcellate SD
inputFile='/Users/shefalirai/Desktop/Memory_SD_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Memory_SD_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Memory_SD_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Memory_SD_Parc=Memory_SD_Parc.cdata;

%parcellate MS
inputFile='/Users/shefalirai/Desktop/Memory_MeanSignal_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Memory_MeanSignal_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Memory_MeanSignal_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Memory_MeanSignal_Parc=Memory_MeanSignal_Parc.cdata;

%% Memory Signal Property Values Regressed

%STEP 1 open rest timeseries%%
allsessions_allsubjects_memorywords=Open_CiftiTimeseries_Regressed('memorywords');
% 
% STEP 2%
words_rm=Remove_Motion('msc_memorywords', allsessions_allsubjects_memorywords);
%

%STEP 1 open rest timeseries%%
allsessions_allsubjects_memoryfaces=Open_CiftiTimeseries_Regressed('memoryfaces');
% 
% STEP 2%
faces_rm=Remove_Motion('msc_memoryfaces', allsessions_allsubjects_memoryfaces);
%

%STEP 1 open rest timeseries%%
allsessions_allsubjects_memoryscenes=Open_CiftiTimeseries_Regressed('memoryscenes');
% 
% STEP 2%
scenes_rm=Remove_Motion('msc_memoryscenes', allsessions_allsubjects_memoryscenes);
%

%Do Steps 1-2 above first then the following
for j=1:10 %ses
    for k=1:10 %sub
        try
        allsessions_allsubjects_memory{1,k}{j,1} = [words_rm{1,k}{j,1} faces_rm{1,k}{j,1} scenes_rm{1,k}{j,1}];
        catch
            fprintf('error\n')
        end
    end
end


%%already calculated min size and minidx
minidx=[9,9,8,3,8,7,8,6,2,7]; 
minsize=[182,166,157,173,156,169,121,169,102,168];

%NOW ADD EMPTY COLUMN 8 TO MOTORS_MC!
allsessions_allsubjects_memory{1,8}=[];

%motor match according to a subject's lowest motor volume for that session
for ses=1:10
    for sub=1:10
        try
            memory_matched{1,sub}{ses,1}=allsessions_allsubjects_memory{1,sub}{ses,1}(:,1:minsize(ses));
        catch
        fprintf('error\n')
        end
    end
end

[Memory_Mean_Sub]=MeanSignal_Values_Jan2023(memory_matched);
[Memory_SD_Sub]=SD_Values_Jan2023(memory_matched);
[Memory_tSNR_Sub]=tSNR_Values_Jan2023(Memory_Mean_Sub, Memory_SD_Sub);

% Save tSNR as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Memory_tSNR_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Memory_tSNR_motormatched_noMSC08_regressed.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save SD as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Memory_SD_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Memory_SD_motormatched_noMSC08_regressed.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save MeanSignal as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Memory_Mean_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Memory_MeanSignal_motormatched_noMSC08_regressed.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

%parcellate TSNR
inputFile='/Users/shefalirai/Desktop/Memory_tSNR_motormatched_noMSC08_regressed.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Memory_tSNR_motormatched_noMSC08_regressed_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Memory_tSNR_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Memory_tSNR_Parc=Memory_tSNR_Parc.cdata;

%parcellate SD
inputFile='/Users/shefalirai/Desktop/Memory_SD_motormatched_noMSC08_regressed.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Memory_SD_motormatched_noMSC08_regressed_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Memory_SD_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Memory_SD_Parc=Memory_SD_Parc.cdata;

%parcellate MS
inputFile='/Users/shefalirai/Desktop/Memory_MeanSignal_motormatched_noMSC08_regressed.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Memory_MeanSignal_motormatched_regressed_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Memory_MeanSignal_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Memory_MeanSignal_Parc=Memory_MeanSignal_Parc.cdata;


%% Memory - REST TASK REGRESSED

% open files if needed
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Memory_MeanSignal_motormatched_noMSC08_regressed.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_Mean_regressed=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Memory_tSNR_motormatched_noMSC08_regressed.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_tSNR_regressed=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Memory_SD_motormatched_noMSC08_regressed.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_SD_regressed=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_MeanSignal_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_Mean_Sub=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_tSNR_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_tSNR_Sub=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_SD_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_SD_Sub=Avg_cifti.cdata;
 

Relative_Memory_Mean_regressed=Memory_Mean_regressed-Rest_Mean_Sub;
Relative_Memory_tSNR_regressed=Memory_tSNR_regressed-Rest_tSNR_Sub;
Relative_Memory_SD_regressed=Memory_SD_regressed-Rest_SD_Sub;

% Save Avg_tSNR as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Relative_Memory_tSNR_regressed;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/MemoryRelative_tSNR_motormatched_noMSC08_regressed.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save Avg_SD as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Relative_Memory_SD_regressed;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/MemoryRelative_SD_motormatched_noMSC08_regressed.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save Avg_MeanSignal as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Relative_Memory_Mean_regressed;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/MemoryRelative_MeanSignal_motormatched_noMSC08_regressed.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% open files if needed
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Memory_MeanSignal_motormatched_regressed_noMSC08_1000parc.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_Mean_regressed=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Memory_tSNR_motormatched_noMSC08_regressed_1000parc.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_tSNR_regressed=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Memory_SD_motormatched_noMSC08_regressed_1000parc.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_SD_regressed=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Volumes/LaCie/Memory_matched_REGRESSED_9subs/AvgSub_Reli_Memory_Reg_1000parc.pscalar.nii ','/Applications/workbench/bin_macosx64/wb_command');
Memory_Reli_Regressed=Avg_cifti.cdata;

% open files if needed
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Memory_MeanSignal_motormatched_regressed_noMSC08_1000parc.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_Mean=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Memory_tSNR_motormatched_noMSC08_regressed_1000parc.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_tSNR=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Memory_SD_motormatched_noMSC08_regressed_1000parc.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_SD=Avg_cifti.cdata;

%Parcellate relative signal properties
%parcellate TSNR
inputFile='/Users/shefalirai/Desktop/MemoryRelative_tSNR_motormatched_noMSC08_regressed.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/MemoryRelative_tSNR_motormatched_noMSC08_regressed_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
MemoryRelative_tSNR_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
MemoryRelative_tSNR_Parc=MemoryRelative_tSNR_Parc.cdata;

%parcellate SD
inputFile='/Users/shefalirai/Desktop/MemoryRelative_SD_motormatched_noMSC08_regressed.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/MemoryRelative_SD_motormatched_noMSC08_regressed_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
MemoryRelative_SD_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
MemoryRelative_SD_Parc=MemoryRelative_SD_Parc.cdata;

%parcellate MS
inputFile='/Users/shefalirai/Desktop/MemoryRelative_MeanSignal_motormatched_noMSC08_regressed.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/MemoryRelative_MeanSignal_motormatched_noMSC08_regressed_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
MemoryRelative_MeanSignal_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
MemoryRelative_MeanSignal_Parc=MemoryRelative_MeanSignal_Parc.cdata;

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
MemoryRelative_SD_Parc(:,2)=AvgSub_NETS;


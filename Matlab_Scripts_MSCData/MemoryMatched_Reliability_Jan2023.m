%% MEMORY ONLY 9 MSC SUBJECTS_MotorMatched No regression

%STEP 1 open rest timeseries%%
allsessions_allsubjects_faces=Open_CiftiTimeseries('memoryfaces');
% 
% STEP 2%
memoryfaces_rm=Remove_Motion('msc_memoryfaces', allsessions_allsubjects_faces);
%

%STEP 1 open rest timeseries%%
allsessions_allsubjects_scenes=Open_CiftiTimeseries('memoryscenes');
% 
% STEP 2%
memoryscenes_rm=Remove_Motion('msc_memoryscenes', allsessions_allsubjects_scenes);
%

%STEP 1 open rest timeseries%%
allsessions_allsubjects_words=Open_CiftiTimeseries('memorywords');
% 
% STEP 2%
memorywords_rm=Remove_Motion('msc_memorywords', allsessions_allsubjects_words);
%


%Do Steps 1-2 above first then the following
faces_mc=MeanCenter_Timeseries(memoryfaces_rm);
scenes_mc=MeanCenter_Timeseries(memoryscenes_rm);
words_mc=MeanCenter_Timeseries(memorywords_rm);

for j=1:10 %ses
    for k=1:10 %sub
        try
        allmemory_mc{1,k}{j,1} = [faces_mc{1,k}{j,1} scenes_mc{1,k}{j,1} words_mc{1,k}{j,1}];
        catch
            fprintf('error\n')
        end
    end
end


%%already calculated min size and minidx
minidx=[9,9,8,3,8,7,8,6,2,7]; 
minsize=[182,166,157,173,156,169,121,169,102,168];

%NOW ADD EMPTY COLUMN 8!
allmemory_mc{1,8}=[];

%motor match according to a subject's lowest motor volume for that session
for ses=1:10
    for sub=1:10
        try
            allmemory_matched{1,sub}{ses,1}=allmemory_mc{1,sub}{ses,1}(:,1:minsize(ses));
        catch
        fprintf('error\n')
        end
    end
end

%%STEP 4%%
[memory_firsthalf_matched, memory_lasthalf_matched, memory_mc]=Concatenate_Connectomes(allmemory_matched);


%%STEP7%%
%Now we run Connectome_Corr.m for subjects
for sub=1:10
    try
        memory_corr=Connectome_Corr(memory_firsthalf_matched{sub}, memory_lasthalf_matched{sub}, sub, 'memoryfaces','memory');
    catch
        fprintf('error\n')
    end
end

%%STEP 8%%
%average the reliabilities
for sub=1:10
    try
        memory_matched_cifti{sub}=ciftiopen(sprintf('/Volumes/LaCie/Memory_matched_noregression_9subs/Sub%d_memory_FirstLast_Corr.dscalar.nii', sub),'/Applications/workbench/bin_macosx64/wb_command');
        memory_matched_cifti{sub}=memory_matched_cifti{sub}.cdata;
    catch
        fprintf('error\n')
    end
end

AvgSub_Reli_Memory=(memory_matched_cifti{1}+memory_matched_cifti{2}+ memory_matched_cifti{3}+ memory_matched_cifti{4}+ memory_matched_cifti{5}+ memory_matched_cifti{6}+ memory_matched_cifti{7}+memory_matched_cifti{9}+memory_matched_cifti{10})/9;

%Open subject's original cifti
subject_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');

% Replace original .cdata with correlated data
subject_cifti.cdata=AvgSub_Reli_Memory;
ciftisavereset(subject_cifti, '/Users/shefalirai/Desktop/AvgSub_Reli_Memory.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');

%MotorReliability parcellated
inputFile='/Users/shefalirai/Desktop/AvgSub_Reli_Memory.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/AvgSub_Reli_Memory_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Avg_ReliParc_MemoryMatched=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_ReliParc_MemoryMatched=Avg_ReliParc_MemoryMatched.cdata;

%Open memory reliability 
File='/Volumes/LaCie/Memory_matched_noregression_9subs/AvgSub_Reli_Memory_1000parc.pscalar.nii'; 
AvgSub_Reli_Memory_Parc=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Memory_Parc=AvgSub_Reli_Memory_Parc.cdata;


%% REST ONLY 9 MSC SUBJECTS_MotorMatched

%Already calculated from MotorMatched_Reliability_Nov2022.m file


%% Relative reliability between Memory and Rest both motor matched and only 9 subjects NO REGRESSION

%Open Rest reliability first
File='/Volumes/LaCie/REST_Motor_matched_9subs/AvgSub_Reli_Rest.dscalar.nii'; 
AvgSub_Reli_Rest=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Rest=AvgSub_Reli_Rest.cdata;

%Open Rest reliability first
File='/Volumes/LaCie/REST_Motor_matched_9subs/AvgSub_Reli_Rest_1000parc.pscalar.nii'; 
AvgSub_Reli_Rest_Parc=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Rest_Parc=AvgSub_Reli_Rest_Parc.cdata;

%Open memory reliability first
File='/Volumes/LaCie/Memory_matched_noregression_9subs/AvgSub_Reli_Memory.dscalar.nii'; 
AvgSub_Reli_Memory=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Memory=AvgSub_Reli_Memory.cdata;

%Absolute reliability difference between memory and rest 
Absolute_MemoryReli=AvgSub_Reli_Memory-AvgSub_Reli_Rest;

%Open subject's original cifti
subject_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');

% Replace original .cdata with correlated data
subject_cifti.cdata=Absolute_MemoryReli;
ciftisavereset(subject_cifti, '/Users/shefalirai/Desktop/AvgSub_Relative_MemoryReli.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');

%Relative Reliability parcellated
inputFile='/Users/shefalirai/Desktop/AvgSub_Relative_MemoryReli.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/AvgSub_Relative_MemoryReli_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Avg_ReliParc_MemoryMatched=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_ReliParc_MemoryMatched=Avg_ReliParc_MemoryMatched.cdata;


%% MEMORY ONLY 9 MSC SUBJECTS_MotorMatched WITH TASK REGRESSION

%STEP 1 open rest timeseries%%
%Run Open_CiftiTimeseries_Regressed.m
memoryfaces_reg=Open_CiftiTimeseries_Regressed('memoryfaces');
memoryscenes_reg=Open_CiftiTimeseries_Regressed('memoryscenes');
memorywords_reg=Open_CiftiTimeseries_Regressed('memorywords');

%STEP 2%
memoryfaces_reg_rm=Remove_Motion('msc_memoryfaces', memoryfaces_reg);
memoryscenes_reg_rm=Remove_Motion('msc_memoryscenes', memoryscenes_reg);
memorywords_reg_rm=Remove_Motion('msc_memorywords', memorywords_reg);

%Mean center separately
memoryfaces_reg_rm_mc=MeanCenter_Timeseries(memoryfaces_reg_rm);
memoryscenes_reg_rm_mc=MeanCenter_Timeseries(memoryscenes_reg_rm);
memorywords_reg_rm_mc=MeanCenter_Timeseries(memorywords_reg_rm);

for j=1:10 %ses
    for k=1:10 %sub
        try
        allmemory_reg_rm_mc{1,k}{j,1} = [memoryfaces_reg_rm_mc{1,k}{j,1} memoryscenes_reg_rm_mc{1,k}{j,1} memorywords_reg_rm_mc{1,k}{j,1}];
        catch
            fprintf('error\n')
        end
    end
end

%NOW ADD EMPTY COLUMN 8 TO MOTORS_REG_RM_MC! 
%To exclue MSC08
allmemory_reg_rm_mc{1,8}=[];

%minimum size per session for motor
% [minsize, minidx] = min(cellfun('size', motors_reg_rm_mc', 2));
%%already calculated min size and minidx for 9 subjects 
minidx=[9,9,8,3,8,7,8,6,2,7]; 
minsize=[182,166,157,173,156,169,121,169,102,168];


%motor match according to a subject's lowest motor volume for that session
for ses=1:10
    for sub=1:10
        try
            allmemory_matched_reg{1,sub}{ses,1}=allmemory_reg_rm_mc{1,sub}{ses,1}(:,1:minsize(ses));
        catch
        fprintf('error\n')
        end
    end
end

%%STEP 4%%
[memory_reg_firsthalf_matched, memory_reg_lasthalf_matched, memory_reg_mc]=Concatenate_Connectomes(allmemory_matched_reg);


%%STEP7%%
%Now we run Connectome_Corr.m for subjects
for sub=1:10
    try
        memory_reg_corr=Connectome_Corr(memory_reg_firsthalf_matched{sub}, memory_reg_lasthalf_matched{sub}, sub, 'memoryfaces','memory');
    catch
        fprintf('error\n')
    end
end

%%STEP 8%%
%avergae the memory reliabilities
for sub=1:10
    try
        memory_reg_matched_cifti{sub}=ciftiopen(sprintf('/Users/shefalirai/Desktop/Sub%d_memory_FirstLast_Corr.dscalar.nii', sub),'/Applications/workbench/bin_macosx64/wb_command');
        memory_reg_matched_cifti{sub}=memory_reg_matched_cifti{sub}.cdata;
    catch
        fprintf('error\n')
    end
end

AvgSub_Reli_Memory_Reg=(memory_reg_matched_cifti{1}+memory_reg_matched_cifti{2}+ memory_reg_matched_cifti{3}+ memory_reg_matched_cifti{4}+ memory_reg_matched_cifti{5}+ memory_reg_matched_cifti{6}+ memory_reg_matched_cifti{7}+memory_reg_matched_cifti{9}+memory_reg_matched_cifti{10})/9;

%Open subject's original cifti
subject_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');

% Replace original .cdata with correlated data
subject_cifti.cdata=AvgSub_Reli_Memory_Reg;
ciftisavereset(subject_cifti, '/Users/shefalirai/Desktop/AvgSub_Reli_Memory_Reg.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');

%MotorReliability parcellated
inputFile='/Users/shefalirai/Desktop/AvgSub_Reli_Memory_Reg.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/AvgSub_Reli_Memory_Reg_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Avg_ReliParc_MemoryMatched_Reg=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_ReliParc_MemoryMatched_Reg=Avg_ReliParc_MemoryMatched_Reg.cdata;

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
Avg_ReliParc_MemoryMatched_Reg(:,2)=AvgSub_NETS;

parcelFile='/Volumes/LaCie/Memory_matched_REGRESSED_9subs/AvgSub_Reli_Memory_Reg_1000parc.pscalar.nii'; 
Avg_ReliParc_MemoryMatched=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_ReliParc_MemoryMatched=Avg_ReliParc_MemoryMatched.cdata;
Avg_ReliParc_MemoryMatched(:,2)=AvgSub_NETS;

%% Relative reliability between Memory and Rest both motor matched and only 9 subjects WITH REGRESSION

%Open Rest reliability first
File='/Volumes/LaCie/REST_Motor_matched_9subs/AvgSub_Reli_Rest.dscalar.nii'; 
AvgSub_Reli_Rest=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Rest=AvgSub_Reli_Rest.cdata;

%Open memory reliability first
File='/Volumes/LaCie/Memory_matched_REGRESSED_9subs/AvgSub_Reli_Memory_Reg.dscalar.nii'; 
AvgSub_Reli_Memory_Reg=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Memory_Reg=AvgSub_Reli_Memory_Reg.cdata;

%Calculate difference between memory and rest 
Relative_MemoryReli_Reg=AvgSub_Reli_Memory_Reg-AvgSub_Reli_Rest;

%Open subject's original cifti
subject_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');

% Replace original .cdata with correlated data
subject_cifti.cdata=Relative_MemoryReli_Reg;
ciftisavereset(subject_cifti, '/Users/shefalirai/Desktop/AvgSub_Relative_MemoryReli_Reg.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');

%Relative Reliability parcellated
inputFile='/Users/shefalirai/Desktop/AvgSub_Relative_MemoryReli_Reg.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/AvgSub_Relative_MemoryReli_Reg_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Avg_ReliParc_MemoryMatched_Reg=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_ReliParc_MemoryMatched_Reg=Avg_ReliParc_MemoryMatched_Reg.cdata;

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
Avg_ReliParc_MemoryMatched_Reg(:,2)=AvgSub_NETS;

%% Open parcelled files

%Open Rest reliability first
File='/Volumes/LaCie/REST_Motor_matched_9subs/AvgSub_Reli_Rest_1000parc.pscalar.nii'; 
AvgSub_Reli_Rest=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Rest=AvgSub_Reli_Rest.cdata;

File='/Volumes/LaCie/REST_Motor_matched_9subs/AvgSub_Reli_Rest.dscalar.nii'; 
AvgSub_Reli_Rest=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Rest=AvgSub_Reli_Rest.cdata;

%Open memory reliability first
File='/Volumes/LaCie/Memory_matched_REGRESSED_9subs/AvgSub_Reli_Memory_Reg_1000parc.pscalar.nii'; 
AvgSub_Reli_Memory_Reg=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Memory_Reg=AvgSub_Reli_Memory_Reg.cdata;

File='/Volumes/LaCie/Memory_matched_noregression_9subs/AvgSub_Reli_Memory.dscalar.nii'; 
AvgSub_Reli_Memory=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Memory=AvgSub_Reli_Memory.cdata;

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
AvgSub_Reli_Memory_Reg(:,2)=AvgSub_NETS;
AvgSub_Reli_Rest(:,2)=AvgSub_NETS;
AvgSub_Reli_Memory(:,2)=AvgSub_NETS;

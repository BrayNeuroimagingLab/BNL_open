%% GLASS ONLY 9 MSC SUBJECTS_MotorMatched No regression

%STEP 1 open rest timeseries%%
allsessions_allsubjects_task=Open_CiftiTimeseries('glasslexical_run01');
% 
% STEP 2%
glassrun1_rm=Remove_Motion('msc_glass_run1', allsessions_allsubjects_task);
%

%STEP 1 open rest timeseries%%
allsessions_allsubjects_task=Open_CiftiTimeseries('glasslexical_run02');
% 
% STEP 2%
glassrun2_rm=Remove_Motion('msc_glass_run2', allsessions_allsubjects_task);
%

%Do Steps 1-2 above first then the following
glassrun1_mc=MeanCenter_Timeseries(glassrun1_rm);
glassrun2_mc=MeanCenter_Timeseries(glassrun2_rm);

for j=1:10 %ses
    for k=1:10 %sub
        try
        allglass_mc{1,k}{j,1} = [glassrun1_mc{1,k}{j,1} glassrun2_mc{1,k}{j,1}];
        catch
            fprintf('error\n')
        end
    end
end


%%already calculated min size and minidx
minidx=[9,9,8,3,8,7,8,6,2,7]; 
minsize=[182,166,157,173,156,169,121,169,102,168];

%NOW ADD EMPTY COLUMN 8!
allglass_mc{1,8}=[];

%motor match according to a subject's lowest motor volume for that session
for ses=1:10
    for sub=1:10
        try
            allglass_matched{1,sub}{ses,1}=allglass_mc{1,sub}{ses,1}(:,1:minsize(ses));
        catch
        fprintf('error\n')
        end
    end
end

%%STEP 4%%
[glass_firsthalf_matched, glass_lasthalf_matched, glass_mc]=Concatenate_Connectomes(allglass_matched);


%%STEP7%%
%Now we run Connectome_Corr.m for subjects
for sub=1:10
    try
        glass_corr=Connectome_Corr(glass_firsthalf_matched{sub}, glass_lasthalf_matched{sub}, sub, 'glasslexical_run01','glass');
    catch
        fprintf('error\n')
    end
end

%%STEP 8%%
%average the glass reliabilities
for sub=1:10
    try
        glass_matched_cifti{sub}=ciftiopen(sprintf('/Volumes/LaCie/Glass_matched_noregression_9subs/Sub%d_glass_FirstLast_Corr.dscalar.nii', sub),'/Applications/workbench/bin_macosx64/wb_command');
        glass_matched_cifti{sub}=glass_matched_cifti{sub}.cdata;
    catch
        fprintf('error\n')
    end
end

AvgSub_Reli_Glass=(glass_matched_cifti{1}+glass_matched_cifti{2}+ glass_matched_cifti{3}+ glass_matched_cifti{4}+ glass_matched_cifti{5}+ glass_matched_cifti{6}+ glass_matched_cifti{7}+glass_matched_cifti{9}+glass_matched_cifti{10})/9;

%Open subject's original cifti
subject_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');

% Replace original .cdata with correlated data
subject_cifti.cdata=AvgSub_Reli_Glass;
ciftisavereset(subject_cifti, '/Users/shefalirai/Desktop/AvgSub_Reli_Glass.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');

%MotorReliability parcellated
inputFile='/Users/shefalirai/Desktop/AvgSub_Reli_Glass.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/AvgSub_Reli_Glass_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Avg_ReliParc_GlassMatched=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_ReliParc_GlassMatched=Avg_ReliParc_GlassMatched.cdata;

%Open glass reliability 
File='/Volumes/LaCie/Glass_matched_noregression_9subs/AvgSub_Reli_Glass_1000parc.pscalar.nii'; 
AvgSub_Reli_Glass=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Glass=AvgSub_Reli_Glass.cdata;


%% REST ONLY 9 MSC SUBJECTS_MotorMatched

%Already calculated from MotorMatched_Reliability_Nov2022.m file

%% Relative reliability between Glass and Rest both motor matched and only 9 subjects NO REGRESSION

File='/Volumes/LaCie/Glass_matched_noregression_9subs/AvgSub_Reli_Glass.dscalar.nii'; 
AvgSub_Reli_Glass=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Glass=AvgSub_Reli_Glass.cdata;

%Absolute reliability difference between memory and rest 
Absolute_GlassReli=AvgSub_Reli_Glass-AvgSub_Reli_Rest;

%Open subject's original cifti
subject_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');

% Replace original .cdata with correlated data
subject_cifti.cdata=Absolute_GlassReli;
ciftisavereset(subject_cifti, '/Users/shefalirai/Desktop/AvgSub_Relative_GlassReli.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');

%Relative Reliability parcellated
inputFile='/Users/shefalirai/Desktop/AvgSub_Relative_GlassReli.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/AvgSub_Relative_GlassReli_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Avg_ReliParc_GlassMatched=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_ReliParc_GlassMatched=Avg_ReliParc_GlassMatched.cdata;

%Open glass reliability first
File='/Volumes/LaCie/Glass_matched_noregression_9subs/AvgSub_Relative_GlassReli_1000parc.pscalar.nii'; 
AvgSub_Reli_Glass=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Glass=AvgSub_Reli_Glass.cdata;

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
AvgSub_Reli_Glass(:,2)=AvgSub_NETS;




%% GLASS ONLY 9 MSC SUBJECTS_MotorMatched WITH TASK REGRESSION

%STEP 1 open rest timeseries%%
%Run Open_CiftiTimeseries_Regressed.m
glassrun1_reg=Open_CiftiTimeseries_Regressed('glassrun1');
glassrun2_reg=Open_CiftiTimeseries_Regressed('glassrun2');

%STEP 2%
glassrun1_reg_rm=Remove_Motion('msc_glass_run1', glassrun1_reg);
glassrun2_reg_rm=Remove_Motion('msc_glass_run2', glassrun2_reg);

%Mean center separately
glassrun1_reg_rm_mc=MeanCenter_Timeseries(glassrun1_reg_rm);
glassrun2_reg_rm_mc=MeanCenter_Timeseries(glassrun2_reg_rm);

for j=1:10 %ses
    for k=1:10 %sub
        try
        allglass_reg_rm_mc{1,k}{j,1} = [glassrun1_reg_rm_mc{1,k}{j,1} glassrun2_reg_rm_mc{1,k}{j,1}];
        catch
            fprintf('error\n')
        end
    end
end

%NOW ADD EMPTY COLUMN 8 TO MOTORS_REG_RM_MC! 
%To exclue MSC08
allglass_reg_rm_mc{1,8}=[];

%minimum size per session for motor
% [minsize, minidx] = min(cellfun('size', motors_reg_rm_mc', 2));
%%already calculated min size and minidx for 9 subjects 
minidx=[9,9,8,3,8,7,8,6,2,7]; 
minsize=[182,166,157,173,156,169,121,169,102,168];


%motor match according to a subject's lowest motor volume for that session
for ses=1:10
    for sub=1:10
        try
            allglass_matched_reg{1,sub}{ses,1}=allglass_reg_rm_mc{1,sub}{ses,1}(:,1:minsize(ses));
        catch
        fprintf('error\n')
        end
    end
end

%%STEP 4%%
[glass_reg_firsthalf_matched, glass_reg_lasthalf_matched, glass_reg_mc]=Concatenate_Connectomes(allglass_matched_reg);


%%STEP7%%
%Now we run Connectome_Corr.m for subjects
for sub=1:10
    try
        glass_reg_corr=Connectome_Corr(glass_reg_firsthalf_matched{sub}, glass_reg_lasthalf_matched{sub}, sub, 'glasslexical_run01','glass');
    catch
        fprintf('error\n')
    end
end

%%STEP 8%%
%avergae the glass reliabilities
for sub=1:10
    try
        glass_reg_matched_cifti{sub}=ciftiopen(sprintf('/Users/shefalirai/Desktop/Sub%d_glass_FirstLast_Corr.dscalar.nii', sub),'/Applications/workbench/bin_macosx64/wb_command');
        glass_reg_matched_cifti{sub}=glass_reg_matched_cifti{sub}.cdata;
    catch
        fprintf('error\n')
    end
end

AvgSub_Reli_Glass_Reg=(glass_reg_matched_cifti{1}+glass_reg_matched_cifti{2}+ glass_reg_matched_cifti{3}+ glass_reg_matched_cifti{4}+ glass_reg_matched_cifti{5}+ glass_reg_matched_cifti{6}+ glass_reg_matched_cifti{7}+glass_reg_matched_cifti{9}+glass_reg_matched_cifti{10})/9;

%Open subject's original cifti
subject_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');

% Replace original .cdata with correlated data
subject_cifti.cdata=AvgSub_Reli_Glass_Reg;
ciftisavereset(subject_cifti, '/Users/shefalirai/Desktop/AvgSub_Reli_Glass_Reg.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');

%MotorReliability parcellated
inputFile='/Users/shefalirai/Desktop/AvgSub_Reli_Glass_Reg.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/AvgSub_Reli_Glass_Reg_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Avg_ReliParc_GlassMatched_Reg=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_ReliParc_GlassMatched_Reg=Avg_ReliParc_GlassMatched_Reg.cdata;

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
Avg_ReliParc_GlassMatched_Reg(:,2)=AvgSub_NETS;

parcelFile='/Volumes/LaCie/Glass_matched_REGRESSED_9subs/AvgSub_Reli_Glass_Reg_1000parc.pscalar.nii'; 
Avg_ReliParc_GlassMatched=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_ReliParc_GlassMatched=Avg_ReliParc_GlassMatched.cdata;
Avg_ReliParc_GlassMatched(:,2)=AvgSub_NETS;

%% Relative reliability between Glass and Rest both motor matched and only 9 subjects WITH REGRESSION

%Open Rest reliability first
File='/Volumes/LaCie/REST_Motor_matched_9subs/AvgSub_Reli_Rest.dscalar.nii'; 
AvgSub_Reli_Rest=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Rest=AvgSub_Reli_Rest.cdata;

%Open glass reliability first
File='/Volumes/LaCie/Glass_matched_REGRESSED_9subs/AvgSub_Reli_Glass_Reg.dscalar.nii'; 
AvgSub_Reli_Glass_Reg=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Glass_Reg=AvgSub_Reli_Glass_Reg.cdata;

%Calculate difference between glass and rest 
Relative_GlassReli_Reg=AvgSub_Reli_Glass_Reg-AvgSub_Reli_Rest;

%Open subject's original cifti
subject_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');

% Replace original .cdata with correlated data
subject_cifti.cdata=Relative_GlassReli_Reg;
ciftisavereset(subject_cifti, '/Users/shefalirai/Desktop/AvgSub_Relative_GlassReli_Reg.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');

%Relative Reliability parcellated
inputFile='/Users/shefalirai/Desktop/AvgSub_Relative_GlassReli_Reg.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/AvgSub_Relative_GlassReli_Reg_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Avg_ReliParc_GlassMatched_Reg=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_ReliParc_GlassMatched_Reg=Avg_ReliParc_GlassMatched_Reg.cdata;

%% Open parcelled files

%Open Rest reliability first
File='/Volumes/LaCie/REST_Motor_matched_9subs/AvgSub_Reli_Rest_1000parc.pscalar.nii'; 
AvgSub_Reli_Rest=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Rest=AvgSub_Reli_Rest.cdata;

%Open glass reliability first
File='/Volumes/LaCie/Glass_matched_REGRESSED_9subs/AvgSub_Reli_Glass_Reg_1000parc.pscalar.nii'; 
AvgSub_Reli_Glass_Reg=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Glass_Reg=AvgSub_Reli_Glass_Reg.cdata;

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
AvgSub_Reli_Glass_Reg(:,2)=AvgSub_NETS;
AvgSub_Reli_Rest(:,2)=AvgSub_NETS;
AvgSub_Reli_Glass(:,2)=AvgSub_NETS;
Avg_ReliParc_GlassMatched_Reg(:,2)=AvgSub_NETS;

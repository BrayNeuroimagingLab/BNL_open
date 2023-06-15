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


%% Glass Signal Property Values NO REGRESSION

%STEP 1 open rest timeseries%%
allsessions_allsubjects_glass1=Open_CiftiTimeseries('glasslexical_run01');
% 
% STEP 2%
glassrun1_rm=Remove_Motion('msc_glass_run1', allsessions_allsubjects_glass1);
%

%STEP 1 open rest timeseries%%
allsessions_allsubjects_glass2=Open_CiftiTimeseries('glasslexical_run02');
% 
% STEP 2%
glassrun2_rm=Remove_Motion('msc_glass_run2', allsessions_allsubjects_glass2);
%

glassrun1_rm_mc=MeanCenter_Timeseries(glassrun1_rm);
glassrun2_rm_mc=MeanCenter_Timeseries(glassrun2_rm);

% %already calculated min size and minidx for all 10 subjects
minidx=[9,9,8,3,8,7,8,6,2,7]; 
minsize=[182,166,157,173,156,169,121,169,102,168];
% 

%Do Steps 1-2 above first then the following
for j=1:10 %ses
    for k=1:10 %sub
        try
            glass_nomc{1,k}{j,1} = [glassrun1_rm{1,k}{j,1} glassrun2_rm{1,k}{j,1}];
        catch
            fprintf('error\n')
        end
    end
end

%Do Steps 1-2 above first then the following
for j=1:10 %ses
    for k=1:10 %sub
        try
            glass_mc{1,k}{j,1} = [glassrun1_rm_mc{1,k}{j,1} glassrun2_rm_mc{1,k}{j,1}];
        catch
            fprintf('error\n')
        end
    end
end

%NOW ADD EMPTY COLUMN 8 !
glasss_mc{1,8}=[];
glasss_nomc{1,8}=[];

%  %STEP 3
for ses=1:10
    for sub=1:10
        try
            glass_matched_mc{1,sub}{ses,1}=glass_mc{1,sub}{ses,1}(:,1:minsize(ses));
        catch
            fprintf('error\n')
        end
    end
end

for ses=1:10
    for sub=1:10
        try
            glass_matched_nomc{1,sub}{ses,1}=glass_nomc{1,sub}{ses,1}(:,1:minsize(ses));
        catch
            fprintf('error\n')
        end
    end
end

[Glass_Mean_Sub]=MeanSignal_Values_Jan2023(glass_matched_nomc);
[Glass_SD_Sub]=SD_Values_Jan2023(glass_matched_mc);
[Glass_tSNR_Sub]=tSNR_Values_Jan2023(Glass_Mean_Sub, Glass_SD_Sub);

% Save tSNR as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Glass_tSNR_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Glass_tSNR_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save SD as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Glass_SD_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Glass_SD_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save MeanSignal as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Glass_Mean_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Glass_MeanSignal_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

%parcellate TSNR
inputFile='/Users/shefalirai/Desktop/Glass_tSNR_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Glass_tSNR_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Glass_tSNR_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Glass_tSNR_Parc=Glass_tSNR_Parc.cdata;

%parcellate SD
inputFile='/Users/shefalirai/Desktop/Glass_SD_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Glass_SD_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Glass_SD_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Glass_SD_Parc=Glass_SD_Parc.cdata;

%parcellate MS
inputFile='/Users/shefalirai/Desktop/Glass_MeanSignal_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Glass_MeanSignal_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Glass_MeanSignal_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Glass_MeanSignal_Parc=Glass_MeanSignal_Parc.cdata;


%% GLASS - REST
%Open rest signal property files
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_MeanSignal_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_Mean_Sub=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_SD_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_SD_Sub=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_tSNR_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_tSNR_Sub=Avg_cifti.cdata;

Relative_Glass_Mean=Glass_Mean_Sub-Rest_Mean_Sub;
Relative_Glass_tSNR=Glass_tSNR_Sub-Rest_tSNR_Sub;
Relative_Glass_SD=Glass_SD_Sub-Rest_SD_Sub;

% Save Avg_tSNR as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Relative_Glass_tSNR;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/GlassRelative_tSNR_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save Avg_SD as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Relative_Glass_SD;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/GlassRelative_SD_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save Avg_MeanSignal as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Relative_Glass_Mean;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/GlassRelative_MeanSignal_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

%parcellate TSNR
inputFile='/Users/shefalirai/Desktop/GlassRelative_tSNR_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/GlassRelative_tSNR_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
GlassRelative_tSNR_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
GlassRelative_tSNR_Parc=GlassRelative_tSNR_Parc.cdata;

%parcellate SD
inputFile='/Users/shefalirai/Desktop/GlassRelative_SD_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/GlassRelative_SD_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
GlassRelative_SD_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
GlassRelative_SD_Parc=GlassRelative_SD_Parc.cdata;

%parcellate MS
inputFile='/Users/shefalirai/Desktop/GlassRelative_MeanSignal_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/GlassRelative_MeanSignal_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
GlassRelative_MeanSignal_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
GlassRelative_MeanSignal_Parc=GlassRelative_MeanSignal_Parc.cdata;

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
GlassRelative_SD_Parc(:,2)=AvgSub_NETS;

%% Glass signal vs reli

% Save tSNR as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Glass_tSNR_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Glass_tSNR_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save SD as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Glass_SD_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Glass_SD_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save MeanSignal as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Glass_Mean_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Glass_MeanSignal_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

%parcellate TSNR
inputFile='/Users/shefalirai/Desktop/Glass_tSNR_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Glass_tSNR_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Glass_tSNR_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Glass_tSNR_Parc=Glass_tSNR_Parc.cdata;

%parcellate SD
inputFile='/Users/shefalirai/Desktop/Glass_SD_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Glass_SD_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Glass_SD_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Glass_SD_Parc=Glass_SD_Parc.cdata;

%parcellate MS
inputFile='/Users/shefalirai/Desktop/Glass_MeanSignal_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Glass_MeanSignal_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Glass_MeanSignal_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Glass_MeanSignal_Parc=Glass_MeanSignal_Parc.cdata;

%% Glass Signal Property Values REGRESSED

%STEP 1 open rest timeseries%%
allsessions_allsubjects_glass1=Open_CiftiTimeseries_Regressed('glassrun1');
% 
% STEP 2%
glassrun1_rm=Remove_Motion('msc_glass_run1', allsessions_allsubjects_glass1);
%

%STEP 1 open rest timeseries%%
allsessions_allsubjects_glass2=Open_CiftiTimeseries_Regressed('glassrun2');
% 
% STEP 2%
glassrun2_rm=Remove_Motion('msc_glass_run2', allsessions_allsubjects_glass2);
%

%Do Steps 1-2 above first then the following
for j=1:10 %ses
    for k=1:10 %sub
        try
        allsessions_allsubjects_glass{1,k}{j,1} = [glassrun1_rm{1,k}{j,1} glassrun2_rm{1,k}{j,1}];
        catch
            fprintf('error\n')
        end
    end
end


%%already calculated min size and minidx
minidx=[9,9,8,3,8,7,8,6,2,7]; 
minsize=[182,166,157,173,156,169,121,169,102,168];

%NOW ADD EMPTY COLUMN 8 TO MOTORS_MC!
allsessions_allsubjects_glass{1,8}=[];

%motor match according to a subject's lowest motor volume for that session
for ses=1:10
    for sub=1:10
        try
            glass_matched{1,sub}{ses,1}=allsessions_allsubjects_glass{1,sub}{ses,1}(:,1:minsize(ses));
        catch
        fprintf('error\n')
        end
    end
end

[Glass_Mean_Sub, Glass_SD_Sub, Glass_tSNR_Sub]=Signal_Property_Values(glass_matched);

% Save tSNR as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Glass_tSNR_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Glass_tSNR_motormatched_noMSC08_regressed.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save SD as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Glass_SD_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Glass_SD_motormatched_noMSC08_regressed.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save MeanSignal as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Glass_Mean_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Glass_MeanSignal_motormatched_noMSC08_regressed.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

%parcellate TSNR
inputFile='/Users/shefalirai/Desktop/Glass_tSNR_motormatched_noMSC08_regressed.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Glass_tSNR_motormatched_noMSC08_regressed_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Glass_tSNR_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Glass_tSNR_Parc=Glass_tSNR_Parc.cdata;

%parcellate SD
inputFile='/Users/shefalirai/Desktop/Glass_SD_motormatched_noMSC08_regressed.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Glass_SD_motormatched_noMSC08_regressed_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Glass_SD_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Glass_SD_Parc=Glass_SD_Parc.cdata;

%parcellate MS
inputFile='/Users/shefalirai/Desktop/Glass_MeanSignal_motormatched_noMSC08_regressed.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Glass_MeanSignal_motormatched_regressed_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Glass_MeanSignal_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Glass_MeanSignal_Parc=Glass_MeanSignal_Parc.cdata;

%% Glass - REST TASK REGRESSED

% open files if needed
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Glass_MeanSignal_motormatched_noMSC08_regressed.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_Mean_regressed=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Glass_tSNR_motormatched_noMSC08_regressed.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_tSNR_regressed=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Glass_SD_motormatched_noMSC08_regressed.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_SD_regressed=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_MeanSignal_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_Mean_Sub=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_tSNR_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_tSNR_Sub=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_SD_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_SD_Sub=Avg_cifti.cdata;
 

Relative_Glass_Mean_regressed=Glass_Mean_regressed-Rest_Mean_Sub;
Relative_Glass_tSNR_regressed=Glass_tSNR_regressed-Rest_tSNR_Sub;
Relative_Glass_SD_regressed=Glass_SD_regressed-Rest_SD_Sub;

% Save Avg_tSNR as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Relative_Glass_tSNR_regressed;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/GlassRelative_tSNR_motormatched_noMSC08_regressed.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save Avg_SD as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Relative_Glass_SD_regressed;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/GlassRelative_SD_motormatched_noMSC08_regressed.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save Avg_MeanSignal as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Relative_Glass_Mean_regressed;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/GlassRelative_MeanSignal_motormatched_noMSC08_regressed.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

%Parcellate relative signal properties
%parcellate TSNR
inputFile='/Users/shefalirai/Desktop/GlassRelative_tSNR_motormatched_noMSC08_regressed.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/GlassRelative_tSNR_motormatched_noMSC08_regressed_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
GlassRelative_tSNR_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
GlassRelative_tSNR_Parc=GlassRelative_tSNR_Parc.cdata;

%parcellate SD
inputFile='/Users/shefalirai/Desktop/GlassRelative_SD_motormatched_noMSC08_regressed.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/GlassRelative_SD_motormatched_noMSC08_regressed_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
GlassRelative_SD_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
GlassRelative_SD_Parc=GlassRelative_SD_Parc.cdata;

%parcellate MS
inputFile='/Users/shefalirai/Desktop/GlassRelative_MeanSignal_motormatched_noMSC08_regressed.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/GlassRelative_MeanSignal_motormatched_noMSC08_regressed_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
GlassRelative_MeanSignal_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
GlassRelative_MeanSignal_Parc=GlassRelative_MeanSignal_Parc.cdata;

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
GlassRelative_SD_Parc(:,2)=AvgSub_NETS;



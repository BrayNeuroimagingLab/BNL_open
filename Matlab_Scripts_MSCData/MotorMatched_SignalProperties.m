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

[Rest_Mean_Sub, Rest_Mean_eachsub]=MeanSignal_Values_Jan2023(rest_matched_nomc);
[Rest_SD_Sub, Rest_SD_eachsub]=SD_Values_Jan2023(rest_matched_mc);
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

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
Rest_MeanSignal_Parc(:,2)=AvgSub_NETS;
Rest_SD_Parc(:,2)=AvgSub_NETS;


%% Motor Signal Property Values NO REGRESSION

%STEP 1 open rest timeseries%%
allsessions_allsubjects_motor1=Open_CiftiTimeseries('motor_run1');
% 
% STEP 2%
motorrun1_rm=Remove_Motion('msc_motor1', allsessions_allsubjects_motor1);
%

%STEP 1 open rest timeseries%%
allsessions_allsubjects_motor2=Open_CiftiTimeseries('motor_run2');
% 
% STEP 2%
motorrun2_rm=Remove_Motion('msc_motor2', allsessions_allsubjects_motor2);
%
motorrun1_rm_mc=MeanCenter_Timeseries(motorrun1_rm);
motorrun2_rm_mc=MeanCenter_Timeseries(motorrun2_rm);

% %already calculated min size and minidx for all 10 subjects
minidx=[9,9,8,3,8,7,8,6,2,7]; 
minsize=[182,166,157,173,156,169,121,169,102,168];
% 

%Do Steps 1-2 above first then the following
for j=1:10 %ses
    for k=1:10 %sub
        try
            motors_nomc{1,k}{j,1} = [motorrun1_rm{1,k}{j,1} motorrun2_rm{1,k}{j,1}];
        catch
            fprintf('error\n')
        end
    end
end

%Do Steps 1-2 above first then the following
for j=1:10 %ses
    for k=1:10 %sub
        try
            motors_mc{1,k}{j,1} = [motorrun1_rm_mc{1,k}{j,1} motorrun2_rm_mc{1,k}{j,1}];
        catch
            fprintf('error\n')
        end
    end
end

%NOW ADD EMPTY COLUMN 8 !
motors_mc{1,8}=[];
motors_nomc{1,8}=[];

%  %STEP 3
for ses=1:10
    for sub=1:10
        try
            motors_matched_mc{1,sub}{ses,1}=motors_mc{1,sub}{ses,1}(:,1:minsize(ses));
        catch
            fprintf('error\n')
        end
    end
end

for ses=1:10
    for sub=1:10
        try
            motors_matched_nomc{1,sub}{ses,1}=motors_nomc{1,sub}{ses,1}(:,1:minsize(ses));
        catch
            fprintf('error\n')
        end
    end
end

[Motor_Mean_Sub]=MeanSignal_Values_Jan2023(motors_matched_nomc);
[Motor_SD_Sub]=SD_Values_Jan2023(motors_matched_mc);
[Motor_tSNR_Sub]=tSNR_Values_Jan2023(Motor_Mean_Sub, Motor_SD_Sub);

% Save tSNR as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Motor_tSNR_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Motor_tSNR_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save SD as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Motor_SD_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Motor_SD_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save MeanSignal as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Motor_Mean_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Motor_MeanSignal_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

%parcellate TSNR
inputFile='/Users/shefalirai/Desktop/Motor_tSNR_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Motor_tSNR_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Motor_tSNR_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Motor_tSNR_Parc=Motor_tSNR_Parc.cdata;

%parcellate SD
inputFile='/Users/shefalirai/Desktop/Motor_SD_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Motor_SD_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Motor_SD_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Motor_SD_Parc=Motor_SD_Parc.cdata;

%parcellate MS
inputFile='/Users/shefalirai/Desktop/Motor_MeanSignal_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Motor_MeanSignal_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Motor_MeanSignal_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Motor_MeanSignal_Parc=Motor_MeanSignal_Parc.cdata;



%% MOTOR - REST

%Open rest signal property files
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_MeanSignal_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_Mean_Sub=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_SD_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_SD_Sub=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_tSNR_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_tSNR_Sub=Avg_cifti.cdata;

%calculate different from motor to rest
Relative_Motor_Mean=Motor_Mean_Sub-Rest_Mean_Sub;
Relative_Motor_tSNR=Motor_tSNR_Sub-Rest_tSNR_Sub;
Relative_Motor_SD=Motor_SD_Sub-Rest_SD_Sub;

% Save Avg_tSNR as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Relative_Motor_tSNR;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/MotorRelative_tSNR_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save Avg_SD as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Relative_Motor_SD;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/MotorRelative_SD_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save Avg_MeanSignal as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Relative_Motor_Mean;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/MotorRelative_MeanSignal_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

%parcellate TSNR
inputFile='/Users/shefalirai/Desktop/MotorRelative_tSNR_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/MotorRelative_tSNR_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
MotorRelative_tSNR_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
MotorRelative_tSNR_Parc=MotorRelative_tSNR_Parc.cdata;

%parcellate SD
inputFile='/Users/shefalirai/Desktop/MotorRelative_SD_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/MotorRelative_SD_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
MotorRelative_SD_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
MotorRelative_SD_Parc=MotorRelative_SD_Parc.cdata;

%parcellate MS
inputFile='/Users/shefalirai/Desktop/MotorRelative_MeanSignal_motormatched_noMSC08.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/MotorRelative_MeanSignal_motormatched_noMSC08_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
MotorRelative_MeanSignal_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
MotorRelative_MeanSignal_Parc=MotorRelative_MeanSignal_Parc.cdata;

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
MotorRelative_SD_Parc(:,2)=AvgSub_NETS;

%% Open network names for parcels

AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;


%% Motor Signal Property Values REGRESSED

%STEP 1 open rest timeseries%%
allsessions_allsubjects_motor1_reg=Open_CiftiTimeseries_Regressed('motorrun1');
% 
% STEP 2%
motorrun1_rm_reg=Remove_Motion('msc_motor1', allsessions_allsubjects_motor1_reg);
%

%STEP 1 open rest timeseries%%
allsessions_allsubjects_motor2_reg=Open_CiftiTimeseries_Regressed('motorrun2');
% 
% STEP 2%
motorrun2_rm_reg=Remove_Motion('msc_motor2', allsessions_allsubjects_motor2_reg);
%
 
% %already calculated min size and minidx for all 10 subjects
minidx=[9,9,8,3,8,7,8,6,2,7]; 
minsize=[182,166,157,173,156,169,121,169,102,168];
% 

motorrun1_rm_mc_reg=MeanCenter_Timeseries(motorrun1_rm_reg);
motorrun2_rm_mc_reg=MeanCenter_Timeseries(motorrun2_rm_reg);

%Do Steps 1-2 above first then the following
for j=1:10 %ses
    for k=1:10 %sub
        try
            motors_mc_reg{1,k}{j,1} = [motorrun1_rm_mc_reg{1,k}{j,1} motorrun2_rm_mc_reg{1,k}{j,1}];
        catch
            fprintf('error\n')
        end
    end
end

%NOW ADD EMPTY COLUMN 8 !
motors_mc_reg{1,8}=[];

for ses=1:10
    for sub=1:10
        try
            motors_matched_mc_reg{1,sub}{ses,1}=motors_mc_reg{1,sub}{ses,1}(:,1:minsize(ses));
        catch
            fprintf('error\n')
        end
    end
end

[Motor_Mean_Sub]=MeanSignal_Values_Jan2023(motors_matched_mc_reg);
[Motor_SD_Sub]=SD_Values_Jan2023(motors_matched_mc_reg);
[Motor_tSNR_Sub]=tSNR_Values_Jan2023(Motor_Mean_Sub, Motor_SD_Sub);

% Save tSNR as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Motor_tSNR_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Motor_tSNR_motormatched_noMSC08_Reg.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save SD as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Motor_SD_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Motor_SD_motormatched_noMSC08_Reg.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save MeanSignal as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Motor_Mean_Sub;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Motor_MeanSignal_motormatched_noMSC08_Reg.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

%parcellate TSNR
inputFile='/Users/shefalirai/Desktop/Motor_tSNR_motormatched_noMSC08_Reg.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Motor_tSNR_motormatched_noMSC08_Reg_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Motor_tSNR_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Motor_tSNR_Parc=Motor_tSNR_Parc.cdata;

%parcellate SD
inputFile='/Users/shefalirai/Desktop/Motor_SD_motormatched_noMSC08_Reg.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Motor_SD_motormatched_noMSC08_Reg_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Motor_SD_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Motor_SD_Parc=Motor_SD_Parc.cdata;

%parcellate MS
inputFile='/Users/shefalirai/Desktop/Motor_MeanSignal_motormatched_noMSC08_Reg.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/Motor_MeanSignal_motormatched_noMSC08_Reg_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Motor_MeanSignal_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Motor_MeanSignal_Parc=Motor_MeanSignal_Parc.cdata;


%% MOTOR - REST TASK REGRESSED
%Open rest ciftis
Avg_cifti=ciftiopen('/Volumes/LaCie/Rest_Motor_matched_9subs/AvgSub_Reli_Rest.dscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_Reli_motormatched=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_MeanSignal_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_MS_motormatched=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_SD_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_SD_motormatched=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_tSNR_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_tSNR_motormatched=Avg_cifti.cdata;

Relative_Motor_Mean=Motor_Mean_Sub-Rest_MS_motormatched;
Relative_Motor_tSNR=Motor_tSNR_Sub-Rest_tSNR_motormatched;
Relative_Motor_SD=Motor_SD_Sub-Rest_SD_motormatched;

% Save Avg_tSNR as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Relative_Motor_tSNR;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/MotorRelative_tSNR_motormatched_noMSC08_Reg.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save Avg_SD as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Relative_Motor_SD;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/MotorRelative_SD_motormatched_noMSC08_Reg.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

% Save Avg_MeanSignal as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Relative_Motor_Mean;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/MotorRelative_MeanSignal_motormatched_noMSC08_Reg.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');


%parcellate TSNR
inputFile='/Users/shefalirai/Desktop/MotorRelative_tSNR_motormatched_noMSC08_Reg.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/MotorRelative_tSNR_motormatched_noMSC08_Reg_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
MotorRelative_tSNR_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
MotorRelative_tSNR_Parc=MotorRelative_tSNR_Parc.cdata;

%parcellate SD
inputFile='/Users/shefalirai/Desktop/MotorRelative_SD_motormatched_noMSC08_Reg.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/MotorRelative_SD_motormatched_noMSC08_Reg_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
MotorRelative_SD_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
MotorRelative_SD_Parc=MotorRelative_SD_Parc.cdata;

%parcellate MS
inputFile='/Users/shefalirai/Desktop/MotorRelative_MeanSignal_motormatched_noMSC08_Reg.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Volumes/LaCie/SignalProperties_noMSC08/MotorRelative_MeanSignal_motormatched_noMSC08_Reg_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
MotorRelative_MeanSignal_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
MotorRelative_MeanSignal_Parc=MotorRelative_MeanSignal_Parc.cdata;

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
MotorRelative_SD_Parc(:,2)=AvgSub_NETS;


%% TSNR %%

Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_tSNR_motormatched_noMSC08_1000parc.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_tSNR_motormatched=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/MotorRelative_tSNR_motormatched_noMSC08_1000parc.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Motor_tSNR_motormatched=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/GlassRelative_tSNR_motormatched_noMSC08_1000parc.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_tSNR_motormatched=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/MemoryRelative_tSNR_motormatched_noMSC08_1000parc.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_tSNR_motormatched=Avg_cifti.cdata;

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
Rest_tSNR_motormatched(:,2)=AvgSub_NETS;
Motor_tSNR_motormatched(:,2)=AvgSub_NETS;
Glass_tSNR_motormatched(:,2)=AvgSub_NETS;
Memory_tSNR_motormatched(:,2)=AvgSub_NETS;

%Sort by ascending networks 1-17 and paste into MSCData excel file


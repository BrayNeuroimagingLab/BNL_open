% %% REST_Motor_matched_all10subs %%
%  
% %STEP 1 open rest timeseries%%
% %Run Open_CiftiTimeseries_REST.m
% 
% %STEP 2%
%  rest_rm=Remove_Motion('msc_rest', allsessions_allsubjects_task);
% 
% rest_mc=MeanCenter_Timeseries(rest_rm);
% %already calculated min size and minidx for all 10 subjects
% % minidx=[10,10,9,8,8,7,9,8,9,8]
% % minsize=[182,166,157,167,154,169,121,133,141,154];
% 
%  %STEP 3
% for ses=1:10
%     for sub=1:10
%         rest_matched{1,sub}{ses,1}=rest_mc{1,sub}{ses,1}(:,1:minsize(ses));
%     end
% end
% 
% %%STEP 4%%
% %Run Meancentering then Concatenate connectome.m files first
% % rest_meancent=MeanCenter_Timeseries(rest_matched);
% [rest_firsthalf_matched, rest_lasthalf_matched, rest_mc]=Concatenate_Connectomes(rest_matched);
% 
% 
% %%STEP7%%
% %Now we run Connectome_Corr.m for subjects
% for sub=1:10
%     try
%         rest_corr=Connectome_Corr(rest_firsthalf_matched{sub}, rest_lasthalf_matched{sub}, sub, 'rest','rest');
%     catch
%         fprintf('error\n')
%     end
% end
% 
% %%STEP 8%%
% %avergae the rest reliabilities
% for sub=1:10
%     try
%         rest_matched_cifti{sub}=ciftiopen(sprintf('/Users/shefalirai/Desktop/Sub%d_rest_FirstLast_Corr.dscalar.nii', sub),'/Applications/workbench/bin_macosx64/wb_command');
%         rest_matched_cifti{sub}=rest_matched_cifti{sub}.cdata;
%     catch
%         fprintf('error\n')
%     end
% end
% 
% AvgSub_Reli_Rest=(rest_matched_cifti{1}+rest_matched_cifti{2}+ rest_matched_cifti{3}+ rest_matched_cifti{4}+ rest_matched_cifti{5}+ rest_matched_cifti{6}+ rest_matched_cifti{7}+ rest_matched_cifti{8}+rest_matched_cifti{9}+rest_matched_cifti{10})/10;
% 
% %Open subject's original cifti
% subject_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
% 
% % Replace original .cdata with correlated data
% subject_cifti.cdata=AvgSub_Reli_Rest;
% ciftisavereset(subject_cifti, '/Users/shefalirai/Desktop/AvgSub_Reli_Rest.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');
% 
% %RestReliability parcellated
% inputFile='/Users/shefalirai/Desktop/AvgSub_Reli_Rest.dscalar.nii';
% parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
% parcelFile='/Users/shefalirai/Desktop/AvgSub_Reli_Rest_1000parc.pscalar.nii'; 
% eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
% Avg_ReliParc_RestMatched=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
% Avg_ReliParc_RestMatched=Avg_ReliParc_RestMatched.cdata;

%% MOTOR ONLY 9 MSC SUBJECTS_MotorMatched No regression

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

for j=1:10 %ses
    for k=1:10 %sub
        try
        allsessions_allsubjects_motors_mc{1,k}{j,1} = [motorrun1_rm_mc{1,k}{j,1} motorrun2_rm_mc{1,k}{j,1}];
        catch
            fprintf('error\n')
        end
    end
end

%find minimum size per session for motor
%[minsize, minidx] = min(cellfun('size', motors_rm', 2));
%%already calculated min size and minidx
minidx=[9,9,8,3,8,7,8,6,2,7]; 
minsize=[182,166,157,173,156,169,121,169,102,168];

%NOW ADD EMPTY COLUMN 8 TO MOTORS_MC!

%motor match according to a subject's lowest motor volume for that session
for ses=1:10
    for sub=1:10
        try
            motor_matched{1,sub}{ses,1}=allsessions_allsubjects_motors_mc{1,sub}{ses,1}(:,1:minsize(ses));
        catch
        fprintf('error\n')
        end
    end
end

%%STEP 4%%
[motor_firsthalf_matched, motor_lasthalf_matched, motor_mc]=Concatenate_Connectomes(motor_matched);


%%STEP7%%
%Now we run Connectome_Corr.m for subjects
for sub=1:10
    try
        motor_corr=Connectome_Corr(motor_firsthalf_matched{sub}, motor_lasthalf_matched{sub}, sub, 'motor_run1','motor');
    catch
        fprintf('error\n')
    end
end

%%STEP 8%%
%avergae the motor reliabilities
for sub=1:10
    try
        motor_matched_cifti{sub}=ciftiopen(sprintf('/Volumes/LaCie/Motor_matched_noregression_9subs/Sub%d_motor_FirstLast_Corr.dscalar.nii', sub),'/Applications/workbench/bin_macosx64/wb_command');
        motor_matched_cifti{sub}=motor_matched_cifti{sub}.cdata;
    catch
        fprintf('error\n')
    end
end

AvgSub_Reli_Motor=(motor_matched_cifti{1}+motor_matched_cifti{2}+ motor_matched_cifti{3}+ motor_matched_cifti{4}+ motor_matched_cifti{5}+ motor_matched_cifti{6}+ motor_matched_cifti{7}+motor_matched_cifti{9}+motor_matched_cifti{10})/9;

%Open subject's original cifti
subject_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');

% Replace original .cdata with correlated data
subject_cifti.cdata=AvgSub_Reli_Motor;
ciftisavereset(subject_cifti, '/Users/shefalirai/Desktop/AvgSub_Reli_Motor.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');

%MotorReliability parcellated
inputFile='/Users/shefalirai/Desktop/AvgSub_Reli_Motor.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/AvgSub_Reli_Motor_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Avg_ReliParc_MotorMatched=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_ReliParc_MotorMatched=Avg_ReliParc_MotorMatched.cdata;



%% REST ONLY 9 MSC SUBJECTS_MotorMatched

%Do Steps 1-2 above first then the following
% %STEP 1 open rest timeseries%%
rest=Open_CiftiTimeseries_REST('rest');
% 
% %STEP 2%
rest_rm=Remove_Motion('msc_rest', rest);

%Step 3 meancenter
rest_rm_mc=MeanCenter_Timeseries(rest_rm);

%%STEP 4%%
%motor match according to a subject's lowest motor volume for that session
%%already calculated min size and minidx for 9 subjects only 
minidx=[9,9,8,3,8,7,8,6,2,7]; 
minsize=[182,166,157,173,156,169,121,169,102,168];

for ses=1:10
    for sub=1:10
        try
            rest_matched{1,sub}{ses,1}=rest_rm_mc{1,sub}{ses,1}(:,1:minsize(ses));
        catch
            fprintf('error\n')
        end
    end
end

[rest_firsthalf_matched, rest_lasthalf_matched, rest_mc]=Concatenate_Connectomes(rest_matched);

%%STEP7%%
%Now we run Connectome_Corr.m for subjects
for sub=1:10
    try
        rest_corr=Connectome_Corr(rest_firsthalf_matched{sub}, rest_lasthalf_matched{sub}, sub, 'rest','rest');
    catch
        fprintf('error\n')
    end
end

%%STEP 8%%
%avergae the rest reliabilities
for sub=1:10
    try
        rest_matched_cifti{sub}=ciftiopen(sprintf('/Volumes/LaCie/Rest_Motor_matched_9subs/Sub%d_rest_FirstLast_Corr.dscalar.nii', sub),'/Applications/workbench/bin_macosx64/wb_command');
        rest_matched_cifti{sub}=rest_matched_cifti{sub}.cdata;
    catch
        fprintf('error\n')
    end
end

AvgSub_Reli_Rest=(rest_matched_cifti{1}+rest_matched_cifti{2}+ rest_matched_cifti{3}+ rest_matched_cifti{4}+ rest_matched_cifti{5}+ rest_matched_cifti{6}+ rest_matched_cifti{7}+rest_matched_cifti{9}+rest_matched_cifti{10})/9;

%Open subject's original cifti
subject_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');

% Replace original .cdata with correlated data
subject_cifti.cdata=AvgSub_Reli_Rest;
ciftisavereset(subject_cifti, '/Users/shefalirai/Desktop/AvgSub_Reli_Rest.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');

%RestReliability parcellated
inputFile='/Users/shefalirai/Desktop/AvgSub_Reli_Rest.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/AvgSub_Reli_Rest_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Avg_ReliParc_RestMatched=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_ReliParc_RestMatched=Avg_ReliParc_RestMatched.cdata;

parcelFile='/Volumes/LaCie/REST_Motor_matched_9subs/AvgSub_Reli_Rest_1000parc.pscalar.nii'; 
Avg_ReliParc_RestMatched=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_ReliParc_RestMatched=Avg_ReliParc_RestMatched.cdata;
Avg_ReliParc_RestMatched(:,2)=AvgSub_NETS;

%% Relative reliability between Motor and Rest_motor matched and only 9 subjects no regression

File='/Volumes/LaCie/Motor_matched_noregression_9subs/AvgSub_Reli_Motor.dscalar.nii'; 
AvgSub_Reli_Motor=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Motor=AvgSub_Reli_Motor.cdata;

%Absolute reliability difference between memory and rest 
Absolute_MotorReli=AvgSub_Reli_Motor-AvgSub_Reli_Rest;


%Open subject's original cifti
subject_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');

% Replace original .cdata with correlated data
subject_cifti.cdata=Absolute_MotorReli;
ciftisavereset(subject_cifti, '/Users/shefalirai/Desktop/AvgSub_Relative_MotorReli.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');

%Relative Reliability parcellated
inputFile='/Users/shefalirai/Desktop/AvgSub_Relative_MotorReli.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/AvgSub_Relative_MotorReli_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Avg_ReliParc_MotorMatched=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_ReliParc_MotorMatched=Avg_ReliParc_MotorMatched.cdata;


%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
Avg_ReliParc_MotorMatched(:,2)=AvgSub_NETS;
Avg_ReliParc_RestMatched(:,2)=AvgSub_NETS;

File='/Volumes/LaCie/REST_Motor_matched_9subs/AvgSub_Reli_Rest_1000parc.pscalar.nii'; 
AvgSub_Reli_Rest_parc=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Rest_parc=AvgSub_Reli_Rest_parc.cdata;

%% MOTOR ONLY 9 MSC SUBJECTS_MotorMatched WITH TASK REGRESSION

%STEP 1 open rest timeseries%%
%Run Open_CiftiTimeseries_Regressed.m
motorrun1_reg=Open_CiftiTimeseries_MotorRegressed('motorrun1');
motorrun2_reg=Open_CiftiTimeseries_MotorRegressed('motorrun2');

%STEP 2%
motorrun1_reg_rm=Remove_Motion('msc_motor1', motorrun1_reg);
motorrun2_reg_rm=Remove_Motion('msc_motor2', motorrun2_reg);

%Mean center separately
motorrun1_reg_rm_mc=MeanCenter_Timeseries(motorrun1_reg_rm);
motorrun2_reg_rm_mc=MeanCenter_Timeseries(motorrun2_reg_rm);

for j=1:10 %ses
    for k=1:10 %sub
        try
        motors_reg_rm_mc{1,k}{j,1} = [motorrun1_reg_rm_mc{1,k}{j,1} motorrun2_reg_rm_mc{1,k}{j,1}];
        catch
            fprintf('error\n')
        end
    end
end

%NOW ADD EMPTY COLUMN 8 TO MOTORS_REG_RM_MC! 
%To exclue MSC08
motors_reg_rm_mc{1,8}={};

%minimum size per session for motor
% [minsize, minidx] = min(cellfun('size', motors_reg_rm_mc', 2));
%%already calculated min size and minidx for 9 subjects 
minidx=[9,9,8,3,8,7,8,6,2,7]; 
minsize=[182,166,157,173,156,169,121,169,102,168];


%motor match according to a subject's lowest motor volume for that session
for ses=1:10
    for sub=1:10
        try
            motors_matched_reg{1,sub}{ses,1}=motors_reg_rm_mc{1,sub}{ses,1}(:,1:minsize(ses));
        catch
        fprintf('error\n')
        end
    end
end

%%STEP 4%%
[motor_reg_firsthalf_matched, motor_reg_lasthalf_matched, motors_reg_mc]=Concatenate_Connectomes(motors_matched_reg);


%%STEP7%%
%Now we run Connectome_Corr.m for subjects
for sub=1:10
    try
        motors_reg_corr=Connectome_Corr(motor_reg_firsthalf_matched{sub}, motor_reg_lasthalf_matched{sub}, sub, 'motor_run1','motor');
    catch
        fprintf('error\n')
    end
end

%%STEP 8%%
%avergae the motor reliabilities
for sub=1:10
    try
        motor_reg_matched_cifti{sub}=ciftiopen(sprintf('/Users/shefalirai/Desktop/Sub%d_motor_FirstLast_Corr.dscalar.nii', sub),'/Applications/workbench/bin_macosx64/wb_command');
        motor_reg_matched_cifti{sub}=motor_reg_matched_cifti{sub}.cdata;
    catch
        fprintf('error\n')
    end
end

AvgSub_Reli_Motor_Reg=(motor_reg_matched_cifti{1}+motor_reg_matched_cifti{2}+ motor_reg_matched_cifti{3}+ motor_reg_matched_cifti{4}+ motor_reg_matched_cifti{5}+ motor_reg_matched_cifti{6}+ motor_reg_matched_cifti{7}+motor_reg_matched_cifti{9}+motor_reg_matched_cifti{10})/9;

%Open subject's original cifti
subject_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');

% Replace original .cdata with correlated data
subject_cifti.cdata=AvgSub_Reli_Motor_Reg;
ciftisavereset(subject_cifti, '/Users/shefalirai/Desktop/AvgSub_Reli_Motor_Reg.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');

%MotorReliability parcellated
inputFile='/Users/shefalirai/Desktop/AvgSub_Reli_Motor_Reg.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/AvgSub_Reli_Motor_Reg_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Avg_ReliParc_MotorMatched_Reg=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_ReliParc_MotorMatched_Reg=Avg_ReliParc_MotorMatched_Reg.cdata;

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
Avg_ReliParc_MotorMatched_Reg(:,2)=AvgSub_NETS;

parcelFile='/Volumes/LaCie/Motor_matched_REGRESSED_9subs/AvgSub_Reli_Motor_Reg_1000parc.pscalar.nii'; 
Avg_ReliParc_MotorMatched=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_ReliParc_MotorMatched=Avg_ReliParc_MotorMatched.cdata;
Avg_ReliParc_MotorMatched(:,2)=AvgSub_NETS;

%% Relative reliability between Motor and Rest_motor matched and only 9 subjects WITH REGRESSION

%Open Rest reliability first
File='/Volumes/LaCie/REST_Motor_matched_9subs/AvgSub_Reli_Rest.dscalar.nii'; 
AvgSub_Reli_Rest=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Rest=AvgSub_Reli_Rest.cdata;

%Open Motor reliability
File='/Volumes/LaCie/Motor_matched_REGRESSED_9subs/AvgSub_Reli_Motor_Reg.dscalar.nii'; 
AvgSub_Reli_Motor_Reg=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_Motor_Reg=AvgSub_Reli_Motor_Reg.cdata;


%Calculate difference between motor and rest 
Relative_MotorReli_Reg=AvgSub_Reli_Motor_Reg-AvgSub_Reli_Rest;

%Open subject's original cifti
subject_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');

% Replace original .cdata with correlated data
subject_cifti.cdata=Relative_MotorReli_Reg;
ciftisavereset(subject_cifti, '/Users/shefalirai/Desktop/AvgSub_Relative_MotorReli_Reg.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');

%Relative Reliability parcellated
inputFile='/Volumes/LaCie/Motor_matched_REGRESSED_9subs/AvgSub_Relative_MotorReli_Reg.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/AvgSub_Relative_MotorReli_Reg_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Avg_ReliParc_MotorMatched_Reg=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_ReliParc_MotorMatched_Reg=Avg_ReliParc_MotorMatched_Reg.cdata;




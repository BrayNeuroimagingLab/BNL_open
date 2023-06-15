%LME code ROI_testretest across subjects

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

% Save mean signal as a Cifti
for subject=1:10
        if subject==10
            try
                j=subject;
                sub_cifti=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC%d/sub-MSC%d/MNINonLinear/Results/task-rest_ses-func01_smoothed_midrefvolume/task-rest_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',j,j)),'/Applications/workbench/bin_macosx64/wb_command');
                sub_cifti.cdata=Rest_Mean_eachsub{1,subject};
                ciftisavereset(sub_cifti, sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Rest_Mean_motormatched_noMSC08.dtseries.nii',j), '/Applications/workbench/bin_macosx64/wb_command');
            catch
             fprintf('error\n')
            end
        elseif subject~=10
            try
                j=subject;
                sub_cifti=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC0%d/sub-MSC0%d/MNINonLinear/Results/task-rest_ses-func01_smoothed_midrefvolume/task-rest_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',j,j)),'/Applications/workbench/bin_macosx64/wb_command');
                sub_cifti.cdata=Rest_Mean_eachsub{1,subject};
                ciftisavereset(sub_cifti, sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Rest_Mean_motormatched_noMSC08.dtseries.nii',j), '/Applications/workbench/bin_macosx64/wb_command');
            catch
             fprintf('error\n')
            end
        end
end


% Save SD as a Cifti
for subject=1:10
        if subject==10
            try
                j=subject;
                sub_cifti=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC%d/sub-MSC%d/MNINonLinear/Results/task-rest_ses-func01_smoothed_midrefvolume/task-rest_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',j,j)),'/Applications/workbench/bin_macosx64/wb_command');
                sub_cifti.cdata=Rest_SD_eachsub{1,subject};
                ciftisavereset(sub_cifti, sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Rest_SD_motormatched_noMSC08.dtseries.nii',j), '/Applications/workbench/bin_macosx64/wb_command');
            catch
             fprintf('error\n')
            end
        elseif subject~=10
            try
                j=subject;
                sub_cifti=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC0%d/sub-MSC0%d/MNINonLinear/Results/task-rest_ses-func01_smoothed_midrefvolume/task-rest_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',j,j)),'/Applications/workbench/bin_macosx64/wb_command');
                sub_cifti.cdata=Rest_SD_eachsub{1,subject};
                ciftisavereset(sub_cifti, sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Rest_SD_motormatched_noMSC08.dtseries.nii',j), '/Applications/workbench/bin_macosx64/wb_command');
            catch
             fprintf('error\n')
            end
        end
end


%parcellate MS
for subject=1:10
        if subject==10
            try
                j=subject;
                inputFile=sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Rest_Mean_motormatched_noMSC08.dtseries.nii',j);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Rest_Mean_motormatched_noMSC08.ptseries.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_rest_mean_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_rest_mean_parc{subject}=sub_rest_mean_parc{subject}.cdata;
            catch
             fprintf('error\n')
            end
        elseif subject~=10
            try
                j=subject;
                inputFile=sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Rest_Mean_motormatched_noMSC08.dtseries.nii',j);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Rest_Mean_motormatched_noMSC08.ptseries.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_rest_mean_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_rest_mean_parc{subject}=sub_rest_mean_parc{subject}.cdata;            catch
             fprintf('error\n')
            end
        end
end

%parcellate SD
for subject=1:10
        if subject==10
            try
                j=subject;
                inputFile=sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Rest_SD_motormatched_noMSC08.dtseries.nii',j);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Rest_SD_motormatched_noMSC08.ptseries.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_rest_sd_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_rest_sd_parc{subject}=sub_rest_sd_parc{subject}.cdata;
            catch
             fprintf('error\n')
            end
        elseif subject~=10
            try
                j=subject;
                inputFile=sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Rest_SD_motormatched_noMSC08.dtseries.nii',j);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Rest_SD_motormatched_noMSC08.ptseries.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_rest_sd_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_rest_sd_parc{subject}=sub_rest_sd_parc{subject}.cdata;            catch
             fprintf('error\n')
            end
        end
end

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
for subject=1:10
    try 
       sub_rest_mean_parc{subject}(:,2)=AvgSub_NETS;
       sub_rest_sd_parc{subject}(:,2)=AvgSub_NETS;
    catch
        fprintf('error\n')
    end
end

save("sub_rest_mean_parc.mat", "sub_rest_mean_parc");
save("sub_rest_sd_parc.mat", "sub_rest_sd_parc");

%parcellate rest reliability by subject
for subject=1:10
            try
                j=subject;
                inputFile=sprintf('/Volumes/LaCie/REST_Motor_matched_9subs/Sub%d_rest_FirstLast_Corr.dscalar.nii',j);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Volumes/LaCie/REST_Motor_matched_9subs/Sub%d_rest_FirstLast_Corr_Parc.pscalar.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_rest_reli_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_rest_reli_parc{subject}=sub_rest_reli_parc{subject}.cdata;
            catch
             fprintf('error\n')
            end
end

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

[Motor_Mean_Sub, Motor_Mean_eachsub]=MeanSignal_Values_Jan2023(motors_matched_nomc);
[Motor_SD_Sub, Motor_SD_eachsub]=SD_Values_Jan2023(motors_matched_mc);

% Save mean signal as a Cifti
for subject=1:10
        if subject==10
            try
                j=subject;
                sub_cifti=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC%d/sub-MSC%d/MNINonLinear/Results/task-motor_run1_ses-func01_smoothed_midrefvolume/task-motor_run1_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',j,j)),'/Applications/workbench/bin_macosx64/wb_command');
                sub_cifti.cdata=Motor_Mean_eachsub{1,subject};
                ciftisavereset(sub_cifti, sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Motor_Mean_motormatched_noMSC08.dtseries.nii',j), '/Applications/workbench/bin_macosx64/wb_command');
            catch
             fprintf('error\n')
            end
        elseif subject~=10
            try
                j=subject;
                sub_cifti=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC0%d/sub-MSC0%d/MNINonLinear/Results/task-motor_run1_ses-func01_smoothed_midrefvolume/task-motor_run1_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',j,j)),'/Applications/workbench/bin_macosx64/wb_command');
                sub_cifti.cdata=Motor_Mean_eachsub{1,subject};
                ciftisavereset(sub_cifti, sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Motor_Mean_motormatched_noMSC08.dtseries.nii',j), '/Applications/workbench/bin_macosx64/wb_command');
            catch
             fprintf('error\n')
            end
        end
end


% Save SD as a Cifti
for subject=1:10
        if subject==10
            try
                j=subject;
                sub_cifti=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC%d/sub-MSC%d/MNINonLinear/Results/task-motor_run1_ses-func01_smoothed_midrefvolume/task-motor_run1_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',j,j)),'/Applications/workbench/bin_macosx64/wb_command');
                sub_cifti.cdata=Motor_SD_eachsub{1,subject};
                ciftisavereset(sub_cifti, sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Motor_SD_motormatched_noMSC08.dtseries.nii',j), '/Applications/workbench/bin_macosx64/wb_command');
            catch
             fprintf('error\n')
            end
        elseif subject~=10
            try
                j=subject;
                sub_cifti=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC0%d/sub-MSC0%d/MNINonLinear/Results/task-motor_run1_ses-func01_smoothed_midrefvolume/task-motor_run1_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',j,j)),'/Applications/workbench/bin_macosx64/wb_command');
                sub_cifti.cdata=Motor_SD_eachsub{1,subject};
                ciftisavereset(sub_cifti, sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Motor_SD_motormatched_noMSC08.dtseries.nii',j), '/Applications/workbench/bin_macosx64/wb_command');
            catch
             fprintf('error\n')
            end
        end
end


%parcellate MS
for subject=1:10
        if subject==10
            try
                j=subject;
                inputFile=sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Motor_Mean_motormatched_noMSC08.dtseries.nii',j);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Motor_Mean_motormatched_noMSC08.ptseries.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_motor_mean_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_motor_mean_parc{subject}=sub_motor_mean_parc{subject}.cdata;
            catch
             fprintf('error\n')
            end
        elseif subject~=10
            try
                j=subject;
                inputFile=sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Motor_Mean_motormatched_noMSC08.dtseries.nii',j);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Motor_Mean_motormatched_noMSC08.ptseries.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_motor_mean_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_motor_mean_parc{subject}=sub_motor_mean_parc{subject}.cdata;            catch
             fprintf('error\n')
            end
        end
end

%parcellate SD
for subject=1:10
        if subject==10
            try
                j=subject;
                inputFile=sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Motor_SD_motormatched_noMSC08.dtseries.nii',j);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Motor_SD_motormatched_noMSC08.ptseries.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_motor_sd_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_motor_sd_parc{subject}=sub_motor_sd_parc{subject}.cdata;
            catch
             fprintf('error\n')
            end
        elseif subject~=10
            try
                j=subject;
                inputFile=sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Motor_SD_motormatched_noMSC08.dtseries.nii',j);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Motor_SD_motormatched_noMSC08.ptseries.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_motor_sd_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_motor_sd_parc{subject}=sub_motor_sd_parc{subject}.cdata;            catch
             fprintf('error\n')
            end
        end
end

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
for subject=1:10
    try 
       sub_motor_mean_parc{subject}(:,2)=AvgSub_NETS;
       sub_motor_sd_parc{subject}(:,2)=AvgSub_NETS;
    catch
        fprintf('error\n')
    end
end

save("sub_motor_mean_parc.mat", "sub_motor_mean_parc");
save("sub_motor_sd_parc.mat", "sub_motor_sd_parc");

%% MOTOR - REST

%calculate different from motor to rest
for subject=1:10
    sub_relativemean_motor_parc{subject}=sub_motor_mean_parc{subject}-sub_rest_mean_parc{subject};
    sub_relativesd_motor_parc{subject}=sub_motor_sd_parc{subject}-sub_rest_sd_parc{subject};
end

%open reliability
for subject=1:10
        try
            sub_reli{subject}=ciftiopen(sprintf('/Volumes/LaCie/Rest_analysis/Sub%d_rest_FirstLast_Corr.dscalar.nii',subject),'/Applications/workbench/bin_macosx64/wb_command');
            sub_reli{subject}=sub_reli{subject}.cdata;
        catch
            fprintf('error\n')
        end
end

save("sub_rest_reliability_full.mat", "sub_reli");

%parcellate rest full reliability
for subject=1:10
            try
                inputFile=sprintf('/Volumes/LaCie/Rest_analysis/Sub%d_rest_FirstLast_Corr.dscalar.nii',subject);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Volumes/LaCie/Rest_analysis/Sub%d_rest_FirstLast_Corr.pscalar.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_rest_reli_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_rest_reli_parc{subject}=sub_rest_reli_parc{subject}.cdata;
            catch
             fprintf('error\n')
            end
end


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

[Glass_Mean_Sub, Glass_Mean_eachsub]=MeanSignal_Values_Jan2023(glass_matched_nomc);
[Glass_SD_Sub, Glass_SD_eachsub]=SD_Values_Jan2023(glass_matched_mc);


% Save mean signal as a Cifti
for subject=1:10
        if subject==10
            try
                j=subject;
                sub_cifti=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC%d/sub-MSC%d/MNINonLinear/Results/task-glasslexical_run01_ses-func01_smoothed_midrefvolume/task-glasslexical_run01_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',j,j)),'/Applications/workbench/bin_macosx64/wb_command');
                sub_cifti.cdata=Glass_Mean_eachsub{1,subject};
                ciftisavereset(sub_cifti, sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Glass_Mean_motormatched_noMSC08.dtseries.nii',j), '/Applications/workbench/bin_macosx64/wb_command');
            catch
             fprintf('error\n')
            end
        elseif subject~=10
            try
                j=subject;
                sub_cifti=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC0%d/sub-MSC0%d/MNINonLinear/Results/task-glasslexical_run01_ses-func01_smoothed_midrefvolume/task-glasslexical_run01_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',j,j)),'/Applications/workbench/bin_macosx64/wb_command');
                sub_cifti.cdata=Glass_Mean_eachsub{1,subject};
                ciftisavereset(sub_cifti, sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Glass_Mean_motormatched_noMSC08.dtseries.nii',j), '/Applications/workbench/bin_macosx64/wb_command');
            catch
             fprintf('error\n')
            end
        end
end


% Save SD as a Cifti
for subject=1:10
        if subject==10
            try
                j=subject;
                sub_cifti=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC%d/sub-MSC%d/MNINonLinear/Results/task-glasslexical_run01_ses-func01_smoothed_midrefvolume/task-glasslexical_run01_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',j,j)),'/Applications/workbench/bin_macosx64/wb_command');
                sub_cifti.cdata=Glass_SD_eachsub{1,subject};
                ciftisavereset(sub_cifti, sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Glass_SD_motormatched_noMSC08.dtseries.nii',j), '/Applications/workbench/bin_macosx64/wb_command');
            catch
             fprintf('error\n')
            end
        elseif subject~=10
            try
                j=subject;
                sub_cifti=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC0%d/sub-MSC0%d/MNINonLinear/Results/task-glasslexical_run01_ses-func01_smoothed_midrefvolume/task-glasslexical_run01_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',j,j)),'/Applications/workbench/bin_macosx64/wb_command');
                sub_cifti.cdata=Glass_SD_eachsub{1,subject};
                ciftisavereset(sub_cifti, sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Glass_SD_motormatched_noMSC08.dtseries.nii',j), '/Applications/workbench/bin_macosx64/wb_command');
            catch
             fprintf('error\n')
            end
        end
end


%parcellate MS
for subject=1:10
        if subject==10
            try
                j=subject;
                inputFile=sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Glass_Mean_motormatched_noMSC08.dtseries.nii',j);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Glass_Mean_motormatched_noMSC08.ptseries.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_glass_mean_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_glass_mean_parc{subject}=sub_glass_mean_parc{subject}.cdata;
            catch
             fprintf('error\n')
            end
        elseif subject~=10
            try
                j=subject;
                inputFile=sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Glass_Mean_motormatched_noMSC08.dtseries.nii',j);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Glass_Mean_motormatched_noMSC08.ptseries.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_glass_mean_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_glass_mean_parc{subject}=sub_glass_mean_parc{subject}.cdata;            
            catch
             fprintf('error\n')
            end
        end
end

%parcellate SD
for subject=1:10
        if subject==10
            try
                j=subject;
                inputFile=sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Glass_SD_motormatched_noMSC08.dtseries.nii',j);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Glass_SD_motormatched_noMSC08.ptseries.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_glass_sd_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_glass_sd_parc{subject}=sub_glass_sd_parc{subject}.cdata;
            catch
             fprintf('error\n')
            end
        elseif subject~=10
            try
                j=subject;
                inputFile=sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Glass_SD_motormatched_noMSC08.dtseries.nii',j);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Glass_SD_motormatched_noMSC08.ptseries.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_glass_sd_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_glass_sd_parc{subject}=sub_glass_sd_parc{subject}.cdata;            catch
             fprintf('error\n')
            end
        end
end

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
for subject=1:10
    try 
       sub_glass_mean_parc{subject}(:,2)=AvgSub_NETS;
       sub_glass_sd_parc{subject}(:,2)=AvgSub_NETS;
    catch
        fprintf('error\n')
    end
end

save("sub_glass_mean_parc.mat", "sub_glass_mean_parc");
save("sub_glass_sd_parc.mat", "sub_glass_sd_parc");


%% Glass - REST

%calculate different from Glass to rest
for subject=1:10
    sub_relativemean_glass_parc{subject}=sub_glass_mean_parc{subject}-sub_rest_mean_parc{subject};
    sub_relativesd_glass_parc{subject}=sub_glass_sd_parc{subject}-sub_rest_sd_parc{subject};
end

%open reliability
for subject=1:10
        try
            sub_reli{subject}=ciftiopen(sprintf('/Volumes/LaCie/Rest_analysis/Sub%d_rest_FirstLast_Corr.dscalar.nii',subject),'/Applications/workbench/bin_macosx64/wb_command');
            sub_reli{subject}=sub_reli{subject}.cdata;
        catch
            fprintf('error\n')
        end
end


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

[Memory_Mean_Sub, Memory_Mean_eachsub]=MeanSignal_Values_Jan2023(memory_matched_nomc);
[Memory_SD_Sub, Memory_SD_eachsub]=SD_Values_Jan2023(memory_matched_mc);

% Save mean signal as a Cifti
for subject=1:10
        if subject==10
            try
                j=subject;
                sub_cifti=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC%d/sub-MSC%d/MNINonLinear/Results/task-memorywords_ses-func01_smoothed_midrefvolume/task-memorywords_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',j,j)),'/Applications/workbench/bin_macosx64/wb_command');
                sub_cifti.cdata=Memory_Mean_eachsub{1,subject};
                ciftisavereset(sub_cifti, sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Memory_Mean_motormatched_noMSC08.dtseries.nii',j), '/Applications/workbench/bin_macosx64/wb_command');
            catch
             fprintf('error\n')
            end
        elseif subject~=10
            try
                j=subject;
                sub_cifti=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC0%d/sub-MSC0%d/MNINonLinear/Results/task-memorywords_ses-func01_smoothed_midrefvolume/task-memorywords_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',j,j)),'/Applications/workbench/bin_macosx64/wb_command');
                sub_cifti.cdata=Memory_Mean_eachsub{1,subject};
                ciftisavereset(sub_cifti, sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Memory_Mean_motormatched_noMSC08.dtseries.nii',j), '/Applications/workbench/bin_macosx64/wb_command');
            catch
             fprintf('error\n')
            end
        end
end


% Save SD as a Cifti
for subject=1:10
        if subject==10
            try
                j=subject;
                sub_cifti=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC%d/sub-MSC%d/MNINonLinear/Results/task-memorywords_ses-func01_smoothed_midrefvolume/task-memorywords_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',j,j)),'/Applications/workbench/bin_macosx64/wb_command');
                sub_cifti.cdata=Memory_SD_eachsub{1,subject};
                ciftisavereset(sub_cifti, sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Memory_SD_motormatched_noMSC08.dtseries.nii',j), '/Applications/workbench/bin_macosx64/wb_command');
            catch
             fprintf('error\n')
            end
        elseif subject~=10
            try
                j=subject;
                sub_cifti=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC0%d/sub-MSC0%d/MNINonLinear/Results/task-memorywords_ses-func01_smoothed_midrefvolume/task-memorywords_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',j,j)),'/Applications/workbench/bin_macosx64/wb_command');
                sub_cifti.cdata=Memory_SD_eachsub{1,subject};
                ciftisavereset(sub_cifti, sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Memory_SD_motormatched_noMSC08.dtseries.nii',j), '/Applications/workbench/bin_macosx64/wb_command');
            catch
             fprintf('error\n')
            end
        end
end


%parcellate MS
for subject=1:10
        if subject==10
            try
                j=subject;
                inputFile=sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Memory_Mean_motormatched_noMSC08.dtseries.nii',j);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Memory_Mean_motormatched_noMSC08.ptseries.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_memory_mean_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_memory_mean_parc{subject}=sub_memory_mean_parc{subject}.cdata;
            catch
             fprintf('error\n')
            end
        elseif subject~=10
            try
                j=subject;
                inputFile=sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Memory_Mean_motormatched_noMSC08.dtseries.nii',j);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Memory_Mean_motormatched_noMSC08.ptseries.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_memory_mean_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_memory_mean_parc{subject}=sub_memory_mean_parc{subject}.cdata;            
            catch
             fprintf('error\n')
            end
        end
end

%parcellate SD
for subject=1:10
        if subject==10
            try
                j=subject;
                inputFile=sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Memory_SD_motormatched_noMSC08.dtseries.nii',j);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Users/shefalirai/Desktop/sub-MSC%d_Memory_SD_motormatched_noMSC08.ptseries.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_memory_sd_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_memory_sd_parc{subject}=sub_memory_sd_parc{subject}.cdata;
            catch
             fprintf('error\n')
            end
        elseif subject~=10
            try
                j=subject;
                inputFile=sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Memory_SD_motormatched_noMSC08.dtseries.nii',j);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Users/shefalirai/Desktop/sub-MSC0%d_Memory_SD_motormatched_noMSC08.ptseries.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_memory_sd_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_memory_sd_parc{subject}=sub_memory_sd_parc{subject}.cdata;            catch
             fprintf('error\n')
            end
        end
end

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
for subject=1:10
    try 
       sub_memory_mean_parc{subject}(:,2)=AvgSub_NETS;
       sub_memory_sd_parc{subject}(:,2)=AvgSub_NETS;
    catch
        fprintf('error\n')
    end
end

save("sub_memory_mean_parc.mat", "sub_memory_mean_parc");
save("sub_memory_sd_parc.mat", "sub_memory_sd_parc");


%% MEMORY - REST

%calculate different from memory to rest
for subject=1:10
    sub_relativemean_memory_parc{subject}=sub_memory_mean_parc{subject}-sub_rest_mean_parc{subject};
    sub_relativesd_memory_parc{subject}=sub_memory_sd_parc{subject}-sub_rest_sd_parc{subject};
end

%open reliability
for subject=1:10
        try
            sub_reli{subject}=ciftiopen(sprintf('/Volumes/LaCie/Rest_analysis/Sub%d_rest_FirstLast_Corr.dscalar.nii',subject),'/Applications/workbench/bin_macosx64/wb_command');
            sub_reli{subject}=sub_reli{subject}.cdata;
        catch
            fprintf('error\n')
        end
end


%% Parcel wise and each subject wise LME reliability values
%parcel 1 mean and sd for each task per subject for LME

for subject=1:10
    motor_mean_parcel1(subject)=sub_motor_mean_parc{1,subject}(1,1);
    motor_sd_parcel1(subject)=sub_motor_sd_parc{1,subject}(1,1);
    glass_mean_parcel1(subject)=sub_glass_mean_parc{1,subject}(1,1);
    glass_sd_parcel1(subject)=sub_glass_sd_parc{1,subject}(1,1); 
   memory_mean_parcel1(subject)=sub_memory_mean_parc{1,subject}(1,1);
   memory_sd_parcel1(subject)=sub_memory_sd_parc{1,subject}(1,1); 
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Open cifti of each tasks reliability

%motor
%open reliability
for subject=1:10
        try
            sub_motor_reli{subject}=ciftiopen(sprintf('/Volumes/LaCie/Motor_matched_noregression_9subs/Sub%d_motor_FirstLast_Corr.dscalar.nii',subject),'/Applications/workbench/bin_macosx64/wb_command');
            sub_motor_reli{subject}=sub_motor_reli{subject}.cdata;
        catch
            fprintf('error\n')
        end
end

%parcellate motor reliability by subject
for subject=1:10
            try
                j=subject;
                inputFile=sprintf('/Volumes/LaCie/Motor_matched_noregression_9subs/Sub%d_motor_FirstLast_Corr.dscalar.nii',j);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Volumes/LaCie/Motor_matched_noregression_9subs/Sub%d_motor_FirstLast_Corr_Parc.pscalar.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_motor_reli_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_motor_reli_parc{subject}=sub_motor_reli_parc{subject}.cdata;
            catch
             fprintf('error\n')
            end
end


%glass
%open reliability
for subject=1:10
        try
            sub_glass_reli{subject}=ciftiopen(sprintf('/Volumes/LaCie/Glass_matched_noregression_9subs/Sub%d_glass_FirstLast_Corr.dscalar.nii',subject),'/Applications/workbench/bin_macosx64/wb_command');
            sub_glass_reli{subject}=sub_glass_reli{subject}.cdata;
        catch
            fprintf('error\n')
        end
end

%parcellate glass reliability by subject
for subject=1:10
            try
                j=subject;
                inputFile=sprintf('/Volumes/LaCie/Glass_matched_noregression_9subs/Sub%d_glass_FirstLast_Corr.dscalar.nii',j);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Volumes/LaCie/Glass_matched_noregression_9subs/Sub%d_glass_FirstLast_Corr_Parc.pscalar.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_glass_reli_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_glass_reli_parc{subject}=sub_glass_reli_parc{subject}.cdata;
            catch
             fprintf('error\n')
            end
end

%memory
%open reliability
for subject=1:10
        try
            sub_memory_reli{subject}=ciftiopen(sprintf('/Volumes/LaCie/Memory_matched_noregression_9subs/Sub%d_memory_FirstLast_Corr.dscalar.nii',subject),'/Applications/workbench/bin_macosx64/wb_command');
            sub_memory_reli{subject}=sub_memory_reli{subject}.cdata;
        catch
            fprintf('error\n')
        end
end

%parcellate memory reliability by subject
for subject=1:10
            try
                j=subject;
                inputFile=sprintf('/Volumes/LaCie/Memory_matched_noregression_9subs/Sub%d_memory_FirstLast_Corr.dscalar.nii',j);
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Volumes/LaCie/Memory_matched_noregression_9subs/Sub%d_memory_FirstLast_Corr_Parc.pscalar.nii',j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_memory_reli_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_memory_reli_parc{subject}=sub_memory_reli_parc{subject}.cdata;
            catch
             fprintf('error\n')
            end
end


for subject=1:10
    try
        motor_reli_parcel1(subject)=sub_motor_reli_parc{1,subject}(1,1);
        glass_reli_parcel1(subject)=sub_glass_reli_parc{1,subject}(1,1);
        memory_reli_parcel1(subject)=sub_memory_reli_parc{1,subject}(1,1);
    catch
      fprintf('error\n')
     end
end



%% Create LME matrix

%for all tasks and reliability cell arrays
%create a matrix of zeros with the right size
lme_data=zeros(36000,7);
% 
% for parcel=1:1000
%     for subject=1:10
%         try
%         lme_data(subject,1)=sub_rest_reli_parc{1,subject}(parcel,1); 
%         output=[lme_data; lme_data(subject,1)];
%         catch
%             fprintf('error\n')
%         end
%     end
% end

%reliability
rest_reliability = vertcat(sub_rest_reli_parc{:});
motor_reliability = vertcat(sub_motor_reli_parc{:});
language_reliability = vertcat(sub_glass_reli_parc{:});
memory_reliability = vertcat(sub_memory_reli_parc{:});

lme_data(:,1)=[rest_reliability; motor_reliability; language_reliability; memory_reliability];

%mean signal
%make sure sub 08 is empty
sub_rest_mean_parc{1,8}=[];
sub_motor_mean_parc{1,8}=[];
sub_glass_mean_parc{1,8}=[];
sub_memory_mean_parc{1,8}=[];

rest_meansignal = vertcat(sub_rest_mean_parc{:});
motor_meansignal = vertcat(sub_motor_mean_parc{:});
language_meansignal = vertcat(sub_glass_mean_parc{:});
memory_meansignal = vertcat(sub_memory_mean_parc{:});

lme_data(:,2)=[rest_meansignal(:,1); motor_meansignal(:,1); language_meansignal(:,1); memory_meansignal(:,1)];
lme_data(:,7)=[rest_meansignal(:,2); motor_meansignal(:,2); language_meansignal(:,2); memory_meansignal(:,2)];

%SD
%make sure sub 08 is empty
sub_rest_sd_parc{1,8}=[];
sub_motor_sd_parc{1,8}=[];
sub_glass_sd_parc{1,8}=[];
sub_memory_sd_parc{1,8}=[];

rest_sd = vertcat(sub_rest_sd_parc{:});
motor_sd = vertcat(sub_motor_sd_parc{:});
language_sd = vertcat(sub_glass_sd_parc{:});
memory_sd = vertcat(sub_memory_sd_parc{:});

lme_data(:,3)=[rest_sd(:,1); motor_sd(:,1); language_sd(:,1); memory_sd(:,1)];

%add subject column
subs = [1:7,9:10];
lme_data(:,4)=[repelem(subs,1000)'; repelem(subs,1000)'; repelem(subs,1000)'; repelem(subs,1000)'];

%add parcel column
lme_data(:,5)=repmat((reshape( 1:1000, 1, 1000) .'), 36, 1);

%add task name column
%Rest=1
%Motor=2
%Language=3
%Memory=4

task=[1:4];
lme_data(:,6)=[repelem(task,9000)'];

%% Each subject's 2nd Level PEs per task 

%parcellate PE for each subject for motor
for subject=1:10
        if subject==10
            try
                j=subject;
                inputFile=(sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC%d/sub-MSC%d/MNINonLinear/Results/2ndLevel_Motors_NoMSC08_Stats_average5copes_LMEdata_pe%d_subject%d.dscalar.nii',j,j,j,j));
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC%d/sub-MSC%d/MNINonLinear/Results/2ndLevel_Motors_NoMSC08_Stats_average5copes_LMEdata_pe%d_subject%d_Parc.pscalar.nii',j,j,j,j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_motor_PE_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_motor_PE_parc{subject}=sub_motor_PE_parc{subject}.cdata;
            catch
             fprintf('error\n')
            end
        elseif subject~=10
            try
                j=subject;
                inputFile=(sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC0%d/sub-MSC0%d/MNINonLinear/Results/2ndLevel_Motors_NoMSC08_Stats_average5copes_LMEdata_pe%d_subject%d.dscalar.nii',j,j,j,j));
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC0%d/sub-MSC0%d/MNINonLinear/Results/2ndLevel_Motors_NoMSC08_Stats_average5copes_LMEdata_pe%d_subject%d_Parc.pscalar.nii',j,j,j,j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_motor_PE_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_motor_PE_parc{subject}=sub_motor_PE_parc{subject}.cdata;
            catch
             fprintf('error\n')
            end
        end
end




%parcellate PE for each subject for glass
for subject=1:10
        if subject==10
            try
                j=subject;
                inputFile=(sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC%d/sub-MSC%d/MNINonLinear/Results/2ndLevel_Glass_NoMSC08_Stats_average8copes_LMEdata_pe%d_subject%d.dscalar.nii',j,j,j,j));
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC%d/sub-MSC%d/MNINonLinear/Results/2ndLevel_Glass_NoMSC08_Stats_average8copes_LMEdata_pe%d_subject%d_Parc.pscalar.nii',j,j,j,j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_glass_PE_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_glass_PE_parc{subject}=sub_glass_PE_parc{subject}.cdata;
            catch
             fprintf('error\n')
            end
        elseif subject~=10
            try
                j=subject;
                inputFile=(sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC0%d/sub-MSC0%d/MNINonLinear/Results/2ndLevel_Glass_NoMSC08_Stats_average8copes_LMEdata_pe%d_subject%d.dscalar.nii',j,j,j,j));
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC0%d/sub-MSC0%d/MNINonLinear/Results/2ndLevel_Glass_NoMSC08_Stats_average8copes_LMEdata_pe%d_subject%d_Parc.pscalar.nii',j,j,j,j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_glass_PE_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_glass_PE_parc{subject}=sub_glass_PE_parc{subject}.cdata;
            catch
             fprintf('error\n')
            end
        end
end



%parcellate PE for each subject for Memory
for subject=1:10
        if subject==10
            try
                j=subject;
                inputFile=(sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC%d/sub-MSC%d/MNINonLinear/Results/2ndLevel_AllMemory_NoMSC08_Stats_average9copes_LMEdata_pe%d_subject%d.dscalar.nii',j,j,j,j));
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC%d/sub-MSC%d/MNINonLinear/Results/2ndLevel_AllMemory_NoMSC08_Stats_average9copes_LMEdata_pe%d_subject%d_Parc.pscalar.nii',j,j,j,j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_memory_PE_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_memory_PE_parc{subject}=sub_memory_PE_parc{subject}.cdata;
            catch
             fprintf('error\n')
            end
        elseif subject~=10
            try
                j=subject;
                inputFile=(sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC0%d/sub-MSC0%d/MNINonLinear/Results/2ndLevel_AllMemory_NoMSC08_Stats_average9copes_LMEdata_pe%d_subject%d.dscalar.nii',j,j,j,j));
                parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
                parcelFile=sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC0%d/sub-MSC0%d/MNINonLinear/Results/2ndLevel_AllMemory_NoMSC08_Stats_average9copes_LMEdata_pe%d_subject%d_Parc.pscalar.nii',j,j,j,j); 
                eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
                sub_memory_PE_parc{subject}=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
                sub_memory_PE_parc{subject}=sub_memory_PE_parc{subject}.cdata;
            catch
             fprintf('error\n')
            end
        end
end

motor_PE = vertcat(sub_motor_PE_parc{:});
language_PE = vertcat(sub_glass_PE_parc{:});
memory_PE = vertcat(sub_memory_PE_parc{:});

rest_PE=zeros(9000,1);
alltasks_PE=[rest_PE; motor_PE; language_PE; memory_PE];

%% Transfer from LME_Excel sheet

LME_betas =readtable('/Users/shefalirai/Desktop/LME_betas_eachparcel_dataframe.xlsx');
meansignal_betas = LME_betas(LME_betas.term=="`Mean Signal`", : );
meansignal_betas(:,1)=[];


sd_betas = LME_betas(LME_betas.term=="SD", : );
sd_betas(:,1)=[];


pe_betas = LME_betas(LME_betas.term=="PE", : );
pe_betas(:,1)=[];

%nsert row 555 and 908 as zeros (parcels with missing values) to
%have a final 1000 x 2 table
rowNum =555;
meansignal_betas_new = meansignal_betas([1:rowNum,rowNum:end], :); 
meansignal_betas_new{rowNum,:} = [0, rowNum]; 

rowNum =908;
meansignal_betas_new = meansignal_betas_new([1:rowNum,rowNum:end], :); 
meansignal_betas_new{rowNum,:} = [0, rowNum]; 


rowNum =555;
sd_betas_new = sd_betas([1:rowNum,rowNum:end], :); 
sd_betas_new{rowNum,:} = [0, rowNum]; 

rowNum =908;
sd_betas_new = sd_betas_new([1:rowNum,rowNum:end], :); 
sd_betas_new{rowNum,:} = [0, rowNum]; 


rowNum =555;
pe_betas_new = pe_betas([1:rowNum,rowNum:end], :); 
pe_betas_new{rowNum,:} = [0, rowNum]; 

rowNum =908;
pe_betas_new = pe_betas_new([1:rowNum,rowNum:end], :); 
pe_betas_new{rowNum,:} = [0, rowNum]; 

%convert to array
meansignal_betas_new=table2array(meansignal_betas_new);
sd_betas_new=table2array(sd_betas_new);
pe_betas_new=table2array(pe_betas_new);
meansignal_betas_new(:,2)=[];
sd_betas_new(:,2)=[];
pe_betas_new(:,2)=[];


%parcellate averaged timeseries so we can visualize on a parcel level
inputFile='/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='//Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])

%save as cifti to visualize betas across the averaged brain 
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=meansignal_betas_new;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/LME_meansignal_betas_motormatched_noMSC08.ptseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=sd_betas_new;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/LME_sd_betas_motormatched_noMSC08.ptseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=pe_betas_new;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/LME_pe_betas_motormatched_noMSC08.ptseries.nii', '/Applications/workbench/bin_macosx64/wb_command');



%Rest full data excluding MSC08, Reliability, SD, TSNR and Mean
%Calculations
%Not motor matched for full rest reliability values!

Sub1=ciftiopen('/Volumes/LaCie/Rest_analysis/Sub1_rest_FirstLast_Corr.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');
Sub1=Sub1.cdata;
Sub2=ciftiopen('/Volumes/LaCie/Rest_analysis/Sub2_rest_FirstLast_Corr.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');
Sub3=ciftiopen('/Volumes/LaCie/Rest_analysis/Sub3_rest_FirstLast_Corr.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');
Sub4=ciftiopen('/Volumes/LaCie/Rest_analysis/Sub4_rest_FirstLast_Corr.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');
Sub5=ciftiopen('/Volumes/LaCie/Rest_analysis/Sub5_rest_FirstLast_Corr.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');
Sub6=ciftiopen('/Volumes/LaCie/Rest_analysis/Sub6_rest_FirstLast_Corr.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');
Sub7=ciftiopen('/Volumes/LaCie/Rest_analysis/Sub7_rest_FirstLast_Corr.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');
Sub9=ciftiopen('/Volumes/LaCie/Rest_analysis/Sub9_rest_FirstLast_Corr.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');
Sub10=ciftiopen('/Volumes/LaCie/Rest_analysis/Sub10_rest_FirstLast_Corr.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');
Sub2=Sub2.cdata;
Sub3=Sub3.cdata;
Sub4=Sub4.cdata;
Sub5=Sub5.cdata;
Sub6=Sub6.cdata;
Sub7=Sub7.cdata;
Sub9=Sub9.cdata;
Sub10=Sub10.cdata;
AvgSub_Reli_Rest_NOMSC08=Test_Retest_MSC(Sub1, Sub2, Sub3, Sub4, Sub5, Sub6, Sub7, Sub9, Sub10, 'rest');

% Save Avg_tSNR as a Cifti
main_task='rest';
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=AvgSub_Reli_Rest_NOMSC08;
ciftisavereset(Avg_cifti, sprintf('/Users/shefalirai/Desktop/AvgSub_ReliWITHOUTSUB08_%s.dscalar.nii', main_task), '/Applications/workbench/bin_macosx64/wb_command');

%Rest Reliability parcellated
inputFile='/Users/shefalirai/Desktop/AvgSub_ReliWITHOUTSUB08_rest.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/AvgSub_ReliWITHOUTSUB08_rest_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Avg_ReliParc_Rest_NOMSC08=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_ReliParc_Rest_NOMSC08=Avg_ReliParc_Rest_NOMSC08.cdata;

AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
Avg_ReliParc_Rest_NOMSC08(:,2)=AvgSub_NETS;


%rest
for i=1:10
    for j=1:10
        MSCrest{i,j}=size(allsessions_allsubjects_rest_rm{1,j}{i,1});
        MSCrest{i,j}=MSCrest{i,j}(:,2);
    end
end

for i=1:10
    for j=1:10
        MSCmemorywords{i,j}=size(allsessions_allsubjects_memorywords_rm{1,j}{i,1});
        MSCmemorywords{i,j}=MSCmemorywords{i,j}(:,2);
    end
end


%Fig3 Mean,SD,tSNR for rest after calculating Signal_Property_Values.m

% Save Avg_tSNR as a Cifti
main_task='rest';
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Avg_tSNR_Sub;
ciftisavereset(Avg_cifti, sprintf('/Users/shefalirai/Desktop/Avg_tSNR_%s.dtseries.nii', main_task), '/Applications/workbench/bin_macosx64/wb_command');

% Save Avg_SD as a Cifti
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Avg_SD_Sub;
ciftisavereset(Avg_cifti, sprintf('/Users/shefalirai/Desktop/Avg_SD_%s.dtseries.nii', main_task), '/Applications/workbench/bin_macosx64/wb_command');

% Save Avg_MeanSignal as a Cifti
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Avg_Mean_Sub;
ciftisavereset(Avg_cifti, sprintf('/Users/shefalirai/Desktop/Avg_Mean_%s.dtseries.nii', main_task), '/Applications/workbench/bin_macosx64/wb_command');

%% Standard deviation of reliability 

AvgSub_Reli_FullRest=[Sub1,Sub2,Sub3,Sub4,Sub5,Sub6,Sub7,Sub9,Sub10];
AvgSub_StdofReli_FullRest=std(AvgSub_Reli_FullRest,[],2);

%save cifti 
Avg_cifti=ciftiopen(['/Volumes/LaCie/REST_Motor_matched_9subs/AvgSub_Reli_Rest.dscalar.nii'],'/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=AvgSub_StdofReli_FullRest;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/AvgSub_StdofReli_NoMSC08.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');







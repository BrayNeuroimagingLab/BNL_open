%Parcellate PEs from 3rd level 

%Motor
%open PE files
Motor_PE=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/Motors_3rdLevel_Stats_5Copescombined_pe1.dscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
Motor_PE=Motor_PE.cdata;

%parcellate
inputFile='/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/Motors_3rdLevel_Stats_5Copescombined_pe1.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/Motor_3rdlevel_PEs_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Motor_PE_parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Motor_PE_parc=Motor_PE_parc.cdata;

%Glass
%open PE files
Glass_PE=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/Glass_3rdLevel_Stats_10Copescombined_pe1.dscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_PE=Glass_PE.cdata;

%parcellate
inputFile='/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/Glass_3rdLevel_Stats_10Copescombined_pe1.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/Glass_3rdlevel_PEs_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Glass_PE_parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Glass_PE_parc=Glass_PE_parc.cdata;

%Memory
%open PE files
Memory_PE=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/Memory_3rdLevel_Stats_3Copescombined_pe1.dscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_PE=Memory_PE.cdata;

%parcellate
inputFile='/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/Memory_3rdLevel_Stats_3Copescombined_pe1.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/Memory_3rdlevel_PEs_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Memory_PE_parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Memory_PE_parc=Memory_PE_parc.cdata;

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
Motor_PE_parc(:,2)=AvgSub_NETS;
Glass_PE_parc(:,2)=AvgSub_NETS;
Memory_PE_parc(:,2)=AvgSub_NETS;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Task effects/zstat from 3rd level & parcellate

%Motor
%open PE files
Motor_ZSTAT=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/Motors_3rdLevel_Stats_5Copescombined_zstat1.dscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
Motor_ZSTAT=Motor_ZSTAT.cdata;

%parcellate
inputFile='/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/Motors_3rdLevel_Stats_5Copescombined_zstat1.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/Motor_3rdlevel_ZSTAT_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Motor_ZSTAT_parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Motor_ZSTAT_parc=Motor_ZSTAT_parc.cdata;

%Glass
%open ZSTAT files
Glass_ZSTAT=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/Glass_3rdLevel_Stats_10Copescombined_zstat1.dscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_ZSTAT=Glass_ZSTAT.cdata;

%parcellate
inputFile='/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/Glass_3rdLevel_Stats_10Copescombined_zstat1.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/Glass_3rdlevel_ZSTAT_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Glass_ZSTAT_parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Glass_ZSTAT_parc=Glass_ZSTAT_parc.cdata;

%Memory
%open ZSTAT files
Memory_ZSTAT=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/Memory_3rdLevel_Stats_3Copescombined_zstat1.dscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_ZSTAT=Memory_ZSTAT.cdata;

%parcellate
inputFile='/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/Memory_3rdLevel_Stats_3Copescombined_zstat1.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/Memory_3rdlevel_ZSTAT_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Memory_ZSTAT_parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Memory_ZSTAT_parc=Memory_ZSTAT_parc.cdata;

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
Motor_ZSTAT_parc(:,2)=AvgSub_NETS;
Glass_ZSTAT_parc(:,2)=AvgSub_NETS;
Memory_ZSTAT_parc(:,2)=AvgSub_NETS;




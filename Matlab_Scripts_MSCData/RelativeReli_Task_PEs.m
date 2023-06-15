%% MOTOR Relative reliability versus Beta values from 3rd level

Avg_cifti=ciftiopen('/Volumes/LaCie/Motor_matched_REGRESSED_9subs/AvgSub_Relative_MotorReli_Reg_1000parc.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
Motor_Reg_RelativeReli=Avg_cifti.cdata;

%1 to 5 PE (bet values)
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-motor_pe1_3rdlevel_beta/task-motor_pe1_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Motor_PE1=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-motor_pe2_3rdlevel_beta/task-motor_pe2_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Motor_PE2=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-motor_pe3_3rdlevel_beta/task-motor_pe3_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Motor_PE3=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-motor_pe4_3rdlevel_beta/task-motor_pe4_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Motor_PE4=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-motor_pe5_3rdlevel_beta/task-motor_pe5_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Motor_PE5=Avg_cifti.cdata;

AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;


%average across all 5 PEs
Avg_Motor_PEs=(Motor_PE1+ Motor_PE2 + Motor_PE3+ Motor_PE4 + Motor_PE5)/5;

% Save Avg_PEs as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Avg_Motor_PEs;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Avg_Motor_PEs.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');


Avg_cifti=ciftiopen('/Volumes/LaCie/Motor_matched_REGRESSED_9subs/AvgSub_Relative_MotorReli_Reg.dscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
Motor_Reg_RelativeReli_vertex=Avg_cifti.cdata;
scatter(Avg_Motor_PEs, Motor_Reg_RelativeReli_vertex);
hold on
%parcellate PEs file
inputFile='/Users/shefalirai/Desktop/Avg_Motor_PEs.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/Avg_Motor_PEs_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Avg_Motor_PEs_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_Motor_PEs_Parc=Avg_Motor_PEs_Parc.cdata;

scatter(Avg_Motor_PEs_Parc, Motor_Reg_RelativeReli);

%% Glass Relative reliability versus Beta values from 3rd level

Avg_cifti=ciftiopen('/Volumes/LaCie/Glass_matched_REGRESSED_9subs/AvgSub_Relative_GlassReli_Reg_1000parc.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_Reg_RelativeReli=Avg_cifti.cdata;

%1 to 10 PE (bet values)
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-glass_pe1_3rdlevel_beta/task-glass_pe1_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_PE1=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-glass_pe2_3rdlevel_beta/task-glass_pe2_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_PE2=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-glass_pe3_3rdlevel_beta/task-glass_pe3_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_PE3=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-glass_pe4_3rdlevel_beta/task-glass_pe4_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_PE4=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-glass_pe5_3rdlevel_beta/task-glass_pe5_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_PE5=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-glass_pe6_3rdlevel_beta/task-glass_pe6_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_PE6=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-glass_pe7_3rdlevel_beta/task-glass_pe7_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_PE7=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-glass_pe8_3rdlevel_beta/task-glass_pe8_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_PE8=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-glass_pe9_3rdlevel_beta/task-glass_pe9_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_PE9=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-glass_pe10_3rdlevel_beta/task-glass_pe10_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_PE10=Avg_cifti.cdata;


AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;


%average across all 5 PEs
Avg_Glass_PEs=(Glass_PE1+ Glass_PE2 + Glass_PE3+ Glass_PE4 + Glass_PE5 + Glass_PE6+ Glass_PE7 + Glass_PE8+ Glass_PE9 + Glass_PE10)/10;

% Save Avg_PEs as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Avg_Glass_PEs;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Avg_Glass_PEs.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

%parcellate PEs file
inputFile='/Users/shefalirai/Desktop/Avg_Glass_PEs.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/Avg_Glass_PEs_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Avg_Glass_PEs_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_Glass_PEs_Parc=Avg_Glass_PEs_Parc.cdata;

%% Memory Relative reliability versus Beta values from 3rd level

Avg_cifti=ciftiopen('/Volumes/LaCie/Memory_matched_REGRESSED_9subs/AvgSub_Relative_MemoryReli_Reg_1000parc.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_Reg_RelativeReli=Avg_cifti.cdata;

%1 to 9 PE (beta values)
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-memoryfaces_pe1_3rdlevel_beta/task-memoryfaces_pe1_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_PE1=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-memoryfaces_pe2_3rdlevel_beta/task-memoryfaces_pe2_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_PE2=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-memoryfaces_pe3_3rdlevel_beta/task-memoryfaces_pe3_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_PE3=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-memorywords_pe1_3rdlevel_beta/task-memorywords_pe1_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_PE4=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-memorywords_pe2_3rdlevel_beta/task-memorywords_pe2_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_PE5=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-memorywords_pe3_3rdlevel_beta/task-memorywords_pe3_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_PE6=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-memoryscenes_pe1_3rdlevel_beta/task-memoryscenes_pe1_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_PE7=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-memoryscenes_pe2_3rdlevel_beta/task-memoryscenes_pe2_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_PE8=Avg_cifti.cdata;
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects_taskregressed/sub-MSCAvg/sub-MSCAvg/MNINonLinear/Results/task-memoryscenes_pe3_3rdlevel_beta/task-memoryscenes_pe3_3rdlevel_beta_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_PE9=Avg_cifti.cdata;

AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;


%average across all PEs
Avg_Memory_PEs=(Memory_PE1+ Memory_PE2 + Memory_PE3+ Memory_PE4 + Memory_PE5 + Memory_PE6+ Memory_PE7 + Memory_PE8+ Memory_PE9 )/9;

% Save Avg_PEs as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Avg_Memory_PEs;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/Avg_Memory_PEs.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

%parcellate PEs file
inputFile='/Users/shefalirai/Desktop/Avg_Memory_PEs.dtseries.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/Avg_Memory_PEs_1000parc.ptseries.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Avg_Memory_PEs_Parc=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_Memory_PEs_Parc=Avg_Memory_PEs_Parc.cdata;



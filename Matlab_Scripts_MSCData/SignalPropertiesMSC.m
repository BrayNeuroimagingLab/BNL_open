
Avg_cifti=ciftiopen('/Volumes/LaCie/Rest_Motor_matched_9subs/AvgSub_Reli_Rest.dscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_Reli_motormatched=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_MeanSignal_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_MS_motormatched=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Rest_SD_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Rest_SD_motormatched=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Glass_SD_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_SD_motormatched=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Motor_SD_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Motor_SD_motormatched=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Memory_SD_motormatched_noMSC08.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_SD_motormatched=Avg_cifti.cdata;


MotorRelative_SD=Motor_SD_motormatched-Rest_SD_motormatched;
GlassRelative_SD=Glass_SD_motormatched-Rest_SD_motormatched;
MemoryRelative_SD=Memory_SD_motormatched-Rest_SD_motormatched;


Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=MotorRelative_SD;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/MotorRelative_SD_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=GlassRelative_SD;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/GlassRelative_SD_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');

Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=MemoryRelative_SD;
ciftisavereset(Avg_cifti, '/Users/shefalirai/Desktop/MemoryRelative_SD_motormatched_noMSC08.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');


%%%%%%%%%%%%%%%%
Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Glass_MeanSignal_motormatched_noMSC08_1000parc.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_MS_motormatched=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Motor_MeanSignal_motormatched_noMSC08_1000parc.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Motor_MS_motormatched=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Memory_MeanSignal_motormatched_noMSC08_1000parc.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_MS_motormatched=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Glass_SD_motormatched_noMSC08_1000parc.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_SD_motormatched=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Motor_SD_motormatched_noMSC08_1000parc.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Motor_SD_motormatched=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/Memory_SD_motormatched_noMSC08_1000parc.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_SD_motormatched=Avg_cifti.cdata;

%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
Motor_MS_motormatched(:,2)=AvgSub_NETS;
Glass_MS_motormatched(:,2)=AvgSub_NETS;
Memory_MS_motormatched(:,2)=AvgSub_NETS;
Motor_SD_motormatched(:,2)=AvgSub_NETS;
Glass_SD_motormatched(:,2)=AvgSub_NETS;
Memory_SD_motormatched(:,2)=AvgSub_NETS;

%%%%%%%%%%%%%%
Avg_cifti=ciftiopen('/Volumes/LaCie/Glass_matched_noregression_9subs/AvgSub_Reli_Glass_1000parc.pscalar.nii ','/Applications/workbench/bin_macosx64/wb_command');
Glass_Reli_motormatched=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/Motor_matched_noregression_9subs/AvgSub_Reli_Motor_1000parc.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
Motor_Reli_motormatched=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/Memory_matched_noregression_9subs/AvgSub_Reli_Memory_1000parc.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_Reli_motormatched=Avg_cifti.cdata;

Motor_Reli_motormatched(:,2)=AvgSub_NETS;
Glass_Reli_motormatched(:,2)=AvgSub_NETS;
Memory_Reli_motormatched(:,2)=AvgSub_NETS;
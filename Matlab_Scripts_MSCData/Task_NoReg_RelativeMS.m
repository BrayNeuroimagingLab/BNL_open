%Mean signal relative 

%Motor
Motor_MS=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/MotorRelative_MeanSignal_motormatched_noMSC08_1000parc.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Motor_MS=Motor_MS.cdata;


%Glass
Glass_MS=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/GlassRelative_MeanSignal_motormatched_noMSC08_1000parc.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_MS=Glass_MS.cdata;

%Memory
Memory_MS=ciftiopen('/Volumes/LaCie/SignalProperties_noMSC08/MemoryRelative_MeanSignal_motormatched_noMSC08_1000parc.ptseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_MS=Memory_MS.cdata;


%Add second column to specify which network each parcel belongs to
AvgSub_NETS=ciftiopen('/Volumes/LaCie/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
AvgSub_NETS=AvgSub_NETS.cdata;
Motor_MS(:,2)=AvgSub_NETS;
Glass_MS(:,2)=AvgSub_NETS;
Memory_MS(:,2)=AvgSub_NETS;


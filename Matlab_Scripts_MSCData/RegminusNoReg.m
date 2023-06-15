%
%Relative reliability of regressed minus no regression
%% MOTOR
File='/Volumes/LaCie/Motor_matched_noregression_9subs/AvgSub_Relative_MotorReli.dscalar.nii'; 
AvgSub_Reli_MotorRelative_NoReg=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_MotorRelative_NoReg=AvgSub_Reli_MotorRelative_NoReg.cdata;


File='/Volumes/LaCie/Motor_matched_REGRESSED_9subs/AvgSub_Relative_MotorReli_Reg.dscalar.nii'; 
AvgSub_Reli_MotorRelative_Reg=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_MotorRelative_Reg=AvgSub_Reli_MotorRelative_Reg.cdata;

AvgSub_RegminusNoReg=AvgSub_Reli_MotorRelative_Reg-AvgSub_Reli_MotorRelative_NoReg;


%Open subject's original cifti
subject_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');

% Replace original .cdata with correlated data
subject_cifti.cdata=AvgSub_RegminusNoReg;
ciftisavereset(subject_cifti, '/Users/shefalirai/Desktop/AvgSub_Motor_RegminusNoReg.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');

%% GLASS
File='/Volumes/LaCie/Glass_matched_noregression_9subs/AvgSub_Relative_GlassReli.dscalar.nii'; 
AvgSub_Reli_GlassRelative_NoReg=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_GlassRelative_NoReg=AvgSub_Reli_GlassRelative_NoReg.cdata;


File='/Volumes/LaCie/Glass_matched_REGRESSED_9subs/AvgSub_Relative_GlassReli_Reg.dscalar.nii'; 
AvgSub_Reli_GlassRelative_Reg=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_GlassRelative_Reg=AvgSub_Reli_GlassRelative_Reg.cdata;

AvgSub_Glass_RegminusNoReg=AvgSub_Reli_GlassRelative_Reg-AvgSub_Reli_GlassRelative_NoReg;


%Open subject's original cifti
subject_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');

% Replace original .cdata with correlated data
subject_cifti.cdata=AvgSub_Glass_RegminusNoReg;
ciftisavereset(subject_cifti, '/Users/shefalirai/Desktop/AvgSub_Glass_RegminusNoReg.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');

%% Memory
File='/Volumes/LaCie/Memory_matched_noregression_9subs/AvgSub_Relative_MemoryReli.dscalar.nii'; 
AvgSub_Reli_MemoryRelative_NoReg=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_MemoryRelative_NoReg=AvgSub_Reli_MemoryRelative_NoReg.cdata;


File='/Volumes/LaCie/Memory_matched_REGRESSED_9subs/AvgSub_Relative_MemoryReli_Reg.dscalar.nii'; 
AvgSub_Reli_MemoryRelative_Reg=ciftiopen(File, '/Applications/workbench/bin_macosx64/wb_command');
AvgSub_Reli_MemoryRelative_Reg=AvgSub_Reli_MemoryRelative_Reg.cdata;

AvgSub_Memory_RegminusNoReg=AvgSub_Reli_MemoryRelative_Reg-AvgSub_Reli_MemoryRelative_NoReg;


%Open subject's original cifti
subject_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');

% Replace original .cdata with correlated data
subject_cifti.cdata=AvgSub_Memory_RegminusNoReg;
ciftisavereset(subject_cifti, '/Users/shefalirai/Desktop/AvgSub_Memory_RegminusNoReg.dscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');

%% Open Reg-NoReg


Avg_cifti=ciftiopen('/Volumes/LaCie/AvgSub_Motor_RegminusNoReg.dscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
Motor_RegminusNoReg=Avg_cifti.cdata;


Avg_cifti=ciftiopen('/Volumes/LaCie/AvgSub_Glass_RegminusNoReg.dscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
Glass_RegminusNoReg=Avg_cifti.cdata;

Avg_cifti=ciftiopen('/Volumes/LaCie/AvgSub_Memory_RegminusNoReg.dscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
Memory_RegminusNoReg=Avg_cifti.cdata;



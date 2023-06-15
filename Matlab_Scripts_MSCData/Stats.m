%Statistical analysis

%Task regression reliability vs. non-regressed task reliability 
%Open 
Motor_Reg_Reli=ciftiopen('/Volumes/LaCie/Motor_matched_REGRESSED_9subs/AvgSub_Reli_Motor_Reg.dscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
Motor_Reg_Reli=Motor_Reg_Reli.cdata;

Motor_NOReg_Reli=ciftiopen('/Volumes/LaCie/Memory_matched_noregression_9subs/AvgSub_Reli_Memory.dscalar.nii','/Applications/workbench/bin_macosx64/wb_command');
Motor_NOReg_Reli=Motor_NOReg_Reli.cdata;

[h,p] = ttest(Motor_Reg_Reli,Motor_NOReg_Reli, 'Alpha',0.001);


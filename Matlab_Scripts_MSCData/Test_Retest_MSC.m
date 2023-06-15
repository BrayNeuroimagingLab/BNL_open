function AvgSub_Reli_Task=Test_Retest_MSC(Sub1_Corr_Task, Sub2_Corr_Task, Sub3_Corr_Task, Sub4_Corr_Task, Sub5_Corr_Task, Sub6_Corr_Task, Sub7_Corr_Task, Sub9_Corr_Task, Sub10_Corr_Task, task)
%task must be a string i.e. 'rest'
%Use this function after running Connectome_Corr.m 
%excluding MSC08

AvgSub_Reli_Task=(Sub1_Corr_Task+Sub2_Corr_Task+Sub3_Corr_Task+Sub4_Corr_Task+Sub5_Corr_Task+Sub6_Corr_Task+Sub7_Corr_Task+Sub9_Corr_Task+Sub10_Corr_Task)/9;

%Save correlated connectomes
%Open subject's original cifti
subject_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');

% Replace original .cdata with correlated data
subject_cifti.cdata=AvgSub_Reli_Task;
ciftisavereset(subject_cifti, sprintf('/Users/shefalirai/Desktop/AvgSub_Reli_%s.dscalar.nii', task), '/Applications/workbench/bin_macosx64/wb_command');

end

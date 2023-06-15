function sub_corr_firstlasthalf_task=Connectome_Corr(task_firsthalf, task_lasthalf, sub, task, taskshort)
%Correlate first and last half connectomes
%task_firsthalf must be in workspace and entered with subject cell number
%i.e. glass_firsthalf{1}, glass_lasthalf{1} for Subject 1
%sub must be entered as 01, 02, 03...10
%task must be entered as a string and the same as the cifitify subject task i.e. 'glasslexical_run01'
%taskshort must be entered as a string and the short title version i.e. 'Glass'

%Create first half and last half connectomes
tic
task_firsthalf_connectome =  corr(task_firsthalf');
task_lasthalf_connectome =  corr(task_lasthalf');


%Remove any NAN values from connectomes

task_firsthalf_connectome(isnan(task_firsthalf_connectome))=0;
task_lasthalf_connectome(isnan(task_lasthalf_connectome))=0;


%Correlate the first half and last half connectomes to get your correlated connectomes

for r = 1:91282  
    sub_corr_firstlasthalf_task(r) = corr(task_firsthalf_connectome(r,:)', task_lasthalf_connectome(r,:)');
end


%Save correlated connectomes
% Open subject's original cifti
if sub<10
    subject_cifti=ciftiopen(sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC0%d/sub-MSC0%d/MNINonLinear/Results/task-%s_ses-func01_smoothed_midrefvolume/task-%s_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',sub,sub,task, task),'/Applications/workbench/bin_macosx64/wb_command');
else
    subject_cifti=ciftiopen(sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC%d/sub-MSC%d/MNINonLinear/Results/task-%s_ses-func01_smoothed_midrefvolume/task-%s_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii',sub,sub,task, task),'/Applications/workbench/bin_macosx64/wb_command');
end

% Replace original .cdata with correlated data
subject_cifti.cdata=sub_corr_firstlasthalf_task';
ciftisavereset(subject_cifti, sprintf('/Users/shefalirai/Desktop/Sub%d_%s_FirstLast_Corr.dscalar.nii', sub,taskshort), '/Applications/workbench/bin_macosx64/wb_command');
toc


end


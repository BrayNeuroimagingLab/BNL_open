function [Avg_tSNR_AllTasks, Avg_SD_AllTasks, Avg_Mean_AllTasks]=Signal_AllTask(allsessions_allsubjects_task, allsessions_allsubjects_task2, allsessions_allsubjects_task3, main_task)
%main_task must be a string i.e. 'Motor' or "Glass" or "Rest"
%Run Open_CiftiTimeseries for all runs of the task
%Run Remove_Motion for all runs of the task
%Workspace should have allsessions_allsubjects_task(s) i.e. allsessions_allsubjects_glassrun1 and allsessions_allsubjects_glassrun2

if exist('allsessions_allsubjects_task3','var')
    try
        Avg_tSNR_task=Signal_Property_Values(allsessions_allsubjects_task);
        Avg_tSNR_task2=Signal_Property_Values(allsessions_allsubjects_task2);
        Avg_tSNR_task3=Signal_Property_Values(allsessions_allsubjects_task3);
        Avg_tSNR_AllTasks=(Avg_tSNR_task+Avg_tSNR_task2+Avg_tSNR_task3)/3;
        Avg_SD_AllTasks=(Avg_SD_task+Avg_SD_task2+Avg_SD_task3)/3;
        Avg_Mean_AllTasks=(Avg_Mean_task+Avg_Mean_task2+Avg_Mean_task3)/3;
    catch
        fprintf('error\n')
    end
elseif exist('allsessions_allsubjects_task2','var')
    try
        Avg_tSNR_task=Signal_Property_Values(allsessions_allsubjects_task);
        Avg_tSNR_task2=Signal_Property_Values(allsessions_allsubjects_task2);
        Avg_tSNR_AllTasks=(Avg_tSNR_task+Avg_tSNR_task2)/2;
        Avg_SD_AllTasks=(Avg_SD_task+Avg_SD_task2)/2;
        Avg_Mean_AllTasks=(Avg_Mean_task+Avg_Mean_task2)/2;
    catch
        fprintf('error\n')
    end
else
    try
        Avg_tSNR_task=Signal_Property_Values(allsessions_allsubjects_task);
        Avg_tSNR_AllTasks=(Avg_tSNR_task);
        Avg_SD_AllTasks=(Avg_SD_task);
        Avg_Mean_AllTasks=(Avg_Mean_task);
    catch
        fprintf('error\n')
    end
end
        

% Save Avg_tSNR as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Avg_tSNR_AllTasks;
ciftisavereset(Avg_cifti, sprintf('/Users/shefalirai/Desktop/Avg_tSNR_%s.dtseries.nii', main_task), '/Applications/workbench/bin_macosx64/wb_command');

% Save Avg_SD as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Avg_SD_AllTasks;
ciftisavereset(Avg_cifti, sprintf('/Users/shefalirai/Desktop/Avg_SD_%s.dtseries.nii', main_task), '/Applications/workbench/bin_macosx64/wb_command');

% Save Avg_MeanSignal as a Cifti
Avg_cifti=ciftiopen('/Volumes/LaCie/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=Avg_Mean_AllTasks;
ciftisavereset(Avg_cifti, sprintf('/Users/shefalirai/Desktop/Avg_Mean_%s.dtseries.nii', main_task), '/Applications/workbench/bin_macosx64/wb_command');



end




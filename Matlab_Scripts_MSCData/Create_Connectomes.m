function  task_meancent=Create_Connectomes(task_folder, task)
%First step to run test-retest reliability on a specific task
%Calls the following functions: Open_CiftiTimeseries.m, Remove_Motion.m, MeanCenter_Timeseries.m, Concatenate_Connectomes.m
%task_folder must be entered as a string and the same as the task folder name i.e. 'msc_rest'
%task must be a string as the task name i.e. 'rest'
%for example: glass1=Create_Connectomes('msc_glass_run1','glasslexical_run01');

%Run this script multiple times (up to 3) for each run of a task 
%Final workspace for glass: allsessions_allsubjects_glassrun1, allsessions_allsubjects_glassrun2

allsessions_allsubjects_task=Open_CiftiTimeseries_REST(task);

allsessions_allsubjects_task=Remove_Motion(task_folder, allsessions_allsubjects_task);

task_meancent=MeanCenter_Timeseries(allsessions_allsubjects_task);

%Run Concatenate_Connectomes.m next 

end



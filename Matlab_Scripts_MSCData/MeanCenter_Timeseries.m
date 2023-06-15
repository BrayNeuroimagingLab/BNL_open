function task_variable=MeanCenter_Timeseries(allsessions_allsubjects_task)
% Mean center each session for each subject
%allsessions_allsubjects variable must be in workspace and entered as an input
%task_variable must be a string i.e. 'memorywords_meancent'

% create new cell array for faster for loop
task_variable=allsessions_allsubjects_task;

tic
for subject=1:10
    for session=1:10
        try
            task_variable{1,subject}{session,1}=(allsessions_allsubjects_task{1,subject}{session,1}'-mean(allsessions_allsubjects_task{1,subject}{session,1}'))';
        catch
            fprintf('error\n');
        end
    end
end
toc
% usually 15 seconds

end


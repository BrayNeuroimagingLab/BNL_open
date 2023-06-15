function [Avg_Mean_Sub, Mean_Sub]=MeanSignal_Values_Jan2023(allsessions_allsubjects_task)
% Average tSNR, SD, Mean signal Map for each subject
% Mean, SD and tSNR of each session per subject on the original time series
% For this analysis do not mean center the timeseries since we want to
% analyze signal variation 
%excluding MSC08 


%manually run each cell, some sessions may be missing and rows need to be deleted manually before computing 
for subject=1:10
    try
        allsessions_allsubjects_task{subject}=allsessions_allsubjects_task{1,subject}(~cellfun(@isempty, allsessions_allsubjects_task{1,subject}(:,1)), :);
    catch
        fprintf('error\n')
    end
end


for subject=1:10
    try
        Mean_Sub{subject}=cellfun(@(allsessions_allsubjects_task) mean(allsessions_allsubjects_task,2), allsessions_allsubjects_task{1,subject},'UniformOutput',false);
        Mean_Sub{subject} = mean(cat(3,Mean_Sub{subject}{:}),3);
    catch
        fprintf('error\n')
    end
end


% Averaged tSNR, mean and SD from all sessions for each subject
Avg_Mean_Sub = mean(cat(3, Mean_Sub{:}), 3);


function [Avg_SD_Sub, Std_Sub]=SD_Values_Jan2023(allsessions_allsubjects_task)
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
        Std_Sub{subject}=cellfun(@(allsessions_allsubjects_task) std(allsessions_allsubjects_task,[],2), allsessions_allsubjects_task{1,subject},'UniformOutput',false);
        Std_Sub{subject} = mean(cat(3,Std_Sub{subject}{:}),3);
    catch
        fprintf('error\n')
    end
end



Avg_SD_Sub = mean(cat(3, Std_Sub{:}), 3);


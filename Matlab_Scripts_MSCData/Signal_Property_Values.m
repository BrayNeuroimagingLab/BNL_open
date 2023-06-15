function [Avg_Mean_Sub, Avg_SD_Sub, Avg_tSNR_Sub]=Signal_Property_Values(allsessions_allsubjects_task)
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

for subject=1:10
    try
        Std_Sub{subject}=cellfun(@(allsessions_allsubjects_task) std(allsessions_allsubjects_task,[],2), allsessions_allsubjects_task{1,subject},'UniformOutput',false);
        Std_Sub{subject} = mean(cat(3,Std_Sub{subject}{:}),3);
    catch
        fprintf('error\n')
    end
end


% Mean_Sub1=cellfun(@(allsessions_allsubjects) mean(allsessions_allsubjects,2), allsessions_allsubjects_task{1,1},'UniformOutput',false);
% Mean_Sub2=cellfun(@(allsessions_allsubjects) mean(allsessions_allsubjects,2), allsessions_allsubjects_task{1,2},'UniformOutput',false);
% Mean_Sub3=cellfun(@(allsessions_allsubjects) mean(allsessions_allsubjects,2), allsessions_allsubjects_task{1,3},'UniformOutput',false);
% Mean_Sub4=cellfun(@(allsessions_allsubjects) mean(allsessions_allsubjects,2), allsessions_allsubjects_task{1,4},'UniformOutput',false);
% Mean_Sub5=cellfun(@(allsessions_allsubjects) mean(allsessions_allsubjects,2), allsessions_allsubjects_task{1,5},'UniformOutput',false);
% Mean_Sub6=cellfun(@(allsessions_allsubjects) mean(allsessions_allsubjects,2), allsessions_allsubjects_task{1,6},'UniformOutput',false);
% Mean_Sub7=cellfun(@(allsessions_allsubjects) mean(allsessions_allsubjects,2), allsessions_allsubjects_task{1,7},'UniformOutput',false);
% Mean_Sub8=cellfun(@(allsessions_allsubjects) mean(allsessions_allsubjects,2), allsessions_allsubjects_task{1,8},'UniformOutput',false);
% Mean_Sub9=cellfun(@(allsessions_allsubjects) mean(allsessions_allsubjects,2), allsessions_allsubjects_task{1,9},'UniformOutput',false);
% Mean_Sub10=cellfun(@(allsessions_allsubjects) mean(allsessions_allsubjects,2), allsessions_allsubjects_task{1,10},'UniformOutput',false);
% Mean_Sub1 = cat(3,Mean_Sub1{:});
% Mean_Sub1 = mean(Mean_Sub1,3);
% Mean_Sub2 = cat(3,Mean_Sub2{:});
% Mean_Sub2 = mean(Mean_Sub2,3);
% Mean_Sub3 = cat(3,Mean_Sub3{:});
% Mean_Sub3 = mean(Mean_Sub3,3);
% Mean_Sub4 = cat(3,Mean_Sub4{:});
% Mean_Sub4 = mean(Mean_Sub4,3);
% Mean_Sub5 = cat(3,Mean_Sub5{:});
% Mean_Sub5 = mean(Mean_Sub5,3);
% Mean_Sub6 = cat(3,Mean_Sub6{:});
% Mean_Sub6 = mean(Mean_Sub6,3);
% Mean_Sub7 = cat(3,Mean_Sub7{:});
% Mean_Sub7 = mean(Mean_Sub7,3);
% Mean_Sub8 = cat(3,Mean_Sub8{:});
% Mean_Sub8 = mean(Mean_Sub8,3);
% Mean_Sub9 = cat(3,Mean_Sub9{:});
% Mean_Sub9 = mean(Mean_Sub9,3);
% Mean_Sub10 = cat(3,Mean_Sub10{:});
% Mean_Sub10= mean(Mean_Sub10,3);
% Avg_Mean_task=(Mean_Sub1 + Mean_Sub2 + Mean_Sub3 + Mean_Sub4 + Mean_Sub5 + Mean_Sub6 + Mean_Sub7 + Mean_Sub8 + Mean_Sub9 + Mean_Sub10)/10;


% Std_Sub1=cellfun(@(allsessions_allsubjects) std(allsessions_allsubjects,[],2), allsessions_allsubjects_task{1,1},'UniformOutput',false);
% Std_Sub2=cellfun(@(allsessions_allsubjects) std(allsessions_allsubjects,[],2), allsessions_allsubjects_task{1,2},'UniformOutput',false);
% Std_Sub3=cellfun(@(allsessions_allsubjects) std(allsessions_allsubjects,[],2), allsessions_allsubjects_task{1,3},'UniformOutput',false);
% Std_Sub4=cellfun(@(allsessions_allsubjects) std(allsessions_allsubjects,[],2), allsessions_allsubjects_task{1,4},'UniformOutput',false);
% Std_Sub5=cellfun(@(allsessions_allsubjects) std(allsessions_allsubjects,[],2), allsessions_allsubjects_task{1,5},'UniformOutput',false);
% Std_Sub6=cellfun(@(allsessions_allsubjects) std(allsessions_allsubjects,[],2), allsessions_allsubjects_task{1,6},'UniformOutput',false);
% Std_Sub7=cellfun(@(allsessions_allsubjects) std(allsessions_allsubjects,[],2), allsessions_allsubjects_task{1,7},'UniformOutput',false);
% Std_Sub8=cellfun(@(allsessions_allsubjects) std(allsessions_allsubjects,[],2), allsessions_allsubjects_task{1,8},'UniformOutput',false);
% Std_Sub9=cellfun(@(allsessions_allsubjects) std(allsessions_allsubjects,[],2), allsessions_allsubjects_task{1,9},'UniformOutput',false);
% Std_Sub10=cellfun(@(allsessions_allsubjects) std(allsessions_allsubjects,[],2), allsessions_allsubjects_task{1,10},'UniformOutput',false);
% Std_Sub1 = cat(3,Std_Sub1{:});
% Std_Sub1 = mean(Std_Sub1,3);
% Std_Sub2 = cat(3,Std_Sub2{:});
% Std_Sub2 = mean(Std_Sub2,3);
% Std_Sub3 = cat(3,Std_Sub3{:});
% Std_Sub3 = mean(Std_Sub3,3);
% Std_Sub4 = cat(3,Std_Sub4{:});
% Std_Sub4 = mean(Std_Sub4,3);
% Std_Sub5 = cat(3,Std_Sub5{:});
% Std_Sub5 = mean(Std_Sub5,3);
% Std_Sub6 = cat(3,Std_Sub6{:});
% Std_Sub6 = mean(Std_Sub6,3);
% Std_Sub7 = cat(3,Std_Sub7{:});
% Std_Sub7 = mean(Std_Sub7,3);
% Std_Sub8 = cat(3,Std_Sub8{:});
% Std_Sub8 = mean(Std_Sub8,3);
% Std_Sub9 = cat(3,Std_Sub9{:});
% Std_Sub9 = mean(Std_Sub9,3);
% Std_Sub10 = cat(3,Std_Sub10{:});
% Std_Sub10= mean(Std_Sub10,3);
% Avg_SD_task=(Std_Sub1 + Std_Sub2 + Std_Sub3 + Std_Sub4 + Std_Sub5 + Std_Sub6 + Std_Sub7 + Std_Sub8 +Std_Sub9 + Std_Sub10)/10;
% 
for subject=1:10
    try
        tSNR_Sub{subject}=Mean_Sub{subject}./Std_Sub{subject};
    catch
        fprintf('error\n')
    end
end

% Averaged tSNR, mean and SD from all sessions for each subject
Avg_tSNR_Sub = mean(cat(3, tSNR_Sub{:}), 3);
Avg_SD_Sub = mean(cat(3, Std_Sub{:}), 3);
Avg_Mean_Sub = mean(cat(3, Mean_Sub{:}), 3);



% %Uncomment the following and edit if we need to save SD and Mean for each subject
% % Save mean for each subject
% subject1_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects/ciftify_sub-MSC01/sub-MSC01/MNINonLinear/Results/task-motor_run1_ses-func01_smoothed_midrefvolume/task-motor_run1_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
% subject1_cifti.cdata=mean(cat(3, Mean_Sub1{:}), 3);
% ciftisavereset(subject1_cifti, '/Users/shefalirai/Desktop/Sub1_Mean_Rest.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');
% 
% 
% % Save SD for each subject
% subject1_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects/ciftify_sub-MSC01/sub-MSC01/MNINonLinear/Results/task-motor_run1_ses-func01_smoothed_midrefvolume/task-motor_run1_ses-func01_smoothed_midrefvolume_Atlas_s4.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
% subject1_cifti.cdata=mean(cat(3, Std_Sub1{:}), 3);
% ciftisavereset(subject1_cifti, '/Users/shefalirai/Desktop/Sub1_SD_Rest.dtseries.nii', '/Applications/workbench/bin_macosx64/wb_command');
% 






function allsessions_allsubjects_task=Open_CiftiTimeseries_REST(task)
%This function was edited for REST ONLY! Since we need the
%redopreprocessing file and replace a missing timepoint with 0



% Open timeseries from each subject and each session that has been smoothed with 4mm kernel
% j represents subjects = row
% k represents sessions = column 
% subject_ses{subject#, session#}
tic
for j=1:10
    for k=1:10
        if j==10 && k== 10
            try
                subject_ses{j,k}=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC%d/sub-MSC%d/MNINonLinear/Results/task-%s_ses-func%d_smoothed_midrefvolume_redopreproc/task-%s_ses-func%d_smoothed_midrefvolume_redopreproc_Atlas_s4.dtseries.nii',j,j,task,k,task,k)),'/Applications/workbench/bin_macosx64/wb_command');
            catch
                fprintf('error: file does not exist\n')
            end
        elseif j==10 && k~= 10
            try
                subject_ses{j,k}=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC%d/sub-MSC%d/MNINonLinear/Results/task-%s_ses-func0%d_smoothed_midrefvolume_redopreproc/task-%s_ses-func0%d_smoothed_midrefvolume_redopreproc_Atlas_s4.dtseries.nii',j,j,task,k,task,k)),'/Applications/workbench/bin_macosx64/wb_command');
            catch
                fprintf('error: file does not exist\n')
            end
        elseif j~=10 && k==10
            try
                subject_ses{j,k}=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC0%d/sub-MSC0%d/MNINonLinear/Results/task-%s_ses-func%d_smoothed_midrefvolume_redopreproc/task-%s_ses-func%d_smoothed_midrefvolume_redopreproc_Atlas_s4.dtseries.nii',j,j,task,k,task,k)),'/Applications/workbench/bin_macosx64/wb_command');
            catch
                fprintf('error: file does not exist\n')
            end
        else
            try
                subject_ses{j,k}=ciftiopen((sprintf('/Volumes/LaCie/subjects/ciftify_sub-MSC0%d/sub-MSC0%d/MNINonLinear/Results/task-%s_ses-func0%d_smoothed_midrefvolume_redopreproc/task-%s_ses-func0%d_smoothed_midrefvolume_redopreproc_Atlas_s4.dtseries.nii',j,j,task,k,task,k)),'/Applications/workbench/bin_macosx64/wb_command');
            catch
                fprintf('error: file does not exist\n')
            end
        end
     end
end
toc
% usually 125 seconds


% Store .cdata from original giftis so each cell contains each subject's 10 sessions store in rows
for j=1:10
    for k=1:10
        if j==10 && k== 10
            try
                all_subject_ses{j,k}=subject_ses{j,k}.cdata;
            catch
                fprintf('error: .cdata not available\n')
            end
        elseif j==10 && k~= 10
            try
                all_subject_ses{j,k}=subject_ses{j,k}.cdata;
            catch
                fprintf('error: .cdata not available\n')
            end
        elseif j~=10 && k==10
            try
                all_subject_ses{j,k}=subject_ses{j,k}.cdata;
            catch
                fprintf('error: .cdata not available\n')
            end
        else
            try
                all_subject_ses{j,k}=subject_ses{j,k}.cdata;
            catch
                fprintf('error: .cdata not available\n')
            end
        end
     end
end

%Concatenate all cell arrays into one cell
k=1;
for j=1:10
    try
        allsessions_allsubjects_task{j}={all_subject_ses{j,k}; all_subject_ses{j,k+1}; all_subject_ses{j,k+2}; all_subject_ses{j,k+3}; ...
        all_subject_ses{j,k+4}; all_subject_ses{j,k+5}; all_subject_ses{j,k+6}; all_subject_ses{j,k+7}; all_subject_ses{j,k+8}; all_subject_ses{j,k+9}};
    catch
        fprintf('error\n')
    end
end


%******** USE THIS ONLY FOR RESTING STATE DATA!!!!********
% Replace timepoint 818 with 0 for subject 6, session 8 since it is missing
% In order to have all equal matrix sizes for motion removal step
for allvertices=1:91282
    allsessions_allsubjects_task{1,6}{8,1}(allvertices,818)=0;
end

end

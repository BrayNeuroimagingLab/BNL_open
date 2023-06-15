function allsessions_allsubjects_task=Remove_Motion(foldername, allsessions_allsubjects_task)
%Function to remove high motion volumes (censoring) 
%foldername variable input must be a string i.e. 'msc_memorywords'
%allsessions_allsubjects variable must be in the workspace from the "Open_CiftiTimeseries.m" function



%Step1: Combine all PowerFD motion files 
%open PowerFD csv files for each subject and session
for j=1:10
    for k=1:10
        if j==10 && k== 10
            try
                subject_motion{j,k}=readmatrix(sprintf('/Volumes/Expansion/%s/sub-MSC%d/ses-func%d/func/sub-MSC%d_ses-func%d_PowerFD.csv',foldername,j,k,j,k));
            catch
                fprintf('error\n')
            end
        elseif j==10 && k~= 10
            try
                subject_motion{j,k}=readmatrix(sprintf('/Volumes/Expansion/%s/sub-MSC%d/ses-func0%d/func/sub-MSC%d_ses-func0%d_PowerFD.csv',foldername,j,k,j,k));
            catch
                fprintf('error\n')
            end
        elseif j~=10 && k==10
            try
                subject_motion{j,k}=readmatrix(sprintf('/Volumes/Expansion/%s/sub-MSC0%d/ses-func%d/func/sub-MSC0%d_ses-func%d_PowerFD.csv',foldername,j,k,j,k));
            catch
                fprintf('error\n')
            end
         else
             try
                 subject_motion{j,k}=readmatrix(sprintf('/Volumes/Expansion/%s/sub-MSC0%d/ses-func0%d/func/sub-MSC0%d_ses-func0%d_PowerFD.csv',foldername,j,k,j,k));
             catch
                   fprintf('error\n')
             end
        end
    end
end

%create cell array of all session motion values
m=1;
for j=1:10
    try
        subject_motion_cat{j}=[subject_motion{j,m}; subject_motion{j,m+1}; subject_motion{j,m+2}; subject_motion{j,m+3}; subject_motion{j,m+4}; subject_motion{j,m+5}; subject_motion{j,m+6}; subject_motion{j,m+7}; subject_motion{j,m+8}; subject_motion{j,m+9}];
    catch
        fprintf('error\n')
    end
end


% Step2: Remove motion for each subject and each session based on FD csv file

for subject=1:10
    try
        MotionTable{subject}=array2table(subject_motion_cat{1,subject});
        MotionTable{subject}=renamevars(MotionTable{subject},'Var1','Time');
        MotionTable{subject}=renamevars(MotionTable{subject},'Var2','FD');
    catch
        fprintf('error\n')
    end
end


% Remove any rows that have header information, just in case
for subject=1:10
    try
        MotionTable{subject}=rmmissing(MotionTable{subject});
        %Remove FD <0.2 values from motion table
        MotionTable{subject}.Mask=MotionTable{subject}.FD<0.2;
    catch
        fprintf('error\n')
    end
end

% Create a new column to indicate Session

for subject=1:10
    session=1;
    num=0;
    for p=1:height(MotionTable{subject})
        if num == length(subject_motion{1,1}) %818 or 104 for MSC data
            num = 0;
            if session > 9
                session = 1;
            else
                session = session+1;
            end
        end
        MotionTable{subject}.Session(p)=session;
        num=num+1;
    end
end

% usually 7 seconds

% Find which volumes are "bad volumes" (i.e. where the Mask equals 0)
for subject=1:10
    try
        MotionRows{subject}=MotionTable{subject}(MotionTable{subject}.Mask==0,:);
    catch
        fprintf('error\n')
    end
end



% Delete all bad volume columns from the dataset

for subject=1:10
    for session=1:10
        try
            Sub_Ses_MotionValues{subject}=MotionRows{subject}.Time(MotionRows{subject}.Session==session);
            Sub_Ses_MotionValues{subject}=Sub_Ses_MotionValues{subject}+1;
            allsessions_allsubjects_task{1,subject}{session,1}(:,Sub_Ses_MotionValues{subject})=[];
        catch
            fprintf('error: skipping subject, does not exist\n')
        end
    end
end

end












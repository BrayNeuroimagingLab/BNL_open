function [task_firsthalf, task_lasthalf, task_meancent]=Concatenate_Connectomes(task_meancent1, task_meancent2, task_meancent3)
% Concatenate task values  to create first and last half session matrices
%Since MSC data has more than 1 run for the same task i.e. glass run1 and glass run 2
if exist('task_meancent3','var')
    for subject=1:10
        for session=1:10
            try
                task_meancent{1,subject}{session,1}=[task_meancent1{1,subject}{session,1} task_meancent2{1,subject}{session,1} task_meancent3{1,subject}{session,1}];
            catch
                fprintf('error\n')
            end
        end
    end
elseif exist('task_meancent2','var')
    for subject=1:10
        for session=1:10
            try
                task_meancent{1,subject}{session,1}=[task_meancent1{1,subject}{session,1} task_meancent2{1,subject}{session,1}];
            catch
                fprintf('error\n')
            end
        end
    end
else
    for subject=1:10
        for session=1:10
            try
                task_meancent{1,subject}{session,1}=[task_meancent1{1,subject}{session,1}];
            catch
                fprintf('error\n')
            end
        end
    end    
end


%Split into first half and last half variables, the output cell array is
%for all 9 subjects
for subject=1:10
    try
        task_firsthalf{subject}=[task_meancent{1,subject}{1,1} task_meancent{1,subject}{2,1} task_meancent{1,subject}{3,1} task_meancent{1,subject}{4,1} task_meancent{1,subject}{5,1}];
        task_lasthalf{subject}=[task_meancent{1,subject}{6,1} task_meancent{1,subject}{7,1} task_meancent{1,subject}{8,1} task_meancent{1,subject}{9,1} task_meancent{1,subject}{10,1}];
    catch
        fprintf('error\n')
    end
end



end

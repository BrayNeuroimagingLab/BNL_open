function df=MSCaccuracy(foldernumber,task)

% df=tdfread('/Users/shefalirai/Desktop/Documents/MSC Data/ds000224_R1.0-8.2/sub-MSC09/ses-func01/func/sub-MSC09_ses-func01_task-memoryfaces_events.tsv','\t');
% df=df.correct;
% task='memorywords_events';

for j=1:10
    for k=1:10
        if j==10 && k==10
            try
                df{j,k}=tdfread(sprintf('/Users/shefalirai/Desktop/Documents/MSC Data/%s/sub-MSC%d/ses-func%d/func/sub-MSC%d_ses-func%d_task-%s.tsv',foldernumber,j,k,j,k,task),'\t');
                df{j,k}=df{j,k}.correct;
            catch
                fprintf('error\n')
            end
        elseif j==10 && k~=10
            try
                df{j,k}=tdfread(sprintf('/Users/shefalirai/Desktop/Documents/MSC Data/%s/sub-MSC%d/ses-func0%d/func/sub-MSC%d_ses-func0%d_task-%s.tsv',foldernumber,j,k,j,k,task),'\t');
                df{j,k}=df{j,k}.correct;
            catch
                fprintf('error\n')
            end
        elseif j~=10 && k==10
            try
                df{j,k}=tdfread(sprintf('/Users/shefalirai/Desktop/Documents/MSC Data/%s/sub-MSC0%d/ses-func%d/func/sub-MSC0%d_ses-func%d_task-%s.tsv',foldernumber,j,k,j,k,task),'\t');
                df{j,k}=df{j,k}.correct;
            catch
                fprintf('error\n')
            end
         else
             try
                df{j,k}=tdfread(sprintf('/Users/shefalirai/Desktop/Documents/MSC Data/%s/sub-MSC0%d/ses-func0%d/func/sub-MSC0%d_ses-func0%d_task-%s.tsv',foldernumber,j,k,j,k,task),'\t');
                df{j,k}=df{j,k}.correct;
             catch
                   fprintf('error\n')
             end
        end
    end
end


%Motor matching for all tasks

%MOTOR
% After running Open_CiftiTimeseries.m and Remove_Motion
% concatenate all tasks to match with the lowest motor volume of that
% session, which ranges from 102 to 182

%Open rest run separately due to missing volume
allsessions_allsubjects_glass1=Open_CiftiTimeseries('glasslexical_run01');
allsessions_allsubjects_glass2=Open_CiftiTimeseries('glasslexical_run02');
allsessions_allsubjects_memorywords=Open_CiftiTimeseries('memorywords'); 
allsessions_allsubjects_memoryscenes=Open_CiftiTimeseries('memoryscenes');
allsessions_allsubjects_memoryfaces=Open_CiftiTimeseries('memoryfaces');
allsessions_allsubjects_motor1=Open_CiftiTimeseries('motor_run1');
allsessions_allsubjects_motor2=Open_CiftiTimeseries('motor_run2');

allsessions_allsubjects_rest_rm=Remove_Motion('msc_rest', allsessions_allsubjects_rest);
allsessions_allsubjects_glass1_rm=Remove_Motion('msc_glass_run1', allsessions_allsubjects_glass1);
allsessions_allsubjects_glass2_rm=Remove_Motion('msc_glass_run2', allsessions_allsubjects_glass2);
allsessions_allsubjects_memorywords_rm=Remove_Motion('msc_memorywords', allsessions_allsubjects_memorywords);
allsessions_allsubjects_memoryfaces_rm=Remove_Motion('msc_memoryscenes', allsessions_allsubjects_memoryfaces);
allsessions_allsubjects_memoryscenes_rm=Remove_Motion('msc_memoryfaces', allsessions_allsubjects_memoryscenes);
allsessions_allsubjects_motor1_rm=Remove_Motion('msc_motor1', allsessions_allsubjects_motor1);
allsessions_allsubjects_motor2_rm=Remove_Motion('msc_motor2', allsessions_allsubjects_motor2);

    
%first combine motor1 and motor2 together
for j=1:10 %ses
    for k=1:10 %sub
        allsessions_allsubjects_motors_rm{j,k} = [allsessions_allsubjects_motor1_rm{1,k}{j,1} allsessions_allsubjects_motor2_rm{1,k}{j,1}];
    end
end

%exclude MSC08
motors_rm=allsessions_allsubjects_motors_rm(:,[1:7,9:10]);
%find length of each motor session 
allsize= cellfun('size', motors_rm, 2);
%find minimum size per session for motor
[minsize, minidx] = min(cellfun('size', motors_rm', 2));
%%already calculated min size and minidx
% minidx=[9,9,8,3,8,7,8,6,2,7]; 
% minsize=[182,166,157,173,156,169,121,169,102,168];

%motor match according to a subject's lowest motor volume for that session
for ses=1:10
    for sub=1:9
        motor_matched{1,sub}{ses,1}=motors_rm{ses,sub}(:,1:minsize(ses));
    end
end



%REST
%exclude MSC08
rest_rm=allsessions_allsubjects_rest_rm(:,[1:7,9:10]);
%rest-motor match according to a subject's lowest motor volume for that session
for ses=1:10
    for sub=1:9
        rest_matched{1,sub}{ses,1}=rest_rm{1,sub}{ses,1}(:,1:minsize(ses));
    end
end



%exclude MSC08
glass1_rm=allsessions_allsubjects_glass1_rm(:,[1:7,9:10]);
glass2_rm=allsessions_allsubjects_glass2_rm(:,[1:7,9:10]);
%first combine glass1 and glass2 together
for j=1:10 %ses
    for k=1:9 %sub
        glass_rm{j,k} = [glass1_rm{1,k}{j,1} glass2_rm{1,k}{j,1}];
    end
end
%glass-motor match according to a subject's lowest motor volume for that session
for ses=1:10
    for sub=1:9
        glass_matched{ses,sub}=glass_rm{ses,sub}(:,1:minsize(ses));
    end
end


%exclude MSC08
faces_rm=allsessions_allsubjects_memoryfaces_rm(:,[1:7,9:10]);
scenes_rm=allsessions_allsubjects_memoryscenes_rm(:,[1:7,9:10]);
words_rm=allsessions_allsubjects_memorywords_rm(:,[1:7,9:10]);
%first combine glass1 and glass2 together
for j=1:10 %ses
    for k=1:9 %sub
        memory_rm{j,k} = [faces_rm{1,k}{j,1} scenes_rm{1,k}{j,1} words_rm{1,k}{j,1}];
    end
end
%glass-motor match according to a subject's lowest motor volume for that session
for ses=1:10
    for sub=1:9
        memory_matched{ses,sub}=memory_rm{ses,sub}(:,1:minsize(ses));
    end
end


%Run Meancentering then Concatenate connectome.m files first
% motor_meancent=MeanCenter_Timeseries(motor_matched);
[motor_firsthalf_matched, motor_lasthalf_matched, motor_mc]=Concatenate_Connectomes(motor_matched);
%add empty cell array for MSC08 which connectome_corr will skip/error over
motor_firsthalf_matched={motor_firsthalf_matched{1:7}, [], motor_firsthalf_matched{8:end}};
motor_lasthalf_matched={motor_lasthalf_matched{1:7}, [], motor_lasthalf_matched{8:end}};

%Now we run Connectome_Corr.m for each subject
for sub=1:10
    try
        motor_corr=Connectome_Corr(motor_firsthalf_matched{sub}, motor_lasthalf_matched{sub}, sub, 'motor_run1','motor');
    catch
        fprintf('error\n')
    end
end



%REST
%Run Meancentering then Concatenate connectome.m files first
rest_meancent=MeanCenter_Timeseries(rest_matched);
[rest_firsthalf_matched, rest_lasthalf_matched]=Concatenate_Connectomes(rest_meancent);
rest_firsthalf_matched={rest_firsthalf_matched{1:7}, [], rest_firsthalf_matched{8:end}};
rest_lasthalf_matched={rest_lasthalf_matched{1:7}, [], rest_lasthalf_matched{8:end}};

%Now we run Connectome_Corr.m for each subject 
for sub=1:10
    try
        rest_corr=Connectome_Corr(rest_firsthalf_matched{sub}, rest_lasthalf_matched{sub}, sub, 'rest','rest');
    catch
        fprint('error\n')
    end
end


%MEMORY
%Run Meancentering then Concatenate connectome.m files first
memory_meancent=MeanCenter_Timeseries(memory_matched);
[memory_firsthalf_matched, memory_lasthalf_matched]=Concatenate_Connectomes(memory_meancent);
memory_firsthalf_matched={memory_firsthalf_matched{1:7}, [], memory_firsthalf_matched{8:end}};
memory_lasthalf_matched={memory_lasthalf_matched{1:7}, [], memory_lasthalf_matched{8:end}};

%Now we run Connectome_Corr.m for each subject 
for sub=1:10
    try
        memory_corr=Connectome_Corr(memory_firsthalf_matched{sub}, memory_lasthalf_matched{sub}, sub, 'memoryfaces','memory');
    catch
        fprint('error\n')
    end
end

%GLASS/LANGUAGE
%Run Meancentering then Concatenate connectome.m files first
glass_meancent=MeanCenter_Timeseries(glass_matched);
[glass_firsthalf_matched, glass_lasthalf_matched]=Concatenate_Connectomes(glass_meancent);
glass_firsthalf_matched={glass_firsthalf_matched{1:7}, [], glass_firsthalf_matched{8:end}};
glass_lasthalf_matched={glass_lasthalf_matched{1:7}, [], glass_lasthalf_matched{8:end}};

%Now we run Connectome_Corr.m for each subject 
for sub=1:10
    try
        glass_corr=Connectome_Corr(glass_firsthalf_matched{sub}, glass_lasthalf_matched{sub}, sub, 'glasslexical_run01','glass');
    catch
        fprint('error\n')
    end
end


%%%%%%%%%%%%%%%%%%%Figure 10 
%how much have correlation values changed, using connectome values
%parcellate first and then calculate connectome on parcel level

%Motor
motor_full=[motor_firsthalf_matched motor_lasthalf_matched];
motor_mean_avg=cellfun(@(motor_full) mean(motor_full,2), motor_full{1,subject},'UniformOutput',false);

%save as cifti
main_task='motor';
Avg_cifti=ciftiopen('/Users/shefalirai/Desktop/subjects/averaged_sub/Averaged_Timeseries.dtseries.nii','/Applications/workbench/bin_macosx64/wb_command');
Avg_cifti.cdata=motor_mean_avg;
ciftisavereset(Avg_cifti, sprintf('/Users/shefalirai/Desktop/AvgSub_Motor%s.dscalar.nii', main_task), '/Applications/workbench/bin_macosx64/wb_command');

%parcellate
inputFile='/Users/shefalirai/Desktop/AvgSub_Motor.dscalar.nii';
parcelCIFTIFile='/Users/shefalirai/Downloads/Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii';
parcelFile='/Users/shefalirai/Desktop/AvgSub_Motor_1000parc.pscalar.nii'; 
eval(['! /Applications/workbench/bin_macosx64/wb_command -cifti-parcellate ' inputFile ' ' parcelCIFTIFile ' COLUMN ' parcelFile ' -method MEAN'])
Avg_Motor=ciftiopen(parcelFile, '/Applications/workbench/bin_macosx64/wb_command');
Avg_Motor=Avg_Motor.cdata;
motor_connectome =  corr(Avg_Motor');





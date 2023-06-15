%% Run Infomap & Consensus Networks 

% Infomap run from Gordon paper: [infomapfolder '/Infomap-0.15.7/Infomap --clu -2 -N' num2str(reps) ' ' pajekfilename ' ' pathstr]);

% Thresholds 2-5% and run Infomap to create networks for each subject
for thresholds=2:5
    for subjects=1:10
        pajekfilename=sprintf('/Users/shefalirai/Desktop/thresholded_connectomes/Sub%d_thresh0%d_1000parc_17nets',subjects,thresholds);
        pathstr='/Users/shefalirai/Desktop/Infomap_Out';
        reps=1000; 
        infomapfolder='/Users/shefalirai/Desktop/infomap-1.2.1';
        system([infomapfolder '/Infomap --clu -2 -N' num2str(reps) ' ' pajekfilename ' ' pathstr]); % not using -s random seed since it gives different results everytime 
    end
end

% After running Infomap, open .clu network file for each subject across each threshold
for thresholds=2:5
    for subjects=1:10
        fid=fopen(sprintf('/Users/shefalirai/Desktop/Infomap_Out/Sub%d_thresh0%d_1000parc_17nets.clu',subjects, thresholds));
        sub_networks{subjects,thresholds}= cell2mat(textscan(fid,'%f %f %f', 'headerlines', 9, 'delimiter', ' ')); 
        fclose(fid);
    end
end




% %% Thresholds 2-10% and run Infomap to create networks for each subject
% for thresholds=0.02:0.01:0.1
%     for subjects=1:10
%         pajekfilename=sprintf('/Users/shefalirai/Desktop/thresholded_connectomes/Sub%d_thresh%d_1000parc_17nets',subjects,thresholds);
%         pathstr='/Users/shefalirai/Desktop/Infomap_Out';
%         reps=1000; 
%         infomapfolder='/Users/shefalirai/Desktop/infomap-1.2.1';
%         system([infomapfolder '/Infomap --clu -2 -N' num2str(reps) ' ' pajekfilename ' ' pathstr]); % not using -s random seed since it gives different results everytime 
%     end
% end
% 
% % After running Infomap, open .clu network file for each subject across each threshold
% for thresholds=1:9
%     for subjects=1:10
%         fid=fopen(sprintf('/Users/shefalirai/Desktop/Infomap_Out/Sub%d_thresh%d.clu',subjects, thresholds));
%         sub_networks{subjects,thresholds}= cell2mat(textscan(fid,'%f %f %f', 'headerlines', 9, 'delimiter', ' ')); 
%         fclose(fid);
%     end
% end




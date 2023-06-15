%% Run Infomap on Consensus Matrices

% Run Infomap on consensus matrix for each subject
for subs=1:10
    pajekfilename=sprintf('/Volumes/LaCie/consensus_matrices/Sub%d_Allthresh_ConsensusD',subs);
    pathstr='/Volumes/LaCie/consensus_matrices';
    reps=1000;
    infomapfolder='/Users/shefalirai/Desktop/infomap-1.2.1';
    system([infomapfolder '/Infomap --clu -2 -N' num2str(reps) ' ' pajekfilename ' ' pathstr]);
end


% After running Infomap, open .clu network file for each subject across each threshold
for subs=1:10
    fid=fopen(sprintf('/Volumes/LaCie/consensus_matrices/Sub%d_Allthresh_ConsensusD.clu',subs));
    sub_consensus_networks{subs}= cell2mat(textscan(fid,'%f %f %f', 'headerlines', 9, 'delimiter', ' '));
    fclose(fid);
end

% % Saved the original edited consensus networks to stay within 17 networks
% in total
% save('sub_consensus_networks_MANUALEDIT.mat','sub_consensus_networks');

% Keep track of ambigious/changed parcels adjusted to fit 17 networks
for subs=1:10
    [rows, columns] = find(sub_consensus_networks{1,subs}(:,2) > 17);
    ambig_networks{subs}=sub_consensus_networks{1,subs}(rows,:); 
    ambig_networks{subs}=sortrows(ambig_networks{subs},1);
end



% %% Threshold 2-10%
% % Run Infomap on consensus matrix for each subject
% for subs=1:10
%     pajekfilename=sprintf('/Users/shefalirai/Desktop/consensus_matrices/Sub%d_2to10Thresh_ConsensusD',subs);
%     pathstr='/Users/shefalirai/Desktop/consensus_matrices';
%     reps=1000;
%     infomapfolder='/Users/shefalirai/Desktop/infomap-1.2.1';  
%     system([infomapfolder '/Infomap --clu -2 -N' num2str(reps) ' ' pajekfilename ' ' pathstr]);
% end
% 
% 
% % After running Infomap, open .clu network file for each subject across each threshold
% for subs=1:10
%     fid=fopen(sprintf('/Users/shefalirai/Desktop/consensus_matrices/Sub%d_2to10Thresh_ConsensusD.clu',subs));
%     sub_consensus_networks{subs}= cell2mat(textscan(fid,'%f %f %f', 'headerlines', 9, 'delimiter', ' '));
%     fclose(fid);
% end
% 
% % Keep track of ambigious/changed parcels adjusted to fit 17 networks
% 
% 
% 
% % visualize on the surface
% for subs=1:10
%     consensus_allthresh{subs}=ciftiopen(sprintf('/Users/shefalirai/Desktop/parcelled_subjects/sub%d_1000parc_17nets.ptseries.nii',subs), '/Applications/workbench/bin_macosx64/wb_command');
%     sub_consensus_networks{subs}=sortrows(sub_consensus_networks{subs},1);
%     consensus_allthresh{subs}.cdata=sub_consensus_networks{subs}(:,2);
%     ciftisavereset(consensus_allthresh{subs},sprintf('/Users/shefalirai/Desktop/consensus_surface/Sub%d_2to10Thresh.pscalar.nii',subs), '/Applications/workbench/bin_macosx64/wb_command');
% end
% 
% 
% 
% 




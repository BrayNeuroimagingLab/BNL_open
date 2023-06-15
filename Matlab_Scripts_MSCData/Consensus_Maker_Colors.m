%% Consensus_Maker_Colors

for subs=1:10
    sub_consensus_networks{subs}=sortrows(sub_consensus_networks{subs},1);
end

AllSubs_Consensus=[sub_consensus_networks{1,1}(:,2) sub_consensus_networks{1,2}(:,2) sub_consensus_networks{1,3}(:,2) sub_consensus_networks{1,4}(:,2) sub_consensus_networks{1,5}(:,2) sub_consensus_networks{1,6}(:,2) sub_consensus_networks{1,7}(:,2) sub_consensus_networks{1,8}(:,2) sub_consensus_networks{1,9}(:,2) sub_consensus_networks{1,10}(:,2)];

addpath '/Users/shefalirai/Documents/MATLAB/MSCcodebase-master/Utilities/Infomap_wrapper';

% Get averaged subjects networks
AvgSub=ciftiopen('/Users/shefalirai/Desktop/consensus_surface/AvgSubs_ConsensusInfomap_17netFINAL.pscalar.nii', '/Applications/workbench/bin_macosx64/wb_command');
AvgSub=AvgSub.cdata;

for subjects=1:10
    consensus_maker_knowncolors_textonly(AllSubs_Consensus(:,subjects),AvgSub, sprintf('Sub%dvGroup',subjects));
    fid = fopen(sprintf('Sub%dvGroup_recolored.txt',subjects));
    Allsubs_FinalConsensus{subjects} = textscan(fid,'%f');
    fclose(fid);
    Allsubs_FinalConsensus{subjects}=cell2mat(Allsubs_FinalConsensus{subjects});
end

Allsubs_FinalConsistent=[Allsubs_FinalConsensus{1,1} Allsubs_FinalConsensus{1,2} Allsubs_FinalConsensus{1,3} Allsubs_FinalConsensus{1,4} Allsubs_FinalConsensus{1,5} Allsubs_FinalConsensus{1,6} Allsubs_FinalConsensus{1,7} Allsubs_FinalConsensus{1,8} Allsubs_FinalConsensus{1,9} Allsubs_FinalConsensus{1,10}];

%EDITED the consensus_maker_knowncolors_textonly.m file!!!
% To have less than 22-23 networks (using the .m file without modifications)
% I edited the .m file and removed potential colors list (remove
% 17,16,15,14,13
% new list is: [1 2 10 9 3 5 6 11 7 8 12 4];


% visualize on the surface
for subs=1:10
    allsubs_consistent{subs}=ciftiopen(sprintf('/Users/shefalirai/Desktop/parcelled_subjects/sub%d_1000parc_17nets.ptseries.nii',subs), '/Applications/workbench/bin_macosx64/wb_command');
    allsubs_consistent{subs}.cdata=Allsubs_FinalConsistent(:,subs);
    ciftisavereset(allsubs_consistent{subs},sprintf('/Users/shefalirai/Desktop/consistent_surface/Sub%d_Consistent_EDITED_Removeupto13nets.pscalar.nii',subs), '/Applications/workbench/bin_macosx64/wb_command');
end



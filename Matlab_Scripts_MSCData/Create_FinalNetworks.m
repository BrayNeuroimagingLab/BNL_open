function Create_FinalNetworks(folderpath, parcellation_folderpath, variable_stringname, personID, task)
%Combines these 5 scripts: Open_CiftiTimeseries.m, MeanCenter_Timeseries.mCreate_Consensus_Networks.m, Consensus_Communities.m, Run_Infomap_ConsensusD.m
%This function takes about 2 minutes to run per 6 sessions of each subject's data 
%Example usage: Create_FinalNetworks('/Users/shefalirai/Desktop', '/Users/shefalirai/Downloads', child002, 'child002', '002C', 'video');

subjectdata=Open_CiftiTimeseries(folderpath, personID, task);

variable_name=MeanCenter_Timeseries(subjectdata);

variable_consensusnetworks=Create_Consensus_Networks(folderpath, parcellation_folderpath,variable_name, variable_stringname, personID);

Consensus_Communities(folderpath, variable_consensusnetworks, variable_stringname);

Run_Infomap_ConsensusD(folderpath, variable_stringname);

end


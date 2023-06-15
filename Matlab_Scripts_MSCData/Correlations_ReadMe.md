Test-retest reliabilty and individual functional network scripts for Midnight Scan Club dataset
Author: Shefali Rai
Last updated: June 3, 2021 

Must have the following in your Matlab path:
   ciftiopen.m 
   ciftisave.m
   ciftisavereset.m
   Open_CiftiTimeseries.m
   Remove_Motion.m
   MeanCenter_Timeseries.m

Part 1:
To perfrom test-retest analysis and create group-averaged reliability maps:
    ***1A. Motor_Matched.m (If you want to concatenate all tasks according to the lowest motor matched volume)***
    1. Create_Connectomes.m
    2. Concatenate_Connectomes.m
    3. Connectome_Corr.m 
    4. Test_Retest_MSC.m

Part 2:
To create tSNR, SD and Mean Signal group-averaged maps:
    1. Open_CiftiTimeseries.m
    2. Remove_Motion.m 
    3. Signal_Property_Values.m
    4. Signal_AllTask.m

Part 3:
To create individual networks:
    1. Create_Connectomes.m 
    2. Create_Consensus_Networks.m
    3. Consensus_Communities.m
    4. Run_Infomap_ConsensusD.m
    5. Group_Parcels_Avg.m
    6. Consensus_Maker_Colors.m

Part 4:
To perform ICC: 
*Must have created group averaged consensus networks from Part 3
    1. Open_CiftiTimeseries.m
    2. Remove_Motion.m
    3. MeanCenter_Timeseries.m
    4. Edge_ICC.m 

Part 5:
To perform network-wise group level Reliability versus tSNR plots: 
 *Must have created group averaged consensus networks
 *After running Parts 1-3
    1. Network_tSNRvReli.m 



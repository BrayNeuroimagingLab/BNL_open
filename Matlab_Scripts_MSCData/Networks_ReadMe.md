*Creating functional networks for PrcKids*
*Author: Shefali Rai*
*Last updated: Oct 6, 2021*

_Must have the following downloaded and in your Matlab path:_
   ciftiopen.m 
   ciftisave.m
   ciftisavereset.m
   cifti-matlab-master
   gifti-1.6
   BCT folder (threshold_proportional.m)
   Open_CiftiTimeseries.m
   MeanCenter_Timeseries.m
   *(Remove_Motion.m is an old file only needed if not using ME data that requires motion removal)
   Create_Consensus_Networks.m
   Consensus_Communities.m
   Run_Infomap_ConsensusD.m
   Create_FinalNetworks.m
   CreateNetworks_KMeans

IF USING INFOMAP: 

_Must download the following:_
HCP Schaefer atlas to a folder(easiest to leave in Downloads folder), we are specifically using this file: Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii

_Create an empty folder in your directory called Infomap_Out (easiest to have on Desktop or Documents or the folder/directly you are saving intermediate files on)_

_To create individual networks run:_
    1. Create_FinalNetworks.m

After running the script, open the appropriate .spec file from your data_path/subject/MNINonLinear/fsaverage_LR32k folder in wb_view and click Load. 
Change the view to inflated.32k_fs_LR.surf.gii for both left and right surfaces
Double click to open the XXXME_17networks.pscalar.nii file that was created from this script
Click the wrench tool (under settings) and select the power_surf palette

_All intermediate files can be deleted if needed_ 

***********************************************************************************************************
IF USING KMEANS FOR 3D BRAINS:

_Must download the following:_
HCP Schaefer atlas to a folder(easiest to leave in Downloads folder), we are specifically using this file: Parcellations/HCP/fslr32k/cifti/Schaefer2018_1000Parcels_17Networks_order.dlabel.nii

_To create individual networks run:_
    1. Create_FinalNetworksKMeans.m

After running the script, open the appropriate .spec file from your data_path/subject/MNINonLinear/fsaverage_LR32k folder in wb_view and click Load. 
Change the view to inflated.32k_fs_LR.surf.gii for both left and right surfaces
Double click to open the XXXME_Allvideos_parc_Kmeans.pscalar.nii file that was created from this script
Click the wrench tool (under settings) and select the power_surf palette

_All intermediate files can be deleted if needed_ 


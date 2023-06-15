function [Avg_tSNR_Sub]=tSNR_Values_Jan2023(Mean_Sub, Std_Sub)
% Average tSNR, SD, Mean signal Map for each subject
% Mean, SD and tSNR of each session per subject on the original time series
% For this analysis do not mean center the timeseries since we want to
% analyze signal variation 
%excluding MSC08 



Avg_tSNR_Sub=Mean_Sub./Std_Sub;





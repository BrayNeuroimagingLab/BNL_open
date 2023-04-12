This is the GitHub repository for the code from Tansey et al. (2023) "Functional MRI responses to naturalistic stimuli are increasingly typical across early childhood."

There are 4 scripts used in this manuscript:
1) study_funcs.py -> the functions written for these analyses that the other Python scripts call on
2) TemporalROIAnalyses -> this is the code for the shred group average signal regression analysis. The results of this analysis can be found in the "Group average signal regression analysis" section of the Results, and in Figure 4.
3) SpatialROIAnalyses -> this is the code for both the diffuse to localized analysis and the calculation of the Dice coefficients for the Dice coefficient analysis (the final LMEs used for this analysis can be found in the R script listed below). You can find these results in their respective sections of the Result and in Figure 5 of the manuscript.
4) SpatialROI_lme.R -> this is the R code used to create linear mixed effects models with crossed random effects to do the Dice coefficient analysis. This code is based on the LMEs with CRE that are recommended for pairwise ISC analysis in Chen et al. (2016) ("Untangling the effects... part II") and their subsequent implementation in the AFNI program 3dISC (https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dISC.html).

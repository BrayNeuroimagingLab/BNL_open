------------------------------------------------
How to generate the data used in each EEG figure
------------------------------------------------

Read the preprocessing guide up to source localization 7.py. That does all the relevant preprocessing of raw data and generates the forward solution between source and sensor space.

-Running source_localization_8_june2024.py makes connectomes for each recording for all relevant connectivity measures. This is used for figures 1-3 and 5
-Running source_localization_8_makesimconnectomes.py makes connectomes based on simulated data. This is used for figures 1-3 and 4
-Running source_localization_8_task_june2024_v2.py makes connectomes for all recordings from ses1-2 and all recordings from ses3-4. This is used for figure 6
-Running source_localization_8_task_june2024_agesessplit.py does something conceptually similar, but only uses the connectomes that are shared between parent and child, i.e., the 5 shared files for ses1-2 and the 5 shared for ses3-4 (assuming none missing). This is used for figure 7


------------------------------------------------
Figure 1,2,3, average connectomes
------------------------------------------------
After generating simulated connectomes and real connectomes

The program makeavg_to_plot_average_connectome.py creates average connectomes for both sim and non simulated connectomes

The programs simtoreal_correlations.py, simtoreal_avgdf_correlations.py, simtoreal_avg of indivs_correlations.py creates the correlations between real and simulated connectomes
	-simtoreal = for each recording, the correlation between sim and real
	-simtoreal_avg of indivs = average those correlations
-simtoreal_avgdf = the real to sim correlation for the average real connectome and average simulated connectome

The program fig1_plot_average_connectome_plotting.py makes the plots

------------------------------------------------
Figure 4, fingerprinting stats with fake connectomes
------------------------------------------------
After generating the simulated connectomes

Analyzeconnectomes fingerprint simulated_connectomes.py creates the fingerprinting/matching stats

Fig4_fingerprinting.py makes the plots (set to use fake data rather than real data)

------------------------------------------------
Figure 5 and fingerprinting stats with real connectomes
------------------------------------------------
After generating the real connectomes

Analyzeconnectomes fingerprint june2024.py creates the fingerprinting/matching stats

Fig4_fingerprinting.py makes the plots (set to use real data rather than fake data)

Fig5_sup_fingerprinting_stats_chart.py makes the chart of significance tests between connectivity measures


------------------------------------------------
Figure 6 fingerprinting by timesubset
------------------------------------------------
After generating the connectomes for ses1+2 and ses3+4 for the different number of epochs

Analyzeconnectomes fingerprint firsthalfsecondhalf June2024.py will calculate the fingerprinting/matching stats

Fig6_fingerprintingbylength.py will make the plot

------------------------------------------------
Figure 7 age effects
------------------------------------------------
After generating the connectomes for ses1+2 and ses3+4, only using the overlapping files between parent and child

The program ageeffect_timesubset_nov2024_pt1.py runs t-tests for each edge, comparing parent vs child. This data is then used by ageeffect_timesubset_nov2024_pt2.py to run the correlation between ses12 and ses34 edge t values. Do the same edges show age effects? 

The program fig7_ageeffectbylength.py makes the plot.



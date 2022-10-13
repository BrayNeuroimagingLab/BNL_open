#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 10:44:54 2022

@author: ryanntansey
"""
import os
import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.multitest import multipletests

os.chdir('/Users/ryanntansey/Dropbox/Aim2_Age_FinalScripts/')
from study_funcs import pcorr_perm, percent_sig_voxels

# =============================================================================
# Load variables for analysis
# =============================================================================
behav_data = pd.read_pickle('/Users/ryanntansey/Dropbox/Aim2_Age_FinalScripts/behav_data_Jul29-2022.pkl')
gm_mask = '/Users/ryanntansey/Dropbox/parcellations/HarvardOxford_atlas/HarvardOxford-cort-maxprob-thr25-2mm_Mask.nii.gz'
tmasks = pd.read_pickle('/Users/ryanntansey/Dropbox/Aim2_Age_FinalScripts/tmasks.pkl')

# ROIs
rhFFA = '/Users/ryanntansey/Documents/visfAtlas/nifti_volume/visfAtlas_faces/rh_FFA_2mm.nii'
lhFFA = '/Users/ryanntansey/Documents/visfAtlas/nifti_volume/visfAtlas_faces/lh_FFA_flip_2mm.nii'

rhSTS = '/Users/ryanntansey/Documents/SENSAAS/SENSAAS_STS3_and_STS4_rh.nii'
lhSTS = '/Users/ryanntansey/Documents/SENSAAS/SENSAAS_STS3_and_STS4.nii'


# =============================================================================
# Percent GM associated with shared signal --> create DataFrame
# =============================================================================
rhFFA_zmaps = glob.glob('/Users/ryanntansey/Documents/VSDevel_final_preproc_fMRI/FEAT_results_rhFFA/*_rhFFA.feat/stats/zstat1.nii.gz')
rhFFA_gm_perc = [percent_sig_voxels(i, gm_mask, 1.6449) for i in rhFFA_zmaps]
rhFFA_perc_data = pd.DataFrame()
rhFFA_perc_data['AgeAtScan'] = behav_data['AgeAtScan']
rhFFA_perc_data['Motion'] = behav_data['volmotion']
rhFFA_perc_data['Sex'] = behav_data['Gender']
rhFFA_perc_data['Sex'] = rhFFA_perc_data['Sex'].replace(to_replace = 'F', value = 0)
rhFFA_perc_data['Sex'] = rhFFA_perc_data['Sex'].replace(to_replace = 'M', value = 1)
rhFFA_perc_data['PercentGM'] = rhFFA_gm_perc 

lhFFA_zmaps = glob.glob('/Users/ryanntansey/Documents/VSDevel_final_preproc_fMRI/FEAT_results_lhFFA/*_lhFFA.feat/stats/zstat1.nii.gz')
lhFFA_gm_perc = [percent_sig_voxels(i, gm_mask, 1.6449) for i in lhFFA_zmaps]
lhFFA_perc_data = pd.DataFrame()
lhFFA_perc_data['AgeAtScan'] = behav_data['AgeAtScan']
lhFFA_perc_data['Motion'] = behav_data['volmotion']
lhFFA_perc_data['Sex'] = behav_data['Gender']
lhFFA_perc_data['Sex'] = lhFFA_perc_data['Sex'].replace(to_replace = 'F', value = 0)
lhFFA_perc_data['Sex'] = lhFFA_perc_data['Sex'].replace(to_replace = 'M', value = 1)
lhFFA_perc_data['PercentGM'] = lhFFA_gm_perc 


rhSTS_zmaps = glob.glob('/Users/ryanntansey/Documents/VSDevel_final_preproc_fMRI/FEAT_results_rhSTS/*_rhSTS.feat/stats/zstat1.nii.gz')
rhSTS_gm_perc = [percent_sig_voxels(i, gm_mask, 1.6449) for i in rhSTS_zmaps]
rhSTS_perc_data = pd.DataFrame()
rhSTS_perc_data['AgeAtScan'] = behav_data['AgeAtScan']
rhSTS_perc_data['Motion'] = behav_data['volmotion']
rhSTS_perc_data['Sex'] = behav_data['Gender']
rhSTS_perc_data['Sex'] = rhSTS_perc_data['Sex'].replace(to_replace = 'F', value = 0)
rhSTS_perc_data['Sex'] = rhSTS_perc_data['Sex'].replace(to_replace = 'M', value = 1)
rhSTS_perc_data['PercentGM'] = rhSTS_gm_perc 

lhSTS_zmaps = glob.glob('/Users/ryanntansey/Documents/VSDevel_final_preproc_fMRI/FEAT_results_lhSTS/*_lhSTS.feat/stats/zstat1.nii.gz')
lhSTS_gm_perc = [percent_sig_voxels(i, gm_mask, 1.6449) for i in lhSTS_zmaps]
lhSTS_perc_data = pd.DataFrame()
lhSTS_perc_data['AgeAtScan'] = behav_data['AgeAtScan']
lhSTS_perc_data['Motion'] = behav_data['volmotion']
lhSTS_perc_data['Sex'] = behav_data['Gender']
lhSTS_perc_data['Sex'] = lhSTS_perc_data['Sex'].replace(to_replace = 'F', value = 0)
lhSTS_perc_data['Sex'] = lhSTS_perc_data['Sex'].replace(to_replace = 'M', value = 1)
lhSTS_perc_data['PercentGM'] = lhSTS_gm_perc 


# =============================================================================
# Percent GM associated with shared signal --> do hypothesis testing
# =============================================================================
rhFFA_perc_r, rhFFA_perc_p, rhFFA_perc_null = pcorr_perm(rhFFA_perc_data, 
                                                         'AgeAtScan', 
                                                         'PercentGM', 
                                                         covar = ['Motion', 'Sex'],
                                                         method = 'spearman', 
                                                         n_perms = 10000, 
                                                         tail = 'less')


lhFFA_perc_r, lhFFA_perc_p, lhFFA_perc_null = pcorr_perm(lhFFA_perc_data, 
                                                         'AgeAtScan', 
                                                         'PercentGM', 
                                                         covar = ['Motion', 'Sex'],
                                                         method = 'spearman', 
                                                         n_perms = 10000, 
                                                         tail = 'less')


rhSTS_perc_r, rhSTS_perc_p, rhSTS_perc_null = pcorr_perm(rhSTS_perc_data, 
                                                         'AgeAtScan', 
                                                         'PercentGM', 
                                                         covar = ['Motion', 'Sex'],
                                                         method = 'spearman', 
                                                         n_perms = 10000, 
                                                         tail = 'less')

lhSTS_perc_r, lhSTS_perc_p, lhSTS_perc_null = pcorr_perm(lhSTS_perc_data, 
                                                         'AgeAtScan', 
                                                         'PercentGM', 
                                                         covar = ['Motion', 'Sex'],
                                                         method = 'spearman', 
                                                         n_perms = 10000, 
                                                         tail = 'less')


# =============================================================================
# Multiple comparisons
# =============================================================================
multipletests([rhFFA_perc_p, lhFFA_perc_p, rhSTS_perc_p, lhSTS_perc_p],
              alpha = 0.05, method = 'fdr_bh')


# =============================================================================
# FIGURES - setting global Seaborn variables
# =============================================================================
sns.set(rc={'figure.figsize':(5,4)})
sns.set(rc={"figure.dpi":1000, 'savefig.dpi':1000})
sns.set_context('notebook')
sns.set_style('ticks')

pal = sns.color_palette('viridis', n_colors = 10)
# 0 = FFA
# 7 = STS


# =============================================================================
# FIGURES - figure 2
# =============================================================================
fig, subax = plt.subplots(2, 2, sharex = True, sharey = True, figsize = (10,8))
lhFFA_perc_fig = sns.regplot(ax = subax[0,0], x = lhFFA_perc_data['AgeAtScan'], y = lhFFA_perc_data['PercentGM'], color = pal[0], ci = None)
rhFFA_perc_fig = sns.regplot(ax = subax[0,1], x = rhFFA_perc_data['AgeAtScan'], y = rhFFA_perc_data['PercentGM'], color = pal[0], ci = None)
lhSTS_perc_fig = sns.regplot(ax = subax[1,0], x = lhSTS_perc_data['AgeAtScan'], y = lhSTS_perc_data['PercentGM'], color = pal[7], ci = None)
rhSTS_perc_fig = sns.regplot(ax = subax[1,1], x = rhSTS_perc_data['AgeAtScan'], y = rhSTS_perc_data['PercentGM'], color = pal[7], ci = None)

lhFFA_perc_fig.set_title('Left FFA', weight = 'bold')
rhFFA_perc_fig.set_title('Right FFA', weight = 'bold')
lhSTS_perc_fig.set_title('Left STS', weight = 'bold')
rhSTS_perc_fig.set_title('Right STS', weight = 'bold')

lhFFA_perc_fig.set_ylabel('% of grey matter voxels')

rhFFA_perc_fig.set_ylabel(' ')
lhSTS_perc_fig.set_ylabel('% of grey matter voxels')
rhSTS_perc_fig.set_ylabel(' ')

lhFFA_perc_fig.set_xlabel(' ')
rhFFA_perc_fig.set_xlabel(' ')
lhSTS_perc_fig.set_xlabel('Age (years)')
rhSTS_perc_fig.set_xlabel('Age (years)')

subax[0,0].spines.right.set_visible(False)
subax[0,0].spines.top.set_visible(False)
subax[0,0].text(4.1, 0.10, 'rho = ' + '%.4f'%(lhFFA_perc_r))
subax[0,0].text(4.1, 0.085, 'p = ' + '%.4f'%(lhFFA_perc_p))

subax[0,1].spines.right.set_visible(False)
subax[0,1].spines.top.set_visible(False)
subax[0,1].text(4.1, 0.10, 'rho = ' + '%.4f'%(rhFFA_perc_r))
subax[0,1].text(4.1, 0.085, 'p = ' + '%.4f'%(rhFFA_perc_p))

subax[1,0].spines.right.set_visible(False)
subax[1,0].spines.top.set_visible(False)
subax[1,0].text(4.1, 0.10, 'rho = ' + '%.4f'%(lhSTS_perc_r))
subax[1,0].text(4.1, 0.085, 'p = ' + '%.4f'%(lhSTS_perc_p))

subax[1,1].spines.right.set_visible(False)
subax[1,1].spines.top.set_visible(False)
subax[1,1].text(4.1, 0.10, 'rho = ' + '%.4f'%(rhSTS_perc_r))
subax[1,1].text(4.1, 0.085, 'p = ' + '%.4f'%(rhSTS_perc_p))


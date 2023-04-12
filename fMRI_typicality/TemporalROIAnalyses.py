#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 12:32:46 2022

@author: ryanntansey
"""
import os
import glob
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.multitest import multipletests

os.chdir('/Users/.../code_folder/')
from study_funcs import pcorr_perm, generate_ROI_ts, reg_ts

# =============================================================================
# Load variables for analysis
# =============================================================================
fmri_files = sorted(glob.glob('/Users/.../sub-*_ses-*.nii.gz'))
behav_data = pd.read_pickle('/Users/.../behav_data.pkl')
subs_names = behav_data.index.values
tmasks = pd.read_pickle('/Users/.../tmasks.pkl')
motion_dir = '/Users/.../Motion_Vols/'
motion_ext = '_MotionVols.txt'

# ROIs
rhFFA = '/Users/.../rh_FFA_2mm.nii'
lhFFA = '/Users/.../lh_FFA_flip_2mm.nii'

rhSTS = '/Users/.../SENSAAS_STS3_and_STS4_rh.nii'
lhSTS = '/Users/.../SENSAAS_STS3_and_STS4.nii'

# =============================================================================
# Generate the leave-one-out group average time courses (w/ standardizing
#   + censoring)
# =============================================================================
rhFFA_indiv_ts_censor, rhFFA_grp_avg_ts = generate_ROI_ts(fmri_files, tmasks, 
                                                          rhFFA, subs_names, 
                                                          433, zscore = True, 
                                                          censor = True, 
                                                          grp_avg = True)

lhFFA_indiv_ts_censor, lhFFA_grp_avg_ts = generate_ROI_ts(fmri_files, tmasks, 
                                                          lhFFA, subs_names, 
                                                          433, zscore = True, 
                                                          censor = True, 
                                                          grp_avg = True)


rhSTS_indiv_ts_censor, rhSTS_grp_avg_ts = generate_ROI_ts(fmri_files, tmasks, 
                                                          rhSTS, subs_names, 
                                                          433, zscore = True, 
                                                          censor = True, 
                                                          grp_avg = True)

lhSTS_indiv_ts_censor, lhSTS_grp_avg_ts = generate_ROI_ts(fmri_files, tmasks, 
                                                          lhSTS, subs_names, 
                                                          433, zscore = True, 
                                                          censor = True, 
                                                          grp_avg = True)


# =============================================================================
# Generate the individual ROI time courses (w/o standardizing or censoring)
# =============================================================================
rhFFA_indiv_ts = generate_ROI_ts(fmri_files, tmasks, rhFFA, subs_names, 433,
                                 zscore = False, censor = False, grp_avg = False)

lhFFA_indiv_ts = generate_ROI_ts(fmri_files, tmasks, lhFFA, subs_names, 433,
                                 zscore = False, censor = False, grp_avg = False)


rhSTS_indiv_ts = generate_ROI_ts(fmri_files, tmasks, rhSTS, subs_names, 433,
                                 zscore = False, censor = False, grp_avg = False)

lhSTS_indiv_ts = generate_ROI_ts(fmri_files, tmasks, lhSTS, subs_names, 433,
                                 zscore = False, censor = False, grp_avg = False)


# =============================================================================
# Regress group average time course out of each individual's time course
# =============================================================================
rhFFA_betas, rhFFA_coefs, rhFFA_resid = reg_ts(rhFFA_indiv_ts, rhFFA_grp_avg_ts, motion_dir, motion_ext, leaveout = True)
lhFFA_betas, lhFFA_coefs, lhFFA_resid = reg_ts(lhFFA_indiv_ts, lhFFA_grp_avg_ts, motion_dir, motion_ext, leaveout = True)
rhSTS_betas, rhSTS_coefs, rhSTS_resid = reg_ts(rhSTS_indiv_ts, rhSTS_grp_avg_ts, motion_dir, motion_ext, leaveout = True)
lhSTS_betas, lhSTS_coefs, lhSTS_resid = reg_ts(lhSTS_indiv_ts, lhSTS_grp_avg_ts, motion_dir, motion_ext, leaveout = True)


# =============================================================================
# Make DataFrames with all group level variables for correlations
# =============================================================================
rhFFA_data = pd.DataFrame()
rhFFA_data['AgeAtScan'] = behav_data['AgeAtScan']
rhFFA_data['Beta'] = rhFFA_betas
rhFFA_data['RStDev'] = [np.std(i) for i in rhFFA_resid]
rhFFA_data['RMean'] = [np.mean(i) for i in rhFFA_resid]
rhFFA_data['Sex'] = behav_data['Gender']
rhFFA_data['Motion'] = behav_data['volmotion']

lhFFA_data = pd.DataFrame()
lhFFA_data['AgeAtScan'] = behav_data['AgeAtScan']
lhFFA_data['Beta'] = lhFFA_betas
lhFFA_data['RStDev'] = [np.std(i) for i in lhFFA_resid]
lhFFA_data['RMean'] = [np.mean(i) for i in lhFFA_resid]
lhFFA_data['Sex'] = behav_data['Gender']
lhFFA_data['Motion'] = behav_data['volmotion']

rhSTS_data = pd.DataFrame()
rhSTS_data['AgeAtScan'] = behav_data['AgeAtScan']
rhSTS_data['Beta'] = rhSTS_betas
rhSTS_data['RStDev'] = [np.std(i) for i in rhSTS_resid]
rhSTS_data['RMean'] = [np.mean(i) for i in rhSTS_resid]
rhSTS_data['Sex'] = behav_data['Gender']
rhSTS_data['Motion'] = behav_data['volmotion']

lhSTS_data = pd.DataFrame()
lhSTS_data['AgeAtScan'] = behav_data['AgeAtScan']
lhSTS_data['Beta'] = lhSTS_betas
lhSTS_data['RStDev'] = [np.std(i) for i in lhSTS_resid]
lhSTS_data['RMean'] = [np.mean(i) for i in lhSTS_resid]
lhSTS_data['Sex'] = behav_data['Gender']
lhSTS_data['Motion'] = behav_data['volmotion']


# =============================================================================
# Compute partial Spearman correlations + permutation tests
# =============================================================================
rhFFA_beta_r, rhFFA_beta_p, rhFFA_beta_null = pcorr_perm(rhFFA_data, 
                                                         'AgeAtScan', 
                                                         'Beta', 
                                                         covar = ['Sex', 'Motion'],
                                                         method = 
                                                         'spearman', 
                                                         n_perms = 10000, 
                                                         tail = 'greater')
rhFFA_rstd_r, rhFFA_rstd_p, rhFFA_rstd_null = pcorr_perm(rhFFA_data, 
                                                         'AgeAtScan', 
                                                         'RStDev', 
                                                         covar = ['Sex', 'Motion'],
                                                         method = 
                                                         'spearman', 
                                                         n_perms = 10000, 
                                                         tail = 'less')


lhFFA_beta_r, lhFFA_beta_p, lhFFA_beta_null = pcorr_perm(lhFFA_data, 
                                                         'AgeAtScan', 
                                                         'Beta', 
                                                         covar = ['Sex', 'Motion'],
                                                         method = 
                                                         'spearman', 
                                                         n_perms = 10000, 
                                                         tail = 'greater')
lhFFA_rstd_r, lhFFA_rstd_p, lhFFA_rstd_null = pcorr_perm(lhFFA_data, 
                                                         'AgeAtScan', 
                                                         'RStDev', 
                                                         covar = ['Sex', 'Motion'],
                                                         method = 
                                                         'spearman', 
                                                         n_perms = 10000, 
                                                         tail = 'less')


rhSTS_beta_r, rhSTS_beta_p, rhSTS_beta_null = pcorr_perm(rhSTS_data, 
                                                         'AgeAtScan', 
                                                         'Beta', 
                                                         covar = ['Sex', 'Motion'],
                                                         method = 
                                                         'spearman', 
                                                         n_perms = 10000, 
                                                         tail = 'greater')
rhSTS_rstd_r, rhSTS_rstd_p, rhSTS_rstd_null = pcorr_perm(rhSTS_data, 
                                                         'AgeAtScan', 
                                                         'RStDev', 
                                                         covar = ['Sex', 'Motion'],
                                                         method = 
                                                         'spearman', 
                                                         n_perms = 10000, 
                                                         tail = 'less')


lhSTS_beta_r, lhSTS_beta_p, lhSTS_beta_null = pcorr_perm(lhSTS_data, 
                                                         'AgeAtScan', 
                                                         'Beta', 
                                                         covar = ['Sex', 'Motion'],
                                                         method = 
                                                         'spearman', 
                                                         n_perms = 10000, 
                                                         tail = 'greater')
lhSTS_rstd_r, lhSTS_rstd_p, lhSTS_rstd_null = pcorr_perm(lhSTS_data, 
                                                         'AgeAtScan', 
                                                         'RStDev', 
                                                         covar = ['Sex', 'Motion'],
                                                         method = 
                                                         'spearman', 
                                                         n_perms = 10000, 
                                                         tail = 'less')


# =============================================================================
# Multiple comparisons
# =============================================================================
multipletests([rhFFA_beta_p, lhFFA_beta_p, rhSTS_beta_p, lhSTS_beta_p],
              alpha = 0.05, method = 'fdr_bh')

multipletests([rhFFA_rstd_p, lhFFA_rstd_p, rhSTS_rstd_p, lhSTS_rstd_p],
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
# FIGURES - sfigure 3
# =============================================================================
fig, subax = plt.subplots(2, 4, sharex = True, sharey = True, figsize = (15,8))
lhFFA_beta_fig = sns.regplot(ax = subax[0,0], x = lhFFA_data['AgeAtScan'], y = lhFFA_data['Beta'], color = pal[0], ci = None)
rhFFA_beta_fig = sns.regplot(ax = subax[0,1], x = rhFFA_data['AgeAtScan'], y = rhFFA_data['Beta'], color = pal[0], ci = None)
lhSTS_beta_fig = sns.regplot(ax = subax[0,2], x = lhSTS_data['AgeAtScan'], y = lhSTS_data['Beta'], color = pal[7], ci = None)
rhSTS_beta_fig = sns.regplot(ax = subax[0,3], x = rhSTS_data['AgeAtScan'], y = rhSTS_data['Beta'], color = pal[7], ci = None)

lhFFA_RStDev_fig = sns.regplot(ax = subax[1,0], x = lhFFA_data['AgeAtScan'], y = lhFFA_data['RStDev'], color = pal[0], ci = None)
rhFFA_RStDev_fig = sns.regplot(ax = subax[1,1], x = rhFFA_data['AgeAtScan'], y = rhFFA_data['RStDev'], color = pal[0], ci = None)
lhSTS_RStDev_fig = sns.regplot(ax = subax[1,2], x = lhSTS_data['AgeAtScan'], y = lhSTS_data['RStDev'], color = pal[7], ci = None)
rhSTS_RStDev_fig = sns.regplot(ax = subax[1,3], x = rhSTS_data['AgeAtScan'], y = rhSTS_data['RStDev'], color = pal[7], ci = None)


lhFFA_beta_fig.set_title('Left FFA', weight = 'bold')
rhFFA_beta_fig.set_title('Right FFA', weight = 'bold')
lhSTS_beta_fig.set_title('Left STS', weight = 'bold')
rhSTS_beta_fig.set_title('Right STS', weight = 'bold')

lhFFA_beta_fig.set_ylabel('β value of group average time series')
lhFFA_RStDev_fig.set_ylabel('Standard deviation of residuals')

rhFFA_beta_fig.set_ylabel(' ')
lhSTS_beta_fig.set_ylabel(' ')
rhSTS_beta_fig.set_ylabel(' ')
rhFFA_RStDev_fig.set_ylabel(' ')
lhSTS_RStDev_fig.set_ylabel(' ')
rhSTS_RStDev_fig.set_ylabel(' ')


lhFFA_beta_fig.set_xlabel(' ')
rhFFA_beta_fig.set_xlabel(' ')
lhSTS_beta_fig.set_xlabel(' ')
rhSTS_beta_fig.set_xlabel(' ')
lhFFA_RStDev_fig.set_xlabel('Age (years)')
rhFFA_RStDev_fig.set_xlabel('Age (years)')
lhSTS_RStDev_fig.set_xlabel('Age (years)')
rhSTS_RStDev_fig.set_xlabel('Age (years)')

# beta
subax[0,0].spines.right.set_visible(False)
subax[0,0].spines.top.set_visible(False)
subax[0,0].text(4.2, 4.6, 'rho = ' + '%.4f'%(lhFFA_beta_r))
subax[0,0].text(4.2, 4.2, 'p = ' + '%.4f'%(lhFFA_beta_p))

subax[0,1].spines.right.set_visible(False)
subax[0,1].spines.top.set_visible(False)
subax[0,1].text(4.2, 4.6, 'rho = ' + '%.4f'%(rhFFA_beta_r))
subax[0,1].text(4.2, 4.2, 'p = ' + '%.4f'%(rhFFA_beta_p))

subax[0,2].spines.right.set_visible(False)
subax[0,2].spines.top.set_visible(False)
subax[0,2].text(6.2, 4.6, 'rho = ' + '%.4f'%(lhSTS_beta_r))
subax[0,2].text(6.2, 4.2, 'p = ' + '%.4f'%(lhSTS_beta_p))

subax[0,3].spines.right.set_visible(False)
subax[0,3].spines.top.set_visible(False)
subax[0,3].text(4.2, 4.6, 'rho = ' + '%.4f'%(rhSTS_beta_r))
subax[0,3].text(4.2, 4.2, 'p = ' + '%.4f'%(rhSTS_beta_p))


# rstdev
subax[1,0].spines.right.set_visible(False)
subax[1,0].spines.top.set_visible(False)
subax[1,0].text(4.2, 4.6, 'rho = ' + '%.4f'%(lhFFA_rstd_r))
subax[1,0].text(4.2, 4.2, 'p = ' + '%.4f'%(lhFFA_rstd_p))

subax[1,1].spines.right.set_visible(False)
subax[1,1].spines.top.set_visible(False)
subax[1,1].text(4.2, 4.6, 'rho = ' + '%.4f'%(rhFFA_rstd_r))
subax[1,1].text(4.2, 4.2, 'p = ' + '%.4f'%(rhFFA_rstd_p))

subax[1,2].spines.right.set_visible(False)
subax[1,2].spines.top.set_visible(False)
subax[1,2].text(4.2, 4.6, 'rho = ' + '%.4f'%(lhSTS_rstd_r))
subax[1,2].text(4.2, 4.2, 'p = ' + '%.4f'%(lhSTS_rstd_p))

subax[1,3].spines.right.set_visible(False)
subax[1,3].spines.top.set_visible(False)
subax[1,3].text(4.2, 4.6, 'rho = ' + '%.4f'%(rhSTS_rstd_r))
subax[1,3].text(4.2, 4.2, 'p = ' + '%.4f'%(rhSTS_rstd_p))


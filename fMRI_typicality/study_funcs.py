#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 12:06:14 2022

@author: ryanntansey

updated: January 17th, 2023
added pairwise_dice

"""
import numpy as np
import nibabel as nib 
import pandas as pd
from datetime import datetime
from nilearn.maskers import NiftiLabelsMasker
from nilearn.masking import apply_mask
from pingouin import partial_corr, corr
from statsmodels.tools.tools import add_constant
from statsmodels.regression.linear_model import OLS


def generate_ROI_ts(fmri_files, tmasks, ROI_file, subs_list, n_TRs, 
                    zscore = True, censor = True, grp_avg = False):
   
    """
    Parameters
    ----------
    fmri_files : list of str
        A list containing the strings of the filenames where each 
        participant's fMRI data can be found.
        
    tmasks : Pandas DataFrame
        A Pandas DataFrame containing all the temporal masks from each
        subject (from censoring). Should be in the format of n_TRs x n_subs, 
        with each non-censored volume labeled as 1, and each censored
        volume labeled as NaN.
        
    ROI_file : str
        File where the ROI can be found.
        
    subs_list : list of str
        A list of strings of each subject's name/identifier.
        
    n_TRs : float
        A float of the number of volumes in your runs.
        
    zscore : Boolean
        Whether or not you want to standardize the time course of each 
        subject before averaging together. Default = True.
        
    censor : Boolean
        Whether or not you want to censor the time courses by their temporal
        masks or not (will set censored volume to NaN). Default = True.
        
    grp_avg : Boolean
        Whether or not you want to also create leave-one-out group averages
        of the time courses. Default = False.

    Returns
    -------
    ROI_ts_df : Pandas DataFrame
        A n_TRs x n_subs DataFrame that contains, in each column, the ROI 
        time course for the subject whose name is at the top of the column.
    
    rest_grp_avg : Pandas DataFrame
        A n_TRs x n_subs DataFrame that contains, in each column, the 
        leave-one-out group average time course taken over all subjects EXCEPT
        the subject whose name is at the top of the column. I.e., the 
        subject in the column name is the left-out subject, and the column
        values are the average time course of all other subjects.
        
    """
    
    print('Starting to generate ROI time courses... start time: ' + datetime.now().strftime('%H:%M:%S'))
    
    # Set up variables needed in the function
    n_subs = len(fmri_files)
    
    # Load in each participant's ROI time course
    ROI_ts = np.zeros((n_TRs, n_subs))
    ROI_masker = NiftiLabelsMasker(labels_img = ROI_file, standardize = zscore)
    for i in range(n_subs):
        print('Loading subject ' + subs_list[i] + ', start time: ' + datetime.now().strftime('%H:%M:%S'))
        indiv_img = nib.load(fmri_files[i])
        indiv_ROI = ROI_masker.fit_transform(indiv_img)
        indiv_ROI = [i[0] for i in indiv_ROI]
        ROI_ts[:,i] = indiv_ROI
        print('Finished subject ' + subs_list[i] + ', end time: ' + datetime.now().strftime('%H:%M:%S'))
    ROI_ts_df = pd.DataFrame(ROI_ts)
    ROI_ts_df.columns = subs_list
    
    # Censor the time courses based on the t-masks
    if censor == True:
        print('Censoring time courses based on tmasks...')
        ROI_ts_df_censor = ROI_ts_df.copy() * tmasks
        
        # Get the group average time course if both censor & grp_avg == True
        if grp_avg == True:
            print('Calculating leave-one-out group average time courses...')
            rest_grp_avg_censor = pd.DataFrame()
            for i in ROI_ts_df_censor.columns.values:
                rest_ROI_ts_censor = ROI_ts_df_censor.copy()
                rest_ROI_ts_censor = rest_ROI_ts_censor.drop(i, axis = 1)
                rest_avg_ts_censor = rest_ROI_ts_censor.mean(axis = 1, skipna = True)
                rest_grp_avg_censor[i] = rest_avg_ts_censor
                
            print('Finished at ' + datetime.now().strftime('%H:%M:%S'))
            return ROI_ts_df_censor, rest_grp_avg_censor
        
        else:
            print('Finished at ' + datetime.now().strftime('%H:%M:%S'))
            return  ROI_ts_df_censor
    
    # Get the average time course across the group
    elif censor == False and grp_avg == True:
        print('Calculating leave-one-out group average time courses...')
        rest_grp_avg = pd.DataFrame()
        for i in ROI_ts_df.columns.values:
            rest_ROI_ts = ROI_ts_df.copy()
            rest_ROI_ts = rest_ROI_ts.drop(i, axis = 1)
            rest_avg_ts = rest_ROI_ts.mean(axis = 1, skipna = True)
            rest_grp_avg[i] = rest_avg_ts
    
        print('Finished at ' + datetime.now().strftime('%H:%M:%S'))
        return ROI_ts_df, rest_grp_avg
    
    else:
        print('Finished at ' + datetime.now().strftime('%H:%M:%S'))
        return ROI_ts_df


###############################################################################


def reg_ts(indiv_ROI_ts, grp_avg_ROI_ts, motion_dir, motion_ext, leaveout = False):
    
    """
    Parameters
    ----------
    indiv_ROI_ts : Pandas DataFrame
        A DataFrame (time x subjects) containing the ROI time courses for each
        individual in the study.
    
    grp_avg_ROI_ts : Pandas DataFrame
        A DataFrame (time x subjects) containing the leave-one-out average
        ROI time course corresponding to the left-out participant (column name)
        
    motion_dir : str
        String of the directory path where the temporal masks are stored.
        
    motion_ext : str
        String of the extension common to all files of the temporal masks.
    
    leaveout : boolean
        If leaveout = False, uses a Pandas Series of the group average time course
        (no left out individual) as the regressor; if leaveout = True, uses
        the leave-one-out group average time course corresponding to the left
        out individual from a Pandas DataFrame as the regressor.
    
    
    Returns
    -------
    all_betas : list
        A list of all the beta parameters of the group-average response for
        each individual
        
    all_coefs : list
        A list of all the intercepts of the regression for each individual.
        
    all_resid : list
        A list where each cell contains the residuals of the regression for each
        individual.
        
    """
    
    all_betas = []
    all_coefs = []
    all_resid = []
    
    for i in indiv_ROI_ts.columns.values:
        sub_ts = indiv_ROI_ts[i]
        
        if leaveout == True:
            grp_avg = grp_avg_ROI_ts[i]
            grp_avg = add_constant(grp_avg)
            
        else:
            grp_avg = grp_avg_ROI_ts
            grp_avg = add_constant(grp_avg)
            grp_avg = grp_avg.rename(columns = {0:i})
            
        
        motion_filename = motion_dir + i + motion_ext
        motion_file = open(motion_filename, 'r')
        motion_file = motion_file.read()
        
        if str.isspace(motion_file) == True:
            reg = OLS(sub_ts, grp_avg)
            reg = reg.fit()
        
        else:
            motion = pd.read_csv(motion_filename, sep = ' ', header = None)
            sub_all_var = pd.concat([grp_avg, motion], axis = 1)
            
            reg = OLS(sub_ts, sub_all_var)
            reg = reg.fit()

        all_betas.append(reg.params[i])
        all_coefs.append(reg.params['const'])
        all_resid.append(reg.resid.values)
        
    return all_betas, all_coefs, all_resid



###############################################################################


def pcorr_perm(data, x, y, covar, method = 'pearson', n_perms = 1000, tail = 'two-sided'):
    """
    pcorr_perm - a function that performs a permutation test for a partial
                    correlation.
    
    pcorr_perm  regresses the covariates out of both x and y and obtains the
        residuals for each variable, and then correlates them. It then 
        shuffles the y variable residuals and calculates the correlation 
        between the x residuals and the shuffled y residuals. It repeats 
        this procedure the number of times specified by n_perms to calculate a
        null distribution for the correlation statistic.
        
    pcorr_perm has the functionality to implement a one-tailed or two-tailed 
        test. The procedure is based off of that outlined in Gruskin et al. 
        (2020): "Relationships between depressive symptoms and brain responses 
        during emotional movie viewing emerge in adolescence". 
    
    Parameters
    ----------
        
    data : Pandas DataFrame
        DataFrame containing the columns that will be x, y, and the covariates.
    
    x : str
        Column name of one variable of interest.
                
    y : str
        Column name of the other variable of interest.
        
    covar : list of str
        List of the column names that contain the covariates.
    
    method : str    
        Possible values are 'pearson', 'spearman'
        
    n_perms : float
        Number of iterations/permutations to perform.

                    
    tail : str
        Possible values are 'less', 'greater', or 'two-sided'
    
    Returns
    -------
    true_r : float
        the partial correlation between x and y.
    
    p : float
        the p-value
    
    null : list
        the null distribution that the p-value was calculated against.
    
    """
    # Set needed parameters
    null = []
    true_r = partial_corr(data = data, x = x, y = y, covar = covar, 
                          method = method)['r'].to_numpy()[0]
    denom = n_perms + 1
    
    # Regress the covariates out of the variables of interest
    cov = data[covar]
    cov = add_constant(cov)
    
    x_reg = OLS(data[x], cov)
    x_reg = x_reg.fit()
    x_resid = x_reg.resid.values
    
    y_reg = OLS(data[y], cov)
    y_reg = y_reg.fit()
    y_resid = y_reg.resid.values
    
    # Do the permutations to create the null distribution
    for i in range(n_perms):
        y_perm = np.random.permutation(y_resid)
        r_null = corr(x_resid, y_perm, method = method, 
                      alternative = tail)['r'].to_numpy()[0]
        null.append(r_null)

    # Calculate p-value from null distribution
    if tail == 'greater':
        numer = 1 + (sum(i >= true_r for i in null))
        p = numer / denom
    
    elif tail == 'less':
        numer = 1 + (sum(i <= true_r for i in null))
        p = numer / denom
        
    elif tail == 'two-sided':
        numer = 1 + (sum(i >= true_r for i in null)) + (sum(i <= -true_r for i in null))
        p = numer / denom
    
    else:
        raise ValueError('Wrong tail kind specified. Options are greater, less, or two')
        
    return true_r, p, null


###############################################################################


def percent_sig_voxels(img, mask, threshold):
    
    """
    Parameters
    ----------
    img : str
        String of the location of the 3D fMRI NIFTI.
    
    mask : str
        String of the location of the mask NIFTI.
        
    threshold : float
        Threshold above which to count a voxel.
    
    
    Returns
    -------
    percent_sig : float
        The percentage of voxels above the threshold within the mask.

    """
    
    masked_img = apply_mask(img, mask)
    mask_vox = len(masked_img)
    vox_thres = sum(masked_img >= threshold)
    percent_sig = vox_thres / mask_vox
    
    return percent_sig


###############################################################################


def pairwise_dice(img_list, mask, thres = 1.6449):
    
    """
    Parameters
    ----------
    
    img_list : list
        List of all the .nii images that you want to compute DSC for - will do
        all pairs.
        
    mask : str
        String of the location of the mask NIFTI.
        
    thres : float
        Threshold above which to count a voxel as "active" (will binarize and 
        calculate the DSC from these binarized images).
    
    """

    dsc_list = []
    print('Started at: ' + datetime.now().strftime('%H:%M:%S'))

    for i in list(range(len(img_list))):
        for j in list(range(len(img_list))):
        
            if j <= i:
                pass
        
            else:
                x_img = apply_mask(img_list[i], mask)
                y_img = apply_mask(img_list[j], mask)
                x_img_bool = x_img > thres
                y_img_bool = y_img > thres
                denom = sum(x_img_bool) + sum(y_img_bool)
                numer = 2 * (sum(x_img_bool * y_img_bool))
                dsc = numer / denom
                dsc_list.append(dsc)
                
    print('Finished at: ' + datetime.now().strftime('%H:%M:%S'))    
             
    return dsc_list



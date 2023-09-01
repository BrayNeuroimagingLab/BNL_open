#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 18:25:12 2022


This program visualizes the outputs of source localization 5

@author: Kirk
"""



import os.path as op
import subprocess
import os



subjects_dir = '/Users/ivy/Desktop/Test_EEG/Test_MRI_ARCfiles/'


subjecthere = '03C'



#get a list of everything in the starting directory
folders = os.listdir(subjects_dir)


folders2 = []
for folder in folders:
    if folder.startswith('sub') and not folder.endswith('fif'):
        if subjecthere in folder:
            folders2.append(folder)
folders = folders2


if len(folders) != 1:
    print("You've specified multiple files")

else:
    
    subject = folders[0]

    subject_dir = op.join(subjects_dir, subject)
    ants_dir = op.join(subject_dir, 'ANTS_fun')
    bem_dir = op.join(subject_dir, 'bem')


    if 'C' in folder:
        output_file1 = ants_dir + '/nihpd_asym_07.0-11.0_mask_warp_orig.nii.gz'
        output_file2 = ants_dir + '/nihpd_asym_07.0-11.0_mask_warp.nii.gz'  
    elif 'P' in folder:
            output_file1 = ants_dir + '/nihpd_asym_07.0-11.0_mask_warp_adultspace_orig.nii.gz'
            output_file2 = ants_dir + '/nihpd_asym_07.0-11.0_mask_warp_adultspace.nii.gz'   
    else:
        print("Not specified age properly")
        gogo = False


    
    #structural preprocessing outputs. These must exist in the ANTs dir
    refimage = ants_dir + '/transformT1wFltmeantoMNIinverse.nii.gz'
    segwarpmatrix = ants_dir + '/transformT1wFltmeantoMNIinverse.h5'
    
    #bem outputs
    #inner_skull_bem = op.join(bem_dir, 'inner_skull.surf')
    #outer_skull_bem = op.join(bem_dir, 'outer_skull.surf')
    #brain_bem = op.join(bem_dir, 'brain.surf')
    #outer_skin_bem = op.join(bem_dir, 'outer_skin.surf')
    
    
    
    #brain estimate, for viewing purposes
    brainmask_file = subject_dir + '/mri/brainmask.mgz'
    t1_file = subject_dir + '/mri/T1.mgz'
    
    
    #various outputs
    #output_file1 = ants_dir + '/nihpd_asym_07.0-11.0_mask_warp_orig.nii.gz'
    #output_file2 = ants_dir + '/nihpd_asym_07.0-11.0_mask_warp.nii.gz'
    refmasked2 = ants_dir + '/transformT1wFltmeantoMNIinverse_masked.nii.gz'
    refmaskedconvert2 = ants_dir + '/transformT1wFltmeantoMNIinverse_masked.mgz'
    
    altsubdir_parent = subject_dir + '_alt/'
    altsubdir = altsubdir_parent + 'mri/'
    
    segheadfile = altsubdir[:-4] + '/surf/lh.seghead'
    segheadcopy2 = ants_dir + '/lh.seghead_brain_mni'
    
    smoothname2 = 'transformT1wFltmeantoMNIinverse_smooth.mgz'
    refmaskedsmooth2 = ants_dir + '/' + smoothname2
    refmaskedsmooth_copy2 = altsubdir + smoothname2
    
    brain_mni_surface = op.join(ants_dir, 'brain_mni.surf')
    brain_combined_surface = op.join(ants_dir, 'brain_combined.surf')
    inner_skull_new_estimate = op.join(ants_dir, 'inner_skull_new.surf')
    outer_skull_close = op.join(ants_dir, 'outer_skull_close.surf')
    inner_skull_final = op.join(ants_dir, 'inner_skull_final.surf')
    outer_skull_stretch = op.join(ants_dir, 'outer_skull_expanded.surf')
    
    
    #copy some original files for convenience, make new dir
    innerskull_copy = op.join(ants_dir, 'inner_skull_orig.surf')
    outerskull_copy = op.join(ants_dir, 'outer_skull_orig.surf')
    brain_copy = op.join(ants_dir, 'brain_orig.surf')
    outer_skin_copy = op.join(ants_dir, 'outer_skin_orig.surf')
    
    
    
    
    #colors: yellow, green, red, blue, cyan, magenta, orange, white
    
    c10 = 'freeview -v ' 
    c10 = c10 + brainmask_file + ' '
    c10 = c10 + t1_file + ' '
    #c10 + refmaskedsmooth2 + ' '
    
    c10 = c10 + '-f '
    c10 = c10 + brain_copy + ':edgecolor=white '
    c10 = c10 + brain_mni_surface + ':edgecolor=orange '
    c10 = c10 + brain_combined_surface + ':edgecolor=red '

    #c10 = c10 + innerskull_copy + ':edgecolor=yellow '
    #c10 = c10 + outerskull_copy + ':edgecolor=blue '
    c10 = c10 + outer_skin_copy + ':edgecolor=green '
    c10 = c10 + inner_skull_final + ':edgecolor=yellow '
    c10 = c10 + outer_skull_stretch + ':edgecolor=blue '
    
    
    c10 = c10 + '--viewport 3d'
    
    c10 = c10.split(' ')
    
    subprocess.run(c10)
    
    






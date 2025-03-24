#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 11:59:12 2022

This makes surface files

@author: Kirk
"""



import mne
import os
import subprocess


subjects_dir = '/Users/ivy/Desktop/Test_EEG/Test_MRI_ARCfiles/'


subjecthere = 'all'
#subjecthere = '04P'

replacer = False


#get a list of everything in the starting directory
folders = os.listdir(subjects_dir)
folders.sort()


subjlist = []

if subjecthere != 'all':
    folders2 = []
    for folder in folders:
        if folder.startswith('sub') and not folder.endswith('fif'):
            if subjecthere in folder:
                folders2.append(folder)
    folders = folders2

for folder in folders:
    if folder.startswith('sub') and not folder.endswith('fif'):
        subject = folder
        print("Making BEM files and scalp surface for " + subject)
        subjlist.append(subject)
        
        outputfile = subjects_dir + '/' + subject + '/bem/' + subject + '-head-dense.fif'
        
        #this code makes the scalp surfaces
        
        if not (replacer == False and os.path.isfile(outputfile)):
            
            t1 = subjects_dir + '/' + subject + '/mri/T1.mgz'
            t1smooth = subjects_dir + '/' + subject + '/mri/T1_smoothed_3.mgz'

            c9 = 'mri_convert --fwhm 3 ' + t1 + ' ' + t1smooth
            c9 = c9.split(' ')
         
            print("Making smoothed MRI")
            subprocess.run(c9)

            print("Making smoothed surface")
            mne.bem.make_scalp_surfaces(subject=subject,subjects_dir=subjects_dir,no_decimate=True,mri='T1_smoothed_3.mgz',overwrite=True)

        
        if replacer:
            mne.bem.make_watershed_bem(subject=subject, subjects_dir=subjects_dir,overwrite=True)

        #make bem surfaces
        try:
            mne.bem.make_watershed_bem(subject=subject, subjects_dir=subjects_dir)
            
        except:
            print('BEM did not run')
        











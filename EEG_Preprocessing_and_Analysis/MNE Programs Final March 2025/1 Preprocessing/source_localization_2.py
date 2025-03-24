#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This lets you set the fiducial points

Created on Fri Nov 18 16:51:14 2022

@author: Kirk
"""


import mne
import os


subjects_dir = '/Users/ivy/Desktop/Test_EEG/Test_MRI_ARCfiles/'

subjecthere = '3C'

replacer = True



#get a list of everything in the starting directory
folders = os.listdir(subjects_dir)
folders.sort()


subjlist = []
diditworklist = []
didbemrunlist = []


folders2 = []
for folder in folders:
    if folder.startswith('sub') and not folder.endswith('fif'):
        if subjecthere in folder:
            folders2.append(folder)
folders = folders2


for folder in folders:
    if folder.startswith('sub') and not folder.endswith('fif'):
        subject = folder
        print("Making fiducials if they don't exist for " + subject)
        subjlist.append(subject)
        
        outputfile = subjects_dir + '/' + subject + '/bem/' + subject + '-fiducials.fif'
        
        #this code makes the scalp surfaces
        if not (replacer == False and os.path.isfile(outputfile)):    
            mne.gui.coregistration(subject=subject,subjects_dir=subjects_dir,width=2100,height=1050)
        else:
            print("Fiducials already exist")
        

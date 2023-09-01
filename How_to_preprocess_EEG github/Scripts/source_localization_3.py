#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This aligns MRI and EEG

It saves the transformation file, and it save the stretch factor to apply to the EEG data

@author: Kirk
"""



import numpy as np

import mne
from mne.coreg import Coregistration

import pandas as pd

import os


#where is structural data saved
subjects_dir = '/Users/ivy/Desktop/Test_EEG/Test_MRI_ARCfiles/'
electrodefile = '/Users/ivy/Desktop/Test_EEG/AdultAverageNet64_v1.sfp'


subjecthere = 'all'
#subjecthere = '01P'

replacer = True




#get a list of everything in the starting directory
folders = os.listdir(subjects_dir)
folders.sort()


subjlist = []
diditworklist = []
didbemrunlist = []

if subjecthere != 'all':
    folders2 = []
    for folder in folders:
        if folder.startswith('sub') and not folder.endswith('fif'):
            if subjecthere in folder:
                folders2.append(folder)
    folders = folders2


#EEG data locations
locdf = pd.read_csv(electrodefile,sep='\t',header=None,index_col=0)
locdf = locdf*10/1000

nasion=np.array([locdf.loc['FidNz'][1],locdf.loc['FidNz'][2],locdf.loc['FidNz'][3]])
lpa=np.array([locdf.loc['FidT9'][1],locdf.loc['FidT9'][2],locdf.loc['FidT9'][3]])
rpa=np.array([locdf.loc['FidT10'][1],locdf.loc['FidT10'][2],locdf.loc['FidT10'][3]])

locdict = locdf.T.to_dict('list')
del locdict['FidNz']
del locdict['FidT9']
del locdict['FidT10']

#montage of the electrode locations
custmontage = mne.channels.make_dig_montage(nasion=nasion,lpa=lpa,rpa=rpa,ch_pos=locdict)

#fake data but fit to the GSN-HydroCel
ch_names = ['E1', 'E2','E3','E4', 'E5', 'E6', 'E7','E8', 'E9','E10','E11', 'E12','E13','E14','E15','E16','E17','E18','E19','E20','E21',
 'E22', 'E23','E24','E25','E26','E27','E28', 'E29','E30','E31','E32','E33','E34','E35','E36','E37','E38','E39','E40','E41','E42','E43',
 'E44','E45','E46','E47','E48','E49','E50','E51','E52','E53','E54','E55','E56','E57','E58','E59','E60','E61','E62','E63','E64','Cz']
data = np.random.RandomState(0).randn(len(ch_names), 1000)
info = mne.create_info(ch_names, 1000., 'eeg')
raw2 = mne.io.RawArray(data, info)
raw2 = raw2.set_montage(custmontage)

raw2.set_eeg_reference(projection=True)
info_orig = raw2.info



for folder in folders:
    if folder.startswith('sub') and not folder.endswith('fif'):
        subject = folder
        
        transformsave = subjects_dir + '/' + subject + '/bem/transform-trans.fif'
        eegscale = subjects_dir + '/' + subject + '/eegscale'
        
        if (replacer == False and os.path.isfile(eegscale)): 
            print("Output files already exist for " + subject)
        else:
            
            fiducials = mne.coreg.get_mni_fiducials(subject, subjects_dir=subjects_dir)
            
            coreg = Coregistration(info_orig, subject, subjects_dir, fiducials=fiducials)
            coreg.set_scale_mode('3-axis')
            coreg.fit_fiducials(verbose=True,lpa_weight=1.0,nasion_weight=1.0,rpa_weight=1.0)
            coreg.fit_icp(n_iterations=30,verbose=True,lpa_weight=1.0,nasion_weight=1.0,rpa_weight=1.0)
            
            
    
            dists = coreg.compute_dig_mri_distances() * 1e3  # in mm
            print(
                f"Distance between HSP and MRI (mean/min/max):\n{np.mean(dists):.2f} mm "
                f"/ {np.min(dists):.2f} mm / {np.max(dists):.2f} mm"
            )
            
                
            print(coreg.scale)
            
            scale1 = coreg.scale[0]
            scale2 = coreg.scale[1]
            scale3 = coreg.scale[2]    
                
            locdfsubj = locdf.copy()
            locdfsubj[1] = locdfsubj[1]/scale1
            locdfsubj[2] = locdfsubj[2]/scale2
            locdfsubj[3] = locdfsubj[3]/scale3
            
            nasionsubj=np.array([locdfsubj.loc['FidNz'][1],locdfsubj.loc['FidNz'][2],locdfsubj.loc['FidNz'][3]])
            lpasubj=np.array([locdfsubj.loc['FidT9'][1],locdfsubj.loc['FidT9'][2],locdfsubj.loc['FidT9'][3]])
            rpasubj=np.array([locdfsubj.loc['FidT10'][1],locdfsubj.loc['FidT10'][2],locdfsubj.loc['FidT10'][3]])
            
            
            locdictsubj = locdfsubj.T.to_dict('list')
            del locdictsubj['FidNz']
            del locdictsubj['FidT9']
            del locdictsubj['FidT10']
            
            custmontage = mne.channels.make_dig_montage(nasion=nasionsubj,lpa=lpasubj,rpa=rpasubj,ch_pos=locdictsubj)
            
            raw3 = raw2.copy().set_montage(custmontage)
            raw3.set_eeg_reference(projection=True)
            info = raw3.info
            
                    
            coreg = Coregistration(info, subject, subjects_dir, fiducials=fiducials)
            coreg.fit_fiducials(verbose=True,lpa_weight=1.0,nasion_weight=1.0,rpa_weight=1.0)
            coreg.fit_icp(n_iterations=20,verbose=True,lpa_weight=1.0,nasion_weight=1.0,rpa_weight=1.0)
            
            
            dists = coreg.compute_dig_mri_distances() * 1e3  # in mm
            print(
                f"Distance between HSP and MRI (mean/min/max):\n{np.mean(dists):.2f} mm "
                f"/ {np.min(dists):.2f} mm / {np.max(dists):.2f} mm"
            )
            
            print(coreg.scale)
      
            
            mne.write_trans(transformsave, coreg.trans, overwrite = True)
            
            log = []
            log.append(scale1)
            log.append(scale2)
            log.append(scale3)
            print("")
            with open(eegscale, 'w') as f:
                for item in log:
                    f.write("%s\n" % item)
                    print(item)
            f.close()             
            
            
    















































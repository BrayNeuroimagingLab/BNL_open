#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This program averages the connectomes across all participants, for a given frequency band and FC measure

You can run it in absmode or not. In abs mode, it takes the absolute value of all FC measures for each connectome

"""



import numpy as np
import mne
import pandas as pd
import os

import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
import statsmodels.api as sm






#folder with all the participant folders and EEG outputs
dir_start = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/prepro1/'

subjects_dir = '/Users/ivy/Desktop/Graff_EEG_stuff/ZPrecise2_MRI_fixed_rename_FS'

savedir = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/yavg/'


networklabels = '/Users/ivy/Desktop/Graff_EEG_stuff/Desikankilliany/dklabels.csv'



#abs value the connectome
absmode = True





#aparc doesn't work right now
parc = 'aparc.a2009s'
parc = 'aparc'

#this calculates connectivity in 0.5 Hz bands then averages them. 2-3.5 means 2-2.5,2.5-3,3-3.5,3.5-4
fbands = [[4.0,7.5],[8.0,12.5],[13.0,29.5],[2.5,44.5],[30.0,44.5]]
conmethods = ['pli','imcoh','wpli','coh']






fbands = [[8.0,13.0]]
fbands = [[2.5,45.0]]
#fbands = [[4.0,7.5]]
#fbands = [[13.0,30.0]]
#conmethods = ['imcoh']
#conmethods = ['coh']
#conmethods = ['wpli']
#conmethods = ['wpli']




#which file(s) do you want to look at?
families = list(range(2,27))
participant_ages = ['C','P']
sessions = [1,2,3,4,'4x']
tasks = ['DORA','YT','RX']

#families = [2,3,4,5,6,7,23,24,25,26]



#get a list of everything in the starting directory
folders = os.listdir(subjects_dir)
subjectlist = []
for folder in folders:
    if folder.startswith('sub') and not folder.endswith('fif'):
        if '001' not in folder: 
            subject = folder
            subjectlist.append(subject)

mastersubj = subjectlist[0]
labels_parc = mne.read_labels_from_annot(mastersubj, parc=parc,subjects_dir=subjects_dir)                          
label_names = [label.name for label in labels_parc]   


"""
ypos_lists = []
xpos_lists = []
zpos_lists = []

for subject in subjectlist:
    labels_parc = mne.read_labels_from_annot(subject, parc=parc,subjects_dir=subjects_dir)                          

    label_ypos = list()
    label_xpos = list()
    label_zpos = list()
    for name in label_names:
        idx = label_names.index(name)
        xpos = np.mean(labels_parc[idx].pos[:, 0])
        ypos = np.mean(labels_parc[idx].pos[:, 1])
        zpos = np.mean(labels_parc[idx].pos[:, 2])
        label_ypos.append(ypos)
        label_xpos.append(xpos)
        label_zpos.append(zpos)
    
    ypos_lists.append(label_ypos)
    xpos_lists.append(label_xpos)    
    zpos_lists.append(label_zpos)
    
yposarrays = [np.array(x) for x in ypos_lists]
xposarrays = [np.array(x) for x in xpos_lists]
zposarrays = [np.array(x) for x in zpos_lists]

y_pos_avg = [np.mean(k) for k in zip(*yposarrays)]
x_pos_avg = [np.mean(k) for k in zip(*xposarrays)]
z_pos_avg = [np.mean(k) for k in zip(*zposarrays)]




netdf = pd.read_csv(networklabels,index_col=0)
ogid = list(netdf['id_num'])


labnames = netdf['label']
#testdf = pd.DataFrame({'label':labnames,'network':labz,'ypos':label_ypos,'idnum':ogid})
testdf = pd.DataFrame({'label':labnames,'ypos':y_pos_avg,'xpos':x_pos_avg,'zpos':z_pos_avg,'idnum':ogid})
testdf['hemi'] = testdf['label'].str[-2:]

testdf = testdf.sort_values(by=['hemi','ypos'])

subtestdf = testdf[testdf['hemi'] == 'lh']
neutlabel = subtestdf['label'].str[:-3]
lhlabel = neutlabel + '-lh'
lhlabel = list(lhlabel)
rhlabel = neutlabel + '-rh'
rhlabel = list(rhlabel)
neutlabel = list(neutlabel)

newlabel = lhlabel + rhlabel


testdf.label = testdf.label.astype("category")
testdf.label = testdf.label.cat.set_categories(newlabel)
testdf = testdf.sort_values(by=['label'])


#testdf = testdf.sort_values(by=['hemi','ypos'])
labelz = testdf['label']
"""



zero_data = np.zeros(shape=(len(labels_parc),len(labels_parc)))
zerodf = pd.DataFrame(data=zero_data)
zerodf.columns=label_names
zerodf.index=label_names





for fband in fbands:
    fbandstr = str(fband[0]) + '-' + str(fband[1])
    fmin = fband[0]
    fmax = fband[1]
        
    dataname = str(fmin)+'-'+str(fmax)
    
    for cn in range(len(conmethods)):  
        
        conmethod = conmethods[cn]
        
        if absmode:
            avgname = savedir + 'avg_' + fbandstr + '_' + conmethod + '_abs.csv'
        else:
            avgname = savedir + 'avg_' + fbandstr + '_' + conmethod + '_nonabs.csv'

        
        alldf = []

        #loop through all connectomes
        for family in families:
            strnum = str(family)
            if len(strnum) == 1:
                strnum = '0' + strnum
            strfam = 'sub-19730' + strnum
        
            for page in participant_ages:
                strper = strfam + str(page)
                personfolder = dir_start + strper + '/'
                
                for session in sessions:
                    input_data_folder = personfolder + 'ses-' + str(session) + '/eeg/'
                    connectome_folder = personfolder + 'ses-' + str(session) + '/connectomes/' + parc + '/'
                    
                    for task in tasks:
                        
                        raw_data_file_sub = strper + '_ses-' + str(session) + '_task-' + task
                        if os.path.exists(connectome_folder):
                            prefixed = [filename for filename in os.listdir(connectome_folder) if filename.startswith(raw_data_file_sub)]  
                            
                            if len(prefixed) == 0:
                                print("There are no files matching the name " + raw_data_file_sub)
                            else:
                            
                                filetosaveprefix = prefixed[0].split('_')
                                specifictask = filetosaveprefix[2].split('-')[1]
                                filetosaveprefix = strper + '_ses-' + str(session) + '_' + filetosaveprefix[2]
        
                                badparclog = connectome_folder + filetosaveprefix + '_' + parc + '_errorlog.txt'
                                
                                if os.path.isfile(badparclog):
                                    print("This file exists " + badparclog)
                                
        
                                saveconnectome = connectome_folder + filetosaveprefix + '_' + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz.csv'
                                                            
                                if os.path.isfile(saveconnectome):
                                    print("Loading " + saveconnectome) 
                                    
                                    parceldata1 = pd.read_csv(saveconnectome,index_col=0)
                                    parceldatax = parceldata1 + parceldata1.T
                                    
                                    parceldatax = np.arctanh(parceldatax)

                                    alldf.append(parceldatax)
       
                                
                                    



        
        print("")
        print("Making average dfs")
        print("")  
        
            
  
        county = 0
        avgdf = zerodf.copy()
        
        for i in range(len(alldf)):
            
            county = county + 1
            scanhere = alldf[i]
            if absmode:
                avgdf = avgdf + abs(scanhere)
            else:
                avgdf = avgdf + scanhere        
                
        avgdf = avgdf/county

        avgdf.to_csv(avgname)
        
















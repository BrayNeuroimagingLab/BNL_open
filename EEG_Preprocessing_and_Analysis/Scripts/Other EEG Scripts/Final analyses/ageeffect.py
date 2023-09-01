#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Looking at age effects...

For each different specific video (e.g., Dora3, Dora6, Dora9, RX2, etc) 
I ran a paired t-test for each edge, comparing child FC to their parent FC. 
I then averaged the absolute t-statistic across all edges. This gave me 11 different 
averages per frequency band per FC measure. (Why 11 and not 12? Participants only had 3 Dora videos in common). 
Results were similar across frequency bands. Here are the alpha band averages across tasks:
    
psi: 0.921
pli: 0.974
wpli: 0.978
imcoh: 1.15
coh: 1.76
plv: 1.69


This program specifically does the t-test for each edge for each task for each conmethod for each fband
For each conmethod for each fband for each task, it creates a df of all the edge t-values


"""



import numpy as np
import pandas as pd
import os
from scipy.stats.stats import pearsonr
from scipy.stats import ttest_rel



from scipy import stats


#folder with all the EEG connectomes
dir_start = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/prepro1/'

#folder where outputs are saved
savesumdir = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/xresults/parentvchild_ttest/'



#which parcellation to use
#parc = 'aparc.a2009s'
parc = 'aparc'


#which frequency bands and FC measures to use
fbands = [[8.0,13.0],[13.0,30.0],[2.5,45.0],[30.0,45.0],[4.0,8.0]]
fbands = [[8.0,13.0],[13.0,30.0],[2.5,45.0]]
conmethods = ['imcoh','wpli','coh','pli','plv','psi']
#fbands = [[8.0,13.0]]
#conmethods = ['wpli']


#which file(s) do you want to look at?
families = list(range(2,27))
participant_ages = ['C','P']
sessions = [1,2,3,4,'4x']
tasks = ['DORA','YT','RX']

#families = [7,8,9,10]





saveoutputs = True
replacer = False




#get list of all the tasks
specifictasklist = []

fband = fbands[0]
fbandstr = str(fband[0]) + '-' + str(fband[1])
fmin = fband[0]
fmax = fband[1]
conmethod = conmethods[0]

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
                    
                    if not len(prefixed) == 0:
                    
                        filetosaveprefix = prefixed[0].split('_')
                        specifictask = filetosaveprefix[2].split('-')[1]
                        filetosaveprefix = strper + '_ses-' + str(session) + '_' + filetosaveprefix[2]
                    
                        badparclog = connectome_folder + filetosaveprefix + '_' + parc + '_errorlog.txt'
                        
                        if os.path.isfile(badparclog):
                            print("This file exists " + badparclog)
                        
                        saveconnectome = connectome_folder + filetosaveprefix + '_' + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz.csv'
                                                    
                        if os.path.isfile(saveconnectome):                            
                            specifictasklist.append(specifictask)

allspecifictasks = list(set(specifictasklist))
allspecifictasks.sort()
    

#allspecifictasks = allspecifictasks[:3]

for fband in fbands:
    fbandstr = str(fband[0]) + '-' + str(fband[1])
    for conmethod in conmethods:    
        
        lenofcomparisons = []
        
        fmin = fband[0]
        fmax = fband[1]
        
        for specifictask in allspecifictasks:
        
            logname = savesumdir + 'aget_' + conmethod + '_' + fbandstr + '_' + specifictask + '.csv'
    
            if os.path.isfile(logname) == False or replacer == True:
                    
                FCallvec_child = []
                FCallvec_parent = []
                
                tvallist = []
                pvallist = []
                
                for family in families:
                    strnum = str(family)
                    if len(strnum) == 1:
                        strnum = '0' + strnum
                    strfam = 'sub-19730' + strnum

                    parentexist = False
                    childexist = False
                
                    #check if parent has this specific task
                    strper = strfam + 'P'
                    personfolder = dir_start + strper + '/'
                    
                    for session in sessions:
                        input_data_folder = personfolder + 'ses-' + str(session) + '/eeg/'
                        connectome_folder = personfolder + 'ses-' + str(session) + '/connectomes/' + parc + '/'
                        
                        for task in tasks:
                            
                            raw_data_file_sub = strper + '_ses-' + str(session) + '_task-' + task
                            if os.path.exists(connectome_folder):
                                prefixed = [filename for filename in os.listdir(connectome_folder) if filename.startswith(raw_data_file_sub)]  
                                
                                if not len(prefixed) == 0:
                                
                                    filetosaveprefix = prefixed[0].split('_')
                                    specifictaskhere = filetosaveprefix[2].split('-')[1]
                                    filetosaveprefix = strper + '_ses-' + str(session) + '_' + filetosaveprefix[2]
                                    
                                    if specifictaskhere == specifictask:
              
                                        badparclog = connectome_folder + filetosaveprefix + '_' + parc + '_errorlog.txt'
                                        
                                        if os.path.isfile(badparclog):
                                            print("This file exists " + badparclog)
                                        
                                        saveconnectome_parent = connectome_folder + filetosaveprefix + '_' + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz.csv'
                                        if os.path.isfile(saveconnectome_parent):
                                            parentexist = True                                                                                                         
                
                
                    #check if child has this specific task
                    strper = strfam + 'C'
                    personfolder = dir_start + strper + '/'
                    
                    for session in sessions:
                        input_data_folder = personfolder + 'ses-' + str(session) + '/eeg/'
                        connectome_folder = personfolder + 'ses-' + str(session) + '/connectomes/' + parc + '/'
                        
                        for task in tasks:
                            
                            raw_data_file_sub = strper + '_ses-' + str(session) + '_task-' + task
                            if os.path.exists(connectome_folder):
                                prefixed = [filename for filename in os.listdir(connectome_folder) if filename.startswith(raw_data_file_sub)]  
                                
                                if not len(prefixed) == 0:
                                
                                    filetosaveprefix = prefixed[0].split('_')
                                    specifictaskhere = filetosaveprefix[2].split('-')[1]
                                    filetosaveprefix = strper + '_ses-' + str(session) + '_' + filetosaveprefix[2]
                                    
                                    if specifictaskhere == specifictask:
              
                                        badparclog = connectome_folder + filetosaveprefix + '_' + parc + '_errorlog.txt'
                                        
                                        if os.path.isfile(badparclog):
                                            print("This file exists " + badparclog)
                                        
                                        saveconnectome_child = connectome_folder + filetosaveprefix + '_' + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz.csv'
                                        if os.path.isfile(saveconnectome_child):
                                            childexist = True        
                    
                    
                    if parentexist and childexist:
                        print("Loading " + saveconnectome_child)
                        print("Loading " + saveconnectome_parent)
                        
                        parceldata1 = pd.read_csv(saveconnectome_child,index_col=0)
                        
                        FCm = np.squeeze(np.asarray(parceldata1))
                        FCm = np.arctanh(FCm)
                    
                        vec = []
                        for ii in range(1, FCm.shape[0]):
                            for jj in range(ii):
                                vec.append(FCm[ii, jj])
                        
                        FCallvec_child.append(np.asarray(vec))  
                        
                        
                        parceldata1 = pd.read_csv(saveconnectome_parent,index_col=0)
                        
                        FCm = np.squeeze(np.asarray(parceldata1))
                        FCm = np.arctanh(FCm)
                    
                        vec = []
                        for ii in range(1, FCm.shape[0]):
                            for jj in range(ii):
                                vec.append(FCm[ii, jj])
                        
                        FCallvec_parent.append(np.asarray(vec))                          
                        
                  
                    elif parentexist:
                        print("Parent exists but not child for " + strfam)
                    elif childexist:
                        print("Child exists but not parent for " + strfam)
                    else:
                        print("Neither parent nor child exists for " + strfam)
                    
                    
                lenofcomparisons.append(len(FCallvec_parent))
                if len(FCallvec_parent) > 1:
                    print("Running t-tests")
                    veclen = len(FCallvec_parent[0])
                                        
                    for edge in range(veclen):
                        parentedgevec = []
                        childedgevec = []
    
                        for vec in FCallvec_parent:
                            edgeval = vec[edge]
                            parentedgevec.append(edgeval)
    
                        for vec in FCallvec_child:
                            edgeval = vec[edge]
                            childedgevec.append(edgeval)                    
                
                        tres = ttest_rel(parentedgevec,childedgevec)
                        tvallist.append(tres[0])
                        pvallist.append(tres[1])
                        
                    testdf = pd.DataFrame({'tval':tvallist,'pval':pvallist})
                    
                    if saveoutputs:
                        testdf.to_csv(logname)
 
                    
            else:
                lenofcomparisons.append(np.nan)
                    
        taskdfcomps = pd.DataFrame({'task':allspecifictasks,'numcomparisons':lenofcomparisons})
        print(taskdfcomps)

















    
    
    
    
    
    
    
    
    
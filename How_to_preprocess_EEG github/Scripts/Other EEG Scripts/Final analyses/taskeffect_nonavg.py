#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Looking at task effects...
I wasn't exactly sure the best way to do this, so I tried 2 approaches:
    
2) Using data from all the participants that had all 11 common recordings 
(i.e., not including the Dora that didn't overlap), I ran a repeated-measures 
 ANOVA for each edge, comparing the 11 different FC values each participant had 
 (from the 11 different recordings). I then averaged the F-statistic across all 
 edges. Here are the alpha band averages:
psi: 1.23
pli: 1.10
wpli: 1.10
imcoh: 1.17
coh: 1.26
plv: 1.34


This program specifically does the ANOVA for each edge for each conmethod for each fband
For each conmethod for each fband, it creates a df of all the edge F-values    

(note to Kirk: I slightly changed this program, so these numbers are correct, but different from what I emailed Signe)
    
"""



import numpy as np
import pandas as pd
import os
from scipy.stats.stats import pearsonr
from statsmodels.stats.anova import AnovaRM



from scipy import stats


#folder with all the EEG connectomes
dir_start = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/prepro1/'

#folder where outputs are saved
savesumdir = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/xresults/task_anova/'



#which parcellation to use
#parc = 'aparc.a2009s'
parc = 'aparc'


#which frequency bands and FC measures to use
fbands = [[8.0,13.0],[13.0,30.0],[2.5,45.0],[30.0,45.0],[4.0,8.0]]
fbands = [[8.0,13.0],[13.0,30.0],[2.5,45.0]]
conmethods = ['imcoh','wpli','coh','pli','plv','psi']
#fbands = [[8.0,13.0]]
#conmethods = ['plv']


#which file(s) do you want to look at?
families = list(range(2,27))
participant_ages = ['C','P']
sessions = [1,2,3,4,'4x']
tasks = ['DORA','YT','RX']


saveoutputs = True
replacer = True




for fband in fbands:
    fbandstr = str(fband[0]) + '-' + str(fband[1])
    for conmethod in conmethods:    
        
        fmin = fband[0]
        fmax = fband[1]

        logname = savesumdir + 'taskanova_' + conmethod + '_' + fbandstr + '.csv'
        
        FCallvec_all = []

        if os.path.isfile(logname) == False or replacer == True:
    
            for family in families:
                strnum = str(family)
                if len(strnum) == 1:
                    strnum = '0' + strnum
                strfam = 'sub-19730' + strnum
            
                for page in participant_ages:
                    strper = strfam + str(page)
                    personfolder = dir_start + strper + '/'
                    
                    
                    personFCallvec = []
                    personspecifictasks = []
                    
                    for session in sessions:
                        input_data_folder = personfolder + 'ses-' + str(session) + '/eeg/'
                        connectome_folder = personfolder + 'ses-' + str(session) + '/connectomes/' + parc + '/'
                        
                        task = 'DORA'
 
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
                                    
                                    FCm = np.squeeze(np.asarray(parceldata1))
                                    FCm = np.arctanh(FCm)
                                
                                    vec = []
                                    for ii in range(1, FCm.shape[0]):
                                        for jj in range(ii):
                                            vec.append(FCm[ii, jj])
                                    
                                    
                                    if specifictask == 'DORA3' or specifictask == 'DORA6' or specifictask == 'DORA9':
                                        personFCallvec.append(np.asarray(vec))
                                        personspecifictasks.append(specifictask)                                        
                                    
                                    
                        task = 'YT'

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
                                    
                                    FCm = np.squeeze(np.asarray(parceldata1))
                                    FCm = np.arctanh(FCm)
                                
                                    vec = []
                                    for ii in range(1, FCm.shape[0]):
                                        for jj in range(ii):
                                            vec.append(FCm[ii, jj])
                                     
                                    
                                    if specifictask == 'YT1' or specifictask == 'YT10' or specifictask == 'YT7' or specifictask == 'YT4':
                                        personFCallvec.append(np.asarray(vec))
                                        personspecifictasks.append(specifictask)    
                        
                        task = 'RX'

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
                                    
                                    FCm = np.squeeze(np.asarray(parceldata1))
                                    FCm = np.arctanh(FCm)
                                
                                    vec = []
                                    for ii in range(1, FCm.shape[0]):
                                        for jj in range(ii):
                                            vec.append(FCm[ii, jj])
                                    
                                    
                                    if specifictask == 'RX2' or specifictask == 'RX4' or specifictask == 'RX7' or specifictask == 'RX10':
                                        personFCallvec.append(np.asarray(vec))
                                        personspecifictasks.append(specifictask)   

                    
                    if len(personspecifictasks) == 11:                                                
                        personspecifictasks = np.array(personspecifictasks)
                        personFCallvec = np.array(personFCallvec)
                        inds = personspecifictasks.argsort()
                        sortedpersonFCallvec = personFCallvec[inds]
                        
                        FCallvec_all.append(sortedpersonFCallvec)
                        



            print("Running ANOVA")
            veclen = len(FCallvec_all[0][0])
            
            sortedtasks = personspecifictasks.copy()
            sortedtasks.sort()
            
            Fvallist = []
            pvallist = []
            
            #edge = 0
                                
            for edge in range(veclen):
                
                participantlist = []
                tasklist = []
                FClist = []
                    
                for participant in range(len(FCallvec_all)):
                    
                    for taskn in range(len(sortedtasks)):
                        
                        participantlist.append(participant)
                        tasklist.append(sortedtasks[taskn])
                        
                        edgeval = FCallvec_all[participant][taskn][edge]
                        FClist.append(edgeval)
                    
                    
                edgedf = pd.DataFrame({'participant':participantlist,'task':tasklist,'FC':FClist})
                    
                ano = AnovaRM(data=edgedf, depvar='FC',subject='participant', within=['task']).fit()  
                
                Fvallist.append(float(ano.anova_table['F Value']))
                pvallist.append(float(ano.anova_table['Pr > F']))
            

            testdf = pd.DataFrame({'Fval':Fvallist,'pval':pvallist})
            
            if saveoutputs:
                testdf.to_csv(logname)        

                
                
                    

























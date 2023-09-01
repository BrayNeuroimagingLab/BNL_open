#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Looking at task effects...
I wasn't exactly sure the best way to do this, so I tried 2 approaches:
1) For each participant, if they had all 12 recordings, I created an average connectome for Dora,
YT, RX (average of the 4 recordings). I then ran a repeated-measures ANOVA for each edge, 
comparing the 3 averaged connectomes. I then averaged the F-statistic across all edges. 
Here are the alpha band averages:
    
psi: 1.17
pli: 1.33
wpli: 1.26
imcoh: 1.57
coh: 2.25
plv: 2.83

This program specifically does the ANOVA for each edge for each conmethod for each fband
For each conmethod for each fband it creates a df of all the edge F-values
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
savesumdir = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/xresults/avgtask_anova/'



#which parcellation to use
#parc = 'aparc.a2009s'
parc = 'aparc'


#which frequency bands and FC measures to use
fbands = [[8.0,13.0],[13.0,30.0],[2.5,45.0],[30.0,45.0],[4.0,8.0]]
fbands = [[8.0,13.0],[13.0,30.0],[2.5,45.0]]
conmethods = ['imcoh','wpli','coh','pli','plv','psi']
fbands = [[8.0,13.0]]
conmethods = ['plv']


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

        logname = savesumdir + 'avgtaskanova_' + conmethod + '_' + fbandstr + '.csv'
        
        FCallvec_doras = []
        FCallvec_yts = []
        FCallvec_rxs = []

        if os.path.isfile(logname) == False or replacer == True:
    
            for family in families:
                strnum = str(family)
                if len(strnum) == 1:
                    strnum = '0' + strnum
                strfam = 'sub-19730' + strnum
            
                for page in participant_ages:
                    strper = strfam + str(page)
                    personfolder = dir_start + strper + '/'
                    
                    doraFCallvec = []
                    ytFCallvec = []
                    rxFCallvec = []
                    
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
                                    
                                    doraFCallvec.append(np.asarray(vec))
                                    
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
                                    
                                    ytFCallvec.append(np.asarray(vec))                        
                        
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
                                    
                                    rxFCallvec.append(np.asarray(vec))   



                    if len(rxFCallvec) == 4 and len(ytFCallvec) == 4 and len(doraFCallvec) == 4:
                        
                        arrays = [np.array(x) for x in doraFCallvec]
                        doraavg = [np.mean(k) for k in zip(*arrays)]
                        
                        arrays = [np.array(x) for x in rxFCallvec]
                        rxavg = [np.mean(k) for k in zip(*arrays)]
                        
                        arrays = [np.array(x) for x in ytFCallvec]
                        ytavg = [np.mean(k) for k in zip(*arrays)]


                        FCallvec_doras.append(doraavg)
                        FCallvec_yts.append(ytavg)
                        FCallvec_rxs.append(rxavg)




            print("Running ANOVA")
            veclen = len(FCallvec_doras[0])
            
            Fvallist = []
            pvallist = []
                                
            for edge in range(veclen):
                
                participantlist = []
                tasklist = []
                FClist = []
                    
                for participant in range(len(FCallvec_doras)):
                    participantlist.append(participant)
                    tasklist.append('DORA')
                    
                    edgeval = FCallvec_doras[participant][edge]
                    FClist.append(edgeval)
                    
                
                    participantlist.append(participant)
                    tasklist.append('RX')
                    
                    edgeval = FCallvec_rxs[participant][edge]
                    FClist.append(edgeval)            
                    
                    
                    participantlist.append(participant)
                    tasklist.append('YT')
        
                    edgeval = FCallvec_yts[participant][edge]
                    FClist.append(edgeval)    
                    
                edgedf = pd.DataFrame({'participant':participantlist,'task':tasklist,'FC':FClist})
                    
                ano = AnovaRM(data=edgedf, depvar='FC',subject='participant', within=['task']).fit()  
                
                Fvallist.append(float(ano.anova_table['F Value']))
                pvallist.append(float(ano.anova_table['Pr > F']))
                
            testdf = pd.DataFrame({'Fval':Fvallist,'pval':pvallist})
            
            if saveoutputs:
                testdf.to_csv(logname)        
                
                
                
                    

























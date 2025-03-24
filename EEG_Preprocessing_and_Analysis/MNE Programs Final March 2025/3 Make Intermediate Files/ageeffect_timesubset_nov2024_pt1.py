#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Looking at age effects...

For each frequency band and FC measure...
I created an average connectome for each child and each parent, by averaging all the tasks
Tasks were only included if both parent and child had them

I then ran a paired t-test for each edge, comparing child FC to their parent FC. 



This program specifically does the t-test for each edge for each conmethod for each fband
For each conmethod for each fband, it creates a df of all the edge t-values


"""



import numpy as np
import pandas as pd
import os
from scipy.stats import ttest_rel



#folder with all the EEG connectomes
dir_start = '/Volumes/Backup_Backup/Hooray_EEG/prepro1/'

#folder where outputs are saved
savesumdir = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/results_lol2025probably/parentvchild_ttest_timesubset/'




#which parcellation to use
parc = 'aparc'


#which frequency bands and FC measures to use
fbands = [[8.0,13.0],[13.0,30.0],[2.5,45.0]]
conmethods = ['coh','plv','imcoh','ciplv','pli','wpli','psi','ecpwo','ecso']


#which file(s) do you want to look at?
families = list(range(2,27))


#number of epochs to use
subsections = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,20,25,30,35,40,45,50,60,70,80,90,100,110,120,130,140,150]


saveoutputs = False
#replace files that already exist?
replacer = True



#this block of code does the analysis for the ses12 age effects
for timesubx in subsections:
    timesub = int(timesubx*5)
    
    for fband in fbands:
        fbandstr = str(fband[0]) + '-' + str(fband[1])
        for conmethod in conmethods:    
            
            fmin = fband[0]
            fmax = fband[1]
            logname = savesumdir + 'aget_' + conmethod + '_' + fbandstr + '_' + str(timesub) + 'e12.csv'
            
            if os.path.isfile(logname) == False or replacer == True:
                
                FCallvec_child = []
                FCallvec_parent = []            
                tvallist = []
                pvallist = []     
                lenofcomparisons = []   
                
                for family in families:
                    strnum = str(family)
                    if len(strnum) == 1:
                        strnum = '0' + strnum
                    strfam = 'sub-19730' + strnum
                
                    parentexist = False
                    childexist = False
                    saveconnectome_child = 'no'
                    saveconnectome_parent = 'no'
                    
                    page = 'C'
    
                    strper = strfam + str(page)
                    personfolder = dir_start + strper + '/'
                    connectome_folder = personfolder + 'connectomes_combined_1124/' + parc + '/'
                    
                    saveconnectomeprefix = strper + '_combined_' + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_'
    
                    
                    agefiles = [filename for filename in os.listdir(connectome_folder) if filename.startswith(saveconnectomeprefix)]
                    agefiles = [file for file in agefiles if file.endswith('_'+str(timesub)+'e_agematch12.csv')]
                    
                    if len(agefiles) == 1:
                        childexist = True
                        saveconnectome_child = connectome_folder + agefiles[0]
                        
                    page = 'P'
    
                    strper = strfam + str(page)
                    personfolder = dir_start + strper + '/'
                    connectome_folder = personfolder + 'connectomes_combined_1124/' + parc + '/'
                    
                    saveconnectomeprefix = strper + '_combined_' + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_'
    
                    
                    agefiles = [filename for filename in os.listdir(connectome_folder) if filename.startswith(saveconnectomeprefix)]
                    agefiles = [file for file in agefiles if file.endswith('_'+str(timesub)+'e_agematch12.csv')]
                    
                    if len(agefiles) == 1:
                        parentexist = True
                        saveconnectome_parent = connectome_folder + agefiles[0]                    
                        
                        
                    #if the data exists for both the parent and child, read it in
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
                        
                        
    
                print(len(FCallvec_child),len(FCallvec_parent))
                
                
                #for each edge, gather all the relevant edge values across participants and run a t-test for parent vs child
                if len(FCallvec_parent) > 1:
                    print("Running t-tests")
                    veclen = len(FCallvec_parent[0])
                
                    edgetestdf = []
                    for edge in range(veclen):
                        parentedgevec = []
                        childedgevec = []
    
                        for vec in FCallvec_parent:
                            edgeval = vec[edge]
                            parentedgevec.append(edgeval)
    
                        for vec in FCallvec_child:
                            edgeval = vec[edge]
                            childedgevec.append(edgeval)      
                        
                        edgetestdf.append(len(parentedgevec))
                        
                        parentedgevec = np.asarray(parentedgevec)
                        childedgevec = np.asarray(childedgevec)
                        
                        nas = np.logical_or(np.logical_or(np.isinf(parentedgevec),np.isinf(childedgevec)),np.logical_or(np.isnan(parentedgevec),np.isnan(childedgevec)))            
                        tres = ttest_rel(parentedgevec[~nas],childedgevec[~nas])     
                
                        #tres = ttest_rel(parentedgevec,childedgevec,nan_policy='omit')
                        tvallist.append(tres[0])
                        pvallist.append(tres[1])
                        
                    testdf = pd.DataFrame({'tval':tvallist,'pval':pvallist})
                    
                    if saveoutputs:
                        testdf.to_csv(logname)
     
 
    

#this does the ses34 age effects
#yes, obviously, this is very bad code. Why would you just duplicate it???
#sensible code would be like, for seses in [ses12,ses34]: at the very top
#meh, not fixing it
for timesubx in subsections:
    timesub = int(timesubx*5)
    
    for fband in fbands:
        fbandstr = str(fband[0]) + '-' + str(fband[1])
        for conmethod in conmethods:    
            
            fmin = fband[0]
            fmax = fband[1]
            logname = savesumdir + 'aget_' + conmethod + '_' + fbandstr + '_' + str(timesub) + 'e34.csv'
            
            if os.path.isfile(logname) == False or replacer == True:
                
                FCallvec_child = []
                FCallvec_parent = []            
                tvallist = []
                pvallist = []     
                lenofcomparisons = []   
                
                for family in families:
                    strnum = str(family)
                    if len(strnum) == 1:
                        strnum = '0' + strnum
                    strfam = 'sub-19730' + strnum
                
                    parentexist = False
                    childexist = False
                    saveconnectome_child = 'no'
                    saveconnectome_parent = 'no'
                    
                    page = 'C'
    
                    strper = strfam + str(page)
                    personfolder = dir_start + strper + '/'
                    connectome_folder = personfolder + 'connectomes_combined_1124/' + parc + '/'
                    
                    saveconnectomeprefix = strper + '_combined_' + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_'
    
                    
                    agefiles = [filename for filename in os.listdir(connectome_folder) if filename.startswith(saveconnectomeprefix)]
                    agefiles = [file for file in agefiles if file.endswith('_'+str(timesub)+'e_agematch34.csv')]
                    
                    if len(agefiles) == 1:
                        childexist = True
                        saveconnectome_child = connectome_folder + agefiles[0]
                        
                    page = 'P'
    
                    strper = strfam + str(page)
                    personfolder = dir_start + strper + '/'
                    connectome_folder = personfolder + 'connectomes_combined_1124/' + parc + '/'
                    
                    saveconnectomeprefix = strper + '_combined_' + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_'
    
                    
                    agefiles = [filename for filename in os.listdir(connectome_folder) if filename.startswith(saveconnectomeprefix)]
                    agefiles = [file for file in agefiles if file.endswith('_'+str(timesub)+'e_agematch34.csv')]
                    
                    if len(agefiles) == 1:
                        parentexist = True
                        saveconnectome_parent = connectome_folder + agefiles[0]                    
                        
                        
                                    
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
                        
                        
    
                print(len(FCallvec_child),len(FCallvec_parent))
                
                
                
                if len(FCallvec_parent) > 1:
                    print("Running t-tests")
                    veclen = len(FCallvec_parent[0])
                
                    edgetestdf = []
                    for edge in range(veclen):
                        parentedgevec = []
                        childedgevec = []
    
                        for vec in FCallvec_parent:
                            edgeval = vec[edge]
                            parentedgevec.append(edgeval)
    
                        for vec in FCallvec_child:
                            edgeval = vec[edge]
                            childedgevec.append(edgeval)      
                        
                        edgetestdf.append(len(parentedgevec))
                        
                        parentedgevec = np.asarray(parentedgevec)
                        childedgevec = np.asarray(childedgevec)
                        
                        nas = np.logical_or(np.logical_or(np.isinf(parentedgevec),np.isinf(childedgevec)),np.logical_or(np.isnan(parentedgevec),np.isnan(childedgevec)))            
                        tres = ttest_rel(parentedgevec[~nas],childedgevec[~nas])     
                
                        #tres = ttest_rel(parentedgevec,childedgevec,nan_policy='omit')
                        tvallist.append(tres[0])
                        pvallist.append(tres[1])
                        
                    testdf = pd.DataFrame({'tval':tvallist,'pval':pvallist})
                    
                    if saveoutputs:
                        testdf.to_csv(logname)
     



























    
    
    
    
    
    
    
    
    
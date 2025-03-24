#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Calculate the correlation between the real connectome and the average of all simulated connectomes, for every recording
This program does a whole bunch of correlations. It's rather intense, really

"""



import numpy as np
import mne
import pandas as pd
import os
import math
from scipy.stats import spearmanr
from scipy.stats import pearsonr





#folder with all the participant folders and EEG outputs
dir_start = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/prepro1/'

#where structural data is saved
subjects_dir = '/Users/ivy/Desktop/Graff_EEG_stuff/ZPrecise2_MRI_fixed_rename_FS'



#parcellation to use
parc = 'aparc'

#which frequency bands and FC measures to use
fbands = [[8.0,13.0],[13.0,30.0],[2.5,45.0]]
conmethods = ['wpli','imcoh','coh','pli','plv','psi','ciplv','ecso','ecpwo']



#which file(s) do you want to look at?
families = list(range(2,27))
participant_ages = ['C','P']
sessions = [1,2,3,4,'4x']
tasks = ['DORA','YT','RX']




#get a list of everything in the starting directory for structural data
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








corrfamily = []
corrage = []
corrsession = []
corrtask = []
corrspecifictask = []
corrfband = []
corrconmethod = []
corrabs = []
corrcomparison = []
corrcomparisonspecific = []
corrcorrspearman = []
corrcorrpearson = []



#loop through all connectomes
for family in families:
    strnum = str(family)
    if len(strnum) == 1:
        strnum = '0' + strnum
    strfam = 'sub-19730' + strnum

    for page in participant_ages:
        strper = strfam + str(page)
        personfolder = dir_start + strper + '/'
        
        

        sublistval = ''
        
        for subject in subjectlist:
            if strper in subject:
                sublistval = subject
                
        labels_parc = mne.read_labels_from_annot(sublistval, parc=parc,subjects_dir=subjects_dir)                          
    
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


        edgelen = []
        for ii in range(1, len(label_names)):
            x1 = label_xpos[ii]
            y1 = label_ypos[ii]
            z1 = label_zpos[ii]
            
            for jj in range(ii):
                x2 = label_xpos[jj]
                y2 = label_ypos[jj]
                z2 = label_zpos[jj]                            
                
                xdiff = abs(x1-x2)
                ydiff = abs(y1-y2)
                zdiff = abs(z1-z2)
                
                ss = xdiff*xdiff+ydiff*ydiff+zdiff*zdiff
                sr = math.sqrt(ss)
                
                edgelen.append(sr)       
     

        
        for session in sessions:
            input_data_folder = personfolder + 'ses-' + str(session) + '/eeg/'

            connectome_folder_sim = personfolder + 'ses-' + str(session) + '/connectomes_simulated_0624/' + parc + '/'

            connectome_folder_real = personfolder + 'ses-' + str(session) + '/connectomes_0624/' + parc + '/'
            
            if os.path.isdir(connectome_folder_sim):
                pathfiles = os.listdir(connectome_folder_sim)
            else:
                pathfiles = []
            
            for task in tasks:
                
                veclist = []
                vecnamelist = []

                proceed = True

                adjfolder_sim = [file for file in pathfiles if task in file]
                if len(adjfolder_sim) != 1:
                    print("There is no folder for",task,"for",connectome_folder_sim)
                    proceed = False
                else:
                    adjfolder_sim = connectome_folder_sim + adjfolder_sim[0] + '/'

                adjfolder_real = connectome_folder_real
                    
                if proceed:

                    raw_data_file_sub_sim = 'simulated_' + strper + '_ses-' + str(session) + '_task-' + task
                    raw_data_file_sub_real = strper + '_ses-' + str(session) + '_task-' + task
                    
                    if os.path.exists(adjfolder_sim):
                        prefixed = [filename for filename in os.listdir(adjfolder_sim) if filename.startswith(raw_data_file_sub_sim)]  
                        
                        if len(prefixed) == 0:
                            print("There are no files matching the name " + raw_data_file_sub_sim)
                        else:
                                                       
                            filetosaveprefix_og = prefixed[0].split('_')
                            
                            
                            
                            specifictask = filetosaveprefix_og[3].split('-')[1]
                            filetosaveprefix = strper + '_ses-' + str(session) + '_' + filetosaveprefix_og[3] + '_'     
                            
                            for fband in fbands:
                                fbandstr = str(fband[0]) + '-' + str(fband[1])
                                fmin = fband[0]
                                fmax = fband[1]
                                             
                                for cn in range(len(conmethods)):  
                                    conmethod = conmethods[cn]
                                    
                                    saveconnectome_real = adjfolder_real + filetosaveprefix + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_fulle.csv'
                                    
                                    if os.path.isfile(saveconnectome_real):
                                 
                                        
                                        saveconnectome_start = 'simulated_' + filetosaveprefix + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_rand'
                                        
                                        randfiles = [filename for filename in os.listdir(adjfolder_sim) if filename.startswith(saveconnectome_start)]
                                    
                                        if len(randfiles) == 0:
                                            print("AAAAAH SCREW UP")   
                                            
                                        else:
                                            filestoload_sim = [adjfolder_sim + randfile for randfile in randfiles]
                                            filestoload_sim.sort()
                                            
                                            alldflist_sim = []
                                            alldfabslist_sim = []
                                            
                                            for file in filestoload_sim:
                                                print("Loading " + file) 
                                                
                                                parceldata1 = pd.read_csv(file,index_col=0)
                                                
                                                FCm = np.squeeze(np.asarray(parceldata1))
                                                FCm = np.arctanh(FCm)
        
                                                vec = []
                                                for ii in range(1, FCm.shape[0]):
                                                    for jj in range(ii):
                                                        vec.append(FCm[ii, jj])
                                                
                                                alldflist_sim.append(np.asarray(vec))  
                                                alldfabslist_sim.append(np.asarray([abs(x) for x in vec]))
        
        
                                            randvecs = np.array(alldflist_sim)
                                            randvecs = np.transpose(randvecs)
                                                                        
                                            newvec_sim = []
                                            for randvec in randvecs:
                                                test = np.ma.masked_invalid(randvec).mean()
                                                newvec_sim.append(test) 

                                            veclist.append(np.asarray(newvec_sim))
                                            vecnamelist.append(conmethod + '_' + fbandstr + '_simnonabs')
        
        
                                            randvecs = np.array(alldfabslist_sim)
                                            randvecs = np.transpose(randvecs)
                                                                        
                                            newvec_simabs = []
                                            for randvec in randvecs:
                                                test = np.ma.masked_invalid(randvec).mean()
                                                newvec_simabs.append(test) 
                                            
                                            veclist.append(np.asarray(newvec_simabs))
                                            vecnamelist.append(conmethod + '_' + fbandstr + '_simabs')
        
        
                                            print("Loading " + saveconnectome_real) 
                                            parceldata1 = pd.read_csv(saveconnectome_real,index_col=0)
                                            
                                            FCm = np.squeeze(np.asarray(parceldata1))
                                            FCm = np.arctanh(FCm)
        
                                            newvec_real = []
                                            for ii in range(1, FCm.shape[0]):
                                                for jj in range(ii):
                                                    newvec_real.append(FCm[ii, jj])
                                                    
                                            newvec_real = np.asarray(newvec_real)
                                            newvec_realabs = np.asarray([abs(x) for x in newvec_real])
                                            
                                            veclist.append(newvec_real)
                                            vecnamelist.append(conmethod + '_' + fbandstr + '_realnonabs')        
                                            veclist.append(newvec_realabs)
                                            vecnamelist.append(conmethod + '_' + fbandstr + '_realabs')   
                                        
        
        
                print("")
                print("")
                print("")
                print("Checking comparisons for " + filetosaveprefix[:-1])
                print("")
                print("")
                print("")
                if len(veclist) > 1:
                    veclist.append(np.asarray(edgelen))
                    vecnamelist.append('distance')  
                    
                    abslist = ['abs','nonabs']
                    
                    for fband in fbands:
                        fbandstr = str(fband[0]) + '-' + str(fband[1])
                        
                        fbands2 = fbands.copy()
                        fbands2.remove(fband)

                        for cn in range(len(conmethods)):  
                            conmethod = conmethods[cn]    
                            
                            conmethods2 = conmethods.copy()
                            conmethods2.remove(conmethod)
                            
                            for abstype in abslist:
                                
                                if abstype == 'abs':
                                    otherabs = 'nonabs'
                                else:
                                    otherabs = 'abs'
                                    
                            
                                vecname1 = conmethod + '_' + fbandstr + '_real' + abstype
                                indexval1 = vecnamelist.index(vecname1)
                                vec1 = veclist[indexval1]
                                
                            
                            
                            
                            
                                vecname2 = 'distance'
                                indexval2 = vecnamelist.index(vecname2)
                                vec2 = veclist[indexval2]
                                
                                
                                nas = np.logical_or(np.logical_or(np.isinf(vec1),np.isinf(vec2)),np.logical_or(np.isnan(vec1),np.isnan(vec2)))
                                pcorr = pearsonr(vec1[~nas],vec2[~nas])[0]
                                scorr = spearmanr(vec1[~nas],vec2[~nas])[0]
                                
                                
                                corrfamily.append(strfam)
                                corrage.append(page)
                                corrsession.append(session)
                                corrtask.append(task)
                                corrspecifictask.append(specifictask)
                                corrfband.append(fbandstr)
                                corrconmethod.append(conmethod)
                                corrabs.append(abstype)
                                corrcomparison.append('distance')
                                corrcorrpearson.append(pcorr)
                                corrcorrspearman.append(scorr)
                                corrcomparisonspecific.append('distance')
                                


                                vecname2 = conmethod + '_' + fbandstr + '_sim' + abstype
                                indexval2 = vecnamelist.index(vecname2)
                                vec2 = veclist[indexval2]
                                
                                
                                nas = np.logical_or(np.logical_or(np.isinf(vec1),np.isinf(vec2)),np.logical_or(np.isnan(vec1),np.isnan(vec2)))
                                pcorr = pearsonr(vec1[~nas],vec2[~nas])[0]
                                scorr = spearmanr(vec1[~nas],vec2[~nas])[0]
                                
                                
                                corrfamily.append(strfam)
                                corrage.append(page)
                                corrsession.append(session)
                                corrtask.append(task)
                                corrspecifictask.append(specifictask)
                                corrfband.append(fbandstr)
                                corrconmethod.append(conmethod)
                                corrabs.append(abstype)
                                corrcomparison.append('sim')
                                corrcorrpearson.append(pcorr)
                                corrcorrspearman.append(scorr)
                                corrcomparisonspecific.append('sim')
                                
                                
                                
                                vecname2 = conmethod + '_' + fbandstr + '_real' + otherabs
                                indexval2 = vecnamelist.index(vecname2)
                                vec2 = veclist[indexval2]
                                
                                
                                nas = np.logical_or(np.logical_or(np.isinf(vec1),np.isinf(vec2)),np.logical_or(np.isnan(vec1),np.isnan(vec2)))
                                pcorr = pearsonr(vec1[~nas],vec2[~nas])[0]
                                scorr = spearmanr(vec1[~nas],vec2[~nas])[0]
                                
                                
                                corrfamily.append(strfam)
                                corrage.append(page)
                                corrsession.append(session)
                                corrtask.append(task)
                                corrspecifictask.append(specifictask)
                                corrfband.append(fbandstr)
                                corrconmethod.append(conmethod)
                                corrabs.append(abstype)
                                corrcomparison.append('abs_comp')
                                corrcorrpearson.append(pcorr)
                                corrcorrspearman.append(scorr)    
                                corrcomparisonspecific.append(otherabs)
                                


                                for conmethod2 in conmethods2:
                                    
                                    for abstype2 in abslist:
                                    
                                        vecname2 = conmethod2 + '_' + fbandstr + '_real' + abstype2
                                        indexval2 = vecnamelist.index(vecname2)
                                        vec2 = veclist[indexval2]
                                        
                                        
                                        nas = np.logical_or(np.logical_or(np.isinf(vec1),np.isinf(vec2)),np.logical_or(np.isnan(vec1),np.isnan(vec2)))
                                        pcorr = pearsonr(vec1[~nas],vec2[~nas])[0]
                                        scorr = spearmanr(vec1[~nas],vec2[~nas])[0]
                                        
                                        
                                        corrfamily.append(strfam)
                                        corrage.append(page)
                                        corrsession.append(session)
                                        corrtask.append(task)
                                        corrspecifictask.append(specifictask)
                                        corrfband.append(fbandstr)
                                        corrconmethod.append(conmethod)
                                        corrabs.append(abstype)
                                        corrcomparison.append('conmethod')
                                        corrcorrpearson.append(pcorr)
                                        corrcorrspearman.append(scorr)      
                                        corrcomparisonspecific.append(conmethod2+'_'+abstype2)




                                for fband2 in fbands2:
                                    fbandstr2 = str(fband2[0]) + '-' + str(fband2[1])
                                    vecname2 = conmethod + '_' + fbandstr2 + '_real' + abstype
                                    indexval2 = vecnamelist.index(vecname2)
                                    vec2 = veclist[indexval2]
                                    
                                    
                                    nas = np.logical_or(np.logical_or(np.isinf(vec1),np.isinf(vec2)),np.logical_or(np.isnan(vec1),np.isnan(vec2)))
                                    pcorr = pearsonr(vec1[~nas],vec2[~nas])[0]
                                    scorr = spearmanr(vec1[~nas],vec2[~nas])[0]
                                    
                                    
                                    corrfamily.append(strfam)
                                    corrage.append(page)
                                    corrsession.append(session)
                                    corrtask.append(task)
                                    corrspecifictask.append(specifictask)
                                    corrfband.append(fbandstr)
                                    corrconmethod.append(conmethod)
                                    corrabs.append(abstype)
                                    corrcomparison.append('fband')
                                    corrcorrpearson.append(pcorr)
                                    corrcorrspearman.append(scorr)  
                                    corrcomparisonspecific.append(fbandstr2)








resultdf = pd.DataFrame({'family':corrfamily,
                         'age':corrage,
                         'session':corrsession,
                         'task':corrtask,
                         'stask':corrspecifictask,
                         'fband':corrfband,
                         'conmethod':corrconmethod,
                         'abs':corrabs,
                         'comparison':corrcomparison,
                         'compspecific':corrcomparisonspecific,
                         'Pearson':corrcorrpearson,
                         'Spearman':corrcorrspearman
                         })

resultdf.to_csv('/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/results_august2024/individualfilecorrelations100/corrdf.csv')
























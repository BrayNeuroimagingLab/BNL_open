#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This program averages the connectomes across all participants, for a given frequency band and FC measure


"""



import numpy as np
import mne
import pandas as pd
import os




#folder with all the participant folders and EEG outputs
dir_start = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/prepro1/'

#folder where structural data is saved
subjects_dir = '/Users/ivy/Desktop/Graff_EEG_stuff/ZPrecise2_MRI_fixed_rename_FS'

#where to save outputs
savedir = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/results_august2024/avg100/'



#use simulated data
#if false, uses real data
simmode = False



#aparc doesn't work right now
parc = 'aparc'

#which frequency bands and FC measures to use
fbands = [[8.0,13.0],[13.0,30.0],[2.5,45.0]]
conmethods = ['wpli','imcoh','coh','pli','plv','psi','ciplv','ecso','ecpwo']



#which file(s) do you want to look at?
families = list(range(2,27))
participant_ages = ['C','P']
sessions = [1,2,3,4,'4x']
tasks = ['DORA','YT','RX']




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





for fband in fbands:
    fbandstr = str(fband[0]) + '-' + str(fband[1])
    fmin = fband[0]
    fmax = fband[1]
        
    dataname = str(fmin)+'-'+str(fmax)
    
    for cn in range(len(conmethods)):  
        
        conmethod = conmethods[cn]
        
        avgname = savedir + 'avg_' + fbandstr + '_' + conmethod
        if simmode:
            avgname = avgname + '_sim'
        else:
            avgname = avgname + '_nonsim'
            
        avgname_abs = avgname + '_abs.csv'
        avgname_nonabs = avgname + '_nonabs.csv'
        
        
        alldflist = []
        alldfabslist = []

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
                    if simmode:
                        connectome_folder = personfolder + 'ses-' + str(session) + '/connectomes_simulated_0624/' + parc + '/'
                    else:
                        connectome_folder = personfolder + 'ses-' + str(session) + '/connectomes_0624/' + parc + '/'
                    
                    if os.path.isdir(connectome_folder):
                        pathfiles = os.listdir(connectome_folder)
                    else:
                        pathfiles = []
                    
                    for task in tasks:
                        
                        filestoload = []
                        
                        proceed = True
                        if simmode:
                            adjfolder = [file for file in pathfiles if task in file]
                            if len(adjfolder) != 1:
                                print("There is no folder for",task,"for",connectome_folder)
                                proceed = False
                            else:
                                adjfolder = connectome_folder + adjfolder[0] + '/'
                        else:
                            adjfolder = connectome_folder
                            
                        if proceed:
                            
                            if simmode:
                                raw_data_file_sub = 'simulated_' + strper + '_ses-' + str(session) + '_task-' + task
                            else:
                                raw_data_file_sub = strper + '_ses-' + str(session) + '_task-' + task
                            if os.path.exists(adjfolder):
                                prefixed = [filename for filename in os.listdir(adjfolder) if filename.startswith(raw_data_file_sub)]  
                                
                                if len(prefixed) == 0:
                                    print("There are no files matching the name " + raw_data_file_sub)
                                else:
                                                               
                                    filetosaveprefix = prefixed[0].split('_')
                                    
                                    if simmode:
                                        specifictask = filetosaveprefix[3].split('-')[1]
                                        filetosaveprefix = strper + '_ses-' + str(session) + '_' + filetosaveprefix[3] + '_'
                                        saveconnectome_start = 'simulated_' + filetosaveprefix + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_rand'
                                        
                                        randfiles = [filename for filename in os.listdir(adjfolder) if filename.startswith(saveconnectome_start)]
                                    
                                        if len(randfiles) == 0:
                                            print("AAAAAH SCREW UP")   
                                            
                                        else:
                                            filestoload = [adjfolder + randfile for randfile in randfiles]
                                            filestoload.sort()
                                            
                                    else:
                                        specifictask = filetosaveprefix[2].split('-')[1]
                                        filetosaveprefix = strper + '_ses-' + str(session) + '_' + filetosaveprefix[2]                         
                                        saveconnectome = adjfolder + filetosaveprefix + '_' + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_fulle.csv'
                                        
                                        if os.path.isfile(saveconnectome):
                                            filestoload = [saveconnectome]
                    
                    
                                    
                                    for file in filestoload:
                                        print("Loading " + file) 
                                        
                                        parceldata1 = pd.read_csv(file,index_col=0)
                                        
                                        FCm = np.squeeze(np.asarray(parceldata1))
                                        FCm = np.arctanh(FCm)

                                        vec = []
                                        for ii in range(1, FCm.shape[0]):
                                            for jj in range(ii):
                                                vec.append(FCm[ii, jj])
                                        
                                        alldflist.append(np.asarray(vec))  
                                        #also save the absolute value of the connectome
                                        absvec = [abs(x) for x in vec]
                                        alldfabslist.append(np.asarray(absvec))
                                        
                                        
                                        

                                        
        xy = []
        for x in alldflist:
            xy.append(x[0])



        print("")
        print("Making average dfs")
        print("")  
        
        #does this for both the connectomes and the absolute value of connectomes
        
        almostavg = np.array(alldflist)
        almostavg = np.transpose(almostavg)
        
        avg = []
        for edgecol in almostavg:
            test = np.ma.masked_invalid(edgecol).mean()
            avg.append(test)
            


        almostavgabs = np.array(alldfabslist)
        almostavgabs = np.transpose(almostavgabs)
        
        avgabs = []
        for edgecol in almostavgabs:
            test = np.ma.masked_invalid(edgecol).mean()
            avgabs.append(test)
            

        
        
        #turn vector back into df
        avgdf = []
        rl = len(label_names)
        vn = 0
        for ii in range(rl):
            datahere = []
            for x in range(ii):
                datahere.append(avg[vn])
                vn = vn + 1
            for x in range(rl-ii):
                datahere.append(0)
            avgdf.append(datahere)
        avgdf = pd.DataFrame(data=avgdf)
        avgdf = avgdf + avgdf.T
        avgdf.index = label_names
        avgdf.columns = label_names        
        avgdf.to_csv(avgname_nonabs)
        

        #now do it again, but for the absolute value
        avgdf = []
        rl = len(label_names)
        vn = 0
        for ii in range(rl):
            datahere = []
            for x in range(ii):
                datahere.append(avgabs[vn])
                vn = vn + 1
            for x in range(rl-ii):
                datahere.append(0)
            avgdf.append(datahere)
        avgdf = pd.DataFrame(data=avgdf)
        avgdf = avgdf + avgdf.T
        avgdf.index = label_names
        avgdf.columns = label_names        
        avgdf.to_csv(avgname_abs)












#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 18:03:29 2022


This creates the forward solution and remontages the EEG

@author: Kirk
"""




import numpy as np
import mne
import pandas as pd
import os
from shutil import copyfile
import time


#where is structural data saved. There should be one structural file per participant
subjects_dir = '/Users/ivy/Desktop/Test_EEG/Test_MRI_ARCfiles/'


#folder with all the participant folders and EEG outputs
dir_start = '/Users/ivy/Desktop/Test_EEG/Test_EEG_output/'



electrodefile = '/Users/ivy/Desktop/Test_EEG/AdultAverageNet64_v1.sfp'


replacer = False




#which file(s) do you want to look at?
#families = [2,3,5,6,7,8,9,10,11,12,13,14,16,18]
#participant_ages = ['C','P']
#sessions = [1,2,3,4]
#tasks = ['DORA','YT','RX']


families = [3]
participant_ages = ['C']
sessions = [2]
tasks = ['DORA']




#if you need to mark channels as bad due to spatial reasons
specialchange = [['sub-1973018P',['E63','E64']],
                 ['sub-1973012C',['E63','E64']],
                 ['sub-1973001C',['E62']]]





#EEG data locations
locdf = pd.read_csv(electrodefile,sep='\t',header=None,index_col=0)
locdf = locdf*10/1000



for family in families:
    strnum = str(family)
    if len(strnum) == 1:
        strnum = '0' + strnum
    strfam = 'sub-19730' + strnum

    for page in participant_ages:
        strper = strfam + str(page)
        personfolder = dir_start + strper + '/'
        
        specialadj = False
        specialdropch = []
        for spech in specialchange:
            if spech[0] == strper:
                specialadj = True
                specialdropch = spech[1]
                print("This participant requires certain electrodes dropped: " + str(specialdropch))
                print("")
                
        
        prefixed = [filename for filename in os.listdir(subjects_dir) if filename.startswith(strper)]

        personfolder2 = subjects_dir + '/' + prefixed[0]
        subject = prefixed[0]
        eegscale = subjects_dir + '/' + subject + '/eegscale'
        
        if len(prefixed) != 1:
            print('Uh oh, problem with structural data, either 0 or multiple structural files for participant')
        elif os.path.isfile(eegscale) == False:
            print("Do not have the EEG scale file")
            
        else:
            
            antsfolder = subjects_dir + '/' + subject + '/ANTS_fun/'
            bemfolder = subjects_dir + '/' + subject + '/bem/'
            transformsave = bemfolder + 'transform-trans.fif'

            bemlayers = ['brain.surf','inner_skull.surf','outer_skull.surf']
            antslayers = ['brain_combined.surf','inner_skull_final.surf','outer_skull_expanded.surf']
            antscopies = ['brain_orig.surf','inner_skull_orig.surf','outer_skull_orig.surf']

        
            print("Shuffling around BEM layer files")
            
            backupfolder = bemfolder + 'zorig_backup/'
            if not os.path.exists(backupfolder):
                os.makedirs(backupfolder)  
            
            
            for fn in range(len(bemlayers)):
                bemfile = bemfolder + bemlayers[fn]
                antsfile = antsfolder + antslayers[fn]
                copyfile(antsfile,bemfile)
                
                antsfilecopy = antsfolder + antscopies[fn]
                bemfileorig = backupfolder + bemlayers[fn]
                copyfile(antsfilecopy,bemfileorig)


            print("Creating custom EEG montage")
            scalehere = []
            with open(eegscale) as file:
                for line in file:
                    scalehere.append(float(line))

            scale1 = scalehere[0]
            scale2 = scalehere[1]
            scale3 = scalehere[2] 
                
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

        
            if not os.path.exists(personfolder):
                print("This folder doesn't exist: " + personfolder)
            else:
            
                for session in sessions:
                    output_data_folder = personfolder + 'ses-' + str(session) + '/eeg/'
                    
                    for task in tasks:
                                                
                        raw_data_file_sub = strper + '_ses-' + str(session) + '_task-' + task
                        
                        if os.path.exists(output_data_folder):
                            prefixed = [filename for filename in os.listdir(output_data_folder) if filename.startswith(raw_data_file_sub)]
                        else:
                            prefixed = []
                        
                        if len(prefixed) == 0:
                            print("There are no files starting with: " + raw_data_file_sub)
                        
                        else:
                            fullfile = [filename for filename in prefixed if filename.endswith('repint_epo.fif')]
                            
     
                            if len(fullfile) > 1:
                                print("There are multiple files that exist of the same task:")
                                for val in fullfile:
                                    print(val)
                                print("For now, ignoring all of them")
                            elif len(fullfile) == 0:
                                print("There are no files starting with: " + raw_data_file_sub)
                            else:
                                raw_data_file = fullfile[0]                    
     
     
                                filetoload = output_data_folder + raw_data_file
                                filetosave = filetoload[:-7] + 'remontage_epo.fif'
                                
                                savefwd = filetoload[:-7] + 'lol-fwd.fif'
                                
                                if os.path.isfile(savefwd) and replacer == False:
                                        print("Output files already exist for " + subject)
                                
                                else:
                                
                                    starttime = time.time()    
                                
                                    #read in the EEG data, change the montage based on the scale factor, save it
                                    raw = mne.read_epochs(filetoload,preload=True)
                                    
                                    if specialadj:
                                        curbad = raw.info['bads'].copy()
                                        for newbad in specialdropch:
                                            if newbad not in curbad:
                                                curbad.append(newbad)
                                        curbad.sort()
                                        raw.info['bads'] = curbad
                                    
                                    print("Bad channels are:")
                                    print(raw.info['bads'])
                                        
                                        
                                    raw3 = raw.copy().set_montage(custmontage)
                                    raw3.set_eeg_reference(projection=True)
                                    raw3.apply_proj(verbose=True)
                                    raw3.save(filetosave,overwrite=True)
                                    
                                    #add_dist could be True or 'patch'
                                    src = mne.setup_source_space(subject, spacing='oct6', add_dist=True,subjects_dir=subjects_dir)
                                    #src = mne.setup_source_space(subject, spacing='oct6', add_dist='patch',subjects_dir=subjects_dir)
                                    
                                    #conductivity = (0.3,)  # for single layer
                                    conductivity = (0.3, 0.006, 0.3)  # for three layers
                                    model = mne.make_bem_model(subject=subject, ico=4,conductivity=conductivity,subjects_dir=subjects_dir)
                                    bem = mne.make_bem_solution(model)
                        
                                    fwd = mne.make_forward_solution(filetosave, trans=transformsave, src=src, bem=bem,
                                                                    meg=False, eeg=True, mindist=5.0, n_jobs=None,verbose=None)
                                    #print(fwd)
                            
                                    mne.write_forward_solution(savefwd,fwd,overwrite=True)
                                    
                                    endtime = time.time()
                                    timepassed = endtime-starttime
                                    timepassed_min = str(round(timepassed/60,2))
                                    
                                    print("")
                                    print("")
                                    print("Done for " + filetosave)   
                                    print("Done for " + filetosave)    
                                    print("Time passed for this file = " + timepassed_min + ' min')
                                    print("")
                                    print("")
                                    print("")
                                    print("")
                                    print("")
                                    print("")
                                    print("")
                                    print("")
                        
                        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    





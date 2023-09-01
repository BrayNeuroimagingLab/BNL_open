#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This script makes the connectomes for the analysis described in Kirk's EEG paper, where it looked at the effect
of time on individualization. It combines the 12 recordings for each participant into two connectomes.
It does this for various number of epochs used

This program is a variation of the program source localization 8. See it for more information / read my EEG Preprocessing Guide


"""



import mne
import pandas as pd
import os
from mne.minimum_norm import make_inverse_operator, apply_inverse_epochs
from mne_connectivity import spectral_connectivity_epochs
from mne_connectivity import phase_slope_index
import time


#where is structural data saved. There should be one structural file per participant
subjects_dir = '/Users/ivy/Desktop/Test_EEG/Test_MRI_ARCfiles/'

#folder with all the participant folders and EEG outputs
dir_start = '/Users/ivy/Desktop/Test_EEG/Test_EEG_output/'


manadj = '/Users/ivy/Desktop/Test_EEG_tostart/testmanualadj.csv'


replacer = False



#parclist = ['aparc','aparc.a2009s']
parclist = ['aparc']


#which frequency bands and FC measures to generate connectomes for
#as an example, you could use
#fbands = [[4.0,8.0],[8.0,13.0],[13.0,30.0],[2.5,45.0],[30.0,45.0]]
#conmethods = ['wpli','imcoh','coh','plv','pli']

fbands = [[8.0,13.0]]
conmethods = ['imcoh']



#which file(s) do you want to look at?
families = list(range(2,27))
participant_ages = ['P','C']



#source localization method
method = "eLORETA"
snr = 1.0


#which # of epochs do you want to generate for?
subsections = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,20,25,30,35,40,45,50,60,70,80,90,100,110,120,130,140,150]




sessions = [1,2,3,4]
tasks = ['DORA','YT','RX']




adjdf = pd.read_csv(manadj)


for parc in parclist:

    for family in families:
        strnum = str(family)
        if len(strnum) == 1:
            strnum = '0' + strnum
        strfam = 'sub-19730' + strnum
    
        for page in participant_ages:
            starttime = time.time() 
            
            readincount = 0
            
            strper = strfam + str(page)
            personfolder = dir_start + strper + '/'

            if not os.path.exists(personfolder):
                print("This folder doesn't exist: " + personfolder)
                
            else:
            
                print("Makin' connectomes for: " + strper)
                
                prefixed = [filename for filename in os.listdir(subjects_dir) if filename.startswith(strper)]
        
                personfolder2 = subjects_dir + '/' + prefixed[0]
                subject = prefixed[0]
    
                connectome_folder = personfolder + 'connectomes_combined/' + parc + '/'
                
                if not os.path.exists(connectome_folder):
                    os.makedirs(connectome_folder)  
                    
                outputfiles = os.listdir(connectome_folder)
                if len(outputfiles) > 3 and replacer == False:
                    print("Output files already exist for: " + connectome_folder)                
                
                elif len(prefixed) != 1:
                    print('Uh oh, problem with structural data, either 0 or multiple structural files for participant')
                
                else:
                                
                    for session in sessions:
                        input_data_folder = personfolder + 'ses-' + str(session) + '/eeg/'
                        
                        for task in tasks:
                            raw_data_file_sub = strper + '_ses-' + str(session) + '_task-' + task
                            
                            if os.path.exists(input_data_folder):
                                prefixed = [filename for filename in os.listdir(input_data_folder) if filename.startswith(raw_data_file_sub)]
                            else:
                                prefixed = []
                            
                            if len(prefixed) == 0:
                                print("There are no files starting with: " + raw_data_file_sub)
                            
                            else:
                                fullfile = [filename for filename in prefixed if filename.endswith('remontage_epo.fif')]
                                fwdfile = [filename for filename in prefixed if filename.endswith('fwd.fif')]
                            
                                if len(fullfile) > 1 or len(fwdfile) > 1:
                                    print("There are multiple files that exist of the same task:")
                                    for val in fullfile:
                                        print(val)
                                    for val in fwdfile:
                                        print(val)
                                    print("For now, ignoring all of them")
                                elif len(fullfile) == 0 or len(fwdfile) == 0:
                                    print("There are missing files starting with: " + raw_data_file_sub)
                                else:    
                                    filetosaveprefix = fullfile[0].split('eeg_')[0]
                                      
                                    adjdfname = filetosaveprefix + 'eeg.raw'
                                    adjdata = adjdf[adjdf['File'] == adjdfname]
                                    
                                    if len(adjdata) != 1:
                                        print("Info on this scan in adjepochdf is wrong")
                                        
                                    else:
                                        omitdata = adjdata.iloc[0]['Omit']
                                        if omitdata != 'no':
                                            print(filetosaveprefix + ' is being omitted due to the adjepochdf')
                                        
                                        else:

                                            readincount = readincount + 1
                                                
            print("Number of scans for " + strper + ": " + str(readincount))
            label_ts_list = []
            namelist = []            
            if readincount == 12:

                for session in sessions:
                    input_data_folder = personfolder + 'ses-' + str(session) + '/eeg/'
                    
                    for task in tasks:
                        raw_data_file_sub = strper + '_ses-' + str(session) + '_task-' + task
                        prefixed = [filename for filename in os.listdir(input_data_folder) if filename.startswith(raw_data_file_sub)]
                        fullfile = [filename for filename in prefixed if filename.endswith('remontage_epo.fif')]
                        fwdfile = [filename for filename in prefixed if filename.endswith('fwd.fif')]

                        remontage_path = input_data_folder + fullfile[0]   
                        fwd_path = input_data_folder + fwdfile[0]

                        filetosaveprefix = fullfile[0].split('eeg_')[0]

                        print("Makin' connectomes starting with: " + filetosaveprefix)
                        
                        adjdfname = filetosaveprefix + 'eeg.raw'
                        adjdata = adjdf[adjdf['File'] == adjdfname]
                        
                        dropstart = int(adjdata.iloc[0]['Drop_start'])
                        dropend = int(adjdata.iloc[0]['Drop_end'])
                            
                        print("Reading in " + remontage_path)

                        epochsadj = mne.read_epochs(remontage_path,preload=True) 
                        if dropstart > 0:
                            print("Dropping epochs at start: " + str(dropstart))
                            epochsadj = epochsadj[dropstart:].copy()
                        
                        if dropend > 0:
                            print("Dropping epochs at end: " + str(dropend))
                            epochsadj = epochsadj[:-1*dropend].copy()                                                
  
       
                        fwd = mne.read_forward_solution(fwd_path)
                        
                        sfreq = epochsadj.info['sfreq']  # the sampling frequency                        
                        noise_cov = mne.make_ad_hoc_cov(epochsadj.info)
                        

                        #inverse operator
                        inverse_operator = make_inverse_operator(info=epochsadj.info, forward=fwd, noise_cov=noise_cov, depth=3.5)
                        
                        
                        #compute inverse solution
                        lambda2 = 1. / snr ** 2
                        #stcs = apply_inverse_epochs(epochsadj, inverse_operator, lambda2, method,pick_ori="normal", nave=len(epochsadj))
                        stcs = apply_inverse_epochs(epochsadj, inverse_operator, lambda2, method)
                        
                        print("")
                        print("Parcellating")
                        print("")
                        
  
                        #read labels from the freesurfer outputs
                        labels_parc = mne.read_labels_from_annot(subject, parc=parc,subjects_dir=subjects_dir)
                        label_names = [label.name for label in labels_parc]

                        #generate time course data
                        #this is of length 200 (one for each epoch), then each of those is length 68 (for each region), then each of those is 500 (for each timepoint)
                        try:
                            label_ts = mne.extract_label_time_course(stcs=stcs, labels=labels_parc, src=inverse_operator['src'], mode='pca_flip')
                        except:
                            label_ts = mne.extract_label_time_course(stcs=stcs, labels=labels_parc, src=inverse_operator['src'], mode='pca_flip',allow_empty=True)
                            
                            log = []
                            savelog = connectome_folder + filetosaveprefix + parc + '_errorlog.txt'
                            warningmessage = 'Source space does not contain any vertices for 1+ label. Allowing empty'
                            log.append(warningmessage) 
                            print("")
                            with open(savelog, 'w') as f:
                                for item in log:
                                    f.write("%s\n" % item)
                                    print(item)
                            f.close()    
                            
                        label_ts_list.append(label_ts)
                        namelist.append(filetosaveprefix)
            

            if len(namelist) == 12:
                filetosaveprefix = strper + '_combined_'
                
                label_ts0 = label_ts_list[0]
                label_ts1 = label_ts_list[1]
                label_ts2 = label_ts_list[2]
                label_ts3 = label_ts_list[3]
                label_ts4 = label_ts_list[4]
                label_ts5 = label_ts_list[5]        
                
                label_ts6 = label_ts_list[6]
                label_ts7 = label_ts_list[7]
                label_ts8 = label_ts_list[8]
                label_ts9 = label_ts_list[9]
                label_ts10 = label_ts_list[10]
                label_ts11 = label_ts_list[11]                    
                

                for subsection in subsections:
                    sublabel_ts1 = label_ts0[:subsection] + label_ts1[:subsection] + label_ts2[:subsection] + label_ts3[:subsection] + label_ts4[:subsection] + label_ts5[:subsection]
                    sublabel_ts2 = label_ts6[:subsection] + label_ts7[:subsection] + label_ts8[:subsection] + label_ts9[:subsection] + label_ts10[:subsection] + label_ts11[:subsection]


                    for fband in fbands:
                
                        fmin = fband[0]
                        fmax = fband[1]
                        
                        for conmethod in conmethods:              
    
                            filetosave1 = connectome_folder + filetosaveprefix + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_' + str(subsection*6) + 'e_firsthalf.csv'
                            print("Working on " + filetosave1)
                            
                            con = spectral_connectivity_epochs(sublabel_ts1, method=conmethod, mode='multitaper', sfreq=sfreq, fmin=fmin,fmax=fmax, faverage=True, mt_adaptive=True)
                            conmat = con.get_data(output='dense')[:, :, 0]
                            
                            conmatdf = pd.DataFrame(data=conmat)
                            conmatdf.index = label_names
                            conmatdf = conmatdf.set_axis(label_names, axis=1, inplace=False)
                            conmatdf.to_csv(filetosave1)
                            
                            
                            
                            filetosave2 = connectome_folder + filetosaveprefix + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_' + str(subsection*6) + 'e_secondhalf.csv'
                            print("Working on " + filetosave2)
                            
                            con = spectral_connectivity_epochs(sublabel_ts2, method=conmethod, mode='multitaper', sfreq=sfreq, fmin=fmin,fmax=fmax, faverage=True, mt_adaptive=True)
                            conmat = con.get_data(output='dense')[:, :, 0]
                            
                            conmatdf = pd.DataFrame(data=conmat)
                            conmatdf.index = label_names
                            conmatdf = conmatdf.set_axis(label_names, axis=1, inplace=False)
                            conmatdf.to_csv(filetosave2)                           
                        
                            
                        
                        filetosave1 = connectome_folder + filetosaveprefix + parc + '_psi_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_' + str(subsection*6) + 'e_firsthalf.csv'
                        print("Working on " + filetosave1)
                        
                        psi = phase_slope_index(sublabel_ts1,sfreq=sfreq,fmin=fmin, fmax=fmax,mt_adaptive=True)
                        psidata = psi.get_data(output='dense')[:, :, 0]
                        
                        conmatdf = pd.DataFrame(data=psidata)
                        conmatdf.index = label_names
                        conmatdf = conmatdf.set_axis(label_names, axis=1, inplace=False)      
                        conmatdf.to_csv(filetosave1)     
                        
                        
                        
                        filetosave2 = connectome_folder + filetosaveprefix + parc + '_psi_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_' + str(subsection*6) + 'e_secondhalf.csv'
                        print("Working on " + filetosave2)
                        
                        psi = phase_slope_index(sublabel_ts2,sfreq=sfreq,fmin=fmin, fmax=fmax,mt_adaptive=True)
                        psidata = psi.get_data(output='dense')[:, :, 0]
                        
                        conmatdf = pd.DataFrame(data=psidata)
                        conmatdf.index = label_names
                        conmatdf = conmatdf.set_axis(label_names, axis=1, inplace=False)      
                        conmatdf.to_csv(filetosave2)                             


    
                endtime = time.time()
                timepassed = endtime-starttime
                timepassed_min = str(round(timepassed/60,2))
                
                print("")
                print("")
                print("Done for " + connectome_folder)   
                print("Done for " + connectome_folder)    
                print("Time passed for this file = " + timepassed_min + ' min')
                print("")
                print("")                 
    





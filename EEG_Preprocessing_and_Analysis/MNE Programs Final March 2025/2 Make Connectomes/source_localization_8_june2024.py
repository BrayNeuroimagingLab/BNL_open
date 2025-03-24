#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This creates connectomes for each file

"""



import mne
import pandas as pd
import os
from mne.minimum_norm import make_inverse_operator, apply_inverse_epochs
from mne_connectivity import spectral_connectivity_epochs
from mne_connectivity import phase_slope_index
from mne_connectivity import envelope_correlation
import time
import numpy as np
import mne_connectivity


#where is structural data saved. There should be one structural file per participant
subjects_dir = '/Users/ivy/Desktop/Graff_EEG_stuff/ZPrecise2_MRI_fixed_rename_FS'

#folder with all the participant folders and EEG outputs
dir_start = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/prepro1/'

#file with manual adjustments for epochs to include/exclude
manadj = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/manualadj_done.csv'


#write over files if they already exist? If yes, replacer = True. Or ignore them?
replacer = False


#which parcellation(s) to use. This probably only works with aparc(?) but at one point intended to check other parcellations
parclist = ['aparc']


#which frequency bands and FC measures to generate connectomes for
fbands = [[8.0,13.0],[13.0,30.0],[2.5,45.0]]
conmethods = ['wpli','imcoh','coh','plv','pli','ciplv','psi','ecpwo','ecso']



#which file(s) do you want to look at?
families = list(range(2,27))
participant_ages = ['P','C']
sessions = [1,2,3,4,'4x']
tasks = ['DORA','YT','RX']


#source localization method
method = "eLORETA"
snr = 3.0


#what subsets of data to use? 150 = use first 150 epochs, for example. 'full' uses the full scan
#subsections = [150]
subsections = [150,'full']



#filter data, for envelope correlations
def bp_gen(label_ts,fmin,fmax):
    """Make a generator that band-passes on the fly."""
    for ts in label_ts:
        yield mne.filter.filter_data(ts, sfreq, fmin, fmax)
                                                            
                                                            

adjdf = pd.read_csv(manadj)


for family in families:
    strnum = str(family)
    if len(strnum) == 1:
        strnum = '0' + strnum
    strfam = 'sub-19730' + strnum

    for page in participant_ages:
        strper = strfam + str(page)
        personfolder = dir_start + strper + '/'
        
        prefixed = [filename for filename in os.listdir(subjects_dir) if filename.startswith(strper)]

        personfolder2 = subjects_dir + '/' + prefixed[0]
        subject = prefixed[0]

        
        if len(prefixed) != 1:
            print('Uh oh, problem with structural data, either 0 or multiple structural files for participant')
            
        else:
            
            if not os.path.exists(personfolder):
                print("This folder doesn't exist: " + personfolder)
            else:
                
                for parc in parclist:
            
                    for session in sessions:
                        input_data_folder = personfolder + 'ses-' + str(session) + '/eeg/'
                        connectome_folder = personfolder + 'ses-' + str(session) + '/connectomes_0624/' + parc + '/'
                        
                        if not os.path.exists(connectome_folder):
                            os.makedirs(connectome_folder)  
                                
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
                                
                                epochdatafolder = [filename for filename in prefixed if filename.endswith('eeg')]
                                
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
                                    remontage_path = input_data_folder + fullfile[0]   
                                    fwd_path = input_data_folder + fwdfile[0]
    
                                    filetosaveprefix = fullfile[0].split('eeg_')[0]
                                    
                                    
                                    outputfiles = [filename for filename in os.listdir(connectome_folder) if filename.startswith(filetosaveprefix)]
                                    
    
                                    if len(outputfiles) > 0 and replacer == False:
                                        print("Output files already exist starting with: " + filetosaveprefix)
                                    else:
                                        print("Makin' connectomes starting with: " + filetosaveprefix)
                                        
                                        adjdfname = filetosaveprefix + 'eeg.raw'
                                        adjdata = adjdf[adjdf['File'] == adjdfname]
                                        
                                        if len(adjdata) != 1:
                                            print("Info on this scan in adjepochdf is wrong")
                                            
                                        else:
                                            omitdata = adjdata.iloc[0]['Omit']
                                            dropstart = int(adjdata.iloc[0]['Drop_start'])
                                            dropend = int(adjdata.iloc[0]['Drop_end'])
                                            
                                            if omitdata != 'no':
                                                print(filetosaveprefix + ' is being omitted due to the adjepochdf')
                                            
                                            else:
                                                
                                                starttime = time.time()    
                                                    
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
                                                #this is of length 200ish (one for each epoch), then each of those is length 68 (for each region), then each of those is 500 (for each timepoint)
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
            
                                                for subsection in subsections:
                                                    
                                                    if subsection != 'full':
                                                        sublabel_ts = label_ts[:subsection]      
                                                    else:
                                                        sublabel_ts = label_ts.copy()

            
                                                    for fband in fbands:
                                                        
                                                        fmin = fband[0]
                                                        fmax = fband[1]
                                                        
                                                        for conmethod in conmethods:              
            
                                                            filetosave = connectome_folder + filetosaveprefix + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_' + str(subsection) + 'e.csv'
                                                            print("Working on " + filetosave)
                                                            
                                                            corr = []
                                                            
                                                            if conmethod == 'psi':
                                                                                                                                
                                                                psi = phase_slope_index(sublabel_ts,sfreq=sfreq,fmin=fmin, fmax=fmax,mt_adaptive=True)
                                                                corr = psi.get_data(output='dense')[:, :, 0]
                                                                
                                                            elif conmethod == 'ecpwo':
                                                                            
                                                                corr_obj = envelope_correlation(bp_gen(sublabel_ts,fmin,fmax), orthogonalize="pairwise")
                                                                corr = corr_obj.combine()
                                                                corr = corr.get_data(output="dense")[:, :, 0]  
                                                                
                                                            elif conmethod == 'ecso':

                                                                
                                                                label_ts_orth = mne_connectivity.envelope.symmetric_orth(sublabel_ts)
            
                                                                corr_obj = envelope_correlation(bp_gen(label_ts_orth,fmin,fmax), orthogonalize=False)
                                                                corr2 = corr_obj.combine()
                                                                corr2 = corr2.get_data(output="dense")[:, :, 0]
                                                                corr2.flat[:: corr2.shape[0] + 1] = 0  # zero out the diagonal
                                                                corr = np.abs(corr2)   
                                                                
                                                            else:
                                                                
                                                                con = spectral_connectivity_epochs(sublabel_ts, method=conmethod, mode='multitaper', sfreq=sfreq, fmin=fmin,fmax=fmax, faverage=True, mt_adaptive=True)
                                                                corr = con.get_data(output='dense')[:, :, 0]
                                                            

                                                            conmatdf = pd.DataFrame(data=corr)
                                                            conmatdf.index = label_names
                                                            conmatdf.columns = label_names
                                                            conmatdf.to_csv(filetosave)
                                                            
                                                
                                                    

                                            endtime = time.time()
                                            timepassed = endtime-starttime
                                            timepassed_min = str(round(timepassed/60,2))
                                            
                                            print("")
                                            print("")
                                            print("Done for " + filetosaveprefix)   
                                            print("Done for " + filetosaveprefix)    
                                            print("Time passed for this file = " + timepassed_min + ' min')
                                            print("")
                                            print("")
                                            print("")
                                            print("")
                                            print("")
                                            print("")
                                            print("")
                                            print("")
                                                                            
   
    
                                                            



















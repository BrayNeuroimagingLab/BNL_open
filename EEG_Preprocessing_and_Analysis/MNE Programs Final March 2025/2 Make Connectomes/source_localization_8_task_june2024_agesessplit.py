#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This script makes connectomes for the age analysis described in Kirk's EEG paper. Of the families where there are 11 recordings
that both the parent and child watched, it uses 5 from ses1+2 and 5 from ses3+4 to make connectomes of varying length
These can be used to assess age effects (eg by comparing, for each edge, the ses1+2 connectomes for all adults vs all children)
and to assess if age effects are consistent (by comparing the T values for each edge from ses12 with ses34)


This program is a variation of the program source localization 8. See it for more information / read my EEG Preprocessing Guide


"""



import mne
import pandas as pd
import os
from mne.minimum_norm import make_inverse_operator, apply_inverse_epochs
#from mne_connectivity import spectral_connectivity_epochs
#from mne_connectivity import phase_slope_index
import time
from mne_connectivity import envelope_correlation
import numpy as np
import mne_connectivity

from subepochconnectivity import spectral_connectivity_epochs2
from subepochconnectivitypsi import phase_slope_index2


#where is structural data saved. There should be one structural file per participant
subjects_dir = '/Users/ivy/Desktop/Graff_EEG_stuff/ZPrecise2_MRI_fixed_rename_FS'

#folder with all the participant folders and EEG outputs
dir_start = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/prepro1/'
dir_start_output = '/Volumes/Backup_Backup/Hooray_EEG/prepro1/'


manadj = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/manualadj_done.csv'


replacer = False








#which file(s) do you want to look at?
families = list(range(2,27))
participant_ages = ['P','C']


#which # of epochs do you want to generate for?
#10 epochs means 10 x 5 recordings, so really, 50 epochs
subsections = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,20,25,30,35,40,45,50,60,70,80,90,100,110,120,130,140,150]



#don't change these
parclist = ['aparc']
sessions = [1,2,3,4]
tasks = ['DORA','YT','RX']
conmethods = ['wpli','imcoh','coh','plv','pli','ciplv']
fbands = [[8.0,13.0],[13.0,30.0],[2.5,45.0]]


#source localization method
method = "eLORETA"
snr = 3.0

subsections.sort()


fminlist = ()
fmaxlist = ()
for fband in fbands:
    fminlist = fminlist + (fband[0],)
    fmaxlist = fmaxlist + (fband[1],)  


adjdf = pd.read_csv(manadj)


def bp_gen(label_ts,fmin,fmax):
    """Make a generator that band-passes on the fly."""
    for ts in label_ts:
        yield mne.filter.filter_data(ts, sfreq, fmin, fmax)


#how to make connectomes for most connectivity measures
def make_connect_classic(newlabel_ts,altsubsections,fminlist,fmaxlist,sfreq,conmethods,connectome_folder,filetosaveprefix,parc,suffix):
    
    newcorrs = spectral_connectivity_epochs2(newlabel_ts, altsubsections, method=conmethods, mode='multitaper', sfreq=sfreq, fmin=fminlist,fmax=fmaxlist, faverage=True, mt_adaptive=True)

    for ssn in range(len(altsubsections)):
        subsection = altsubsections[ssn]
        
        for cn in range(len(conmethods)):  
            conmethod = conmethods[cn]
            
            for fn in range(len(fbands)):
                fband = fbands[fn]
                
                fmin = fband[0]
                fmax = fband[1]
                
                filetosave = connectome_folder + filetosaveprefix + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_' + str(subsection) + 'e_' + suffix + '.csv'
                
                corr = newcorrs[ssn][cn][fn]
                
                conmatdf = pd.DataFrame(data=corr)
                conmatdf.index = label_names
                conmatdf.columns = label_names
                conmatdf.to_csv(filetosave)  


#how to make envelope correlation connectomes
def make_connect_ec(newlabel_ts,altsubsections,fminlist,fmaxlist,sfreq,conmethods,connectome_folder,filetosaveprefix,parc,suffix):

    for fn in range(len(fminlist)):
        fmin = fminlist[fn]
        fmax = fmaxlist[fn]

        conmethod = 'ecpwo'          
        corr_obj = envelope_correlation(bp_gen(newlabel_ts,fmin,fmax), orthogonalize="pairwise")
        corr = corr_obj.get_data(output="dense")[:, :, :, 0]  
       
        for subsection in altsubsections:

            filetosave = connectome_folder + filetosaveprefix + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_' + str(subsection) + 'e_' + suffix + '.csv'
            
            subcorr = corr[:subsection]
            corrnew = subcorr.mean(axis=0)
            
            conmatdf = pd.DataFrame(data=corrnew)
            conmatdf.index = label_names
            conmatdf.columns = label_names
            conmatdf.to_csv(filetosave)              
            

        conmethod = 'ecso'
        
        label_ts_orth = mne_connectivity.envelope.symmetric_orth(newlabel_ts)
        corr_obj = envelope_correlation(bp_gen(label_ts_orth,fmin,fmax), orthogonalize=False)
        corr = corr_obj.get_data(output="dense")[:, :, :, 0]  
       
        for subsection in altsubsections:

            filetosave = connectome_folder + filetosaveprefix + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_' + str(subsection) + 'e_' + suffix + '.csv'
            
            subcorr = corr[:subsection]
            corrnew = subcorr.mean(axis=0)
            
            corrnew.flat[:: corrnew.shape[0] + 1] = 0  # zero out the diagonal
            corrnew = np.abs(corrnew)  
            
            conmatdf = pd.DataFrame(data=corrnew)
            conmatdf.index = label_names
            conmatdf.columns = label_names
            conmatdf.to_csv(filetosave)  


#psi connectomes
def make_connect_psi(newlabel_ts,altsubsections,fminlist,fmaxlist,sfreq,connectome_folder,filetosaveprefix,parc,suffix):
    
    newcorrs = phase_slope_index2(newlabel_ts, altsubsections, sfreq=sfreq, fmin=fminlist,fmax=fmaxlist, mode='multitaper', mt_adaptive=True)

    conmethod = 'psi'

    for ssn in range(len(altsubsections)):
        subsection = altsubsections[ssn]
        newcorr = newcorrs[ssn]
        
        for fn in range(len(fbands)):
            fband = fbands[fn]
            
            fmin = fband[0]
            fmax = fband[1]
            
            filetosave = connectome_folder + filetosaveprefix + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_' + str(subsection) + 'e_' + suffix + '.csv'
            
            corr = newcorr.get_data(output='dense')[:, :, fn]  
            
            conmatdf = pd.DataFrame(data=corr)
            conmatdf.index = label_names
            conmatdf.columns = label_names
            conmatdf.to_csv(filetosave) 

            



for parc in parclist:

    for family in families:
        strnum = str(family)
        if len(strnum) == 1:
            strnum = '0' + strnum
        strfam = 'sub-19730' + strnum
    
        for page in participant_ages:
            starttime = time.time()    
            strper = strfam + str(page)
            personfolder = dir_start + strper + '/'
            personfolder_output = dir_start_output + strper + '/'



            if page == 'P':
                altpage = 'C'
            else:
                altpage = 'P'
    
            altstrper = strfam + str(altpage)
            altpersonfolder = dir_start + altstrper + '/'    

            label_ts_list = []
            namelist = [] 
            altagetasklist = []
            altagetasklist12 = []
            altagetasklist34 = []
            
            shorttasklist = []
            sessiontasklist = []
            
            proceed = True


            #this first big hunk of code checks the existence of files in the participant's family member
            #so if it's the kid, what files does their parent have?

            if not os.path.exists(altpersonfolder):
                print("This folder doesn't exist: " + altpersonfolder)
                
            else:
            
                print("Checking files for: " + altstrper)
                
                altprefixed = [filename for filename in os.listdir(subjects_dir) if filename.startswith(altstrper)]
        
                personfolder2 = subjects_dir + '/' + altprefixed[0]
                subject = altprefixed[0]
                                    
                for session in sessions:
                    input_data_folder = altpersonfolder + 'ses-' + str(session) + '/eeg/'
                    
                    for task in tasks:
                        raw_data_file_sub = altstrper + '_ses-' + str(session) + '_task-' + task
                        
                        if os.path.exists(input_data_folder):
                            altprefixed = [filename for filename in os.listdir(input_data_folder) if filename.startswith(raw_data_file_sub)]
                        else:
                            altprefixed = []
                        
                        if len(altprefixed) == 0:
                            print("There are no files starting with: " + raw_data_file_sub)
                        
                        else:
                            fullfile = [filename for filename in altprefixed if filename.endswith('remontage_epo.fif')]
                            fwdfile = [filename for filename in altprefixed if filename.endswith('fwd.fif')]
                        
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

                                        altagetask = filetosaveprefix.split('task-')[1]
                                        altagetasklist.append(altagetask)
                                        
                                        if session == 1 or session == 2:
                                            altagetasklist12.append(altagetask)
                                            
                                        if session == 3 or session == 4:
                                            altagetasklist34.append(altagetask)
                                        
                                        




            #this program is ridiculously unoptimal. Probably because I made it over a year after I finished my PhD and I took every shortcut I could
            #so it's probably based off of some other program I made, but I don't remember
            
            #anyway, let's go through all the files for this participant... even if their family member does not have the requisite files
            #this hunk of code will generate the time course data for each parcel of the parcellation for each recording

           
            prefixed = [filename for filename in os.listdir(subjects_dir) if filename.startswith(strper)]
    
            subject = prefixed[0]
                        
            
            connectome_folder = personfolder_output + 'connectomes_combined_1124/' + parc + '/'

            if not os.path.exists(connectome_folder):
                os.makedirs(connectome_folder)              
            
            
            if len(prefixed) != 1:
                print('Uh oh, problem with structural data, either 0 or multiple structural files for participant')
                
            else:
                
                if not os.path.exists(personfolder):
                    print("This folder doesn't exist: " + personfolder)
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
                                    
                                    outputfiletosaveprefix = strper + '_combined_'
                                    outputfiles = [filename for filename in os.listdir(connectome_folder) if filename.startswith(outputfiletosaveprefix)]
                                    
    
                                    if len(outputfiles) > 0 and replacer == False:
                                        print("Output files already exist starting with: " + outputfiletosaveprefix)
                                        proceed = False
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
                                                    #if anyone actually reads this comment, message Kirk. I'll buy you a caramel machiatto from Starbucks, or w/e equivalent value thing you like. Well, I'll consider doing that
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
                                                
                                                agetask = filetosaveprefix.split('task-')[1]
                                                shorttasklist.append(agetask)
                                                sessiontasklist.append(session)
            


            if proceed:

                #figure out how many files overlap between parent and child
                #should have done that before the time consuming process of generating the time courses for our participant
                filetosaveprefix = strper + '_combined_'

                overlap_label_ts_list = []
                for fn in range(len(shorttasklist)):
                    agetask = shorttasklist[fn]
                    session = sessiontasklist[fn]
                    filenamehere = namelist[fn]
                    label_tsx = label_ts_list[fn]
    
                    if agetask in altagetasklist:
                        overlap_label_ts_list.append(label_tsx)
                                
                numrecs = len(overlap_label_ts_list)
                
                


                overlap_label_ts_list12 = []
                for fn in range(len(shorttasklist)):
                    agetask = shorttasklist[fn]
                    session = sessiontasklist[fn]
                    filenamehere = namelist[fn]
                    label_tsx = label_ts_list[fn]
                    
                    if session == 1 or session == 2:
    
                        if agetask in altagetasklist12:
                            overlap_label_ts_list12.append(label_tsx)
                     
                numrecs12 = len(overlap_label_ts_list12)
                
                

                overlap_label_ts_list34 = []
                for fn in range(len(shorttasklist)):
                    agetask = shorttasklist[fn]
                    session = sessiontasklist[fn]
                    filenamehere = namelist[fn]
                    label_tsx = label_ts_list[fn]
                    
                    if session == 3 or session == 4:
    
                        if agetask in altagetasklist34:
                            overlap_label_ts_list34.append(label_tsx)
                     
                numrecs34 = len(overlap_label_ts_list34)
                

                

                
    
                #age effect - subsections if 11 overlapping files
                #if dont have all the necessary files, don't run
                if numrecs == 11 and numrecs12 == 5 and numrecs34 == 5:

                    suffix = 'agematch12'
                    
                    altsubsections = [x * numrecs12 for x in subsections]
                    
                    adjsubsections = [0] + subsections
                    newlabel_ts = []
                    for sn in range(len(subsections)):
                        d1 = adjsubsections[sn]
                        d2 = adjsubsections[sn+1]               
                    
                        for fn in range(numrecs12):
                            subdata = overlap_label_ts_list12[fn][d1:d2]
                            newlabel_ts = newlabel_ts + subdata
                            
    
                    make_connect_classic(newlabel_ts,altsubsections,fminlist,fmaxlist,sfreq,conmethods,connectome_folder,filetosaveprefix,parc,suffix)                               
                    make_connect_ec(newlabel_ts,altsubsections,fminlist,fmaxlist,sfreq,conmethods,connectome_folder,filetosaveprefix,parc,suffix)
                    make_connect_psi(newlabel_ts,altsubsections,fminlist,fmaxlist,sfreq,connectome_folder,filetosaveprefix,parc,suffix)
                    
                    
                    
                    suffix = 'agematch34'
                    
                    altsubsections = [x * numrecs34 for x in subsections]
                    
                    adjsubsections = [0] + subsections
                    newlabel_ts = []
                    for sn in range(len(subsections)):
                        d1 = adjsubsections[sn]
                        d2 = adjsubsections[sn+1]               
                    
                        for fn in range(numrecs34):
                            subdata = overlap_label_ts_list34[fn][d1:d2]
                            newlabel_ts = newlabel_ts + subdata
                            
    
                    make_connect_classic(newlabel_ts,altsubsections,fminlist,fmaxlist,sfreq,conmethods,connectome_folder,filetosaveprefix,parc,suffix)                               
                    make_connect_ec(newlabel_ts,altsubsections,fminlist,fmaxlist,sfreq,conmethods,connectome_folder,filetosaveprefix,parc,suffix)
                    make_connect_psi(newlabel_ts,altsubsections,fminlist,fmaxlist,sfreq,connectome_folder,filetosaveprefix,parc,suffix)                    



    
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
    




















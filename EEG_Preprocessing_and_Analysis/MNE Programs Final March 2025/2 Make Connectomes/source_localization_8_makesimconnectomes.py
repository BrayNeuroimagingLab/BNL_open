

#this program makes simulated connectomes based entirely on random signals, using participants' structural data
#it will generate a random signal of length n (default 20 s), use that to create n/2 epochs worth of random data. This is done for each region on the aparc parcellation
#Then the forward solution is used to apply this data back to the electrodes, then the reverse solution is used to project back to regions
#this connectomes are generated
#this is repeated as many times as you like, default 10



import numpy as np
import mne
import pandas as pd
import os
import time

from mne.minimum_norm import make_inverse_operator, apply_inverse_epochs
from mne_connectivity import spectral_connectivity_epochs
from mne_connectivity import phase_slope_index
from mne_connectivity import envelope_correlation
import mne_connectivity
import random


#folder with all the participant folders and EEG outputs
dir_start = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/prepro1/'

#where is structural data saved. There should be one structural file per participant
subjects_dir = '/Users/ivy/Desktop/Graff_EEG_stuff/ZPrecise2_MRI_fixed_rename_FS'


#write over files if they already exist? If yes, replacer = True. Or ignore them?
replacer = True


#random connectomes can be made in batches
randmax = 10 #how many random connectomes to make
lengthseries = 20 #seconds, must be multiple of 2
namestart = 0 #use 0 if just starting out. This is added to the number when determining the name. Useful if running batches
#e.g. if namestart = 50 and randmax = 25, it'll make random connectomes from n = 51 to n = 75


#parcellation
parc = 'aparc'


#which frequency bands to generate connectomes for
fbands = [[8.0,13.0],[13.0,30.0],[2.5,45.0]]




#which file(s) do you want to look at?
families = list(range(2,27))
participant_ages = ['C','P']
sessions = [1,2,3,4,'4x']
tasks = ['DORA','YT','RX']



#source localization method
method = "eLORETA"
snr = 3.0



#con methods to make simulated connectomes for
#this program will also always make random connectomes for ecso, ecpwo, and psi
#so no real point removing anything from this list
conmethods = ['pli','wpli','imcoh','coh','plv','ciplv']




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


#since epoch length = 2, num epochs is half the length of the series
numepochseach = int(lengthseries/2)
intervals = [0]
for rn in range(randmax):
    intervals.append(int((1+rn)*numepochseach))


fminlist = ()
fmaxlist = ()
for fband in fbands:
    fminlist = fminlist + (fband[0],)
    fmaxlist = fmaxlist + (fband[1],)  



def bp_gen(label_ts,fmin,fmax):
    """Make a generator that band-passes on the fly."""
    for ts in label_ts:
        yield mne.filter.filter_data(ts, sfreq, fmin, fmax)

    
for family in families:
    strnum = str(family)
    if len(strnum) == 1:
        strnum = '0' + strnum
    strfam = 'sub-19730' + strnum

    for page in participant_ages:
        strper = strfam + str(page)
        
        subject_struc = ''
        
        for subject in subjectlist:
            if strper in subject:
                subject_struc = subject
                
        
        
        personfolder = dir_start + strper + '/'
        


        for session in sessions:
            output_data_folder = personfolder + 'ses-' + str(session) + '/eeg/'
            connectome_folder = personfolder + 'ses-' + str(session) + '/connectomes_simulated_0624/' + parc + '/'
            
            if not os.path.exists(connectome_folder):
                os.makedirs(connectome_folder)  
            
            for task in tasks:
                              
                starttime = time.time()   
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
                        
                        filetosaveprefix = fullfile[0].split('eeg_')[0]
                        
                        
                        folderhere = connectome_folder + filetosaveprefix[:-1] + '/'
                        if not os.path.exists(folderhere):
                            os.makedirs(folderhere)   
 
 
                        filetoload = output_data_folder + raw_data_file
                        test_name = filetoload[:-7] + 'remontage_epo.fif'
                        
                        test_fwd = filetoload[:-7] + 'lol-fwd.fif'
                        
                        if os.path.isfile(test_fwd) and os.path.isfile(test_name):
                            print("Output files exist for " + strper)
                        
                            randcount = namestart + randmax

                            efband = fbands[-1]
                            econmethod = 'ecso'

                            fmin = efband[0]
                            fmax = efband[1]
                                        
                            filetosave = folderhere + 'simulated_' + filetosaveprefix + parc + '_' + econmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_rand' + str(randcount) + '.csv'
                            
                            if os.path.isfile(filetosave) and replacer == False:
                                print('Already exists:',filetosave)

                            
                            else:
                                info = mne.io.read_info(test_name).copy()
                                sfreq = info['sfreq']
                                tstep = 1.0 / info['sfreq']
                                
                                print("")
                                print("")
                                print("")
                                print("For",raw_data_file_sub,", reading the fwd solution")
                                fwd = mne.read_forward_solution(test_fwd)
                                src = fwd['src']
                                
                                
                                freqs = np.arange(1, 60, 0.1)
                                
                                    
                                #create fake time series for each region, randmax number of times
                                faketimeseries = []
                                for roi1 in range(len(label_names)):
                                    print("For",raw_data_file_sub,", making fake data for ROI",roi1+1,"of 68") 
                                    
                                    t = np.arange(0,lengthseries,tstep)
                                
                                    source_time_series_total = []
                                    
                                    for randnum in range(randmax):
                                                                    
                                        source_time_series1 = np.array([0]*len(t))
                                        
                                        for sinfreq in freqs:
                                            
                                            amplitude = random.random()
                                            phaseshift = random.random()*np.pi*2
                                            
                                            source_time_series = np.sin(2.0 * np.pi * sinfreq * t - phaseshift) * 10e-9 * amplitude
                                            
                                            source_time_series1 = source_time_series1 + source_time_series
                                            
                                        source_time_series_total = np.concatenate([source_time_series_total, source_time_series1])
                                    
                                        
                                    faketimeseries.append(source_time_series_total)                                
                                
                                    
                                                                
                                events = np.array([[0,0,1]])
                                
                                parceldatalist = []
                                parceldatalabel = []
                                
                                

                                print("")
                                print("For",raw_data_file_sub,", applying fake data to a simulated source")
                                print("")
                                source_simulator = mne.simulation.SourceSimulator(src, tstep=tstep)
                                
                                #apply fake time series data to ROIs
                                for rn in range(len(label_names)):
                                    roi1 = label_names[rn]
                                    
                                    #the signal is projected out from the center 50 mm, which should cover the whole region
                                    location = "center"  # Use the center of the region as a seed.
                                    extent = 50
                                
                                    #will not grow beyond the boundary
                                    selected_label = mne.read_labels_from_annot(subject_struc, regexp=roi1, subjects_dir=subjects_dir,verbose='WARNING')[0]
                                    label1 = mne.label.select_sources(subject_struc, selected_label, location=location, extent=extent, subjects_dir=subjects_dir,grow_outside=False)
                                    
                                    source_time_series1 = faketimeseries[rn]
                                    source_simulator.add_data(label1, source_time_series1, events)
                                
                                
                                #project back to electrodes, add random noise
                                raw = mne.simulation.simulate_raw(info, source_simulator, forward=fwd)
                                cov = mne.make_ad_hoc_cov(raw.info)
                                mne.simulation.add_noise(raw, cov, iir_filter=[0.2, -0.2, 0.04],random_state=42)
                                
                                
                                print("")
                                print("")
                                print("")
                                print("For",raw_data_file_sub,", creating inverse solution")      
                                print("")
                                print("")
                                print("")                                
                                epochsadj = mne.make_fixed_length_epochs(raw,duration=2.0,preload=True)
                                
                                
                                noise_cov = mne.make_ad_hoc_cov(epochsadj.info)
                                
                                #project back to source space
                                
                                #inverse operator
                                inverse_operator = make_inverse_operator(info=epochsadj.info, forward=fwd, noise_cov=noise_cov, depth=3.5)
                                
                                
                                #compute inverse solution
                                
                                lambda2 = 1. / snr ** 2
                                #stcs = apply_inverse_epochs(epochsadj, inverse_operator, lambda2, method,pick_ori="normal", nave=len(epochsadj))
                                stcs = apply_inverse_epochs(epochsadj, inverse_operator, lambda2, method)
                                
                                print("")
                                print("")
                                print("")
                                print("")
                                print("For",raw_data_file_sub,", parcellating")
                                print("")
                                print("")
                                print("")
                                print("")
                                
                                
                                #read labels from the freesurfer outputs
                                labels_parc = mne.read_labels_from_annot(subject_struc, parc=parc,subjects_dir=subjects_dir)
                                
                                label_names = [label.name for label in labels_parc]
                                
                                
                                label_ts = mne.extract_label_time_course(stcs=stcs, labels=labels_parc, src=inverse_operator['src'], mode='pca_flip')

                                
                                #for however many randomizations done, create connectomes
                                for rn in range(randmax):
                                    starte = intervals[rn]
                                    ende = intervals[rn+1]
                                    sublabel_ts = label_ts[starte:ende]
                                    randcount = rn + 1 + namestart

                                    con = spectral_connectivity_epochs(sublabel_ts, method=conmethods, mode='multitaper', sfreq=sfreq, fmin=fminlist,fmax=fmaxlist, faverage=True, mt_adaptive=True)
                                    
                                    for cn in range(len(conmethods)):  
                                        conmethod = conmethods[cn]
                                        conhere = con[cn]
                                        
                                        for fn in range(len(fbands)):
                                            fband = fbands[fn]
                                            
                                            fmin = fband[0]
                                            fmax = fband[1]
                                            
                                            filetosave = folderhere + 'simulated_' + filetosaveprefix + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_rand' + str(randcount) + '.csv'
                                                                                
                                            conmat = conhere.get_data(output='dense')[:, :, fn]

                                            conmatdf = pd.DataFrame(data=conmat)
                                            conmatdf.index = label_names
                                            conmatdf = conmatdf.set_axis(label_names, axis=1)
                                            conmatdf.to_csv(filetosave)                            



                                    psi = phase_slope_index(sublabel_ts,sfreq=sfreq,fmin=fminlist, fmax=fmaxlist,mt_adaptive=True)
                                    
                                    for fn in range(len(fbands)):
                                        fband = fbands[fn]
                                        
                                        fmin = fband[0]
                                        fmax = fband[1]
                                        
                                        conmethod = 'psi'
                                        filetosave = folderhere + 'simulated_' + filetosaveprefix + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_rand' + str(randcount) + '.csv'
                                                                            
                                        conmat = psi.get_data(output='dense')[:, :, fn]

                                        conmatdf = pd.DataFrame(data=conmat)
                                        conmatdf.index = label_names
                                        conmatdf = conmatdf.set_axis(label_names, axis=1)
                                        conmatdf.to_csv(filetosave)                                      



                                    for fn in range(len(fminlist)):
                                        fmin = fminlist[fn]
                                        fmax = fmaxlist[fn]
                                
                                        conmethod = 'ecpwo'          
                                        corr_obj = envelope_correlation(bp_gen(sublabel_ts,fmin,fmax), orthogonalize="pairwise")
                                        corr = corr_obj.combine()
                                        corr = corr.get_data(output="dense")[:, :, 0]  
                                       
                                        filetosave = folderhere + 'simulated_' + filetosaveprefix + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_rand' + str(randcount) + '.csv'
                                         
                                        conmatdf = pd.DataFrame(data=corr)
                                        conmatdf.index = label_names
                                        conmatdf.columns = label_names
                                        conmatdf.to_csv(filetosave)              
                                            
                                
                                
                                        conmethod = 'ecso'
                                        
                                        label_ts_orth = mne_connectivity.envelope.symmetric_orth(sublabel_ts)
                                        corr_obj = envelope_correlation(bp_gen(label_ts_orth,fmin,fmax), orthogonalize=False)
                                        corr2 = corr_obj.combine()
                                        corr2 = corr2.get_data(output="dense")[:, :, 0]
                                        corr2.flat[:: corr2.shape[0] + 1] = 0  # zero out the diagonal
                                        corr = np.abs(corr2)   
                                       
                                        filetosave = folderhere + 'simulated_' + filetosaveprefix + parc + '_' + conmethod + '_' + str(fmin) + 'Hz-' + str(fmax) + 'Hz_rand' + str(randcount) + '.csv'
                                        
                                        conmatdf = pd.DataFrame(data=corr)
                                        conmatdf.index = label_names
                                        conmatdf.columns = label_names
                                        conmatdf.to_csv(filetosave)                                           
                                     


                                endtime = time.time()
                                timepassed = endtime-starttime
                                timepassed_min = str(round(timepassed/60,2))
                                
                                print("")
                                print("")
                                print("Done for " + folderhere)   
                                print("Done for " + folderhere)    
                                print("Time passed for this file = " + timepassed_min + ' min')
                                print("")
                                print("")                 
                            
                        
                        
































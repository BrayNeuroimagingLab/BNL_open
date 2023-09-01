#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v7 tracks the random state
"""

import os
import shutil

import mne
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import transforms
import matplotlib.patches as patches
from matplotlib.colors import Normalize
#%matplotlib inline

from mne_icalabel import label_components
import mne_icalabel




#folder with all the participant folders
dir_start = '/Users/ivy/Desktop/Test_EEG/Test_EEG_BIDS/'

#folder where outputs are saved to
output_dir = '/Users/ivy/Desktop/Test_EEG/Test_EEG_output/'


#logbook name
logname = 'badICdata.txt'


#bad channels file
badch = '/Users/ivy/Desktop/Test_EEG/testbadch.csv'






#which file(s) do you want to look at?
families = [2,3,5,6,7,8,9,10,11,12,13,14,16,18]
participant_ages = ['C','P']
sessions = [1,2,3,4]
tasks = ['DORA','YT','RX']



#these scans will be ignored. Just have nothing in this list if no problem scans
#scans should be written in list like: 'sub-1973007P_ses-1_task-RX2_eeg.raw'
problemscans = []

#ignore all scans except these. Keep this empty if you want to do all scans
#scans should be written in list like: 'sub-1973007P_ses-1_task-RX2_eeg.raw'
onlydothese = []


#bad epoch override. Keep this empty to feed default bad epochs (from badepoch_origdefined) into the ICA algorithm
#if not empty, these are the epochs that will not be fed into the algorithm (cause only good epochs are fed into the algorithm)
#the epochs from badepoch_redefined might be a good choice for bad epoch override
#only do this for one scan at a time!!
badepochoverride = []




#criteria for marking bad epochs. Max and min threshold for good data, and max change in 100 ms
#badchperbadepoch = how many bad channels in a given epoch to say the whole epoch is bad
#badepochperbadch = how many bad epochs in a given bad channel to say the whole channel is bad
#at this point, this is just for quick labelling purposes to give a quick sense of data quality
#bad data isn't deleted or interpolated or anything
#badchperbadepoch is the only one that "matters". Bad epochs aren't fed into the ica
max_threshere = 70
min_threshere = -70
max_changehere = 100
badchperbadepoch = 16
badepochperbadch = 100


#frequency filter
lfreq = 1
hfreq = 45

#downsample frequency
downfreq = 250





#if your specified reference volume file doesn't exist, this creates it
if os.path.isfile(badch) == False:
    refdata = [('test',255)]
    badchdf = pd.DataFrame(data = refdata, columns=['File', 'BadCh'])
    badchdf.to_csv(badch,index=False,header=True)    

#load this to check if bad channel data is available
badchdf = pd.read_csv(badch)
badchdf = badchdf[badchdf['BadCh'] != 'dunno']
files = list(badchdf['File'])
badchlist = list(badchdf['BadCh'])


#what the channel names should be
newnames = ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 
             'E12', 'E13', 'E14', 'E15', 'E16', 'E17', 'E18', 'E19', 'E20', 'E21', 'E22', 
             'E23', 'E24', 'E25', 'E26', 'E27', 'E28', 'E29', 'E30', 'E31', 'E32', 'E33', 
             'E34', 'E35', 'E36', 'E37', 'E38', 'E39', 'E40', 'E41', 'E42', 'E43', 'E44', 
             'E45', 'E46', 'E47', 'E48', 'E49', 'E50', 'E51', 'E52', 'E53', 'E54', 'E55', 
             'E56', 'E57', 'E58', 'E59', 'E60', 'E61', 'E62', 'E63', 'E64']


newnamesorig = newnames.copy()

 
earch = ['E23','E55']
cheekch = ['E61','E62','E63','E64']


#badicauto = '/Users/ivy/Desktop/Test_EEG/badic_automated.csv'
#if os.path.isfile(badicauto) == False:
#    refdata = [('test',255,255,'E255')]
#    badicautodf = pd.DataFrame(data = refdata, columns=['File', 'EyeBadIC','DefaultBadIC','DropTheseElec'])
#    badicautodf.to_csv(badicauto,header=True)   
#badicautodf = pd.read_csv(badicauto,index_col=0)


       
def iccheck(epochs_repaired,badvar):

    picks = mne.pick_types(epochs_repaired.info,eeg=True)
    epoch_data = epochs_repaired.get_data()[:, picks]
    numbad = len(epochs_repaired.info['bads'])

    adjepoch_data = []
    deltas_preica = []
    max_preica = []
    min_preica = []
    
    for epochn in range(len(epoch_data)):
    
        a = []
        adelta = []
        amax = []
        amin = []
        ep = epoch_data[epochn]
        
        for chn in range(len(ep)):
            ch = ep[chn]
            
            if epochn != 0:
                epless = epoch_data[epochn-1]
                chless = epless[chn]
                last100 = chless[-25:]
                
            if epochn != len(epoch_data)-1:
            
                epmore = epoch_data[epochn+1]
                chmore = epmore[chn]
                next100 = chmore[:25]
                
            if epochn == 0:
                adjch = np.concatenate((ch,next100))
                
            elif epochn == len(epoch_data)-1:
                adjch = np.concatenate((last100,ch))    
                
            else:
                adjch = np.concatenate((last100,ch,next100))
            
            a.append(adjch)
            #a.append(ch)
            amax.append(max(adjch))
            amin.append(min(adjch))
            adelta.append(max(adjch)-min(adjch))
    
        adjepoch_data.append(a)
        deltas_preica.append(adelta)
        max_preica.append(amax)
        min_preica.append(amin)
    
        
    deltas_preica = np.asarray(deltas_preica).T
    max_preica = np.asarray(max_preica).T
    min_preica = np.asarray(min_preica).T
    
    deltas_preica = deltas_preica/(1e-6)
    max_preica = max_preica/(1e-6)
    min_preica = min_preica/(1e-6)
    

    max_threshere = badvar[0]
    min_threshere = badvar[1]
    max_changehere = badvar[2]
    badchperbadepoch = badvar[3]-numbad #if we're dropping a channel, that should count against the total bad channels, right?
    badepochperbadch = badvar[4]
    
    
    labels2 = np.zeros((len(epochs_reref), len(epochs_reref.ch_names)))
    labels2.fill(np.nan)
    
    
    #this defaults to labelling as 0 (good), then changes it to 1 if it finds bad
    for ch_idx in range(len(picks)):
        for ep_idx in range(len(epochs_reref)):
            labelval = 0
            delta_max = max_preica[ch_idx][ep_idx]
            if delta_max > max_threshere:
                labelval = 1
            else:
                delta_min = min_preica[ch_idx][ep_idx]
                if delta_min < min_threshere:
                    labelval = 1   
                else:
                    epoch_data_here = adjepoch_data[ep_idx][ch_idx]/(1e-6)
                    #shrink where we need to look for bad data
                    if len(epoch_data_here) == 525:
                        intervalstartz = [0,75,150,225,300,375,425]
                    else:
                        intervalstartz = [0,75,150,225,300,375,450]                        
                    for starting in intervalstartz:
                        if labelval == 0:
                            rangehere = np.ptp(epoch_data_here[starting:starting+100])
                            #get rid of data if the range is too smal
                            if rangehere < 1:
                                labelval = 1

                    if labelval == 0:
                        delta_change = deltas_preica[ch_idx][ep_idx]
                        if delta_change > max_changehere:
                            epoch_data_here = adjepoch_data[ep_idx][ch_idx]/(1e-6)
                            #shrink where we need to look for bad data
                            intervalstartz = [0,75,150,225,300,375,450]
                            badmaybe = []
                            for starting in intervalstartz:
                                rangehere = np.ptp(epoch_data_here[starting:starting+100])
                                if rangehere > max_changehere:
                                    badmaybe.append(starting)
                            for maybestarting in badmaybe:
                                #search for bad data by looking at every 5th spot
                                if labelval == 0:
                                    starting = maybestarting -5
                                    while True:
                                        starting = starting + 5
                                        if starting > len(epoch_data_here)-25:
                                            break
                                        elif starting-maybestarting > 75:
                                            break
                                        else:
                                            rangehere = np.ptp(epoch_data_here[starting:starting+25])
                                            if rangehere > max_changehere:
                                                labelval = 1
                                                break
                                            else:
                                                continue
                            for maybestarting in badmaybe:                                        
                                #if don't find bad data searching every 5th spot... fiiine we'll search every spot!
                                if labelval == 0:
                                     starting = maybestarting -1
                                     while True:
                                         starting = starting + 1
                                         if starting > len(epoch_data_here)-25:
                                             break
                                         elif starting-maybestarting > 75:
                                             break
                                         else:
                                             rangehere = np.ptp(epoch_data_here[starting:starting+25])
                                             if rangehere > max_changehere:
                                                 labelval = 1
                                                 break
                                             else:
                                                 continue                           
                                    
            labels2[ep_idx][picks[ch_idx]] = labelval
    
    
    
    total_bad = np.sum(np.sum(labels2 == 1, axis=0))
    bad_epochs_count = sum(np.sum(labels2 == 1, axis=1)>badchperbadepoch)
    bad_channel_count = sum(np.sum(labels2 == 1, axis=0)>badepochperbadch)       

    return total_bad,bad_epochs_count,bad_channel_count,labels2


raw_data_list = []
numalready = 0

#loop through all potential files and check if they actually exist. If they do, add them to a list
#for preprocessing
#at the same time, add output directories for each file to the list, and check if preprocessing
#has already occurred
for family in families:
    strnum = str(family)
    if len(strnum) == 1:
        strnum = '0' + strnum
    strfam = 'sub-19730' + strnum

    for page in participant_ages:
        strper = strfam + str(page)
        personfolder = dir_start + strper + '/'
        personfolderoutput = output_dir + strper + '/'
        
        if not os.path.exists(personfolder):
            print("This folder doesn't exist: " + personfolder)
        else:
        
            for session in sessions:
                raw_data_folder = personfolder + 'ses-' + str(session) + '/eeg/'
                output_data_folder = personfolderoutput + 'ses-' + str(session) + '/eeg/'
                
                for task in tasks:
                    raw_data_file_sub = strper + '_ses-' + str(session) + '_task-' + task
                    
                    if os.path.exists(raw_data_folder):
                        prefixed = [filename for filename in os.listdir(raw_data_folder) if filename.startswith(raw_data_file_sub)]
                    else:
                        prefixed = []
                    
                    if len(prefixed) == 0:
                        print("There are no files starting with: " + raw_data_file_sub)
                    
                    else:
                        fullfile = [filename for filename in prefixed if filename.endswith('.raw')]
                        
                        if len(fullfile) > 1:
                            print("There are multiple files that exist of the same task:")
                            for val in fullfile:
                                print(val)
                            print("For now, ignoring all of them")
                        elif len(fullfile) == 0:
                            print("There are no files starting with: " + raw_data_file_sub)
                        else:
                            raw_data_file = fullfile[0]
                                                    
                            if not raw_data_file in files:
                                print("There is no bad channel data for " + raw_data_file)
                                
                            elif raw_data_file in problemscans:
                                print(raw_data_file + ' is potentially problematic. Let us ignore it!')
                                
                            else:
                        
                                output_data_folder_task = output_data_folder + raw_data_file[:-4] + '/ICAplots_v3/'
                                output_ch_data = output_data_folder_task + logname
                                output_epoch_folder_task = output_data_folder + raw_data_file[:-4] + '/epochplots/'
                                
                                if os.path.isfile(output_ch_data):
                                    alreadyprocessed = 'y'
                                    numalready = numalready + 1
                                else:
                                    alreadyprocessed = 'n'
    
    
                                if len(onlydothese) > 0:
                                    if raw_data_file in onlydothese:
                                        
                                        persdata = [raw_data_folder,raw_data_file,output_data_folder,output_data_folder_task,output_epoch_folder_task,alreadyprocessed]
                                        raw_data_list.append(persdata)
                                else:
                                    
                                    persdata = [raw_data_folder,raw_data_file,output_data_folder,output_data_folder_task,output_epoch_folder_task,alreadyprocessed]
                                    raw_data_list.append(persdata)   

                            
                            
#ask if you want to preprocess based on how many files exist
#ask to delete files that already exist, and ask to overwrite / add to files that already exist
proceed = False   
deleteold = False
replaceold = False 
alreadydone = False                
if len(raw_data_list) == 0:
    print("There are no files to preprocess")
else:
    print("")
    numfiles = len(raw_data_list)
    print("You have selected " + str(numfiles) + " files to potentially generate data.")
    print(str(numalready) + " files already have existing data.")
    if numfiles == 0:
        print("You don't need to preprocess, apparently!")
        alreadydone = True        
    print("")
    
    if numalready > 0:  #if there aren't already existing files, no point to ask to delete/replace old
        while True:
            print("Delete old data? This cannot be undone, and goes into effect instantly.")
            val = input("(y/n): ")
            if val == 'y' or val == 'n':
                if val == 'y':
                    deleteold = True
                break
            else:
                print("Did not understand input.")
                print("")
                continue

        if deleteold == False:
            while True:
                print("Overwrite / add to old data?")
                print("If no, will only generate data for files with no data.")
                val = input("(y/n): ")
                if val == 'y' or val == 'n':
                    if val == 'y':
                        replaceold = True
                    break
                else:
                    print("Did not understand input.")
                    print("")
                    continue        

        #if we're deleting data, carry out this code
        else:
            for dirinfo in raw_data_list:
                if 'y' in dirinfo:
                    icaplotfolder = dirinfo[3]
                    #epochplotfolder = dirinfo[4]
                    
                    contents = os.listdir(icaplotfolder)
                    actuallydel = True
                    for rawfile in contents:
                        if rawfile.endswith(".raw"):
                            print("Uh oh. Looks like there are valuables saved in: " + icaplotfolder)
                            print("You shouldn't see this error message unless you did something weird to the data")
                            actuallydel = False
                    if actuallydel:
                        shutil.rmtree(icaplotfolder)
                        #since we've deleted data, remove 'y' and add 'n', since we no longer have existing data
                        dirinfo.remove('y')
                        dirinfo.append('n')


        #check how many files exist after potentially deleting files
        newnumalready = 0
        for dirinfo in raw_data_list:        
            if 'y' in dirinfo:
                newnumalready = newnumalready + 1
        
        if replaceold == False:
            filestogen = numfiles - newnumalready
            print("")
            print("You have selected " + str(filestogen) + " files to generate data.")
            print(str(newnumalready) + " files already have existing data and are being ignored.")  
            if filestogen == 0:
                print("You don't need to preprocess! You're done!")
                alreadydone = True
        else:
            print("")
            print("You have selected " + str(numfiles) + " files to generate data.")
            print(str(newnumalready) + " files already have existing data and are being overwritten / added to.")               
    
    #maybe the list is too long. Give the user a chance to not proceed!
    if not alreadydone:       
        while True:
            print("Proceed with all?")
            val = input("(y/n): ")
            if val == 'y' or val == 'n':
                if val == 'y':
                    proceed = True
                break
            else:
                print("Did not understand input.")
                print("")
                continue


if proceed:
    
    #loop through each participant
    for dirinfo in raw_data_list: 
        if not('y' in dirinfo and replaceold == False):
            
            proceed2 = True
            susnames = False
        
            raw_data_folder = dirinfo[0]
            raw_data_file = dirinfo[1]
            output_data_folder = dirinfo[2]
                  
                
            #make a folder for saving outputs    
            icadir = dirinfo[3]
            if not os.path.exists(icadir):
                os.makedirs(icadir)

            chdatabe = output_data_folder + raw_data_file[:-4] + '/channelplots/badepoch_channel_data.txt'          

            print("Generating data for " + raw_data_file)


            #file name
            rawfile = raw_data_folder + raw_data_file                
                 
            #load the raw file
            raw = mne.io.read_raw_egi(rawfile,preload=True)
        
            #check channel names and set channel locations
            curchnames = raw.info.ch_names
            
            if curchnames == newnamesorig + ['E65']:         
                raw_y = raw.copy().rename_channels({'E65':'Cz'})
                raw_y = raw_y.set_montage('GSN-HydroCel-65_1.0')
                print("Your channel names look fine.")
            
            elif curchnames == newnamesorig + ['E65', 'IEND', 'STI 014']:  
                raw_y = raw.copy().rename_channels({'E65':'Cz'})
                raw_y = raw_y.set_montage('GSN-HydroCel-65_1.0')
                raw_y = raw_y.drop_channels(['IEND', 'STI 014'])
                print("Your channel names look sus, but we'll try our best here.")       
                susnames = True

            elif curchnames == newnames + ['E65', 'IBEG', 'IEND', 'STI 014']:  
                raw_y = raw.copy().rename_channels({'E65':'Cz'})
                raw_y = raw_y.set_montage('GSN-HydroCel-65_1.0')
                raw_y = raw_y.drop_channels(['IBEG', 'IEND', 'STI 014'])
                print("Your channel names look sus, but we'll try our best here.")       
                susnames = True   
            
            else:                
                print("Uh oh. Your names are messed up for " + raw_data_file)
                proceed2 = False
                
            #add the reference to names
            newnames = newnamesorig + ['Cz']

                
            if proceed2:


                indexval = files.index(raw_data_file)
                print(raw_data_file + " has bad channel data.\nBad channels = " + badchlist[indexval])
                print("")
                badchannelstemp = badchlist[indexval]
                if badchannelstemp == 'none':
                    badchannels = []
                else:
                    badchannels = badchannelstemp.split(',')
                
                raw_y.info['bads'] = badchannels
                
                #origfreq = raw_y.info['sfreq']

                #notch filter at 60 Hz + multiples, bandpass filter, downsample      
                freqs = (60,120,180,240,300,360,420,480)
                raw_notch = raw_y.copy().notch_filter(freqs=freqs)                    
                raw_filter = raw_notch.copy().filter(l_freq=lfreq, h_freq=hfreq)   
                raw_downsampled = raw_filter.copy().resample(sfreq=downfreq)
            
                sampling_freq = raw_downsampled.info['sfreq']


                log = []
                log.append("ICA data for: ")
                log.append(raw_data_folder)
                log.append(raw_data_file)
                log.append('')
                log.append('Saved to: ')
                log.append(icadir)
                log.append('')
                
                log.append("Channels marked as bad:")
                log.append(badchlist[indexval])
                log.append('')

                log.append('Downsampled to: ' + str(downfreq) + ' Hz')
                log.append('Bandpass filtered at: ' + str(lfreq) + ' to ' + str(hfreq) + ' Hz')
                log.append('')
                
                if 'y' in dirinfo:
                    log.append('This replaced / added to old data. There could be files from the last time this ran')
                    log.append('')
                    
                if susnames:
                    log.append('Weird channel names: The raw scan has stim channels or something, and that is weird')
                else:
                    log.append('Your channel names look fine')
                log.append('')      
                    
                    
                #epoch the data
                epochs = mne.make_fixed_length_epochs(raw_downsampled,duration=2.0,preload=True)
                
                #drop the ends, cause they're sus
                epochs_endadj = epochs.copy()
                epochs_endadj.drop([0,len(epochs_endadj)-1])
                
                
                #bad epochs, based off of the channel data previously generated
                chdatabe_data = np.loadtxt(chdatabe)
                
                #for all bad channels specified, refer to this data as all bad epochs
                for badchan in badchannels:
                    chnum = newnames.index(badchan)
                    chdatabe_data[chnum] = [1]*len(chdatabe_data[chnum])
                
                #dropping the first and last epoch, cause they're sus
                altchdatabe_data = chdatabe_data.T[1:-1].T
                
                altbadepoch = []
                for epn in range(len(altchdatabe_data.T)):
                    ep = altchdatabe_data.T[epn]
                    #if more than 16 channels are "bad" (or whatever # specified above), then it's a bad epoch
                    if sum(ep) > badchperbadepoch:
                        altbadepoch.append(epn)
                        
                        
                newbadepoch = np.array([False]*len(epochs_endadj))        
                for qi in altbadepoch:
                    newbadepoch[qi] = True
                    
                badepochsdefault = altbadepoch.copy()

                goodepochs = ~newbadepoch.copy()
                    
                altbadch = []  
                for chn in range(len(altchdatabe_data)):
                    ch = altchdatabe_data[chn]
                    chname = newnames[chn]
                    if sum(ch) > badepochperbadch:
                        altbadch.append(chname)
                        
    
                totalbaddata = int(sum(sum(altchdatabe_data)))
                adjtotalbaddata = totalbaddata - len(goodepochs)*len(badchannels)



                log.append("Based on checking original data")
                log.append(str(len(altbadepoch)) + '/' + str(len(newbadepoch)) + ' epochs are bad')
                log.append('bad epochs are:')
                log.append(altbadepoch)
                log.append("Bad channels are:")
                log.append(altbadch)
                log.append("Total bad data = " + str(totalbaddata))
                log.append("Total bad data not counting pre-specified bad channels = " + str(adjtotalbaddata))
                log.append('') 


                #make figure of bad epochs
                figure, ax = plt.subplots(figsize=(12, 6))
                ch_names_ = newnames[4::5]
                
                image = altchdatabe_data.copy()
                refrow = np.array([[3]*len(image.T)])
                image = np.append(image,refrow,axis=0)

                for badchan in badchannels:
                    chnum = newnames.index(badchan)
                    image[chnum] = [2]*len(image[chnum])
                    
                image = image.T

                
                legend_label = {0: 'good', 1: 'bad', 2: 'predefined bad',3:'ref'}
                cmap = mpl.colors.ListedColormap(['lightgreen', 'red','grey','black'])

                
                img = ax.imshow(image.T, cmap=cmap,vmin=0, vmax=3)
                ax.set_xlabel('Epochs')
                ax.set_ylabel('Channels')
                plt.setp(ax, yticks=range(4, image.shape[1], 5),yticklabels=ch_names_)  
                plt.setp(ax.get_yticklabels(), fontsize=8)
                
                #add white lines to break up channels
                for za in range(len(image.T)):
                    ax.plot([-0.5,len(image)-0.5],[za+0.5,za+0.5], color='white', linestyle='-', linewidth=1)
                
                # add grey box around rejected epochs
                for idx in np.where(newbadepoch[:len(image)])[0]:
                    ax.add_patch(patches.Rectangle(
                        (idx - 0.5, -0.5), 1, len(image.T), linewidth=1,
                        edgecolor='grey', facecolor='none'))
                
                #add grey box around bad channels
                for badchan in altbadch:
                    chnum = newnames.index(badchan)
                    ax.add_patch(patches.Rectangle(
                        (-0.5,chnum-0.5), len(image), 1, linewidth=1,
                        edgecolor='grey', facecolor='none',zorder=10))     
                
                # add legend
                handles = [patches.Patch(color=img.cmap(img.norm(i)), label=label)
                           for i, label in legend_label.items()]
                ax.legend(handles=handles, bbox_to_anchor=(0.5, 1.15), ncol=4,
                          borderaxespad=0.,loc='center')
                
                anntext = 'original (lenient) definition\nbad epochs: ' + str(len(altbadepoch)) + ', bad channels: ' + str(len(altbadch)) + ', total bad data: ' + str(totalbaddata) + ' (not counting predefined bad channels: ' + str(adjtotalbaddata) + ')'
                ax.annotate(anntext,(0.5,1.05),xycoords='axes fraction',ha='center',va='center')
                
                plt.subplots_adjust(top=0.94,left=0.1,bottom=0.2)
                plt.tight_layout()
                plt.savefig(icadir+'badepoch_origdefined.png',dpi=200)
                plt.show()                    
               


                badvar = max_threshere,min_threshere,max_changehere,badchperbadepoch,badepochperbadch
                
                            

                
                #rereference to average, and add back in the reference channel
                epochs_reref = epochs_endadj.copy()                
                epochs_reref = epochs_reref.set_eeg_reference(ref_channels='average', projection=True)
                epochs_reref.apply_proj(verbose=True)
                
           

                #quick estimate of data quality before any ICs removed
                total_bad,bad_epochs_count,bad_channel_count,labels2 = iccheck(epochs_reref,badvar)
                
                origbad = [total_bad,bad_epochs_count,bad_channel_count]
                

                    

                #bad epochs, based off of stats specified here
                newbadepoch = np.array([False]*len(epochs_reref))
                                
                altbadepoch = []
                altchdatabe_data = labels2.T
                
            
                #for all bad channels specified, refer to this data as all bad epochs
                for badchan in badchannels:
                    chnum = newnames.index(badchan)
                    altchdatabe_data[chnum] = [1]*len(altchdatabe_data[chnum])
                
                for epn in range(len(altchdatabe_data.T)):
                    ep = altchdatabe_data.T[epn]
                    #if more than 16 channels are "bad", then it's a bad epoch
                    if sum(ep) > badchperbadepoch:
                        altbadepoch.append(epn)
                for qi in altbadepoch:
                    newbadepoch[qi] = True
                    
                altbadch = []  
                for chn in range(len(altchdatabe_data)):
                    ch = altchdatabe_data[chn]
                    chname = epochs_reref.ch_names[chn]
                    if sum(ch) > badepochperbadch:
                        altbadch.append(chname)
                        
                totalbaddata = int(sum(sum(altchdatabe_data)))
                adjtotalbaddata = totalbaddata - len(goodepochs)*len(badchannels)
 
    

                log.append("Based on criteria selected here:")
                log.append(str(len(altbadepoch)) + '/' + str(len(newbadepoch)) + ' epochs are bad')
                log.append('bad epochs are:')
                log.append(altbadepoch)
                log.append("Bad channels are:")
                log.append(altbadch)
                log.append("Total bad data = " + str(totalbaddata))
                log.append("Total bad data not counting pre-specified bad channels = " + str(adjtotalbaddata))
                log.append('')             
                    

                figure, ax = plt.subplots(figsize=(12, 6))
                ch_names_ = epochs_reref.ch_names[4::5]
                
                image = altchdatabe_data.copy()

                for badchan in badchannels:
                    chnum = newnames.index(badchan)
                    image[chnum] = [2]*len(image[chnum])
                    
                image = image.T

                
                legend_label = {0: 'good', 1: 'bad', 2: 'predefined bad'}
                cmap = mpl.colors.ListedColormap(['lightgreen', 'red','grey'])

                
                img = ax.imshow(image.T, cmap=cmap,vmin=0, vmax=2)
                ax.set_xlabel('Epochs')
                ax.set_ylabel('Channels')
                plt.setp(ax, yticks=range(4, image.shape[1], 5),yticklabels=ch_names_)  
                plt.setp(ax.get_yticklabels(), fontsize=8)
                
                for za in range(len(image.T)):
                    ax.plot([-0.5,len(image)-0.5],[za+0.5,za+0.5], color='white', linestyle='-', linewidth=1)
                
                # add grey box around rejected epochs
                for idx in np.where(newbadepoch[:len(image)])[0]:
                    ax.add_patch(patches.Rectangle(
                        (idx - 0.5, -0.5), 1, len(image.T), linewidth=1,
                        edgecolor='grey', facecolor='none'))
                    
                for badchan in altbadch:
                    chnum = newnames.index(badchan)
                    ax.add_patch(patches.Rectangle(
                        (-0.5,chnum-0.5), len(image), 1, linewidth=1,
                        edgecolor='grey', facecolor='none',zorder=10))     

                # add legend
                handles = [patches.Patch(color=img.cmap(img.norm(i)), label=label)
                           for i, label in legend_label.items()]
                ax.legend(handles=handles, bbox_to_anchor=(0.5, 1.15), ncol=3,
                          borderaxespad=0.,loc='center')
                
                anntext = 'stricter definition\nbad epochs: ' + str(len(altbadepoch)) + ', bad channels: ' + str(len(altbadch)) + ', total bad data: ' + str(totalbaddata) + ' (not counting predefined bad channels: ' + str(adjtotalbaddata) + ')'
                ax.annotate(anntext,(0.5,1.05),xycoords='axes fraction',ha='center',va='center')
                
                
                plt.subplots_adjust(top=0.94,left=0.1,bottom=0.2)
                plt.tight_layout()
                plt.savefig(icadir+'badepoch_redefined.png',dpi=200)
                plt.show()    


                if len(badepochoverride) > 0:
                    newbadepoch2 = np.array([False]*len(epochs_endadj))        
                    for qi in badepochoverride:
                        newbadepoch2[qi] = True
                    goodepochs = ~newbadepoch2.copy()
                    
                    log.append('Overwrote default bad epochs')

                else:
                    log.append('Did not override default bad epochs')
                    
                log.append('These are the bad epochs for the purposes of the ICA algorithm (i.e., epochs ignored):')
                log.append(badepochoverride)
                log.append('')

                goodch = epochs_reref.ch_names.copy()
                for badchan in badchannels:
                    goodch.remove(badchan)
            
                
                #run the ICA, don't feed in bad epochs (as originally defined - so blinks should go in, longer periods of motion, no)
                ica = mne.preprocessing.ICA(random_state=99,max_iter=2000)
                ica.fit(epochs_reref[goodepochs])
                randstate = 99
                numint = ica.n_iter_
                rerun = False
                
                numreruns = 0
                currandstate = 1
                
                while numint == 2000:
                 numreruns = numreruns + 1
                 ica = mne.preprocessing.ICA(random_state=currandstate,max_iter=2000)
                 ica.fit(epochs_reref[goodepochs]) 
                 randstate = currandstate
                 numint = ica.n_iter_    
                 currandstate = currandstate + 1
                 rerun = True
                


                numcomp = ica.n_components_
                numcomptheory = 64 - len(badchannels)
                numcompdiff = numcomptheory - numcomp
                varexporig = sum(ica.pca_explained_variance_[:numcomp])/sum(ica.pca_explained_variance_)


                #get spatial data of components. Which channels contribute to them
                componentz = ica.get_components() 
                componentz = componentz.T  
                
                selfcorrz = abs(pd.DataFrame(data=componentz.T).corr())
                selfcorrz = selfcorrz - np.identity(len(selfcorrz))
                selfcorrztext = []
                
                selfcorrz.to_csv(icadir+'ic_corrs.csv')
                
                
                for iy in range(len(componentz)):
                    iccorr = selfcorrz[iy]
                    iccorrlist = list(iccorr)
                    iccorrlist.sort()
                    top3corrs = iccorrlist[-3:]
                    top3comps = []
                    top3comps.append(iccorr[iccorr == top3corrs[0]].index.values.astype(int)[0])
                    top3comps.append(iccorr[iccorr == top3corrs[1]].index.values.astype(int)[0])
                    top3comps.append(iccorr[iccorr == top3corrs[2]].index.values.astype(int)[0])
                    textcorr = ''
                    for cn in range(len(top3comps)):
                        adjtop3comp = str(top3comps[2-cn])
                        if len(adjtop3comp) == 1:
                            adjtop3comp = '0' + adjtop3comp
                        textcorr = textcorr + adjtop3comp + ' (' + str(round(top3corrs[2-cn],2)) + '), '
                    textcorr = textcorr[:-2]
                    selfcorrztext.append(textcorr)
                                
                    
                #components likely reflecting bad channels
                badchcomps = []
                for iy in range(len(componentz)):
                    compon = componentz[iy]
                    abscomp = abs(compon)
                    abovlow = abscomp > 0.2
                    numabovlow = sum(abovlow)
                    abovmed = abscomp > 0.25
                    numabovmed = sum(abovmed)    
                    maxch = max(abscomp)
                    if maxch > 0.5 and numabovlow < 3 and numabovmed < 2:
                        badchcomps.append(iy)
                    
                for iy in range(len(componentz)):
                    compon = componentz[iy]
                    abscomp = abs(compon)
                    abovlow = abscomp > 0.25
                    numabovlow = sum(abovlow)
                    abovmed = abscomp > 0.3
                    numabovmed = sum(abovmed)    
                    maxch = max(abscomp)
                    if maxch > 0.6 and numabovlow < 3 and numabovmed < 2:
                        badchcomps.append(iy)
                        
                for iy in range(len(componentz)):
                    compon = componentz[iy]
                    abscomp = abs(compon)
                    abovlow = abscomp > 0.075
                    numabovlow = sum(abovlow)
                    abovmed = abscomp > 0.1
                    numabovmed = sum(abovmed)    
                    maxch = max(abscomp)
                    if maxch > 0.35 and numabovlow < 3 and numabovmed < 2:
                        badchcomps.append(iy)                        
                        
 
                badchcomps.sort()

    
                #automatically classify components
                autolabels = label_components(epochs_reref[goodepochs], ica, method='iclabel')
                guesses = autolabels['labels']
                guessstr = list(autolabels['y_pred_proba'])
                
                features = mne_icalabel.iclabel.get_iclabel_features(epochs_reref[goodepochs], ica)
                predictions = mne_icalabel.iclabel.run_iclabel(features[0],features[1],features[2])                
                
                
                #what the automatic guess numbers refer to. First number is probability it's brain, 2nd number muscle, etc etc
                #guesscat = ['Brain', 'Muscle', 'Eye', 'Heart', 'Line Noise', 'Channel Noise','Other']
                            
                
                #generate default bad ICs
                eyebadic = []
                
                for lnum in range(32):
                    brainguess = predictions[lnum][0]
                    eyeguess = predictions[lnum][2]
                    if eyeguess > 0.6:
                        eyebadic.append(lnum)
                    elif eyeguess > 0.4 and brainguess < 0.2:
                        eyebadic.append(lnum)                        
                
                
                
                defaultbadic = []
                for lnum in eyebadic:
                    defaultbadic.append(lnum)                
                
                
             
                
                #badcounts = []
                badcountseye = []
                for ic in range(numcomp):
                    
                    print("Checking component " + str(ic))
                
                    ica.exclude = [ic]
                                                
                    if ic not in eyebadic:
                        ica.exclude = eyebadic + [ic]
                    else:
                        ica.exclude = [xo for xo in eyebadic if xo != ic]
                                               
                    epochs_repaired = epochs_reref.copy()
                    ica.apply(epochs_repaired, exclude=ica.exclude,verbose=False)
                
                    total_bad,bad_epochs_count,bad_channel_count,labels2 = iccheck(epochs_repaired,badvar)
                    badcountseye.append([total_bad,bad_epochs_count,bad_channel_count])


    
                #remove eye bad IC, see what that looks like
                ica.exclude = eyebadic
                                           
                epochs_repaired = epochs_reref.copy()
                ica.apply(epochs_repaired, exclude=ica.exclude,verbose=False)
                
                total_bad,bad_epochs_count,bad_channel_count,labels2 = iccheck(epochs_repaired,badvar)
                
                eyebad = [total_bad,bad_epochs_count,bad_channel_count]
                

                #bad epochs, based off of removing eye blinks
                newbadepoch = np.array([False]*len(epochs_repaired))
                                
                altbadepoch = []
                altchdatabe_data = labels2.T
                
                #for all bad channels specified, refer to this data as all bad epochs
                for badchan in badchannels:
                    chnum = newnames.index(badchan)
                    altchdatabe_data[chnum] = [1]*len(altchdatabe_data[chnum])
                
                for epn in range(len(altchdatabe_data.T)):
                    ep = altchdatabe_data.T[epn]
                    #if more than 16 channels are "bad", then it's a bad epoch
                    if sum(ep) > badchperbadepoch:
                        altbadepoch.append(epn)
                for qi in altbadepoch:
                    newbadepoch[qi] = True
                    
                altbadch = []  
                for chn in range(len(altchdatabe_data)):
                    ch = altchdatabe_data[chn]
                    chname = epochs_reref.ch_names[chn]
                    if sum(ch) > badepochperbadch:
                        altbadch.append(chname)
                        
                totalbaddata = int(sum(sum(altchdatabe_data)))
                adjtotalbaddata = totalbaddata - len(goodepochs)*len(badchannels)


            
                log.append("Removing eye components:")
                log.append(str(len(altbadepoch)) + '/' + str(len(newbadepoch)) + ' epochs are bad')
                log.append('bad epochs are:')
                log.append(altbadepoch)
                log.append("Bad channels are:")
                log.append(altbadch)
                log.append("Total bad data = " + str(totalbaddata))
                log.append("Total bad data not counting pre-specified bad channels = " + str(adjtotalbaddata))
                log.append('')             
                    

                figure, ax = plt.subplots(figsize=(12, 6))
                ch_names_ = epochs_reref.ch_names[4::5]
                
                image = altchdatabe_data.copy()

                for badchan in badchannels:
                    chnum = newnames.index(badchan)
                    image[chnum] = [2]*len(image[chnum])
                    
                image = image.T

                
                legend_label = {0: 'good', 1: 'bad', 2: 'predefined bad'}
                cmap = mpl.colors.ListedColormap(['lightgreen', 'red','grey'])

                
                img = ax.imshow(image.T, cmap=cmap,vmin=0, vmax=2)
                ax.set_xlabel('Epochs')
                ax.set_ylabel('Channels')
                plt.setp(ax, yticks=range(4, image.shape[1], 5),yticklabels=ch_names_)  
                plt.setp(ax.get_yticklabels(), fontsize=8)
                
                for za in range(len(image.T)):
                    ax.plot([-0.5,len(image)-0.5],[za+0.5,za+0.5], color='white', linestyle='-', linewidth=1)
                
                # add grey box around rejected epochs
                for idx in np.where(newbadepoch[:len(image)])[0]:
                    ax.add_patch(patches.Rectangle(
                        (idx - 0.5, -0.5), 1, len(image.T), linewidth=1,
                        edgecolor='grey', facecolor='none'))
                    
                for badchan in altbadch:
                    chnum = newnames.index(badchan)
                    ax.add_patch(patches.Rectangle(
                        (-0.5,chnum-0.5), len(image), 1, linewidth=1,
                        edgecolor='grey', facecolor='none',zorder=10))     

                # add legend
                handles = [patches.Patch(color=img.cmap(img.norm(i)), label=label)
                           for i, label in legend_label.items()]
                ax.legend(handles=handles, bbox_to_anchor=(0.5, 1.15), ncol=3,
                          borderaxespad=0.,loc='center')
                
                anntext = 'drop eye IC ' + str(eyebadic) + '\nbad epochs: ' + str(len(altbadepoch)) + ', bad channels: ' + str(len(altbadch)) + ', total bad data: ' + str(totalbaddata) + ' (not counting predefined bad channels: ' + str(adjtotalbaddata) + ')'
                ax.annotate(anntext,(0.5,1.05),xycoords='axes fraction',ha='center',va='center')
                
                
                plt.subplots_adjust(top=0.94,left=0.1,bottom=0.2)
                plt.tight_layout()
                plt.savefig(icadir+'badepoch_repaired_dropeye.png',dpi=200)
                plt.show()    




                
                
                badchtrackeye = np.array([0]*len(badcountseye))
                badchtrackeyeloose = np.array([0]*len(badcountseye))
                
                adjbadcountseye = []
                for badcountn in range(len(badcountseye)):
                    badcount = badcountseye[badcountn]
                    if badcountn in eyebadic:
                        adjbadcountseye.append([badcount[0]-eyebad[0],badcount[1]-eyebad[1],badcount[2]-eyebad[2]])
                    else:
                        adjbadcountseye.append([eyebad[0]-badcount[0],eyebad[1]-badcount[1],eyebad[2]-badcount[2]])
                adjbadcountseyeT = np.array(adjbadcountseye).T
                
                typehere = adjbadcountseyeT[0]
                eyebadn = eyebad[0]
                tenpercent = eyebadn/10
                if tenpercent < 50:
                    tenpercent = 50
                for chn in range(len(badchtrackeye)):
                    if typehere[chn] > tenpercent:
                        badchtrackeye[chn] = badchtrackeye[chn] + 1   

                tenpercent = eyebadn/20
                if tenpercent < 25:
                    tenpercent = 25
                for chn in range(len(badchtrackeye)):
                    if typehere[chn] > tenpercent:
                        badchtrackeyeloose[chn] = badchtrackeyeloose[chn] + 1                           
                        
                typehere = adjbadcountseyeT[1]
                eyebadn = eyebad[1]
                tenpercent = 4
                for chn in range(len(badchtrackeye)):
                    if typehere[chn] >= tenpercent:
                        badchtrackeye[chn] = badchtrackeye[chn] + 1 
                        badchtrackeyeloose[chn] = badchtrackeyeloose[chn] + 1    
                        
                typehere = adjbadcountseyeT[2]
                eyebadn = eyebad[2]
                for chn in range(len(badchtrackeye)):
                    if typehere[chn] > 0:
                        badchtrackeye[chn] = badchtrackeye[chn] + 1    
                        badchtrackeyeloose[chn] = badchtrackeyeloose[chn] + 1    
                

                                        
                #get a measure of the importance of each IC
                
                #the variance in each PC
                explainedvartotal = ica.pca_explained_variance_
                explainedvarsubcomp = explainedvartotal[:numcomp]
                
                varexp = sum(explainedvarsubcomp)/sum(explainedvartotal)

                varscores = []
                
                for icnum in range(numcomp):
                    mixma = ica.mixing_matrix_[:,icnum]
                    amixma = abs(mixma)/sum(abs(mixma))
                    
                    varscore = sum(explainedvarsubcomp*amixma)
                    varscores.append(varscore)


                #importance of each electrode
                chimportance = np.zeros(len(componentz[0]))
                
                for ii in range(len(varscores)):
                    varscor = varscores[ii]
                    component_scores = componentz[ii]
                    adjcompscores = abs(varscor*component_scores)
                    chimportance = chimportance + adjcompscores
                  
                chimportance = [(xx-np.mean(chimportance))/np.std(chimportance) for xx in chimportance]
                    
                elecdf = pd.DataFrame({'ch':goodch,'importance':chimportance})
                elecdfsort = elecdf.sort_values(by=['importance'],ascending=False)
                elecdfchannels = list(elecdfsort['ch'])
                elecdfim = list(elecdfsort['importance'])
                
 
                #importance of each electrode
                adjchimportance = np.zeros(len(componentz[0]))
                
                for ii in range(len(varscores)):
                    if ii not in eyebadic:
                        varscor = varscores[ii]
                        component_scores = componentz[ii]
                        adjcompscores = abs(varscor*component_scores)
                        adjchimportance = adjchimportance + adjcompscores
                
                adjchimportance = [(xx-np.mean(adjchimportance))/np.std(adjchimportance) for xx in adjchimportance]
                        
                adjelecdf = pd.DataFrame({'ch':goodch,'adjimportance':adjchimportance})
                adjelecdfsort = adjelecdf.sort_values(by=['adjimportance'],ascending=False)
                adjelecdfchannels = list(adjelecdfsort['ch'])
                adjelecdfim = list(adjelecdfsort['adjimportance'])   
                                
                
                if len(eyebadic) > 5:
                    worse = elecdfsort[elecdfsort['importance'] > 5]
                else:
                    worse = adjelecdfsort[adjelecdfsort['adjimportance'] > 5]
                    

                badelectrodes = list(worse['ch'])

                    
                

            
                
                medimp = np.median(chimportance)


                for lnum in range(len(componentz)):
                             
                    notiftop1 = False
                    notiftop3 = False
                    
                    brainguess = predictions[lnum][0]
                    muscleguess = predictions[lnum][1]
                    eyeguess = predictions[lnum][2]
                    heartguess = predictions[lnum][3]
                    lineguess = predictions[lnum][4]
                    channelguess = predictions[lnum][5]
                    otherguess = predictions[lnum][6]
                    nonbrainnonother = [muscleguess,eyeguess,heartguess,lineguess,channelguess]
                    
                    varscore = varscores[lnum]

                    badchtrackeyehere = badchtrackeye[lnum]
                    badchtrackeyeloosehere = badchtrackeyeloose[lnum]

                    data = componentz[lnum]
                    datal = list(data)
                    datalsort = datal.copy()
                    datalsort.sort(key=abs)
                    best3 = datalsort[-3:]
                    best1 = datalsort[-1]
                    best4th = datalsort[-4]
                    best4 = datalsort[-4:]
                    best5th = datalsort[-5]
                    namebest3 = []
                    numbest3 = []
                    for best in best3:
                        chnum = datal.index(best)
                        ch = goodch[chnum]
                        namebest3.append(ch)

                    namebest4 = []
                    numbest4 = []
                    for best in best4:
                        chnum = datal.index(best)
                        ch = goodch[chnum]
                        namebest4.append(ch)                        
                        
                        
                    chnum = datal.index(best1)
                    namebest1 = goodch[chnum]
                    
                    
                    if lnum in badchcomps:
                        badchcomp = True
                    else:
                        badchcomp = False


                    if eyeguess > 0.6 and badchtrackeyeloosehere > 0:
                        defaultbadic.append(lnum)
                    elif eyeguess > 0.4 and brainguess < 0.3 and badchtrackeyeloosehere > 0:
                        defaultbadic.append(lnum) 
                        notiftop1 = True
                    elif eyeguess > 0.3 and brainguess < 0.3 and badchtrackeyehere > 0:
                        defaultbadic.append(lnum)
                        notiftop1 = True
                    
                    if muscleguess > 0.6 and badchtrackeyeloosehere:
                        defaultbadic.append(lnum)
                        notiftop1 = True
                       
                    if heartguess > 0.6:
                        defaultbadic.append(lnum)
                        
                    if lineguess > 0.6:
                        defaultbadic.append(lnum)                        
                    
                    if max(nonbrainnonother) > 0.6 and badchtrackeyehere > 0:
                        defaultbadic.append(lnum)
                        notiftop1 = True
                    elif max(nonbrainnonother) > 0.4 and brainguess < 0.2 and badchtrackeyehere > 0:
                        defaultbadic.append(lnum)
                        notiftop1 = True
                        
                    if otherguess > 0.6 and brainguess < 0.2 and badchtrackeyehere > 0:
                        defaultbadic.append(lnum)
                        notiftop1 = True                        
                        
                        
                        
                    if badchcomp and badchtrackeyeloosehere > 0:
                        defaultbadic.append(lnum)
                        notiftop1 = True
                        
                    if badchcomp and namebest1 in ['E62','E63']:
                        defaultbadic.append(lnum)
                        
                    if badchcomp and namebest1 in cheekch and len([i for i in cheekch if i in namebest3]) > 1:
                        defaultbadic.append(lnum)                        
                        
                    if len([i for i in cheekch if i in namebest4]) == 4 and abs(best1) > 0.3 and abs(best5th) < 0.15:
                        defaultbadic.append(lnum)
                        
                    if len([i for i in cheekch if i in namebest3]) == 3 and abs(best1) > 0.3 and abs(best4th) < 0.15:
                        defaultbadic.append(lnum)                        

                        
                    if brainguess < 0.6 and len([i for i in cheekch if i in namebest3]) > 0 and badchtrackeyehere > 1:
                        defaultbadic.append(lnum)
                        notiftop3 = True
                        
                    if len([i for i in earch if i in namebest3]) > 0 and notiftop3 and lnum in defaultbadic and lnum not in eyebadic:
                        defaultbadic = [i for i in defaultbadic if i != lnum]
                        
                    if namebest1 in earch and badchcomp and notiftop1 and lnum in defaultbadic and lnum not in eyebadic:
                        defaultbadic = [i for i in defaultbadic if i != lnum]

                                       
                defaultbadic = list(set(defaultbadic))
                defaultbadic.sort()

                        






                
                #remove default bad IC, see what that looks like
                ica.exclude = defaultbadic
                                           
                epochs_repaired = epochs_reref.copy()
                ica.apply(epochs_repaired, exclude=ica.exclude,verbose=False)
                
                total_bad,bad_epochs_count,bad_channel_count,labels2 = iccheck(epochs_repaired,badvar)
                


                #bad epochs, based off of removing default bad ICs
                newbadepoch = np.array([False]*len(epochs_repaired))
                                
                altbadepoch = []
                altchdatabe_data = labels2.T
                
                #for all bad channels specified, refer to this data as all bad epochs
                for badchan in badchannels:
                    chnum = newnames.index(badchan)
                    altchdatabe_data[chnum] = [1]*len(altchdatabe_data[chnum])
                
                for epn in range(len(altchdatabe_data.T)):
                    ep = altchdatabe_data.T[epn]
                    #if more than 16 channels are "bad", then it's a bad epoch
                    if sum(ep) > badchperbadepoch:
                        altbadepoch.append(epn)
                for qi in altbadepoch:
                    newbadepoch[qi] = True
                    
                altbadch = []  
                for chn in range(len(altchdatabe_data)):
                    ch = altchdatabe_data[chn]
                    chname = epochs_reref.ch_names[chn]
                    if sum(ch) > badepochperbadch:
                        altbadch.append(chname)
                        
                totalbaddata = int(sum(sum(altchdatabe_data)))
                adjtotalbaddata = totalbaddata - len(goodepochs)*len(badchannels)

            
                log.append("Removing default bad ICs:")
                log.append(str(len(altbadepoch)) + '/' + str(len(newbadepoch)) + ' epochs are bad')
                log.append('bad epochs are:')
                log.append(altbadepoch)
                log.append("Bad channels are:")
                log.append(altbadch)
                log.append("Total bad data = " + str(totalbaddata))
                log.append("Total bad data not counting pre-specified bad channels = " + str(adjtotalbaddata))
                log.append('')             
                    

                figure, ax = plt.subplots(figsize=(12, 6))
                ch_names_ = epochs_reref.ch_names[4::5]
                
                image = altchdatabe_data.copy()

                for badchan in badchannels:
                    chnum = newnames.index(badchan)
                    image[chnum] = [2]*len(image[chnum])
                    
                image = image.T

                
                legend_label = {0: 'good', 1: 'bad', 2: 'predefined bad'}
                cmap = mpl.colors.ListedColormap(['lightgreen', 'red','grey'])

                
                img = ax.imshow(image.T, cmap=cmap,vmin=0, vmax=2)
                ax.set_xlabel('Epochs')
                ax.set_ylabel('Channels')
                plt.setp(ax, yticks=range(4, image.shape[1], 5),yticklabels=ch_names_)  
                plt.setp(ax.get_yticklabels(), fontsize=8)
                
                for za in range(len(image.T)):
                    ax.plot([-0.5,len(image)-0.5],[za+0.5,za+0.5], color='white', linestyle='-', linewidth=1)
                
                # add grey box around rejected epochs
                for idx in np.where(newbadepoch[:len(image)])[0]:
                    ax.add_patch(patches.Rectangle(
                        (idx - 0.5, -0.5), 1, len(image.T), linewidth=1,
                        edgecolor='grey', facecolor='none'))
                    
                for badchan in altbadch:
                    chnum = newnames.index(badchan)
                    ax.add_patch(patches.Rectangle(
                        (-0.5,chnum-0.5), len(image), 1, linewidth=1,
                        edgecolor='grey', facecolor='none',zorder=10))     

                # add legend
                handles = [patches.Patch(color=img.cmap(img.norm(i)), label=label)
                           for i, label in legend_label.items()]
                ax.legend(handles=handles, bbox_to_anchor=(0.5, 1.15), ncol=3,
                          borderaxespad=0.,loc='center')
                
                anntext = 'drop default bad IC ' + str(defaultbadic) + '\nbad epochs: ' + str(len(altbadepoch)) + ', bad channels: ' + str(len(altbadch)) + ', total bad data: ' + str(totalbaddata) + ' (not counting predefined bad channels: ' + str(adjtotalbaddata) + ')'
                ax.annotate(anntext,(0.5,1.05),xycoords='axes fraction',ha='center',va='center')
                 
                
                plt.subplots_adjust(top=0.94,left=0.1,bottom=0.2)
                plt.tight_layout()
                plt.savefig(icadir+'badepoch_repaired_dropdefaultIC.png',dpi=200)
                plt.show()  





                

                for iy in range(len(componentz)):
                    
                    log2 = []
                    log2.append("This shows the contribution from each channel")
                    for spat in range(len(componentz[iy])):
                        log2.append(ica.info.ch_names[spat] + ': ' + str(round(componentz[iy][spat],3)))
                    
                    compnumt = str(iy)
                    if len(compnumt) == 1:
                        savename = icadir+'spatialdata_comp_0' + compnumt + '.txt'
                    else:
                        savename = icadir+'spatialdata_comp_' + compnumt + '.txt'
                        
                    with open(savename, 'w') as f:
                        for item in log2:
                            f.write("%s\n" % item)
                    f.close()  


                variancey = ica.pca_explained_variance_
                numcompvar6 = sum(~(variancey[0]/variancey > 1e6))
                numcompvar5 = sum(~(variancey[0]/variancey > 1e5))
                    
                
                log.append("In ICA data used:")
                log.append('# components: ' + str(numcomp))
                log.append("Theoretical number of components (64 - # bad channels): " + str(numcomptheory))
                log.append('Difference: ' + str(numcompdiff))
                
                log.append('')
                log.append("Random state used: " + str(randstate))
                log.append("Number of iterations to converge: " + str(numint))
                if rerun:
                    log.append('ICA had to rerun due to lack of convergence with original random state')
                else:
                    log.append('ICA did not rerun due to lack of convergence')
                log.append("Number of reruns: " + str(numreruns))                
                
                log.append('')
                
                log.append('Variance explained: ' + str(round(varexp,4)))
                log.append("")
            
                log.append('Variance measure of each IC')
                for vi in range(numcomp):
                    log.append(str(vi) + ': ' + str(round(varscores[vi],2)))


                #elecdfchannels = list(elecdfsort['ch'])
                #elecdfim = list(elecdfsort['importance'])

                log.append('')
                log.append('Electrode (over) representation')
                for vi in range(numcomp):
                    log.append(elecdfchannels[vi] + ': ' + str(round(elecdfim[vi],2)))        
                    

                log.append('')
                log.append('Adj electrode (over) representation')
                for vi in range(numcomp):
                    log.append(adjelecdfchannels[vi] + ': ' + str(round(adjelecdfim[vi],2)))        
                
                
                if len(badelectrodes) == 0:
                    log.append('')
                    log.append('No bad electrodes based on overrepresentation')
                else:
                    log.append('')
                    log.append('Consider rerunning ICA with the following electrodes removed: ' + str(badelectrodes))
                    
                

                log.append('')
                log.append('Variance measure of each PC that went into the ICA')
                for vi in range(numcomp):
                    log.append(str(vi) + ': ' + str(variancey[vi]))
                log.append('')
                log.append("Number of components, max 1e6 variance ratio: " + str(numcompvar6))
                log.append("Number of components, max 1e5 variance ratio: " + str(numcompvar5))
                
                
                log.append('')
                log.append("Bad components potentially reflecting a single bad channel:")
                log.append(badchcomps)
                log.append("Other components probably aren't a single bad channel")
                log.append("")

                
                log.append("ICLabel guesses of what each IC represents and the probability")
                log.append("Potentially bad ICs:")
                for num in range(len(guesses)):
                    if guesses[num] != 'brain':
                        log.append(str(num) + ": " + guesses[num] + " (" + str(round(guessstr[num],3)) + ')')
                log.append('')
                log.append("Potentially good ICs:")
                for num in range(len(guesses)):
                    if guesses[num] == 'brain':
                        log.append(str(num) + ": " + guesses[num] + " (" + str(round(guessstr[num],3)) + ')')        
                log.append('')                


         
                

                log.append("Default eye component ICs are " + str(eyebadic))
                log.append("Default bad ICs are " + str(defaultbadic))
                
                #badicautodf.loc[badicautodf.File == raw_data_file,'EyeBadIC'] = str(eyebadic)[1:-1]
                #badicautodf.loc[badicautodf.File == raw_data_file,'DefaultBadIC'] = str(defaultbadic)[1:-1]
                #badicautodf.loc[badicautodf.File == raw_data_file,'DropTheseElec'] = str(badelectrodes)[1:-1]


                
                badepfile = icadir+logname
                    
                print("")
                with open(badepfile, 'w') as f:
                    for item in log:
                        f.write("%s\n" % item)
                        print(item)
                f.close()      
               


                positions = epochs_reref.get_montage().get_positions()['ch_pos']
                

                
                locs3d = []
                for ch in goodch:
                    locs3d.append(positions[ch])
                locs3d = np.array(locs3d)
                sphere = np.array([0.   , 0.   , 0.   , 0.095])
                
                cart_coords = mne.transforms._cart_to_sph(locs3d)
                pos = mne.transforms._pol_to_cart(cart_coords[:, 1:][:, ::-1])
                # scale from radians to mm
                pos *= cart_coords[:, [0]] / (np.pi / 2.)
                      
                pos_x, pos_y = pos.T    
                
                outlines = mne.viz.topomap._make_head_outlines(sphere, pos, 'head', (0., 0.))
                extent, Xi, Yi, interp = mne.viz.topomap._setup_interp(pos, 64, 'cubic', 'head', outlines, 'mean')
                
       
                   
                compslist = [list(range(0,15)),list(range(15,32)),list(range(32,47)),list(range(47,numcomp))]
                savenamelist = ["ICA_0to15.pdf","ICA_15to32.pdf","ICA_32to47.pdf","ICA_47onward.pdf"]
                
                for compsheren in range(len(compslist)):
                    comps = compslist[compsheren]
                    savename = savenamelist[compsheren]
                
                    numcomp = len(comps)

                
                    if numcomp % 3 == 0:
                        rows = int(numcomp/3)
                        rem = 0
                    elif numcomp % 3 == 1:
                        rows = int(numcomp/3)+1
                        rem = 1
                    else:
                        rows = int(numcomp/3)+1
                        rem = 2
                    
                    if rows > 1:
                        figure, ax = plt.subplots(rows,6,figsize=(5.5*3, 2.5*rows))
                    else:
                        figure, ax = plt.subplots(2,6,figsize=(5.5*3, 2.5*2))
                        spotlist = [[1,0],[1,1],[1,2],[1,3],[1,4],[1,5]]
                        for spot1 in spotlist:
                            ax[spot1[0],spot1[1]].get_yticks()
                            ax[spot1[0],spot1[1]].xaxis.set_ticks([])
                            ax[spot1[0],spot1[1]].yaxis.set_ticks([])
                            ax[spot1[0],spot1[1]].set_frame_on(False)
                    
                    if rem == 0:
                        rem = 3        
                    while rem != 3:
                        spotlist = [[rows-1,rem*2+1],[rows-1,rem*2]]
                        if rows == 1:
                            spotlist = spotlist + [[rows-2,rem*2+1],[rows-2,rem*2]]
                        for spot1 in spotlist:
                            ax[spot1[0],spot1[1]].get_yticks()
                            ax[spot1[0],spot1[1]].xaxis.set_ticks([])
                            ax[spot1[0],spot1[1]].yaxis.set_ticks([])
                            ax[spot1[0],spot1[1]].set_frame_on(False)
                        rem = rem+1
                    
                    for compn in range(numcomp):
                    
                        if compn % 3 == 0:
                            spot1 = [int(compn/3),0]
                        elif compn % 3 == 1:
                            spot1 = [int(compn/3),2]
                        else:
                            spot1 = [int(compn/3),4]
                    
                        data = componentz[comps[compn]]
                    
                        norm = min(data) >= 0
                        vmax = np.abs(data).max()
                        vmin = 0. if norm else -vmax
                        cmap = plt.get_cmap('Reds' if norm else 'RdBu_r')
                    
                        
                        ax[spot1[0],spot1[1]].get_yticks()
                        ax[spot1[0],spot1[1]].xaxis.set_ticks([])
                        ax[spot1[0],spot1[1]].yaxis.set_ticks([])
                        ax[spot1[0],spot1[1]].set_frame_on(False)
                        
                        #plot electrodes
                        ax[spot1[0],spot1[1]].scatter(pos_x, pos_y, s=0.25, marker='o',edgecolor=['k'] * len(pos_x), facecolor='none')
                        
                        #plot head
                        for key, (x_coord, y_coord) in outlines.items():
                            if not 'mask' in key or key in ('clip_radius', 'clip_origin'):
                                ax[spot1[0],spot1[1]].plot(x_coord, y_coord, color='k', linewidth=1, clip_on=False)
                    
                    
                        interp.set_values(data)
                        Zi = interp.set_locations(Xi, Yi)()
                    
                        
                        #plot colours
                        im = ax[spot1[0],spot1[1]].imshow(Zi, cmap=cmap, origin='lower', aspect='equal',
                                       extent=extent, 
                                       interpolation='bilinear', norm=Normalize(vmin, vmax))
                        
                        #plot contour map
                        cont = ax[spot1[0],spot1[1]].contour(Xi, Yi, Zi, 6, colors='k',linewidths=0.5)
                        
                        #turn into nice circular diagram
                        patch_ = mne.viz.topomap._get_patch(outlines, 'head', interp, ax[spot1[0],spot1[1]])
                        im.set_clip_path(patch_)
                        for col in cont.collections:
                            col.set_clip_path(patch_)
                        
                        
                    for compn in range(numcomp):
                    
                        if compn % 3 == 0:
                            spot1 = [int(compn/3),1]
                        elif compn % 3 == 1:
                            spot1 = [int(compn/3),3]
                        else:
                            spot1 = [int(compn/3),5]
                            
                        icnum = comps[compn]
                        
                        ax[spot1[0],spot1[1]].get_yticks()
                        ax[spot1[0],spot1[1]].xaxis.set_ticks([])
                        ax[spot1[0],spot1[1]].yaxis.set_ticks([])
                        ax[spot1[0],spot1[1]].set_frame_on(False)
                    
                        varscore = varscores[icnum]
                        text1 = 'Variance measure: ' + str(round(varscore,2)) + '$'
                        
                        brainguess = predictions[icnum][0]
                        otherguess = predictions[icnum][6]
                        predictionshere = predictions[icnum][1:6]
                        predictionstitle = ['muscle','eye','heart','line','channel']
                        namesort = [x for _,x in sorted(zip(predictionshere,predictionstitle))]
                        highest = max(predictions[icnum])
                        
                        highest1 = namesort[-1]
                        highest2 = namesort[-2]
                        highest1val = predictionshere[predictionstitle.index(highest1)]
                        highest2val = predictionshere[predictionstitle.index(highest2)]
                        
                        braintext = "brain: " + str(round(brainguess,3))
                        highest1text = '*' + highest1 + ": " + str(round(highest1val,3))
                        highest2text = highest2  + ": " + str(round(highest2val,3)) + '$'
                        othertext = "*other: " + str(round(otherguess,3))
                        
                        if brainguess == highest:
                            braintext = [braintext,'red']
                        if highest1val == highest:
                            highest1text = [highest1text,'red']
                        if highest2val == highest:
                            highest2text = [highest2text,'red']
                        if otherguess == highest:
                            othertext = [othertext,'red']
                        
                        text2 = 'ICLabel predictions:'
                    
                        
                        data = componentz[icnum]
                        datal = list(data)
                        datalsort = datal.copy()
                        datalsort.sort(key=abs)
                        best3 = datalsort[-3:]
                        namebest3 = []
                        numbest3 = []
                        for best in best3:
                            chnum = datal.index(best)
                            ch = goodch[chnum]
                            namebest3.append(ch)
                            numbest3.append(str(round(best,3)))
                        
                        text3 = 'Most contributing channels: '
                        text4 = namebest3[2] + ': ' + numbest3[2] + ', ' + namebest3[1] + ': ' + numbest3[1] + ', ' + namebest3[0] + ': ' + numbest3[0] 
                        
                        if icnum in badchcomps and namebest3[2] not in earch:
                            text5 = ['IC likely reflects bad channel$','blue']
                        else:
                            text5 = ['Not bad$','white']
                            
                        text5B = 'Most similar other ICs: '
                        text5C = selfcorrztext[icnum] + '$'
                            
                            
                        if icnum in defaultbadic:
                            if icnum in eyebadic:
                                text6 = ['Default bad IC + default eye IC$','blue']
                            else:
                                text6 = ['Default bad IC$','blue']
                        else:
                            text6 = ['Not default$','white']
                        
                        
                        
                        #orig = str(origbad[0]) + '/' + str(origbad[1]) + 'ep/' + str(origbad[2]) + 'ch'
                        eyebadstr = str(eyebad[0]) + '/' + str(eyebad[1]) + 'ep/' + str(eyebad[2]) + 'ch'
                        
                        #badcountshere = badcounts[icnum]
                        #badhere = str(badcountshere[0]) + '/' + str(badcountshere[1]) + 'ep/' + str(badcountshere[2]) + 'ch'
                        
                        eyebadcountshere = badcountseye[icnum]
                        eyebadhere = str(eyebadcountshere[0]) + '/' + str(eyebadcountshere[1]) + 'ep/' + str(eyebadcountshere[2]) + 'ch'    
                        
                    
                        
                        text7 = 'Noise change if drop this IC:'
                        #text8 = 'Sole: ' + orig + ' → ' + badhere
                        
                        if icnum in eyebadic:
                            text9 = 'w/ oth eye: ' + eyebadhere + ' → ' + eyebadstr
                        else:
                            text9 = 'w/ eye: ' + eyebadstr + ' → ' + eyebadhere
                            
                        #if badchtrack[icnum] > 0:
                        #    text8 = [text8,'blue']
                    
                        if badchtrackeye[icnum] > 0:
                            text9 = [text9,'blue']
                        elif badchtrackeyeloose[icnum] > 0:
                            text9 = [text9,'green']
                        
                    
                        textx = -0.08
                        icname = str(icnum)
                        if len(icname) == 1:
                            icname = '0' + icname
                            
                        info = 'IC ' + icname
                        ax[spot1[0],spot1[1]].text(textx,0.95,info,fontsize=13)
                        
                        
                        #info = [text1, text2, braintext, highest1text, highest2text, othertext,text3,text4,text5,text5B,text5C,text6,text7,text8,text9]
                        info = [text1, text2, braintext, highest1text, highest2text, othertext,text3,text4,text5,text5B,text5C,text6,text7,text9]
                        
                        
                        t_right = ax[spot1[0],spot1[1]].transData
                        t_down = ax[spot1[0],spot1[1]].transData
                        for dat in info:
                            if isinstance(dat, list):
                                texth = dat[0]
                                color = dat[1]
                            else:
                                texth = dat
                                color = 'black'
                            if texth[0] == '*':
                                moveright = True
                                texth = texth[1:]
                            else:
                                moveright = False
                            if texth[-1] == '$':
                                texth = texth[:-1]
                                adj = -5
                            else:
                                adj = -2
                            if moveright:
                                text = ax[spot1[0],spot1[1]].text(textx,0.85,texth,color=color, transform=t_right, fontsize = 7.5)
                            else:
                                text = ax[spot1[0],spot1[1]].text(textx,0.85,texth,color=color, transform=t_down, fontsize = 7.5)
                                
                            text.draw(figure.canvas.get_renderer())
                            ex = text.get_window_extent()
                            t_right = transforms.offset_copy(text._transform, x=100, units='dots')
                            if moveright == False:
                                t_down = transforms.offset_copy(text._transform, y=-ex.height+adj, units='dots')
                    
                    
                    
                    figure.tight_layout()
                    plt.savefig(icadir + savename,format='pdf')  
                    plt.show()
                    
                                  
                
                plt.close('all')


                #badicautodf.to_csv(badicauto)












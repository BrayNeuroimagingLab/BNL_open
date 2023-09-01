#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v5 now uses the raw files



"""

import os
import shutil

import mne
from autoreject import Ransac
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('Agg')
#%matplotlib inline
import matplotlib.pyplot as plt





#folder with all the participant folders
#the program assumes the files are organized like this:
#dir_start/sub-1973001P/ses-4/eeg/sub-1973001P_ses-4_task-YT10_eeg.raw
dir_start = '/Users/ivy/Desktop/Test_EEG/Test_EEG_BIDS/'

#how participant names start
subjectprefix = 'sub-19730'

#folder where outputs are saved to
output_dir = '/Users/ivy/Desktop/Test_EEG/Test_EEG_output/'


#logbook name
logname = 'badchanneldata.txt'


#which file(s) do you want to look at?
families = [2,3,5,6,7,8,9,10,11,12,13,14,16,18]
participant_ages = ['C','P']
sessions = [1,2,3,4]
tasks = ['DORA','YT','RX']



#frequency filter
lfreq = 1
hfreq = 45

#downsample frequency
downfreq = 250



#plotting settings

#how many seconds should the plots be?
timelen = 10
#where in the time course should the plots start?
startspotplot = [10,150,350]

#how many seconds should the longer plot be?
timelen2 = 50
#where in the time course should the longer plot start?
startspot2 = [50]

#channel ranges for plots
chranges = [[0,16],[16,32],[32,48],[48,64]]





#what the channel names should be
newnames = ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 
             'E12', 'E13', 'E14', 'E15', 'E16', 'E17', 'E18', 'E19', 'E20', 'E21', 'E22', 
             'E23', 'E24', 'E25', 'E26', 'E27', 'E28', 'E29', 'E30', 'E31', 'E32', 'E33', 
             'E34', 'E35', 'E36', 'E37', 'E38', 'E39', 'E40', 'E41', 'E42', 'E43', 'E44', 
             'E45', 'E46', 'E47', 'E48', 'E49', 'E50', 'E51', 'E52', 'E53', 'E54', 'E55', 
             'E56', 'E57', 'E58', 'E59', 'E60', 'E61', 'E62', 'E63', 'E64']



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
    strfam = subjectprefix + strnum

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
                        
                            output_data_folder_task = output_data_folder + raw_data_file[:-4] + '/channelplots/'
                            output_ch_data = output_data_folder_task + logname
                            
                            if os.path.isfile(output_ch_data):
                                alreadyprocessed = 'y'
                                numalready = numalready + 1
                            else:
                                alreadyprocessed = 'n'
        
                            persdata = [raw_data_folder,raw_data_file,output_data_folder,output_data_folder_task,alreadyprocessed]
                            raw_data_list.append(persdata)
                            
      
"""                         
scanlist = []
for x in raw_data_list:
    scanlist.append(x[1])
    
testdf = pd.DataFrame({'scan':scanlist})

testdf.to_csv('/Users/ivy/Desktop/Graff_EEG_stuff/QC/newdatalist.csv')
"""                        
 
    
 
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
                    channelplotfolder = dirinfo[3]
                    contents = os.listdir(channelplotfolder)
                    actuallydel = True
                    for rawfile in contents:
                        if rawfile.endswith(".set"):
                            print("Uh oh. Looks like there are valuables saved in: " + channelplotfolder)
                            print("You shouldn't see this error message unless you did something weird to the data")
                            actuallydel = False
                    if actuallydel:
                        shutil.rmtree(channelplotfolder)
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
            
            print("Generating data for " + raw_data_file)
            
            #make a folder for saving outputs
            newdir = dirinfo[3]
            if not os.path.exists(newdir):
                os.makedirs(newdir)  

            #file name
            rawfile = raw_data_folder + raw_data_file                
                 
            #load the raw file
            raw = mne.io.read_raw_egi(rawfile,preload=True)
        
            #check channel names and set channel locations
            curchnames = raw.info.ch_names
            
            if curchnames == newnames + ['E65']:         
                raw_y = raw.copy().rename_channels({'E65':'Cz'})
                raw_y = raw_y.set_montage('GSN-HydroCel-65_1.0')
                print("Your channel names look fine")

            elif curchnames == newnames + ['E65', 'IEND', 'STI 014']:  
                raw_y = raw.copy().rename_channels({'E65':'Cz'})
                raw_y = raw_y.set_montage('GSN-HydroCel-65_1.0')
                print("Your channel names look sus, but we'll try our best here.")       
                susnames = True                

            elif curchnames == newnames + ['E65', 'IBEG', 'IEND', 'STI 014']:  
                raw_y = raw.copy().rename_channels({'E65':'Cz'})
                raw_y = raw_y.set_montage('GSN-HydroCel-65_1.0')
                print("Your channel names look sus, but we'll try our best here.")       
                susnames = True   


            else:
                
                print("Uh oh. Your channel names are messed up")
                proceed2 = False
                
            
            if proceed2:
                
                origfreq = raw_y.info['sfreq']
                
                #bandpass filter data        
                    
                raw_filter = raw_y.copy().filter(l_freq=lfreq, h_freq=hfreq)   
                raw_downsampled = raw_filter.copy().resample(sfreq=downfreq)
            
                sampling_freq = raw_downsampled.info['sfreq']
            
                #look at ~25 timepoint windows to calculate changes in frequency
                suggestedwindow = 25 #how many timepoints in a window to calculate change in frequency
                intervalunit = 3 #how often to look at windows, if 3, check timepoints 0-24, then 3-27, then 6-30, etc
                #make the window an odd number so there's a center, with same number of timepoints on either side
                if suggestedwindow % 2 == 0:
                    window = int(suggestedwindow + 1)
                else:
                    window = int(suggestedwindow)

                flank = int((window-1)/2)
                mid = int(flank+1)
                scanl = len(raw_downsampled)

                sectlist = []
                for xy in range(mid-1,scanl-mid+1,intervalunit):
                    sectlist.append(xy)  
                numsecs = len(sectlist)
                

                dataj = raw_downsampled[newnames][0]
                datanew = []
                datanan = []
                
                datanew_longer = []
                datanan_longer = []
                
                sectdrop_all = []
                timedrop_all = []
                sectdrop_long = []
                timedrop_long = []
                medamp = []
                
                badints = []
                
                numbadepochs = []
                whichbadepochs = []
                
                badepochshere = []
                
                #loop through all channels
                for channum in range(len(newnames)):
                    
                    chan = dataj[channum].copy()
                    channame = newnames[channum]
                    
                    print("Getting data for " + channame)
                
                    #calculate range for each segment, in intervals defined above
                    adj = []
                    maxlist = []
                    minlist = []
                    for xy in range(mid-1,scanl-mid+1,intervalunit):
                        part = chan[xy-flank:xy+flank+1]
                        sub = max(part)-min(part)
                        adj.append(sub)
                        maxlist.append(max(part))
                        minlist.append(min(part))
                    
                    
                    #any segment with a range/max/min bigger than 4x the median range is probably crap
                    thres = np.median(adj)*4
                    medamp.append(np.median(adj)/(1e-6))
                    

                    #get intervals greater than 4x the median range
                    altgoodbad = []
                    for y in range(numsecs):
                        if adj[y] > thres:
                            altgoodbad.append(0)
                        elif maxlist[y] > thres:
                            altgoodbad.append(0)
                        elif minlist[y]*-1 > thres:
                            altgoodbad.append(0)
                        else:
                            altgoodbad.append(1)

                    #get intervals where data switches between good and bad
                    roller = np.roll(altgoodbad,1)!=altgoodbad
                    roller[0] = False
                    intervalsx = np.where(roller)[0]

                    #if starts bad, put a 0 in front, so 0 to first switch is bad
                    #if starts good, don't do this so first two switches define a bad region
                    if altgoodbad[0] == 0:
                        intervalsx = np.insert(intervalsx,0,0)
                    
                    #if odd number of switches, that means end of scan is bad, so add the end to define the last bad region
                    if len(intervalsx) % 2 == 1:
                        intervalsx = np.append(intervalsx,len(altgoodbad))
                    
                    intervalsx = np.reshape(intervalsx,(-1,2))


                    #combine intervals if the gap between them is small
                    if len(intervalsx) > 1:
                        adjintervals = []
                        curspot = 0
                        curinterval = intervalsx[0]
                        curinterval = [curinterval[0],curinterval[1]]
                        while True:
                            if curspot + 1 == len(intervalsx):
                                adjintervals.append(curinterval)
                                break
                            else:
                                nextinterval = intervalsx[curspot+1]
                                nextinterval = [nextinterval[0],nextinterval[1]]
                                gapdiff = nextinterval[0]-curinterval[1]
                                if gapdiff > 15:
                                    adjintervals.append(curinterval)
                                    curinterval = nextinterval
                                    curspot = curspot + 1
                                    continue
                                else:
                                    curinterval = [curinterval[0],nextinterval[1]]
                                    curspot = curspot + 1
                                    continue
 
                    elif len(intervalsx) == 1:
                        adjintervals = []
                        adjintervals.append(intervalsx[0]) 
                    else:
                        adjintervals = []


                    #also get intervals greater than 4x the median 100 ms range
                    altgoodbad400 = []
                    thres400 = 400*(1e-6)
                    for y in range(numsecs):
                        if adj[y] > thres400:
                            altgoodbad400.append(0)
                        elif maxlist[y] > thres400:
                            altgoodbad400.append(0)
                        elif minlist[y]*-1 > thres400:
                            altgoodbad400.append(0)
                        else:
                            altgoodbad400.append(1)

                    roller = np.roll(altgoodbad400,1)!=altgoodbad400
                    roller[0] = False
                    intervalsx400 = np.where(roller)[0]
                    
                    if altgoodbad400[0] == 0:
                        intervalsx400 = np.insert(intervalsx400,0,0)
                        
                    if len(intervalsx400) % 2 == 1:
                        intervalsx400 = np.append(intervalsx400,len(altgoodbad400))
                    
                    intervalsx400 = np.reshape(intervalsx400,(-1,2))



                    #combine intervals if the gap between them is small
                    if len(intervalsx400) > 1:
                        adjintervals400 = []
                        curspot = 0
                        curinterval = intervalsx400[0]
                        curinterval = [curinterval[0],curinterval[1]]
                        while True:
                            if curspot + 1 == len(intervalsx400):
                                adjintervals400.append(curinterval)
                                break
                            else:
                                nextinterval = intervalsx400[curspot+1]
                                nextinterval = [nextinterval[0],nextinterval[1]]
                                gapdiff = nextinterval[0]-curinterval[1]
                                if gapdiff > 15:
                                    adjintervals400.append(curinterval)
                                    curinterval = nextinterval
                                    curspot = curspot + 1
                                    continue
                                else:
                                    curinterval = [curinterval[0],nextinterval[1]]
                                    curspot = curspot + 1
                                    continue
                    elif len(intervalsx400) == 1:
                        adjintervals400 = []
                        adjintervals400.append(intervalsx400[0])
                    else:
                        adjintervals400 = []
    

                    
                    intlens = []
                    #define bad regions. Both all bad regions, and only the longer bad regions
                    #short bad regions are likely blinks and easily dealt with
                    goodbad = [1]*len(adj)
                    adjgoodbad = [1]*len(adj)
                    for interval in adjintervals:
                        endspot = interval[1]
                        startspot = interval[0]
                        intlen = (endspot-startspot-1)*intervalunit+window
                        intlens.append(intlen)
                        for x in range(interval[0],interval[1]):
                            goodbad[x]=np.nan                        
                        
                        #if bad region longer than 150 timepoints, it's a "long" bad region
                        if intlen > 150:
                            for x in range(interval[0],interval[1]):
                                adjgoodbad[x]=np.nan
                                
                        #if crap in first second, mark it as all bad!     
                        if startspot < 250:
                            for x in range(0,endspot):
                                goodbad[x]=np.nan   
                                adjgoodbad[x]=np.nan

                    #add in the parts of the scan greater than 400, cause those are just crazy
                    for interval in adjintervals400:
                        endspot = interval[1]
                        startspot = interval[0]
                        for x in range(interval[0],interval[1]):
                            adjgoodbad[x]=np.nan
                            goodbad[x]=np.nan



                    #this is how much time is greater than 4x the thres, or greater than 400 microvolts
                    #but excluding the shortest periods
                    goodtime_longer = [1]*len(chan)
                    for xy in range(len(adjgoodbad)):
                        sub = adjgoodbad[xy]
                        if np.isnan(sub):
                            starts = sectlist[xy]
                            goodtime_longer[starts-flank:starts+flank+1] = [0]*window   


                    #this is how much time is greater than 4x the thres, or greater than 400 microvolts
                    #includes very short periods, like eye blinks
                    goodtime = [1]*len(chan)
                    for xy in range(len(goodbad)):
                        sub = goodbad[xy]
                        if np.isnan(sub):
                            starts = sectlist[xy]
                            goodtime[starts-flank:starts+flank+1] = [0]*window   
                            
                    
                    #since we're going in intervals rather than checking every 100 ms period or whatever, mark the very end as bad if necessary
                    if goodtime[-3] == 0:
                        goodtime[-2] = 0
                        goodtime[-1] = 0
                            
                    if goodtime_longer[-3] == 0:
                        goodtime_longer[-2] = 0
                        goodtime_longer[-1] = 0


                    #redefine the channel data after marking out bad sections
                    #this is used to calculate correlation between channels
                    #not very helpful to say channels have high correlations, but it's based off of artifacts
                    newl2 = [a*b if b == 1 else np.nan for a,b in zip(chan,goodtime)]
                    newl3 = [a*b if b == 1 else np.nan for a,b in zip(chan,goodtime_longer)]                    

                    
                    #this finds bad epochs based on above criteria
                    chunks = [newl3[x:x+500] for x in range(0, len(newl3), 500)]
                    if len(chunks[-1]) != 500:
                        chunks = chunks[:-1]
                    chunklist = []
                    for cn in range(len(chunks)):
                        chunk = chunks[cn]
                        if np.isnan(chunk).any():
                            chunklist.append(True)
                        else:
                            chunklist.append(False)
                            
                    
                    #recalculate the bad intervals, including the above 400 microvolts
                    roller = np.roll(goodtime,1)!=goodtime
                    roller[0] = False
                    intervalsadj = np.where(roller)[0]
                    
                    
                    if goodtime[0] == 0:
                        intervalsadj = np.insert(intervalsadj,0,0)
                        
                    if len(intervalsadj) % 2 == 1:
                        intervalsadj = np.append(intervalsadj,len(goodtime))
                    
                    #all the intervals with artifacts, including very short ones
                    intervalsdropped = np.reshape(intervalsadj,(-1,2))
                    
                    intervalmid = [np.mean(xy) for xy in intervalsdropped]
                    badints.append(intervalmid)
                    
                    
                    roller = np.roll(goodtime_longer,1)!=goodtime_longer
                    roller[0] = False
                    intervalsadj = np.where(roller)[0]
                    
                    
                    if goodtime_longer[0] == 0:
                        intervalsadj = np.insert(intervalsadj,0,0)
                        
                    if len(intervalsadj) % 2 == 1:
                        intervalsadj = np.append(intervalsadj,len(goodtime))
                    
                    #all the intervals with longer artifacts dropped
                    intervalsdropped_longer = np.reshape(intervalsadj,(-1,2))                   
                    


                    
                    sectionsdropped = len(intervalsdropped)
                    totaltimedropped = (len(goodtime)-sum(goodtime))/250
                    
                    
                    timedroplongint = (len(goodtime_longer)-sum(goodtime_longer))/250
                    
                    
                    
                    newlnan = np.isnan(newl2)
                    newlnan_longer = np.isnan(newl3)
                    
                    datanew.append(np.array(newl2))
                    datanan.append(newlnan)
                    
                    datanew_longer.append(np.array(newl3))
                    datanan_longer.append(newlnan_longer)
                    
                    sectdrop_all.append(sectionsdropped)
                    timedrop_all.append(totaltimedropped)
                    
                    sectdrop_long.append(len(intervalsdropped_longer))
                    timedrop_long.append(timedroplongint)
                    
                    epochslikelybad = sum(chunklist)
                    whichepochs = np.where(chunklist)[0]
                    
                    badepochshere.append(chunklist)
                    
                    numbadepochs.append(epochslikelybad)
                    whichbadepochs.append(whichepochs)
                    
                    
                badepochshere = np.asarray(badepochshere)
                numbad = []
                for epoc in badepochshere.T:
                    numbad.append(sum(epoc))
                    
                np.savetxt(newdir+'badepoch_channel_data.txt', badepochshere)



                
                print("Calculating correlations between channels")
                #correlations don't include the timepoints marked as bad
                datanewdf = pd.DataFrame(data=datanew).T
                datanewdf.columns = newnames
                    
                corrz = datanewdf.corr()       
                                
                abscorrz = abs(corrz)
                avgcorrzlist = list(abscorrz.mean())
                avgcorrz = abscorrz.mean().sort_values()
                channelcorr = np.array(avgcorrz.index)
                channelcorrval = np.array(avgcorrz)
                
                meancorr = np.mean(channelcorrval)    
                
                
                
                datanewdf_longer = pd.DataFrame(data=datanew_longer).T
                datanewdf_longer.columns = newnames
                    
                corrz = datanewdf_longer.corr()       
                                
                abscorrz = abs(corrz)
                avgcorrzlist_longer = list(abscorrz.mean())
                avgcorrz = abscorrz.mean().sort_values()
                channelcorr_longer = np.array(avgcorrz.index)
                channelcorrval_longer = np.array(avgcorrz)
                
                meancorr_longer = np.mean(channelcorrval_longer)                   
                

                #dataframe of stats for each channel
                chdf = pd.DataFrame({'corr_wo_art':avgcorrzlist,'corr_w_art':avgcorrzlist_longer,'amplitude':medamp,'allartifacts':sectdrop_all,'timeallartifacts':timedrop_all,'longartifacts':sectdrop_long,'timelongartifacts':timedrop_long})
                chdf.index = newnames

                chdf_amp = chdf.sort_values(by=['amplitude'])
                channelamp = np.array(chdf_amp.index)
                channelampval = np.array(chdf_amp['amplitude'])
                
                
                chdf_drop = chdf.sort_values(by=['timeallartifacts'])
                channeldrop = np.array(chdf_drop.index)
                channeldroppval = np.array(chdf_drop['timeallartifacts'])                


                chdf_drop_longer = chdf.sort_values(by=['timelongartifacts'])
                channeldrop_longer = np.array(chdf_drop_longer.index)
                channeldroplongerval = np.array(chdf_drop_longer['timelongartifacts']) 
                
                
                meandiff = np.mean(medamp)
                
                #these are for graphing
                meanmax = np.mean(medamp)*3
                meanmin = 0-np.mean(medamp)*3
            

                
                start_sample = 0
                stop_sample = scanl
                timepoints = raw_downsampled[newnames[0],start_sample:stop_sample][1]

                maxncp = 0
                for chrange in chranges:
                    ncp = chrange[1] - chrange[0]
                    if ncp > maxncp:
                        maxncp = ncp
                



               
                print("Making whole time course plots")
                for chrange in chranges:
                    
                    fig, axs = plt.subplots(maxncp, 1,figsize=(10,0.6*maxncp))                    
                    
                    ncp = chrange[1] - chrange[0]
                    startch = chrange[0]
                                     
                    for ii in range(ncp):
                        
                        ch = chrange[0]+ii
                        
                        medval = medamp[ch]
                    
                        channel = newnames[startch + ii]
                        channeldata = raw_downsampled[channel, start_sample:stop_sample]
                        x = timepoints
                        y = (channeldata[0].T)/(1e-6)  
                        
                        nandata = datanan_longer[ch][start_sample:stop_sample]
                        badint = [xyy/250 for xyy in badints[ch]]
                    
                        axs[ii].plot(x,y,c='black',linewidth=0.4)
                        axs[ii].plot(x,nandata*medval*6,c='red',linewidth=1,zorder=10) 
                        
                        if len(badint) > 0:
                            axs[ii].scatter(badint,[medval*7.7]*len(badint),c='blue',zorder=10,s=1,marker="s") 
                    
                        axs[ii].yaxis.grid(False)
                        axs[ii].spines['right'].set_visible(False)
                        axs[ii].spines['top'].set_visible(False)   
                        axs[ii].annotate(channel, xy=(0.96,0.7), va = 'center',xycoords='axes fraction',fontsize=11)
                        
                        
                        
                        axs[ii].set_ylim(0-medval*8,medval*8)  
                    
                    for ii in range(ncp-1):    
                        axs[ii].set_xticklabels('')
                            
                    axs[ncp-1].set_xlabel('Time (seconds)',fontsize=11)
                    
                    plt.subplots_adjust(top=0.94,left=0.1,bottom=0.2)
                    plt.tight_layout()
                    plt.savefig(newdir + "wholescanbad_channels" + str(startch) + ".pdf",format='pdf')
                    plt.close(fig) 


           
                    fig, axs = plt.subplots(ncp, 1,figsize=(10,0.6*ncp))  
                     
                    for ii in range(ncp):
                        
                        ch = chrange[0]+ii
                        
                        medval = medamp[ch]
                    
                        channel = newnames[startch + ii]
                        y = datanew[ch][start_sample:stop_sample]/(1e-6)
                        x = timepoints
                        
                        nandata = datanan_longer[ch][start_sample:stop_sample]
                        
                        nandata1 = [0 if zz == True else np.nan for zz in nandata]
                    
                        axs[ii].plot(x,y,c='black',linewidth=0.4)
                        axs[ii].plot(x,nandata1,c='red',linewidth=1,zorder=10) 
                    
                        axs[ii].yaxis.grid(False)
                        axs[ii].spines['right'].set_visible(False)
                        axs[ii].spines['top'].set_visible(False)   
                        axs[ii].annotate(channel, xy=(0.96,0.7), va = 'center',xycoords='axes fraction',fontsize=11)
                        
                        axs[ii].set_ylim(meanmin,meanmax)  
                    
                    for ii in range(ncp-1):    
                        axs[ii].set_xticklabels('')
                            
                    axs[ncp-1].set_xlabel('Time (seconds)',fontsize=11)
                    
                    plt.subplots_adjust(top=0.94,left=0.1,bottom=0.2)
                    plt.tight_layout()
                    plt.savefig(newdir + "wholescan_repaired_channels" + str(startch) + ".pdf",format='pdf')
                    plt.close(fig)
                    
                






                #plot channels
                for start in startspotplot:
                    
                    print("Making plots for time = " + str(start))
            
                    start_stop_seconds = np.array([start, start + timelen])
                    start_sample, stop_sample = (start_stop_seconds * sampling_freq).astype(int)
                    
                            
                    for chrange in chranges:
                        ncp = chrange[1] - chrange[0]
                        startch = chrange[0]
                    
                        fig, axs = plt.subplots(ncp, 1,figsize=(10,0.6*ncp))

                        for ii in range(ncp):
                        
                            channel = newnames[startch + ii]
                            channeldata = raw_downsampled[channel, start_sample:stop_sample]
                            x = channeldata[1]
                            y = (channeldata[0].T)/(1e-6)    
                        
                            axs[ii].plot(x,y,c='black',linewidth=0.4)     
                        
                            axs[ii].yaxis.grid(False)
                            axs[ii].spines['right'].set_visible(False)
                            axs[ii].spines['top'].set_visible(False)   
                            axs[ii].annotate(channel, xy=(0.96,0.7), va = 'center',xycoords='axes fraction',fontsize=11)
                        
                        for ii in range(ncp-1):    
                            axs[ii].set_xticklabels('')
                                
                        axs[ncp-1].set_xlabel('Time (seconds)',fontsize=11)
                        
                        plt.subplots_adjust(top=0.94,left=0.1,bottom=0.2)
                        plt.tight_layout()
                        plt.savefig(newdir + "time="+ str(start) + "_channels" + str(startch) + ".pdf",format='pdf')
                        plt.close(fig)   
                     
                                      
                        fig, axs = plt.subplots(ncp, 1,figsize=(10,0.6*ncp))
  
                               
                        for ii in range(ncp):
                        
                            channel = newnames[startch + ii]
                            channeldata = raw_downsampled[channel, start_sample:stop_sample]
                            x = channeldata[1]
                            y = (channeldata[0].T)/(1e-6)    
                        
                            axs[ii].plot(x,y,c='black',linewidth=0.4)     
                        
                            axs[ii].yaxis.grid(False)
                            axs[ii].spines['right'].set_visible(False)
                            axs[ii].spines['top'].set_visible(False)   
                            axs[ii].annotate(channel, xy=(0.96,0.7), va = 'center',xycoords='axes fraction',fontsize=11)
                            axs[ii].set_ylim(meanmin,meanmax)   
                        
                        for ii in range(ncp-1):    
                            axs[ii].set_xticklabels('')
                                
                        axs[ncp-1].set_xlabel('Time (seconds)',fontsize=11)
                        
                        plt.subplots_adjust(top=0.94,left=0.1,bottom=0.2)
                        plt.tight_layout()
                        plt.savefig(newdir + "sameaxis_time="+ str(start) + "_channels" + str(startch) + ".pdf",format='pdf')
                        plt.close(fig)   


                        fig, axs = plt.subplots(ncp, 1,figsize=(10,0.6*ncp))

                               
                        
                        for ii in range(ncp):
                            
                            ch = chrange[0]+ii
                            
                            medval = medamp[ch]
                        
                            channel = newnames[startch + ii]
                            y = datanew[ch][start_sample:stop_sample]/(1e-6)
                            channeldata = raw_downsampled[channel, start_sample:stop_sample]
                            x = channeldata[1]

                            
                            nandata = datanan[ch][start_sample:stop_sample]
                            
                            nandata1 = [0 if zz == True else np.nan for zz in nandata]
                        
                            axs[ii].plot(x,y,c='black',linewidth=0.4)
                            axs[ii].plot(x,nandata1,c='red',linewidth=1,zorder=10) 
    
  
                        
                            axs[ii].yaxis.grid(False)
                            axs[ii].spines['right'].set_visible(False)
                            axs[ii].spines['top'].set_visible(False)   
                            axs[ii].annotate(channel, xy=(0.96,0.7), va = 'center',xycoords='axes fraction',fontsize=11)
                            #axs[ii].set_ylim(meanmin,meanmax)   
                        
                        for ii in range(ncp-1):    
                            axs[ii].set_xticklabels('')
                                
                        axs[ncp-1].set_xlabel('Time (seconds)',fontsize=11)
                        
                        plt.subplots_adjust(top=0.94,left=0.1,bottom=0.2)
                        plt.tight_layout()
                        plt.savefig(newdir + "repaired_time="+ str(start) + "_channels" + str(startch) + ".pdf",format='pdf')
                        plt.close(fig)   
            

                #plot channels
                for start in startspot2:
                    print("Making longer plots for time = " + str(start))
            
                    start_stop_seconds = np.array([start, start + timelen2])
                    start_sample, stop_sample = (start_stop_seconds * sampling_freq).astype(int)
                    
                            
                    for chrange in chranges:
                        ncp = chrange[1] - chrange[0]
                        startch = chrange[0]
                    
                        fig, axs = plt.subplots(ncp, 1,figsize=(10,0.6*ncp))
 
                         
                        for ii in range(ncp):
                        
                            channel = newnames[startch + ii]
                            channeldata = raw_downsampled[channel, start_sample:stop_sample]
                            x = channeldata[1]
                            y = (channeldata[0].T)/(1e-6)    
                        
                            axs[ii].plot(x,y,c='black',linewidth=0.4)     
                        
                            axs[ii].yaxis.grid(False)
                            axs[ii].spines['right'].set_visible(False)
                            axs[ii].spines['top'].set_visible(False)   
                            axs[ii].annotate(channel, xy=(0.96,0.7), va = 'center',xycoords='axes fraction',fontsize=11)
                        
                        for ii in range(ncp-1):    
                            axs[ii].set_xticklabels('')
                                
                        axs[ncp-1].set_xlabel('Time (seconds)',fontsize=11)
                        
                        plt.subplots_adjust(top=0.94,left=0.1,bottom=0.2)
                        plt.tight_layout()
                        plt.savefig(newdir + "longer_time="+ str(start) + "_channels" + str(startch) + ".pdf",format='pdf')
                        plt.close(fig)   
                     
                                      
                        fig, axs = plt.subplots(ncp, 1,figsize=(10,0.6*ncp))

                               
                        for ii in range(ncp):
                        
                            channel = newnames[startch + ii]
                            channeldata = raw_downsampled[channel, start_sample:stop_sample]
                            x = channeldata[1]
                            y = (channeldata[0].T)/(1e-6)    
                        
                            axs[ii].plot(x,y,c='black',linewidth=0.4)     
                        
                            axs[ii].yaxis.grid(False)
                            axs[ii].spines['right'].set_visible(False)
                            axs[ii].spines['top'].set_visible(False)   
                            axs[ii].annotate(channel, xy=(0.96,0.7), va = 'center',xycoords='axes fraction',fontsize=11)
                            axs[ii].set_ylim(meanmin/2,meanmax/2)   
                        
                        for ii in range(ncp-1):    
                            axs[ii].set_xticklabels('')
                                
                        axs[ncp-1].set_xlabel('Time (seconds)',fontsize=11)
                        
                        plt.subplots_adjust(top=0.94,left=0.1,bottom=0.2)
                        plt.tight_layout()
                        plt.savefig(newdir + "longer_sameaxis_time="+ str(start) + "_channels" + str(startch) + ".pdf",format='pdf')
                        plt.close(fig) 


               
                    plt.close('all')
                
                
                #use ransac to predict bad channels with and without filtering
                epochs = mne.make_fixed_length_epochs(raw_y,duration=2.0,preload=True)
                picks = mne.pick_types(epochs.info, eeg=True,
                                       include=[], exclude=[])
                picks = np.delete(picks,64)
                
                #epochs.info['bads'] = ['Cz']
                
                ransac = Ransac(verbose=True, picks=picks, n_jobs=1)
                #ransac = Ransac(verbose=True, picks=picks, n_jobs=1)
                
                
                epochs_clean = ransac.fit_transform(epochs)
                
                badchraw = ransac.bad_chs_        
                    
                
                epochs = mne.make_fixed_length_epochs(raw_downsampled,duration=2.0,preload=True)
                picks = mne.pick_types(epochs.info, eeg=True,
                                       include=[], exclude=[])
                picks = np.delete(picks,64)
                
                ransac = Ransac(verbose=True, picks=picks, n_jobs=1)
                epochs_clean = ransac.fit_transform(epochs)
                
                badchfiltered = ransac.bad_chs_           
                
                
                #print and save outputs of ransac predictions
                log = []
                log.append("Channel data for: ")
                log.append(raw_data_folder)
                log.append(raw_data_file)
                log.append('')
                log.append('Saved to: ')
                log.append(newdir)
                log.append('')
                
                if 'y' in dirinfo:
                    log.append('This replaced / added to old data. There could be files from the last time this ran')
                    log.append('')
                    
                log.append('Original sampling freq: ' + str(origfreq) + ' Hz')
                log.append('Downsampled to: ' + str(downfreq) + ' Hz')
                log.append('Bandpass filtered at: ' + str(lfreq) + ' to ' + str(hfreq) + ' Hz')
                log.append('')
                
                if susnames:
                    log.append('Weird channel names: The raw scan has stim channels or something, and that is weird')
                else:
                    log.append('Your channel names look fine')
                log.append('')                    
                
                log.append('Mean corr between channels (no artifacts): ' + str(round(meancorr,4)))
                log.append('Mean corr between channels (no long artifacts): ' + str(round(meancorr_longer,4)))
                log.append('Mean amplitude for channels: ' + str(round(meandiff,4)))
                log.append('Mean time dropped for channels (all artifacts): ' + str(round(np.mean(chdf['timeallartifacts']),2)))
                log.append('Mean time dropped for channels (longer artifacts): ' + str(round(np.mean(chdf['timelongartifacts']),2)))
                log.append('')
                
                log.append("Individual channel stats:")
                for nam in newnames:
                    subdf = chdf.loc[nam]
                    corr = str(round(subdf['corr_wo_art'],3))
                    amp = str(round(subdf['amplitude'],2))
                    secdr = str(int(subdf['allartifacts']))
                    timedrop = str(round(subdf['timeallartifacts'],2)) + ' s'

                    corr_longer = str(round(subdf['corr_w_art'],3))
                    secdr_longer = str(int(subdf['longartifacts']))
                    timedrop_longer = str(round(subdf['timelongartifacts'],2)) + ' s'                    
                    
                    
                    line = nam + ' : amp = ' + amp
                    log.append(line)
                    line = 'corr w/o artifacts = ' + corr + '; time artifacts = ' + timedrop + '; number artifacts = ' + secdr
                    log.append(line)
                    line = 'corr w/ artifacts = ' + corr_longer + '; time long artifacts = ' + timedrop_longer + '; number longer artifacts = ' + secdr_longer
                    log.append(line)
                    
                log.append('')
                
                log.append('RANSAC predicted bad channels')
                log.append('bad channels when no filtering:')
                log.append(badchraw)
                log.append('bad channels with filtering:')
                log.append(badchfiltered)
                log.append('')
                
                log.append('Channels with the lowest (w/o artifacts) correlation to other channels. Potentially bad:')
                for i in range(5):
                    x = channelcorr[i] + ': ' + str(round(channelcorrval[i],3))
                    log.append(x)
                log.append('')
                log.append('Channels with the highest (w/o artifacts) correlation to other channels. Potentially bad, but doubt it:')
                for i in range(5):
                    x = channelcorr[63-i] + ': ' + str(round(channelcorrval[63-i],3))
                    log.append(x)        
                log.append('')
                
                
                log.append('Channels with the lowest (w/ artifacts) correlation to other channels. Potentially bad:')
                for i in range(5):
                    x = channelcorr_longer[i] + ': ' + str(round(channelcorrval_longer[i],3))
                    log.append(x)
                log.append('')
                log.append('Channels with the highest (w/ artifacts) correlation to other channels. Potentially bad, but doubt it:')
                for i in range(5):
                    x = channelcorr_longer[63-i] + ': ' + str(round(channelcorrval_longer[63-i],3))
                    log.append(x)        
                log.append('')                
                
                
                log.append('Channels with lowest amplitude. Potentially bad:')
                for i in range(5):
                    x = channelamp[i] + ': ' + str(round(channelampval[i],3))
                    log.append(x)    
                log.append('')
                log.append('Channels with highest amplitude. Potentially bad:')
                for i in range(5):
                    x = channelamp[63-i] + ': ' + str(round(channelampval[63-i],3))
                    log.append(x) 
                    
                log.append('')
                log.append('Channels with most seconds dropped for all artifacts. Potentially bad:')
                for i in range(5):
                    x = channeldrop[63-i] + ': ' + str(round(channeldroppval[63-i],2))
                    log.append(x)                   
                    
                log.append('')
                log.append('Channels with most seconds dropped for long artifacts. Potentially bad:')
                for i in range(5):
                    x = channeldrop_longer[63-i] + ': ' + str(round(channeldroplongerval[63-i],2))
                    log.append(x)                        
                    
                log.append('')
                log.append('Signals are recorded in microvolts')
                log.append('')
                log.append('"Amplitude" here means the median difference between high and low signal across 0.1 s segments')
                log.append("Not exactly amplitude, but whatever")
                
            
                print("")
                with open(newdir+logname, 'w') as f:
                    for item in log:
                        f.write("%s\n" % item)
                        print(item)
                f.close()      
                
                                
                                
                         
                        




             

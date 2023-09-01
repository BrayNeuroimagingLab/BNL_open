#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 15:27:19 2022

@author: Kirk
"""


import os
import pandas as pd



#folder with all the participant folders
dir_start = '/Users/ivy/Desktop/Test_EEG/Test_EEG_BIDS/'
output_dir = '/Users/ivy/Desktop/Test_EEG/Test_EEG_output/'


#folder with all the participant folders
#dir_start = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/BIDS1/'
#output_dir = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/prepro1/'






#subjecthere = '01P'
subjecthere = 'all'

#get a list of everything in the starting directory
folders = os.listdir(dir_start)
folders.sort()


if subjecthere != 'all':
    folders2 = []
    for folder in folders:
        if folder.startswith('sub'):
            if subjecthere in folder:
                folders2.append(folder)
    folders = folders2



#print(subdf.to_string())
#print("")






#logbook name
logname = 'badepochs.txt'


#which file(s) do you want to look at?
sessions = [1,2,3,4]
tasks = ['DORA','RX','YT']







standardlength = [
['task-YT1',202],
['task-YT4',209],
['task-YT7',211],
['task-YT10',210],
['task-DORA1',200],
['task-DORA3',203],
['task-DORA6',202],
['task-DORA9',197],
['task-DORA12',201],
['task-RX2',200],
['task-RX4',210],
['task-RX7',208],
['task-RX9',213],
['task-RX10',204],]


raw_data_list = []
numalready = 0

#loop through all potential files and check if they actually exist. If they do, add them to a list
#for preprocessing
#at the same time, add output directories for each file to the list, and check if preprocessing
#has already occurred
        
strper = folders[0].split('_')[0]
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
                
                    output_data_folder_task = output_data_folder + raw_data_file[:-4] + '/afterICA/'
                    output_ch_data = output_data_folder_task + logname
                    
                    if os.path.isfile(output_ch_data):
                        alreadyprocessed = 'y'
                        numalready = numalready + 1
                    else:
                        alreadyprocessed = 'n'

                    persdata = [raw_data_folder,raw_data_file,output_data_folder,output_data_folder_task,alreadyprocessed]
                    raw_data_list.append(persdata)
                            
                            
print("")

outdata = []  
scan = []
channel = []  

totalbads = []

existlist = []

totbadorig = []
totbadorig_wo = []
totbadfix = []
totbadfix_wo = []

fixl = []

totbadfix_adj = []

numepochs = []

task = []

warninglist = []
taskwarning = []
 

for ses in sessions:
    sestext = 'ses-' + str(ses)
    
    
    #loop through each participant
    for dirinfo in raw_data_list: 
        
        raw_data_file = dirinfo[1]
        seshere = raw_data_file.split('_')[1]
        
        if seshere == sestext:
    
        
            raw_data_folder = dirinfo[0]
            
            output_data_folder = dirinfo[2]
            
            exists_q = dirinfo[4]
            
            existlist.append(exists_q)
                  
            #make a folder for saving outputs
            newdir = dirinfo[3]
            if not os.path.exists(newdir):
                os.makedirs(newdir)  
                
           
            
            if exists_q == 'y':
        
                #Fixing lagging relaxing video errors
                linelists = []
                with open(newdir+logname) as file:
                    for line in file:
                        linelists.append(line)
        
                for ln in range(len(linelists)):
                    line = linelists[ln]
                    if "After removing marked bad ICs:" in line:
                        lineofinterest = linelists[ln+1]
                        ls = lineofinterest.split('/')
                        numbad = int(ls[0])
                        numtotal = int(ls[1].split(' ')[0])
                        whichbadtext = linelists[ln+3][1:-2]
                        if len(whichbadtext) > 0:
                            whichbadstr = whichbadtext.split(',')
                            #if len(whichbad) > 1:
                            whichbad = [int(bad) for bad in whichbadstr]
                        else:
                            whichbad = []
                        
                        
                        
                lagproblem = 4
                ls = raw_data_file.split('_')
                taskhere = ls[2]
                for stand in standardlength:
                    tas = stand[0]
                    stanlen = stand[1]
                    if tas == taskhere:
                        if numtotal > stanlen:
                            lagproblem = 1
                            warning = 'For ' + raw_data_file + ', length should be ' + str(stanlen) + ' but it is ' + str(numtotal)
                            print(warning)  
                            numtodrop = numtotal - stanlen
                            
                            print("You've already dropped " + str(len(whichbad)) + ' epochs: ' + str(whichbad))
                            
                            origdrop = list(range(stanlen,numtotal))
                            norigdrop = 0
                            for ep in origdrop:
                                if ep in whichbad:
                                    norigdrop = norigdrop + 1
                                    
                            ntodrop = numtodrop - norigdrop        
                            print(str(norigdrop) + " of those are in the extra, so you should drop " + str(ntodrop))
                            print('')
                            
        
                        else:
                            lagproblem = 0
                            warning = 'For ' + raw_data_file + ', length matches what it should be'
                            print(warning)     
        
        
            taskhere = raw_data_file.split('_')[2]
            task.append(taskhere)
            scan.append(raw_data_file)
    
    
    print('')
    print('')
    
    
    
    
    












                
                

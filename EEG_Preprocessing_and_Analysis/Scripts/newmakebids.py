#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This program renames .raw EEG files and sorts them to meet BIDS naming conventions
For example, this file:
    foldertosearch/1973001p4yt10_20210719_044759.raw
Will become:
    newfolder/sub-1973001P/ses-4/eeg/sub-1973001P_ses-4_task-YT10_eeg.raw


It assumes the raw files are written like this:
    1973001c2yt4_randomothertextordigits.raw
where 1973 is a starting file name that's the same for all files
1973001 is the participant ID (should be exactly 7 characters)
c is the age (should be 1 character)
2 is the session number (should be 1 character)
yt is the task. This can be any number of characters
4 is the task number. Can be any number of characters

Age and task can be written in lower or upper case. Doesn't matter. It's converted to uppercase

Appropriate tasks should be specified in the task dictionary (variable name appropfiletypes)

Any text written after the first underscore (_) is ignored


If two files have the same potential BIDS name, for example:
    1973001c4yt10_20210719_061930.raw
    1973001c4yt10_real_20210719_062052.raw
The program will tell you that there are duplicates, and you'll have to manually deal with duplicates
If you want both, you could manually rename and move one of them to the BIDS folder
Or you could rename one to be something like:
    1973001c4yt10-real_20210719_062052.raw  
    1973001c4yt10-v2_20210719_062052.raw
    1973001c4yt10ignoreotherfile_20210719_062052.raw      
I dunno, up to you. There's probably some official BIDS rule



"""


#folder with all the raw EEG scans
#the scans can be in subfolders in this folder, the program searches all subdirectories within this directory
foldertosearch = '/Users/ivy/Desktop/Test_EEG/Test_EEG_rawfiles/'


#folder where you want EEG scans saved in BIDS format
newfolder = '/Users/ivy/Desktop/Test_EEG/Test_EEG_BIDS/'

#appropriate tasks dictionary, and what they should be renamed to
appropfiletypes = {'D':'DORA','RS':'RX','YT':'YT','IS':'IS'}

#what the raw file names start with. This is basically used to detect files to ignore
startoffile = '1973'

#do you want to copy all the files, or only some? Only some is good if you're not 100% sure you've specified things right
#put either 'all', or a specific number
numfilescopy = 'all'
#numfilescopy = 4





#you shouldn't have to change anything after this point

import os
from shutil import copyfile

#get list of all .raw files in the folder specified
potentialfiles = []

for path, subdirs, files in os.walk(foldertosearch):
    for name in files:
        if name.endswith('.raw') and not name.startswith('._'):
            filesizetest = os.path.getsize(os.path.join(path, name))/1e6           
            potentialfiles.append([os.path.join(path, name),name,filesizetest])





#if only copying some files, only look at those
if numfilescopy != 'all':
    potentialfiles = potentialfiles[:numfilescopy]

newnamelist = []
newdestlist = []
alreadylist = []
repeatlist = []
newfilelist = []
filesizelist = []
for files in potentialfiles:
    filename = files[1]
    filesize = files[2]
    filesizestr = str(int(filesize))
    subname = filename.split('_')[0]
    if not subname.startswith(startoffile):
        print("Not sure what this is, doesn't start with right number: " + filename)
    else:
        subid = subname[:7]
        age = subname[7].upper()
        session = subname[8]
        filetype = subname[9:].upper()

        falsecount = 0
        for startname in appropfiletypes.keys():
            if not filetype.startswith(startname):
                falsecount = falsecount + 1
        
        if falsecount == len(appropfiletypes.keys()):
            print("Not sure what this is, no task match: " + filename)
            
        elif filesize < 50:
                print("File size for this weirdly small: " + filename + ' (' + filesizestr + ' MB)')
        else:    
            for startname in appropfiletypes.keys():
                if filetype.startswith(startname):
                    filenum = filetype.split(startname)[1]
                    filename = appropfiletypes[startname]
                    
                    newname = 'sub-' + subid + age + '_ses-' + session + '_task-' + filename + filenum + '_eeg.raw'
                    newdest = newfolder + 'sub-' + subid + age + '/ses-' + session + '/eeg/'
                    
                    #check if output already exists
                    if os.path.exists(newdest + newname):
                        already = True
                    else:
                        already = False

                    if newname in newnamelist:
                        repeatlist.append(True)
                        indices = [i for i, xa in enumerate(newnamelist) if xa == newname]
                        for dex in indices:
                            repeatlist[dex] = True
                    else:
                        repeatlist.append(False)
                    
                    newnamelist.append(newname)
                    newdestlist.append(newdest)
                    alreadylist.append(already)
                    newfilelist.append(files[0])
                    filesizelist.append(filesize)
             
arepeat = False
for rnum in range(len(repeatlist)):
    repeat = repeatlist[rnum]
    filesize = filesizelist[rnum]
    filesizestr = str(int(filesize))
    if repeat:
        print("These files showed up twice: " + newfilelist[rnum] + ' (' + filesizestr + ' MB)')
        arepeat = True

if arepeat:
    print('')
    print("Repeated files are ignored. Please manually deal with them.")
    print('')

alreadynum = 0
newlenlist = 0
for rnum in range(len(repeatlist)):
    repeat = repeatlist[rnum]
    already = alreadylist[rnum]
    if not repeat:
        newlenlist = newlenlist + 1
        if already:
            alreadynum = alreadynum + 1
            


#ask if you want to preprocess based on how many files exist
#ask to delete files that already exist, and ask to overwrite / add to files that already exist
proceed = False   
deleteold = False
alreadydone = False                
if len(repeatlist) == 0:
    print("There are no files to copy")
else:
    print("")
    numfiles = newlenlist
    print("You have selected " + str(numfiles) + " files to potentially copy.")
    print(str(alreadynum) + " files already have existing data.")
    if numfiles == 0:
        print("You don't need to copy files, apparently!")
        alreadydone = True        
    print("")
    
    if alreadynum > 0:  #if there aren't already existing files, no point to ask to delete/replace old
        while True:
            print("Delete old data in BIDS folder? This cannot be undone, and goes into effect instantly.")
            val = input("(y/n): ")
            if val == 'y' or val == 'n':
                if val == 'y':
                    deleteold = True
                break
            else:
                print("Did not understand input.")
                print("")
                continue

        #if we're deleting data, carry out this code
        if deleteold:
            for rnum in range(len(repeatlist)):
                repeat = repeatlist[rnum]
                already = alreadylist[rnum]
                destinationfile = newdestlist[rnum] + newnamelist[rnum]
                if not repeat:
                    if already:
                        os.remove(destinationfile)
                        print("Deleted " + destinationfile)
                        alreadylist[rnum] = False
    
                
        #check how many files exist after potentially deleting files        
        newalreadynum = 0
        newlenlist = 0
        for rnum in range(len(repeatlist)):
            repeat = repeatlist[rnum]
            already = alreadylist[rnum]
            if not repeat:
                newlenlist = newlenlist + 1
                if already:
                    newalreadynum = newalreadynum + 1
        
        print("")
        print("You have selected " + str(newlenlist-newalreadynum) + " files to generate data.")
        print(str(newalreadynum) + " files already exist.")               
    
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
    for rnum in range(len(repeatlist)):
        repeat = repeatlist[rnum]
        already = alreadylist[rnum]
        if not repeat:
            if not already:
                origfile = newfilelist[rnum]
                destinationfile = newdestlist[rnum] + newnamelist[rnum]
                print("Copying " + origfile)
                
                if not os.path.exists(newdestlist[rnum]):
                    os.makedirs(newdestlist[rnum])
                copyfile(origfile, destinationfile)
             








            
        

        
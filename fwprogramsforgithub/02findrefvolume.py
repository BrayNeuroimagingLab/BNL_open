"""
Determine Reference Volumes & Count Number of Volumes

This program does 3 things
1) It does a rigid body realignment of a 4D image to the first volume, creating
motion estimates - via mcflirt
2) It looks at the FD (framewise displacement) for volumes roughly in the middle of the scan
and determines the one with the least amount of motion. This becomes the reference volume.
A table of 4D images and their reference volume is saved
3) Checks how many volumes are in a 4D image. This can be used to debug. For example,
if a 4D image only has 50 volumes (and you're expecting 150), step 2 will give odd results

You generally only need to run step 1 and 2. Step 3 is just for debugging, basically





Made by Kirk Graff
kirk.graff@ucalgary.ca

Please email me if you have any questions :)
I'm not the best programmer so apologies if something is coded oddly!


Make sure your scans are in BIDS format before running
Edit the things near the top, and the program should run fine!

"""

"""***********************"""
"""GENERAL PROGRAM OPTIONS"""
"""***********************"""
#what directory are your images saved in?
dir_start = '/Users/example/example/directory_with_all_MRI_scans_in_BIDS_format/'


#where the reference volumes file is saved
#if this file doesn't exist, the program will create it
Location = '/Users/example/example/xrefvolumes.csv'

#what participants do you want this to run on? e.g. [1,2,3] or list(range(1,4))
participants = list(range(0,24))

#do you want to run on ses-0, ses-12, or both? If both, type ["ses-0","ses-12"]
imagesession = ["ses-0","ses-12"]

#if replacer is false, temprealign won't run if file already in reference volume list or if output file already exists
#if replacer is true, temprealign will run even if file already in reference volume list
replacer = False

#name of log book that output is saved to
logname = 'xfindref.txt'



#what steps do you want to run? Possible steps are temprealign, refvol, volcount
steps = ['temprealign','refvol','volcount']
#temprealign = Use MCFLIRT to warp to first volume. Generate FD based on this
#refvol = Look through FD to determine reference volumes
#volcount = read through FD list. Count how many volumes there are in 4D data


"""***************"""
"""PROGRAM OPTIONS"""
"""***************"""
inputepi = "task-movie_bold"
outputepi = "task-movie_boldMcFto0"
outputfd = "task-movie_boldMcFto0.nii.gz_rel.rms"


"""*****************************************"""
"""ANYTHING BELOW HERE DOESN'T NEED CHANGING"""
"""**********(OR SO KIRK HOPES)*************"""
"""*****************************************"""

import nipype.interfaces.fsl as fsl
import os
import pandas as pd
import time




#get the current time
totaltimer = time.time()

#get a list of everything in the starting directory
participant_folders = os.listdir(dir_start)

#Start what will be added to the log book for this session
log = ["*************************************************"]
log.append('Starting log for ' + time.ctime())


#if your specified reference volume file doesn't exist, this creates it
if os.path.isfile(Location) == False:
    refdata = [('test',255)]
    df = pd.DataFrame(data = refdata, columns=['File', 'Ref_Volume'])
    
    os.chdir(dir_start)
    #save the data frame as a csv file
    df.to_csv(Location,index=False,header=True)


#Code here is based off of code in the func preprocessing program. See there for more info

for k in steps:
    
    if k == 'temprealign':
        df = pd.read_csv(Location)
        files = list(df['File'])
        refframes = list(df['Ref_Volume'])
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/" + j + "/func/"
                input_file = dir_in + person + "_" + j + "_" + inputepi + ".nii.gz"
                output_file = dir_in + person + "_" + j + "_" + outputepi + ".nii.gz"
                ref_name = person + "_" + j + "_" + outputfd
                if os.path.isfile(input_file) == False:
                    input_file = dir_in + person + "_" + j + "_" + inputepi + ".nii"
                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x)
                else:
                    doit = True
                    if replacer == False:
                        if ref_name in files:
                            x = "Mcflirt did not run, " + person + " " + j + " is already in the reference list."
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        if replacer == False:
                            if os.path.isfile(dir_in + ref_name) == True:
                                x = "McFlirt did not run; this file already exists " + ref_name
                                print(x)
                                log.append(x)
                                doit = False                            
                    if doit == True:
                        steptimer = time.time()

                        x = "McFlirt is beginning to run."
                        print(x)
                        log.append(x)
                        try:
                            os.chdir(dir_in)
                            mymcf = fsl.MCFLIRT()
                            mymcf.inputs.in_file = input_file
                            mymcf.inputs.out_file = output_file
                            mymcf.inputs.save_mats = True
                            mymcf.inputs.save_plots = True
                            mymcf.inputs.save_rms = True
                            mymcf.inputs.ref_vol = 0
                            mymcf.run()                        
                            
                            x = "McFlirt probably created " + output_file
                            print(x)
                            log.append(x)      
                        except:
                            x = "McFlirt failed."
                            print(x)
                            log.append(x)
                        steptimer = round(time.time()-steptimer,3)
                        x = "Individual step took " + str(steptimer) + " s to run."
                        print(x)
                        log.append(x)
                        steptimermin = round(steptimer/60,3)
                        x = "(which is " + str(steptimermin) + " minutes)"
                        print(x)
                        log.append(x)
                        

    if k == 'refvol':
        df = pd.read_csv(Location)
        files = list(df['File'])
        refframes = list(df['Ref_Volume'])
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/" + j + "/func/"
                x = []
                input_file = person + "_" + j + "_" + outputfd
                if os.path.isfile(dir_in + input_file) == False:
                    if input_file in files:
                        x = "Refvol did not run. This file already in reference list (and also no longer exists): " + input_file
                        print(x)
                        log.append(x)
                    else:                        
                        x = "Refvol did not run. This file doesn't exist: " + input_file
                        print(x)
                        log.append(x)
                else:                  
                    os.chdir(dir_in)
                    if not input_file in files:
                        f = open(input_file, "r")
                        for num in f:
                            x.append(float(num))
                        #define the reference volume as the one with the smallest FD roughly in the middle volumes
                        try:
                            thelength = len(x)
                                                        
                            minrange = int(thelength/2-10)
                            maxrange = int(thelength/2+10)
                            
                            if minrange < 0:
                                minrange = 0
                            
                            y = min(x[minrange:maxrange])
                            refframes.append(x.index(y))
                            files.append(input_file)
                            x = person + " " + j + " added to reference list. The reference volume is " + str(x.index(y))
                            print(x)
                            log.append(x)
                        except:
                            x = "Refvol failed for " + person + " " + j + ". Perhaps the image was too short."
                            print(x)
                            log.append(x)                            
                    else:
                        x = "Refvol did not run, " + person + " " + j + " is already in the reference list."
                        print(x)
                        log.append(x)                        

        #create a data frame with the file name and its reference volume
        refdata = list(zip(files,refframes))
        df = pd.DataFrame(data = refdata, columns=['File', 'Ref_Volume'])

        os.chdir(dir_start)
        #print(df)
        #save the data frame as a csv file
        df.to_csv(Location,index=False,header=True)


    if k == 'volcount':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/" + j + "/func/"
                fdlist = []
                input_file = person + "_" + j + "_" + outputfd
                if os.path.isfile(dir_in + input_file) == True:
                    os.chdir(dir_in)
                    f = open(input_file, "r")
                    for num in f:
                        fdlist.append(float(num))
                    x = input_file + " has this many volumes: " + str(len(fdlist))
                    print(x)
                    log.append(x)
                else:
                    x = "this file does not exist: " + input_file
                    print(x)
                    log.append(x)                    




#subtract the new current time from the old current time. Also convert to minutes. Add to log
totaltimer = round(time.time()-totaltimer,3)
totaltimermin = round(totaltimer/60,3)
totaltimerhour = round(totaltimermin/60,3)
x = "All steps took " + str(totaltimer) + " s to run."
print(x)
log.append(x)
x = "(which is " + str(totaltimermin) + " minutes)"
print(x)
log.append(x)
x = "(which is " + str(totaltimerhour) + " hours)"
print(x)
log.append(x)

x = 'The end date/time is ' + time.ctime()
print(x)
log.append(x)

os.chdir(dir_start)
#add a couple blank lines to the log list, to make it look nicer
log.append('')
log.append('')

#open the log file, add the log list to the file
#'a' means append. You could also write a new file every time, if you wanted
with open(logname, 'a') as f:
    for item in log:
        f.write("%s\n" % item)
f.close()                    


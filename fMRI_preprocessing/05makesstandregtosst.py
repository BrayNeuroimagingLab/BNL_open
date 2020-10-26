"""

This aligns reference images to a template using ANTs registration. Or it can create a study specific template
This program also (very crudely) judges the quality of registrations


Made by Kirk Graff
kirk.graff@ucalgary.ca

Please email me if you have any questions :)
I'm not the best programmer so apologies if something is coded oddly!


Make sure your scans are in BIDS format before running
Edit the things near the top, and the program should run fine!


Make sure to run this program after basic functional preprocessing






Info on 'quality checking':
I noticed ANTs registration for functional to functional images routinely failed 
in very obvious ways. A lot of brains ended up with "horns" for some reason, among other issues
Usually rerunning ANTs fixed this issue
To save myself a lot of quality checking, this program can automatically crudely judge if a registration failed
horribly, and then try to fix it. This was more of a Friday afternoon, proof-of-concept addition to this script


THIS IS NOT A REPLACEMENT FOR ACTUALLY QUALITY CHECKING YOUR REGISTRATIONS
THIS IS ONLY INTENDED TO FIND REALLY REALLY BAD REGISTRATIONS


It works by using a "core" region, and an outer region

qccore = a region relative to your template where registered images should fill every voxel of this region
qcouter = a region relative to your template where registered images shouldn't have any voxels beyond it

In a perfect world, every registered image would exactly line up with your template. But that doesn't happen
But we can still say that every registered image should exist within a space slightly smaller than and slightly bigger than the template


The numbers I used to judge quality likely won't work for you, but you can test it out
Have fun. Or just ignore this feature


If you know a better way to automatically quality check registrations, let me know :)
Sad to say I still preferred ANTs to FSL registration approaches

"""



"""***********************"""
"""GENERAL PROGRAM OPTIONS"""
"""***********************"""
#what directory are your images saved in?
dir_start = '/Users/example/example/directory_with_all_MRI_scans_in_BIDS_format/'

#your template and its mask, for registration
templateimage = '/Users/example/example/SST.nii.gz'
templatemask = '/Users/example/example/SST_mask.nii.gz'

#outer and inner core
#If you're not sure what to use,
#make qcouter the same as templatemask, and qccore as some smaller/eroded version of qcouter
#(or just set qccore=qcouter=templatemask and ignore the quality values this program spits out)
qcouter = '/Users/example/example/SSTouterregion.nii.gz'
qccore = '/Users/example/example/SSTcoreregion.nii.gz'

#what participants do you want this to run on? e.g. [1,2,3] or list(range(1,4))
#this is based on the files in the directory. 0 = first file in directory
participants = list(range(0,24))

#do you want to run on ses-0, ses-12, or both? If both, type ["ses-0","ses-12"]
imagesession = ["ses-0","ses-12"]

steps = ['reg']
#reg = checks the quality of registration and fixes it, if desired
#sst = create a study specific template


#name of log book that output is saved to
logname = 'xregimprove.txt'






"""******************************"""
"""REGISTRATION CHECKER AND FIXER"""
"""******************************"""
#the registration checker will check the mask version of the below file. This will also be your final output when generating
#new images
bet2output = "task-movie_boldStcRefArBet"

arinput = "task-movie_boldStcRef"
aroutput = "task-movie_boldStcRefAr"

armatrixoutputname = "transformBOLDtoSST"
#the outputed matrix will add .h5 to the above name
#you'll also generate the inverse matrix that has added inverse.h5 to the above name

#higher BET value, the more the program will try to strip when removing non-brain from brain
bet2frac = 0.35


#how many times the program will try to regenerate images if there are bad volumes
#use 1 if you just want to register your images once
#use 0 if you just want to check the quality and not try to fix broken images
#use a number bigger than 1 if you're crazy or something
regenerationattempts = 1

#maximum time the program can run for (in hours)
#use a ridiculously high number if you want it to run forever
maxtime = 1


#if this is True, the program will first run BET on the image in native space, then warp it
betfirst = False


#if True, the program will attempt to replace all images once, no matter what
replaceall = False


"""******************************************"""
"""AUTOMATIC MEDIOCRE QUALITY CHECKER OPTIONS"""
"""******************************************"""

#quality metric cut off. Only try to fix images below this threshold. Use 100 if you want
#to try to fix any image that doesn't meet overall criteria
#program will never try to fix a low quality image if it meets the criteria
#change the criteria if you aren't happy
#note that this has the potential to create crazy loops
qmco = 100


#bad quality metrics
#if the image falls outside these thresholds, the registered image will be marked as bad

#size of image in core / total size of image. If below this value, the image is bad
percent_in_core_low = 85
#size of image in core / total size of image. If above this value, the image is bad
percent_in_core_high = 95
#size of image not in core but in sst / total size of image. If above this value, image is bad
percent_not_in_core_in_sst = 20
#size of image not in sst / total size of sst. If above this value, image is bad
percent_not_in_sst = 0.25
#size of core that doesn't contain image / total size of sst. If above this value, image is bad
percent_not_in_core = 0.07


#quality scoring - if you want you can ignore these numbers...

#what is the ideal percent of the image that is in the core of the template?
idealpimage_sst_core = 90
#what is the penalty for parts of the image that are not in the core of the template?
penaltynimage_core = 250
#what is the penalty for parts of the image outside the template? First # is multiple, second # is a static penalty if any is outside template
penaltyimage_nsst = [30,5]





"""*******************************"""
"""STUDY SPECIFIC TEMPLATE OPTIONS"""
"""*******************************"""
sstdir = '/Users/example/example/'
filetosst = "task-movie_boldStcRefArBet"



"""*****************************************"""
"""ANYTHING BELOW HERE DOESN'T NEED CHANGING"""
"""**********(OR SO KIRK HOPES)*************"""
"""*****************************************"""

import nipype.interfaces.fsl as fsl
import nipype.interfaces.ants as ants
import os
import pandas as pd
import time
import shutil
import nibabel as nib
import numpy as np


maxtimes = maxtime*3600

#get the current time
totaltimer = time.time()

#get a list of everything in the starting directory
participant_folders = os.listdir(dir_start)

#everything in log gets saved to the logbook. Text often gets appended to log
log = ["*************************************************"]
log.append('Starting log for ' + time.ctime())


img = nib.load(qcouter)
template_data = img.get_fdata()

img = nib.load(qccore)
overlap_data = img.get_fdata()

#get shape of image data
shape = template_data.shape
dim_x = shape[0]
dim_y = shape[1]
dim_z = shape[2]

#loop over every possible voxel in 3D space
voltemplate = 0
volalloverlap = 0

for dimi in range(dim_x):
    for dimj in range(dim_y):
        for dimk in range(dim_z):
            if template_data[dimi][dimj][dimk] == 1:
                voltemplate = voltemplate + 1
            if overlap_data[dimi][dimj][dimk] == 1:
                volalloverlap = volalloverlap + 1






def checkdata():                
    whichperson = []
    session = []
    tvoxels = []
    ximage_sst_ol = []
    ximage_sst_nol = []
    ximage_nsst_nol = []
    xnimage_sst_ol = []
    xnimage_sst_nol = []
    
    xpimage_sst_ol = []
    xpimage_sst_nol = []
    xpimage_nsst_nol = []
    xpnimage_sst_ol = []
    xpnimage_sst_nol = []
    
    goodimage = []
    score = []
    
    
    for i in participants:
        person = participant_folders[i]
        for j in imagesession:
            dir_in = dir_start + person + "/" + j + "/func/"
            input_file = dir_in + person + "_" + j + "_" + bet2output + "_mask.nii.gz"
            input_file2 = dir_in + person + "_" + j + "_" + bet2output + "2_mask.nii.gz"
            if os.path.isfile(input_file) == False:
                if os.path.isfile(input_file2) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x)
                    whichperson.append(person)
                    session.append(j)
                    goodimage.append('N')
                    ximage_sst_ol.append(np.nan)
                    ximage_sst_nol.append(np.nan)
                    ximage_nsst_nol.append(np.nan)
                    xnimage_sst_ol.append(np.nan)
                    xnimage_sst_nol.append(np.nan)            
                    xpimage_sst_ol.append(np.nan)
                    xpimage_sst_nol.append(np.nan)
                    xpimage_nsst_nol.append(np.nan)
                    xpnimage_sst_ol.append(np.nan)
                    xpnimage_sst_nol.append(np.nan)
                    tvoxels.append(np.nan)
                    score.append(0)
                else:
                    x = "Now analyzing new image " + input_file2
                    print(x)
                    log.append(x)
                    
                    img = nib.load(input_file2)
                    image_data = img.get_fdata()
                    
                    numofvoxels2 = 0   
                    image_sst_ol2 = 0
                    image_sst_nol2 = 0
                    image_nsst_nol2 = 0
                    nimage_sst_ol2 = 0
                    nimage_sst_nol2 = 0
                    
                    #loop over every possible voxel in 3D space
                    for dimi in range(dim_x):
                        for dimj in range(dim_y):
                            for dimk in range(dim_z):
                                if image_data[dimi][dimj][dimk] == 1:
                                    numofvoxels2 = numofvoxels2 + 1
                                    if template_data[dimi][dimj][dimk] == 1:
                                        if overlap_data[dimi][dimj][dimk] == 1:
                                            image_sst_ol2 = image_sst_ol2 + 1
                                        else:
                                            image_sst_nol2 = image_sst_nol2 + 1
                                    else:
                                        image_nsst_nol2 = image_nsst_nol2 + 1
                                elif template_data[dimi][dimj][dimk] == 1:
                                    if overlap_data[dimi][dimj][dimk] == 1:
                                        nimage_sst_ol2 = nimage_sst_ol2 + 1
                                    else:
                                        nimage_sst_nol2 = nimage_sst_nol2 + 1
                        
                    pimage_sst_ol2 = round(image_sst_ol2/numofvoxels2*100,2)
                    pimage_sst_nol2 = round(image_sst_nol2/numofvoxels2*100,2)
                    pimage_nsst_nol2 = round(image_nsst_nol2/numofvoxels2*100,3)
                    pnimage_sst_ol2 = round(nimage_sst_ol2/voltemplate*100,3)
                    pnimage_sst_nol2 = round(nimage_sst_nol2/voltemplate*100,2)
        
                    quality2 = 'Y'
                    if pimage_sst_ol2 < percent_in_core_low:
                        quality2 = 'N'
                    if pimage_sst_ol2 > percent_in_core_high:
                        quality2 = 'N'
                    if pimage_sst_nol2 > percent_not_in_core_in_sst:
                        quality2 = 'N'
                    if pimage_nsst_nol2 > percent_not_in_sst:
                        quality2 = 'N'
                    if pnimage_sst_ol2 > percent_not_in_core:
                        quality2 = 'N'
                    
                    qualitymetric2 = 100 - pnimage_sst_ol2*penaltynimage_core - pimage_nsst_nol2*penaltyimage_nsst[0]
                    if pimage_nsst_nol2 > 0:
                        qualitymetric2 = qualitymetric2 - penaltyimage_nsst[1]
                    if pimage_sst_ol2 > idealpimage_sst_core:
                        qualitymetric2 = qualitymetric2 - (pimage_sst_ol2 - idealpimage_sst_core)*2
                    else:
                        qualitymetric2 = qualitymetric2 - (idealpimage_sst_core - pimage_sst_ol2)*2                        
                                                 
                    os.rename(input_file2,input_file)
                    os.rename(dir_in + person + "_" + j + "_" + bet2output + "2.nii.gz",dir_in + person + "_" + j + "_" + bet2output + ".nii.gz")
                    os.rename(dir_in + person + "_" + j + "_" + aroutput + "2.nii.gz",dir_in + person + "_" + j + "_" + aroutput + ".nii.gz")
                    os.rename(dir_in + armatrixoutputname + '2.h5',dir_in + armatrixoutputname + '.h5')
                    os.rename(dir_in + armatrixoutputname + '2inverse.h5',dir_in + armatrixoutputname + 'inverse.h5')
                    os.rename(dir_in + armatrixoutputname + '2inverse.nii.gz',dir_in + armatrixoutputname + 'inverse.nii.gz')
                    
                    whichperson.append(person)
                    session.append(j)
                    tvoxels.append(numofvoxels2)
                    ximage_sst_ol.append(image_sst_ol2)
                    ximage_sst_nol.append(image_sst_nol2)
                    ximage_nsst_nol.append(image_nsst_nol2)
                    xnimage_sst_ol.append(nimage_sst_ol2)
                    xnimage_sst_nol.append(nimage_sst_nol2)
                    xpimage_sst_ol.append(pimage_sst_ol2)
                    xpimage_sst_nol.append(pimage_sst_nol2)
                    xpimage_nsst_nol.append(pimage_nsst_nol2)
                    xpnimage_sst_ol.append(pnimage_sst_ol2)
                    xpnimage_sst_nol.append(pnimage_sst_nol2)
                    goodimage.append(quality2)
                    score.append(qualitymetric2)

                
            else:
                os.chdir(dir_in)
                x = "Now analyzing " + input_file
                print(x)
                log.append(x)
                
                img = nib.load(input_file)
                image_data = img.get_fdata()
                
                numofvoxels = 0   
                image_sst_ol = 0
                image_sst_nol = 0
                image_nsst_nol = 0
                nimage_sst_ol = 0
                nimage_sst_nol = 0
                
                #loop over every possible voxel in 3D space
                for dimi in range(dim_x):
                    for dimj in range(dim_y):
                        for dimk in range(dim_z):
                            if image_data[dimi][dimj][dimk] == 1:
                                numofvoxels = numofvoxels + 1
                                if template_data[dimi][dimj][dimk] == 1:
                                    if overlap_data[dimi][dimj][dimk] == 1:
                                        image_sst_ol = image_sst_ol + 1
                                    else:
                                        image_sst_nol = image_sst_nol + 1
                                else:
                                    image_nsst_nol = image_nsst_nol + 1
                            elif template_data[dimi][dimj][dimk] == 1:
                                if overlap_data[dimi][dimj][dimk] == 1:
                                    nimage_sst_ol = nimage_sst_ol + 1
                                else:
                                    nimage_sst_nol = nimage_sst_nol + 1
                    
                pimage_sst_ol = round(image_sst_ol/numofvoxels*100,2)
                pimage_sst_nol = round(image_sst_nol/numofvoxels*100,2)
                pimage_nsst_nol = round(image_nsst_nol/numofvoxels*100,3)
                pnimage_sst_ol = round(nimage_sst_ol/voltemplate*100,3)
                pnimage_sst_nol = round(nimage_sst_nol/voltemplate*100,2)
   
                quality = 'Y'
                if pimage_sst_ol < percent_in_core_low:
                    quality = 'N'
                if pimage_sst_ol > percent_in_core_high:
                    quality = 'N'
                if pimage_sst_nol > percent_not_in_core_in_sst:
                    quality = 'N'
                if pimage_nsst_nol > percent_not_in_sst:
                    quality = 'N'
                if pnimage_sst_ol > percent_not_in_core:
                    quality = 'N'
                
                qualitymetric = 100 - pnimage_sst_ol*penaltynimage_core - pimage_nsst_nol*penaltyimage_nsst[0]
                if pimage_nsst_nol > 0:
                    qualitymetric = qualitymetric - penaltyimage_nsst[1]
                if pimage_sst_ol > idealpimage_sst_core:
                    qualitymetric = qualitymetric - (pimage_sst_ol - idealpimage_sst_core)*2
                else:
                    qualitymetric = qualitymetric - (idealpimage_sst_core - pimage_sst_ol)*2
                    
                
                if os.path.isfile(input_file2) == True:
                    if quality == 'Y':
                        os.remove(input_file2)
                        os.remove(dir_in + person + "_" + j + "_" + bet2output + "2.nii.gz")
                        os.remove(dir_in + person + "_" + j + "_" + aroutput + "2.nii.gz")
                        os.remove(dir_in + armatrixoutputname + '2.h5')
                        os.remove(dir_in + armatrixoutputname + '2inverse.h5')
                        os.remove(dir_in + armatrixoutputname + '2inverse.nii.gz') 
                    if quality == 'N':
                        x = "Now analyzing new image " + input_file2
                        print(x)
                        log.append(x)
                        
                        img = nib.load(input_file2)
                        image_data = img.get_fdata()
                        
                        numofvoxels2 = 0   
                        image_sst_ol2 = 0
                        image_sst_nol2 = 0
                        image_nsst_nol2 = 0
                        nimage_sst_ol2 = 0
                        nimage_sst_nol2 = 0
                        
                        #loop over every possible voxel in 3D space
                        for dimi in range(dim_x):
                            for dimj in range(dim_y):
                                for dimk in range(dim_z):
                                    if image_data[dimi][dimj][dimk] == 1:
                                        numofvoxels2 = numofvoxels2 + 1
                                        if template_data[dimi][dimj][dimk] == 1:
                                            if overlap_data[dimi][dimj][dimk] == 1:
                                                image_sst_ol2 = image_sst_ol2 + 1
                                            else:
                                                image_sst_nol2 = image_sst_nol2 + 1
                                        else:
                                            image_nsst_nol2 = image_nsst_nol2 + 1
                                    elif template_data[dimi][dimj][dimk] == 1:
                                        if overlap_data[dimi][dimj][dimk] == 1:
                                            nimage_sst_ol2 = nimage_sst_ol2 + 1
                                        else:
                                            nimage_sst_nol2 = nimage_sst_nol2 + 1
                            
                        pimage_sst_ol2 = round(image_sst_ol2/numofvoxels2*100,2)
                        pimage_sst_nol2 = round(image_sst_nol2/numofvoxels2*100,2)
                        pimage_nsst_nol2 = round(image_nsst_nol2/numofvoxels2*100,3)
                        pnimage_sst_ol2 = round(nimage_sst_ol2/voltemplate*100,3)
                        pnimage_sst_nol2 = round(nimage_sst_nol2/voltemplate*100,2)
           
                        quality2 = 'Y'
                        if pimage_sst_ol2 < percent_in_core_low:
                            quality2 = 'N'
                        if pimage_sst_ol2 > percent_in_core_high:
                            quality2 = 'N'
                        if pimage_sst_nol2 > percent_not_in_core_in_sst:
                            quality2 = 'N'
                        if pimage_nsst_nol2 > percent_not_in_sst:
                            quality2 = 'N'
                        if pnimage_sst_ol2 > percent_not_in_core:
                            quality2 = 'N'
                        
                        qualitymetric2 = 100 - pnimage_sst_ol2*penaltynimage_core - pimage_nsst_nol2*penaltyimage_nsst[0]
                        if pimage_nsst_nol2 > 0:
                            qualitymetric2 = qualitymetric2 - penaltyimage_nsst[1]
                        if pimage_sst_ol2 > idealpimage_sst_core:
                            qualitymetric2 = qualitymetric2 - (pimage_sst_ol2 - idealpimage_sst_core)*2
                        else:
                            qualitymetric2 = qualitymetric2 - (idealpimage_sst_core - pimage_sst_ol2)*2                        
                        
                        if quality2 == 'Y':
                            x = "The new image meets quality criteria and will replace the old image. Congrats."
                            print(x)
                            log.append(x)                               
                            os.rename(input_file2,input_file)
                            os.rename(dir_in + person + "_" + j + "_" + bet2output + "2.nii.gz",dir_in + person + "_" + j + "_" + bet2output + ".nii.gz")
                            os.rename(dir_in + person + "_" + j + "_" + aroutput + "2.nii.gz",dir_in + person + "_" + j + "_" + aroutput + ".nii.gz")
                            os.rename(dir_in + armatrixoutputname + '2.h5',dir_in + armatrixoutputname + '.h5')
                            os.rename(dir_in + armatrixoutputname + '2inverse.h5',dir_in + armatrixoutputname + 'inverse.h5')
                            os.rename(dir_in + armatrixoutputname + '2inverse.nii.gz',dir_in + armatrixoutputname + 'inverse.nii.gz')
                            
                            numofvoxels = numofvoxels2
                            image_sst_ol = image_sst_ol2
                            image_sst_nol = image_sst_nol2
                            image_nsst_nol = image_nsst_nol2
                            nimage_sst_ol = nimage_sst_ol2
                            nimage_sst_nol = nimage_sst_nol2
                            pimage_sst_ol = pimage_sst_ol2
                            pimage_sst_nol = pimage_sst_nol2
                            pimage_nsst_nol = pimage_nsst_nol2
                            pnimage_sst_ol = pnimage_sst_ol2
                            pnimage_sst_nol = pnimage_sst_nol2
                            quality = quality2
                            qualitymetric = qualitymetric2                      
                            
                        if quality2 == 'N':
                            if qualitymetric2 < qualitymetric:
                                x = "New image does not meet criteria. New image quality is " + str(qualitymetric2) + ". Old image quality is " + str(qualitymetric)
                                print(x)
                                log.append(x)                                                                
                                x = "The new image is worse than the old image. The new image will be deleted."
                                print(x)
                                log.append(x)
                                os.remove(input_file2)
                                os.remove(dir_in + person + "_" + j + "_" + bet2output + "2.nii.gz")
                                os.remove(dir_in + person + "_" + j + "_" + aroutput + "2.nii.gz")
                                os.remove(dir_in + armatrixoutputname + '2.h5')
                                os.remove(dir_in + armatrixoutputname + '2inverse.h5')
                                os.remove(dir_in + armatrixoutputname + '2inverse.nii.gz') 
                            if qualitymetric2 > qualitymetric:
                                x = "New image does not meet criteria. New image quality is " + str(qualitymetric2) + ". Old image quality is " + str(qualitymetric)
                                print(x)
                                log.append(x)                                                                
                                x = "The new image is better than the old image. The new image will replace the old image."
                                print(x)
                                log.append(x)                                
                                os.rename(input_file2,input_file)
                                os.rename(dir_in + person + "_" + j + "_" + bet2output + "2.nii.gz",dir_in + person + "_" + j + "_" + bet2output + ".nii.gz")
                                os.rename(dir_in + person + "_" + j + "_" + aroutput + "2.nii.gz",dir_in + person + "_" + j + "_" + aroutput + ".nii.gz")
                                os.rename(dir_in + armatrixoutputname + '2.h5',dir_in + armatrixoutputname + '.h5')
                                os.rename(dir_in + armatrixoutputname + '2inverse.h5',dir_in + armatrixoutputname + 'inverse.h5')
                                os.rename(dir_in + armatrixoutputname + '2inverse.nii.gz',dir_in + armatrixoutputname + 'inverse.nii.gz')                                
                                
                                numofvoxels = numofvoxels2
                                image_sst_ol = image_sst_ol2
                                image_sst_nol = image_sst_nol2
                                image_nsst_nol = image_nsst_nol2
                                nimage_sst_ol = nimage_sst_ol2
                                nimage_sst_nol = nimage_sst_nol2
                                pimage_sst_ol = pimage_sst_ol2
                                pimage_sst_nol = pimage_sst_nol2
                                pimage_nsst_nol = pimage_nsst_nol2
                                pnimage_sst_ol = pnimage_sst_ol2
                                pnimage_sst_nol = pnimage_sst_nol2
                                quality = quality2
                                qualitymetric = qualitymetric2

 
                                        
                whichperson.append(person)
                session.append(j)
                tvoxels.append(numofvoxels)
                ximage_sst_ol.append(image_sst_ol)
                ximage_sst_nol.append(image_sst_nol)
                ximage_nsst_nol.append(image_nsst_nol)
                xnimage_sst_ol.append(nimage_sst_ol)
                xnimage_sst_nol.append(nimage_sst_nol)
                xpimage_sst_ol.append(pimage_sst_ol)
                xpimage_sst_nol.append(pimage_sst_nol)
                xpimage_nsst_nol.append(pimage_nsst_nol)
                xpnimage_sst_ol.append(pnimage_sst_ol)
                xpnimage_sst_nol.append(pnimage_sst_nol)
                goodimage.append(quality)
                score.append(qualitymetric)
                
    x = ""
    print(x)
    log.append(x)
    x = "Voxels in template is " + str(voltemplate)
    print(x)
    log.append(x)
    x = "Voxels in core region is " + str(volalloverlap)
    print(x)
    log.append(x)
    
    x = ""
    print(x)
    log.append(x)
                
    #regdf = pd.DataFrame({'person':whichperson,'session':session,'voxels':tvoxels,'image_sst_ol':ximage_sst_ol,'image_sst_nol':ximage_sst_nol,'image_nsst_nol':ximage_nsst_nol,'nimage_sst_ol':xnimage_sst_ol,'nimage_sst_nol':xnimage_sst_nol})
    #print(regdf.to_string())
    
    regpdf = pd.DataFrame({'person':whichperson,'session':session,'voxels':tvoxels,'image_sst_ol':xpimage_sst_ol,'image_sst_nol':xpimage_sst_nol,'image_nsst_nol':xpimage_nsst_nol,'nimage_sst_ol':xpnimage_sst_ol,'nimage_sst_nol':xpnimage_sst_nol,'good?':goodimage,'quality':score})
    regpdf_sort = regpdf.sort_values(by=['quality'], ascending=True, na_position='first')
    x = regpdf_sort.to_string()
    print(x)
    log.append(x)
    
    x = ""
    print(x)
    log.append(x)
    
    badimages = 0
    goodimages = 0
    for index, row in regpdf.iterrows():
        if row['good?'] == 'N':
            badimages = badimages + 1
            #print(row['person'], row['session'])
        if row['good?'] == 'Y':
            goodimages = goodimages + 1
    
    x = "There are " + str(goodimages) + " images that probably do not need realignment. But you should check."
    print(x)
    log.append(x)
    x = "There are " + str(badimages) + " images that need realignment."
    print(x)
    log.append(x)
    x = ""
    print(x)
    log.append(x)

    return regpdf;


def generate(regpdf):
    for index, row in regpdf.sort_values(by=['quality'], ascending=True, na_position='first').iterrows():
        if row['good?'] == 'N':
            regenthis = True
        else:
            regenthis = False
        if replaceall == True:
            regenthis = True
        if regenthis == True:
            if row['quality'] < qmco:
                #print(row['person'], row['session'])
                person = row['person']
                j = row['session']
                dir_in = dir_start + person + "/" + j + "/func/"
                input_file = dir_in + person + "_" + j + "_" + arinput + ".nii.gz"
                tempfile = dir_in + "tempbet.nii.gz"
                output_file = dir_in + person + "_" + j + "_" + aroutput + "2.nii.gz"
                if replaceall == True:
                    output_file = dir_in + person + "_" + j + "_" + aroutput + ".nii.gz"
                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x)
                else:
                    doit = True
                    if time.time()-totaltimer > maxtimes:
                        doit = False
                        x = "ANTS Registration did not run. The program has reached maximum time."
                        print(x)
                        log.append(x)                    
                    if doit == True:
                        steptimer = time.time()
                        os.chdir(dir_in)
        
                        x = "ANTs Registration will now try to run. Registration? I prefer Regisphilbin. Generating for " + output_file
                        print(x)
                        log.append(x)
                        try:
                                                     
                            myar = ants.Registration()
                            myar.inputs.fixed_image = templateimage
                            myar.inputs.fixed_image_masks = templatemask
                            myar.inputs.moving_image = input_file
                            
                            if betfirst == True:
                                mybet = fsl.BET()
                                mybet.inputs.in_file = input_file
                                #specify the fractional intensity for BET
                                mybet.inputs.frac = 0.3
                                mybet.inputs.robust = True   
                                mybet.inputs.out_file = tempfile
                                mybet.inputs.threshold = True
                                mybet.run()
                                
                                myar.inputs.moving_image = tempfile
    
                        
                            #kirk barely understands anything in this section. ANTs is poorly documented
                            #most of this was copied from some website
                            
                            myar.inputs.collapse_output_transforms = True                        
                            myar.inputs.num_threads = 1
                            myar.inputs.output_inverse_warped_image=True
                            myar.inputs.output_warped_image=True
                            myar.inputs.sigma_units=['vox']*3
                            myar.inputs.transforms=['Rigid', 'Affine', 'SyN']
                            myar.inputs.winsorize_lower_quantile=0.005
                            myar.inputs.winsorize_upper_quantile=0.995
                            myar.inputs.convergence_window_size=[10]
                            myar.inputs.metric_weight=[1.0]*3
                            myar.inputs.number_of_iterations=[[1000, 500, 250, 100],[1000, 500, 250, 100],[100, 70, 50, 20]]
                            myar.inputs.radius_or_number_of_bins=[32, 32, 4]
                            myar.inputs.sampling_percentage=[0.25, 0.25, 1]
                            myar.inputs.sampling_strategy=['Regular','Regular','None']
                            myar.inputs.shrink_factors=[[8, 4, 2, 1]]*3
                            myar.inputs.smoothing_sigmas=[[3, 2, 1, 0]]*3
                            myar.inputs.transform_parameters=[(0.1,),(0.1,),(0.1, 3.0, 0.0)]
                            myar.inputs.convergence_threshold=[1e-06]   
                            myar.inputs.use_histogram_matching=True
                            myar.inputs.metric=['MI', 'MI', 'CC']
                            myar.inputs.write_composite_transform=True
                            myar.inputs.initial_moving_transform_com = True

                            
                            
                            myar.run()
                            #rename all the output files to the names we've specified. Since they're better names than the default ones
                            os.rename('transform_Warped.nii.gz',output_file)
                            if replaceall == True:
                                os.rename('transformComposite.h5',armatrixoutputname + '.h5')
                                os.rename('transformInverseComposite.h5',armatrixoutputname + 'inverse.h5')
                                os.rename('transform_InverseWarped.nii.gz',armatrixoutputname + 'inverse.nii.gz')
                            else:                                 
                                os.rename('transformComposite.h5',armatrixoutputname + '2.h5')
                                os.rename('transformInverseComposite.h5',armatrixoutputname + '2inverse.h5')
                                os.rename('transform_InverseWarped.nii.gz',armatrixoutputname + '2inverse.nii.gz')    
                            x = "ANTs Registration probably created " + output_file
                            print(x)
                            log.append(x)
                        except:
                            x = "ANTs Registration failed."
                            print(x)
                            log.append(x)
                        steptimer = round(time.time()-steptimer,3)
                        steptimermin = round(steptimer/60,3)
                        x = "Individual step took " + str(steptimer) + " s to run."
                        log.append(x)
                        print(x)
                        x = "(which is " + str(steptimermin) + " minutes)"
                        print(x)
                        log.append(x)
                
                if replaceall == True:
                    input_file = dir_in + person + "_" + j + "_" + aroutput + ".nii.gz"
                    output_file = dir_in + person + "_" + j + "_" + bet2output + ".nii.gz"
                    output_mask = dir_in + person + "_" + j + "_" + bet2output + "_mask.nii.gz"
                else:
                    input_file = dir_in + person + "_" + j + "_" + aroutput + "2.nii.gz"
                    output_file = dir_in + person + "_" + j + "_" + bet2output + "2.nii.gz"
                    output_mask = dir_in + person + "_" + j + "_" + bet2output + "2_mask.nii.gz"                    
                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x)
                else:
                    doit = True
                    if doit == True:
                        steptimer = time.time()
        
                        x = "Place your BETs. BET is beginning to run."
                        print(x)
                        log.append(x)
                        try:
                            os.chdir(dir_in)
                            mybet = fsl.BET()
                            mybet.inputs.in_file = input_file
                            #specify the fractional intensity for BET
                            mybet.inputs.frac = bet2frac
                            mybet.inputs.robust = True   
                            mybet.inputs.mask = True
                            mybet.inputs.out_file = output_file
                            mybet.inputs.threshold = True
                            mybet.run()
                            
                            mymath = fsl.ImageMaths()
                            mymath.inputs.in_file = output_mask
                            mymath.inputs.out_file = output_mask
                            mymath.inputs.args = "-fillh"
                            mymath.run()
                            
                            x = "BET probably created " + output_file
                            print(x)
                            log.append(x)      
                        except:
                            x = "BET failed."
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

    return;

                     
#the big loop of steps. Each step follows the same basic format
#see comments for mcflirt1
for k in steps: 
    
    if k == 'reg':           
                           
        regpdf = checkdata()
        
        badimages = 0
        for index, row in regpdf.iterrows():
            if row['good?'] == 'N':
                badimages = badimages + 1
        
        while regenerationattempts > 0:
            if time.time()-totaltimer < maxtimes:
                if badimages > 0:
                    x = "Max remaining number of regeneration attempts is " + str(regenerationattempts)
                    print(x)
                    log.append(x)
                    x = "Max remaining time is " + str(round((maxtimes-(time.time()-totaltimer))/3600,3)) + " hours."
                    print(x)
                    log.append(x)            
                    regenerationattempts = regenerationattempts - 1
                    generate(regpdf)
                    regpdf = checkdata()        
                    badimages = 0
                    for index, row in regpdf.iterrows():
                        if row['good?'] == 'N':
                            badimages = badimages + 1
                else:
                    regenerationattempts = 0
            else:
                x = "The program has reached maximum time."
                print(x)
                log.append(x)         
                regenerationattempts = 0
            if replaceall == True:
                replaceall = False



    if k == 'sst':
        steptimer = time.time()
        #this code smooths images (for the purposes of making a study specific template, I guess)
        testdir = sstdir + filetosst + "/"
        smoothdir = testdir + "smooth/"
        if os.path.exists(smoothdir):
            shutil.rmtree(smoothdir)
        os.makedirs(smoothdir) 
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                input_file = testdir + person + "_" + j + "_" + filetosst + ".nii.gz"
                output_file = smoothdir + person + "_" + j + "_" + filetosst + "smooth.nii.gz"
                os.chdir(smoothdir)
                sm = fsl.Smooth()
                sm.inputs.in_file = input_file
                sm.inputs.sigma = 3.0
                sm.run()
                os.rename(smoothdir + person + "_" + j + "_" + filetosst + "_smooth.nii.gz",output_file)
                x = "Smoothin' probably done for " + output_file + ". You've been struck by a smooth criminal."
                print(x)
                log.append(x)         

        #this code makes a smoothed study specific template
        current_time = time.strftime("%y%m%d_%H%M")
        output_file = sstdir + "SST" + current_time + ".nii.gz"
        allimages = os.listdir(smoothdir)
        if ".DS_Store" in allimages:
            allimages.remove(".DS_Store")
        os.chdir(smoothdir)
        allbutfirst = allimages[1:len(allimages)]
        matharg = ""
        for m in allbutfirst:
            matharg = matharg + "-add " + m + " "
        matharg = matharg + "-div " + str(len(allimages))
        mymath = fsl.ImageMaths()
        mymath.inputs.in_file = allimages[0]
        mymath.inputs.out_file = output_file
        mymath.inputs.args = matharg
        mymath.run()
                        
        myrlt = fsl.Threshold()
        myrlt.inputs.in_file = output_file
        myrlt.inputs.out_file = output_file
        myrlt.inputs.use_robust_range = True
        myrlt.inputs.thresh = 10
        myrlt.inputs.use_nonzero_voxels = True
        myrlt.run()
           
        input_file = output_file
        output_file = sstdir + "SST" + current_time + "_mask.nii.gz"
    
        mybin = fsl.UnaryMaths()
        mybin.inputs.in_file = input_file
        mybin.inputs.out_file = output_file
        mybin.inputs.operation = 'bin'
        mybin.run()
                                
        mymath = fsl.ImageMaths()
        mymath.inputs.in_file = output_file
        mymath.inputs.out_file = output_file
        mymath.inputs.args = "-fillh"
        mymath.run()
    
        x = "Study specific template and mask created"
        log.append(x)
        print(x)
            
        steptimer = round(time.time()-steptimer,3)
        x = "Individual step took " + str(steptimer) + " s to run."
        log.append(x)
        print(x)        
        
        
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

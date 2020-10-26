"""
Does preprocessing that varies depending on motion correction model
Run this after running basic func preprocessing
Figure out what you want your pipeline to do, then run accordingly!

Create temporal mask
Detrends + demeans
Temporal filters
Calculates gs/csf signal/wm signal
Detrends+filters HMPs
Regresses
Remeans



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

#regression sub folder. Where all the outputs are saved
#if you want to test different pipelines, you'll want a different folder for each pipeline
regfolder = 'BandpassCensorGSR/'




#what participants do you want this to run on? e.g. [1,2,3] or list(range(1,4))
#this is based on the files in the directory. 0 = first file in directory
participants = list(range(1,59))


#do you want to run on ses-0, ses-12, or both? If both, type ["ses-0","ses-12"]
imagesession = ["ses-0","ses-12"]

#how many times per second data is sampled
#a better program would probably determine this automatically from the image data, but this program doesn't, at least for filtering
fs = 0.4


#if replacer is false, the program won't run if output image already exists
#if replacer is true, the program will write over outputs that already exist
replacer = False

#name of log book that output is saved to
logname = 'xadvpreprocessing.txt'



#what steps do you want the program to run? The steps are run in the order listed


steps = ['createtmask1','makedetrendreg','rundetrendreg','filterall','gs','ns','filterhmp','makereg','runreg','remean']


"""general steps"""
    #createtmask1 = create temporal mask - 1 volume censored per motion artifact
    #createtmask2 = create temporal mask - 2 volumes censored per motion artifact
    #createtmask3 = create temporal mask - 3 volumes censored per motion artifact
    #createtmask4 = create temporal mask - 4 volumes censored per motion artifact

"""ica-aroma steps"""
    #ica-aroma

"""detrend steps - removing linear and quadratic trend, and demean, via linear regression"""
    #makedetrendreg - make excel file with regression data
    #rundetrendreg - run detrend on whole brain

"""filter steps - run a bandpass filter via fft and ifft"""
    #filterall - filter the whole brain

"""signal steps"""
    #gs - find the global signal after filtering
    #ns - find the signal for CSF and WM after filtering

"""filter HMP"""
    #filterhmp - detrends + filters HMP data

"""regression steps"""
    #makereg - make excel file with all regression data
    #runreg - run full regression on whole brain    

"""remean steps"""
    #remean - add the mean to the output of the last step



"""*****************************************"""
"""createtmask: create temporal mask OPTIONS"""
"""*****************************************"""
tmaskinput = 'task-movie_boldMcf.nii.gz_rel.rms'

tmaskoutput = "MASK_TEMPORAL"

#anything above this value is marked for censoring
tmaskthreshold = 0.25
tmaskthreshold = 400

#first volume motion. Set above threshold to censor first volume. Or don't censor it, I dunno
tmaskfirstvolume = 1.0
tmaskfirstvolume = 0




"""*****************"""
"""ICA-AROMA OPTIONS"""
"""*****************"""
#If True, the input image will come from the main folder. If false, will come from regression folder
icamainfolder = False

#the program will add .nii.gz onto the end of these 3 files
icainput = "YCDet"
icamask = 'task-movie_boldStcRefBet_mask'
icaoutput = "YCDetICA"

#these 2 inputs need a suffix
icamatrix = 'transformBOLDtoAugustus.h5'
icamc = 'task-movie_boldMcf.nii.gz.par'

icafolder = 'ICA_outputs/'

templateimage = '/Users/example/example/SST.nii.gz'


"""**********************"""
"""MAKEDETRENDREG OPTIONS"""
"""**********************"""
#text file with global signal
mdtmaskname = "MASK_TEMPORAL"
#name of regressors file that is saved. Saved to regression subfolder
mdregname = 'detrend.csv'


"""*********************"""
"""RUNDETRENDREG OPTIONS"""
"""*********************"""
#If True, the input image will come from the main folder. If false, will come from regression folder
rdmainfolder = True
#file you want to run it on

#pipelines without ICA
rdimagename = "task-movie_boldStcMcf.nii.gz"


#spatial mask file. From the main folder
rdmaskname = "task-movie_boldStcRefConsbet_mask.nii.gz"

#temporal mask file. In the regression subfolder
rdtmaskname = "MASK_TEMPORAL"
#output file of just the residuals. Saved to regression subfolder

rdimagenameoutput = "NCDet.nii.gz"
#rdimagenameoutput = "YCDet.nii.gz"
#output file of the means. Saved to regression subfolder
rdmeanfile = "NCDet_Mean.nii.gz"

#input of all regressors. From the regression subfolder
rdreginput = 'detrend.csv'


"""**************"""
"""FILTER OPTIONS"""
"""**************"""
#file you want to run it on. From regression subfolder
filterimagename = "YCDetInt.nii.gz"
#spatial mask file
filtermaskname = "task-movie_boldStcRefConsbet_mask.nii.gz"
#output file of just the residuals. Saved to regression subfolder
filterimagenameoutput = "YCDetIntFlt.nii.gz"

#FILTERING SPECS
#if you set one of these to 0, it just won't do that type of filtering. So if highcut = 0, it'll be a highpass filter, not a bandpass
#highpass
lowcut = 0.01
#lowpass
highcut = 0.08


"""*******************************************"""
"""gs: fslmeants to find global signal OPTIONS"""
"""*******************************************"""
#input file - from the regression subfolder
gsinput = "YCDetIntFlt.nii.gz"

#spatial whole brain mask
gsmask = "task-movie_boldStcRefBet_mask.nii.gz"

#name of the file with the mean signal at each time point. To regression subfolder
gsoutput = "signalglobal"


"""*********************************************"""
"""ns: fslmeants to find nuisance signal OPTIONS"""
"""*********************************************"""
#input file - from the regression subfolder
nsinput = "YCDetIntFlt.nii.gz"

#CSF and WM spatial masks
nscsfmask = "MASKCSF.nii.gz"
nswmmask = "MASKWM.nii.gz"

#names of the files with the mean signal at each time point. To regression subfolder
nsoutputCSF = "signalCSFnuisance"
nsoutputWM = "signalWMnuisance"


"""*****************"""
"""filterhmp OPTIONS"""
"""*****************"""
#this code assumes that you want to use the same detrending as in the "detrend" step
#and that your filtering low and high pass are the same
#and your temporal mask is the same


#text file with 6 head alignment estimates
filterhmpinput = 'task-movie_boldMcf.nii.gz.par'

#output file of just the residuals. Saved to regression subfolder
filterhmpoutput = 'task-movie_boldMcf.nii.gz.par_flt.csv'


"""***************"""
"""MAKEREG OPTIONS"""
"""***************"""
#text file with 6 head alignment estimates
regheadmotionname = 'task-movie_boldMcf.nii.gz.par_flt.csv'

#temporal mask name
regtmaskname = "MASK_TEMPORAL"

#white matter signal text file - from regression directory
regwmname = 'signalWMnuisance'
#csf signal text file - from regression directory
regcsfname = 'signalCSFnuisance'
#text file with global signal - from regression directory
regglobalsigname = "signalglobal"

#name of regressors file that is saved
regname = 'regressors.csv'

#what to include in the regression
regglobal = True
regWM = True
regCSF = True
regHMP = True
regvolumes = True



"""**************"""
"""RUNREG OPTIONS"""
"""**************"""
#file you want to run it on
regimagename = "YCDetIntFlt.nii.gz"
#mask file
regmaskname = "task-movie_boldStcRefConsbet_mask.nii.gz"
#output file of just the residuals
regimagenameoutput = "YCDetIntFltRgwch.nii.gz"
#input of all regressors
reginput = 'regressors.csv'


"""**************"""
"""REMEAN OPTIONS"""
"""**************"""
#file you want to run it on
remeanimagename = "YCDetIntFltRgwch.nii.gz"
#mean file
remeanmean = "StcMcf_Mean.nii.gz"
#output file
remeanoutput = "YCDetIntFltRgwchRem.nii.gz"



"""*****************************************"""
"""ANYTHING BELOW HERE DOESN'T NEED CHANGING"""
"""**********(OR SO KIRK HOPES)*************"""
"""*****************************************"""

import nipype.interfaces.fsl as fsl
import os
import numpy as np
import pandas as pd
import nibabel as nib
import statsmodels.api as sm
#import matplotlib.pyplot as plt
import time
from scipy.fftpack import fft, ifft
import ICA_AROMA_functions_yellowjacket as aromafunc
import classification_plots
import subprocess
import shutil

#some ICA-AROMA code
scriptDir = os.path.dirname(os.path.abspath(__file__))
fslDir = os.path.join(os.environ["FSLDIR"], 'bin', '')
denType = 'both'
melDir = ''
icadim = 0
affmat = ''




#get the current time
totaltimer = time.time()

#get a list of everything in the starting directory
participant_folders = os.listdir(dir_start)

#everything in log gets saved to the logbook. Text often gets appended to log
log = ["*************************************************"]
log.append('Starting log for ' + time.ctime())



for k in steps: 

    if k == 'createtmask1':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/" + j + "/func/"
                input_file = dir_in + person + "_" + j + "_" + tmaskinput                
                regdir = dir_in + regfolder
                if not os.path.exists(regdir):
                    os.makedirs(regdir)
                output_file = regdir + person + "_" + j + "_" + tmaskoutput

                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x)
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file) == True:
                            x = "Temporal mask did not run; file already exists for " + output_file
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        steptimer = time.time()
                        x = "Temporal mask is beginning to run."
                        print(x)
                        log.append(x)
                        try:
                            fd = [tmaskfirstvolume]
                            with open(input_file) as file:
                                for line in file:
                                    fd.append(float(line))
                            
                            binarybad = []
                            for i in range(len(fd)):
                                if fd[i] > tmaskthreshold:
                                    binarybad.append(0)
                                else:
                                    binarybad.append(1)                            

                            with open(output_file, 'w') as f:
                                for item in binarybad:
                                    f.write("%s\n" % item)
                            f.close()                             
                            
                            x = "Temporal mask probably created " + output_file
                            print(x)
                            log.append(x)      
                        except:
                            x = "Temporal mask failed."
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


    if k == 'createtmask2':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/" + j + "/func/"
                input_file = dir_in + person + "_" + j + "_" + tmaskinput                
                regdir = dir_in + regfolder
                if not os.path.exists(regdir):
                    os.makedirs(regdir)
                output_file = regdir + person + "_" + j + "_" + tmaskoutput

                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x)
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file) == True:
                            x = "Temporal mask did not run; file already exists for " + output_file
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        steptimer = time.time()
                        x = "Temporal mask is beginning to run."
                        print(x)
                        log.append(x)
                        try:
                            fd = [tmaskfirstvolume]
                            with open(input_file) as file:
                                for line in file:
                                    fd.append(float(line))
                            
                            binarybad = []
                            for i in range(len(fd)):
                                if fd[i] > tmaskthreshold:
                                    binarybad.append(0)
                                else:
                                    binarybad.append(1)                            

                            #binarybad = [0,1,1,1,1,1,1,0]
                            aggrbinarybad = [1]*len(binarybad)
                            aggrbinarybad[0] = 0
                            for spot in range(1,len(binarybad)-1):
                                if binarybad[spot] == 0:
                                    aggrbinarybad[spot] = 0
                                    aggrbinarybad[spot+1] = 0
                            if binarybad[-1] == 0:
                                aggrbinarybad[-1] = 0                               

                            with open(output_file, 'w') as f:
                                for item in aggrbinarybad:
                                    f.write("%s\n" % item)
                            f.close()                             
                            
                            x = "Temporal mask probably created " + output_file
                            print(x)
                            log.append(x)      
                        except:
                            x = "Temporal mask failed."
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
    
    
    if k == 'createtmask3':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/" + j + "/func/"
                input_file = dir_in + person + "_" + j + "_" + tmaskinput                
                regdir = dir_in + regfolder
                if not os.path.exists(regdir):
                    os.makedirs(regdir)
                output_file = regdir + person + "_" + j + "_" + tmaskoutput

                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x)
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file) == True:
                            x = "Temporal mask did not run; file already exists for " + output_file
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        steptimer = time.time()
                        x = "Temporal mask is beginning to run."
                        print(x)
                        log.append(x)
                        try:
                            fd = [tmaskfirstvolume]
                            with open(input_file) as file:
                                for line in file:
                                    fd.append(float(line))
                            
                            binarybad = []
                            for i in range(len(fd)):
                                if fd[i] > tmaskthreshold:
                                    binarybad.append(0)
                                else:
                                    binarybad.append(1)                            

                            #binarybad = [0,1,1,1,1,1,1,0]
                            aggrbinarybad = [1]*len(binarybad)
                            aggrbinarybad[0] = 0
                            for spot in range(1,len(binarybad)-1):
                                if binarybad[spot] == 0:
                                    aggrbinarybad[spot-1] = 0
                                    aggrbinarybad[spot] = 0
                                    aggrbinarybad[spot+1] = 0
                            if binarybad[-1] == 0:
                                aggrbinarybad[-1] = 0
                                aggrbinarybad[-2] = 0                                

                            with open(output_file, 'w') as f:
                                for item in aggrbinarybad:
                                    f.write("%s\n" % item)
                            f.close()                             
                            
                            x = "Temporal mask probably created " + output_file
                            print(x)
                            log.append(x)      
                        except:
                            x = "Temporal mask failed."
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
                        
                        
    if k == 'createtmask4':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/" + j + "/func/"
                input_file = dir_in + person + "_" + j + "_" + tmaskinput                
                regdir = dir_in + regfolder
                if not os.path.exists(regdir):
                    os.makedirs(regdir)
                output_file = regdir + person + "_" + j + "_" + tmaskoutput

                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x)
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file) == True:
                            x = "Temporal mask did not run; file already exists for " + output_file
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        steptimer = time.time()
                        x = "Temporal mask is beginning to run."
                        print(x)
                        log.append(x)
                        try:
                            fd = [tmaskfirstvolume]
                            with open(input_file) as file:
                                for line in file:
                                    fd.append(float(line))
                            
                            binarybad = []
                            for i in range(len(fd)):
                                if fd[i] > tmaskthreshold:
                                    binarybad.append(0)
                                else:
                                    binarybad.append(1)                            

                            #binarybad = [0,1,1,1,1,1,1,0,0,1,1,1,1,0,1,1,1,1,1,0,0,1]
                            aggrbinarybad = [1]*len(binarybad)
                            aggrbinarybad[0] = 0
                            for spot in range(1,len(binarybad)-2):
                                if binarybad[spot] == 0:
                                    aggrbinarybad[spot-1] = 0
                                    aggrbinarybad[spot] = 0
                                    aggrbinarybad[spot+1] = 0
                                    aggrbinarybad[spot+2] = 0
                            if binarybad[-2] == 0:
                                aggrbinarybad[-1] = 0
                                aggrbinarybad[-2] = 0
                                aggrbinarybad[-3] = 0
                            if binarybad[-1] == 0:
                                aggrbinarybad[-1] = 0
                                aggrbinarybad[-2] = 0
                            #print(binarybad)
                            #print(aggrbinarybad)                                

                            with open(output_file, 'w') as f:
                                for item in aggrbinarybad:
                                    f.write("%s\n" % item)
                            f.close()                             
                            
                            x = "Temporal mask probably created " + output_file
                            print(x)
                            log.append(x)      
                        except:
                            x = "Temporal mask failed."
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

                            
 
    if k == 'ica-aroma':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/" + j + "/func/"
                regdir = dir_in + regfolder
                imagefile = dir_in + person + "_" + j + "_" + icainput + '.nii.gz'
                if icamainfolder == False:
                    imagefile = regdir + person + "_" + j + "_" + icainput + '.nii.gz'
                
                warp = dir_in + icamatrix
                inmask = dir_in + person + "_" + j + "_" + icamask + '.nii.gz'
                inFile = regdir + person + "_" + j + "_" + icainput + '_smooth.nii.gz'
                mc = dir_in + person + "_" + j + "_" + icamc
                outDir = regdir + icafolder
                outfiledefault = outDir + "denoised_func_data_aggr.nii.gz"
                outputfile = regdir + person + "_" + j + "_" + icaoutput + '.nii.gz'
                if not os.path.exists(regdir):
                    os.makedirs(regdir)                
                x = 'Smoothing for ' + person + ' ' + j
                print(x)
                log.append(x) 
                doit = True
                if replacer == False:
                    if os.path.isfile(inFile) == True:
                        x = "FSL smooth did not run; file already exists for " + inFile
                        print(x)
                        log.append(x) 
                        doit = False
                
                if doit == True:
                    steptimer = time.time()
                    os.chdir(regdir)
                    smoo = fsl.Smooth()
                    smoo.inputs.in_file = imagefile
                    smoo.inputs.fwhm = 6.0
                    smoo.run()
                    
                    steptimer = round(time.time()-steptimer,3)
                    x = "Individual step took " + str(steptimer) + " s to run."
                    print(x)
                    log.append(x) 
                
                doit = True
                if os.path.isfile(outputfile):
                    if replacer == True:
                        shutil.rmtree(outDir)
                        os.makedirs(outDir)
                    else:
                        x = "You already ran ICA-AROMA for " + person + ' ' + j
                        print(x)
                        log.append(x) 
                        doit = False
                elif os.path.exists(outDir):
                    shutil.rmtree(outDir)
                    os.makedirs(outDir)
                else:
                    os.makedirs(outDir)
                
                if doit == True:
                    x = 'Now running ICA-AROMA for ' + person + ' ' + j
                    print(x)
                    log.append(x) 
                    os.chdir(scriptDir)
                    mask = os.path.join(outDir, 'mask.nii.gz')
                    shutil.copyfile(inmask, mask)
                 
                    cmd = ' '.join([os.path.join(fslDir, 'fslinfo'),
                                    inFile,
                                    '| grep pixdim4 | awk \'{print $2}\''])
                    TR = float(subprocess.getoutput(cmd))    
                    
                    print('Step 1) MELODIC')
                    steptimer = time.time()
                    aromafunc.runICA(fslDir, inFile, outDir, melDir, mask, icadim, TR)
                                        
                    print('Step 2) Automatic classification of the components')
                    print('  - registering the spatial maps to MNI')
                    melIC = os.path.join(outDir, 'melodic_IC_thr.nii.gz')
                    melIC_MNI = os.path.join(outDir, 'melodic_IC_thr_MNI2mm.nii.gz')
                    aromafunc.register2MNI(fslDir, melIC, melIC_MNI, affmat, warp)
                    
                    print('  - extracting the CSF & Edge fraction features')
                    edgeFract, csfFract = aromafunc.feature_spatial(fslDir, outDir, scriptDir, melIC_MNI)
                    
                    print('  - extracting the Maximum RP correlation feature')
                    melmix = os.path.join(outDir, 'melodic.ica', 'melodic_mix')
                    maxRPcorr = aromafunc.feature_time_series(melmix, mc)
                    
                    print('  - extracting the High-frequency content feature')
                    melFTmix = os.path.join(outDir, 'melodic.ica', 'melodic_FTmix')
                    HFC = aromafunc.feature_frequency(melFTmix, TR)
                    
                    print('  - classification')
                    motionICs = aromafunc.classification(outDir, maxRPcorr, edgeFract, HFC, csfFract)
                    classification_plots.classification_plot(os.path.join(outDir, 'classification_overview.txt'),
                                                             outDir)
                
                    
                    print('Step 3) Data denoising')
                    aromafunc.denoising(fslDir, inFile, outDir, melmix, denType, motionICs)
                    
                    # Remove thresholded melodic_IC file
                    os.remove(melIC)
                                        
                    os.rename(outfiledefault,outputfile)
                    
                    steptimer = round(time.time()-steptimer,3)
                    x = "Individual step took " + str(steptimer) + " s to run."
                    print(x)
                    log.append(x) 
                    steptimermin = round(steptimer/60,3)
                    x = "(which is " + str(steptimermin) + " minutes)"
                    print(x)
                    log.append(x) 
        
    
    if k == 'makedetrendreg':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                #define file names for this specific kid
                dir_in = dir_start + person + "/" + j + "/func/"
                tmaskfile = dir_in + regfolder + person + "_" + j + "_" + mdtmaskname
                regoutput = dir_in + regfolder + person + "_" + j + "_" + mdregname

                if os.path.isfile(tmaskfile) == False:
                    x = "This file doesn't exist: " + tmaskfile
                    print(x)
                    log.append(x)
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(regoutput) == True:
                            x = "Make detrend data did not run; file already exists for " + regoutput
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        #find the current time
                        steptimer = time.time()
                                        
                        timelist = []
                        timelist2 = []
        
                        #increases by 1 for each volume in time series. Added to timelist and timelist2
                        currenttime = 0
                                  
                        #read in temporal mask
                        #also create a list of timepoints, ie 0, 1, 2, 3, 4, 5, etc
                        with open(tmaskfile, 'r') as file:
                            for line in file:
                                if int(line) == 1:
                                    timelist.append(currenttime)
                                    timelist2.append(currenttime**2)
                                currenttime = currenttime + 1
        
                        #create a dataframe of the time series, global signal, motion parameters, and the time course
                        allregressorsDF = pd.DataFrame(
                            {'Time' : timelist - np.mean(timelist),
                             'Time2' : timelist2 - np.mean(timelist2)
                            })
                        
                        #add a constant to dataframe
                        allregressorsDF = sm.add_constant(allregressorsDF)
                                        
                        #save regressors as a CSV file
                        allregressorsDF.to_csv(regoutput)
                        x = "Detrend data saved to " + regoutput
                        log.append(x)
                        print(x)
                        
                        #find the final time, save info to log
                        steptimer = round(time.time()-steptimer,3)
                        x = "Individual step took " + str(steptimer) + " s to run."
                        print(x)
                        log.append(x)    
                
                    
    if k == 'rundetrendreg':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                #define file names for this specific kid
                dir_in = dir_start + person + "/" + j + "/func/"
                regdir = dir_in + regfolder
                
                if rdmainfolder == True:
                    input_file = dir_in + person + "_" + j + "_" + rdimagename
                else:
                    input_file = regdir + person + "_" + j + "_" + rdimagename
                
                input_mask = dir_in + person + "_" + j + "_" + rdmaskname
                input_reg = regdir + person + "_" + j + "_" + rdreginput
                output_file = regdir + person + "_" + j + "_" + rdimagenameoutput
                mean_output = regdir + person + "_" + j + "_" + rdmeanfile
                tmaskfile = regdir + person + "_" + j + "_" + rdtmaskname

                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x)
                elif os.path.isfile(input_reg) == True:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file) == True:
                            x = "Detrend did not run; file already exists for " + output_file
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:

                        #find the current time
                        steptimer = time.time()
                        
                        #load the regression df
                        regdata = pd.read_csv(input_reg, index_col=0)

                        #load the temporal mask
                        tmask = []
                        with open(tmaskfile, 'r') as file:
                            for line in file:
                                tmask.append(int(line))
                        
                        timelist = list(range(0,len(tmask)))
                        
                        subtimelist = []
                        missingtime = []
                        
                        for data in range(len(tmask)):
                            if tmask[data] == 1:
                                subtimelist.append(timelist[data])
                            else:
                                missingtime.append(timelist[data])
                        
                        fulltime = subtimelist+missingtime
                        
                        #load the image using some package I found called NiBabel
                        img = nib.load(input_file)
                        image_data = img.get_fdata()
                        new_data = image_data.copy()
                              
                        #load the mask
                        img2 = nib.load(input_mask)
                        mask_data = img2.get_fdata()
                        mean_data = mask_data.copy()
                        
                        #get shape of image data
                        shape = image_data.shape
                        dim_x = shape[0]
                        dim_y = shape[1]
                        dim_z = shape[2]
                            
                        x = "Running the detrend for " + person + " " + j
                        print(x)
                        log.append(x)
                        
                        numofvoxels = 0
                        #loop over every possible voxel in 3D space
                        for dimi in range(dim_x):
                            print("Running for x dimension slice " + str(dimi + 1) + " of " + str(dim_x) + " for " + person + " " + j)
                            for dimj in range(dim_y):
                                for dimk in range(dim_z):                              
                                    #only create model if voxel is in brain mask
                                    if mask_data[dimi][dimj][dimk] == 1:
                                        #load series
                                        currentseries = image_data[dimi][dimj][dimk]
                                                                               
                                        subcurseries = []               
                                        missingseries = []
                                        
                                        for data in range(len(currentseries)):
                                            if tmask[data] == 1:
                                                subcurseries.append(currentseries[data])
                                            else:
                                                missingseries.append(0)
                                        
                                        mean = sum(subcurseries)/len(subcurseries)                                        
                                        
                                        timeseriesDF = pd.DataFrame(
                                            {'Time_Series': subcurseries
                                            })  
                                        y = timeseriesDF["Time_Series"] 
                                             
                                        #create the model. Predict y (the time series) as a function of X (all the nuisance regressors)
                                        model = sm.OLS(y, regdata).fit()
                                        residuals = model.resid.tolist()
                                        #constant = model.params['const']

                                        numofvoxels = numofvoxels + 1
                                        
                                        fulldata = residuals+missingseries
                                        fulldata = [fulldata for _,fulldata in sorted(zip(fulltime,fulldata))]                                        
                                        
                                        new_data[dimi][dimj][dimk] = fulldata
                                        mean_data[dimi][dimj][dimk] = mean
                                        
                                        #for testing, this makes every voxel equal to the volume:
                                        #new_data[dimi][dimj][dimk] = [qq for qq in range(len(new_data[dimi][dimj][dimk]))]
                                    else:
                                        new_data[dimi][dimj][dimk] = [0]*len(tmask)
                                        mean_data[dimi][dimj][dimk] = 0
                                              
                        #save image
                        regressor_img = nib.Nifti1Image(new_data, img.affine, img.header)
                        nib.save(regressor_img,output_file)
                        
                        mean_img = nib.Nifti1Image(mean_data, img2.affine, img2.header)
                        nib.save(mean_img,mean_output)                       
                        
                        x = "Number of voxels updated is " + str(numofvoxels)
                        print(x)
                        log.append(x)     
                        
                        #find the final time, save info to log
                        steptimer = round(time.time()-steptimer,3)
                        x = "Individual step took " + str(steptimer) + " s to run."
                        print(x)
                        log.append(x)
                        steptimermin = round(steptimer/60,3)
                        x = "(which is " + str(steptimermin) + " minutes)"
                        print(x)
                        log.append(x)   
                        
                else:
                    x = "This file doesn't exist: " + input_reg
                    print(x)
                    log.append(x)                    

    
    if k == 'filterall':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                #define file names for this specific kid
                dir_in = dir_start + person + "/" + j + "/func/" + regfolder
                input_file = dir_in + person + "_" + j + "_" + filterimagename
                output_file = dir_in + person + "_" + j + "_" + filterimagenameoutput
                input_mask = dir_start + person + "/" + j + "/func/" + person + "_" + j + "_" + filtermaskname

                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x)
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file) == True:
                            x = "Filter did not run; file already exists for " + output_file
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        #find the current time
                        steptimer = time.time()

                        #load the image using some package I found called NiBabel
                        img = nib.load(input_file)
                        image_data = img.get_fdata()
                        new_data = image_data.copy()
                              
                        #load the mask
                        img = nib.load(input_mask)
                        mask_data = img.get_fdata()
                        
                        #get shape of image data
                        shape = image_data.shape
                        dim_x = shape[0]
                        dim_y = shape[1]
                        dim_z = shape[2]

                        #length of time series
                        N = shape[3]

                        #this spits out the timepoints. 0, 2.5, 5, 7.5 etc
                        t = np.linspace(0.0, N/fs-1/fs, N)

                        #this creates an x axis from 0 to half of fs. This x axis has half as many points as N
                        tf = np.linspace(0.0,fs/2,int(N/2))

                        #define upper and lower frequencies
                        lowpass_freq = highcut
                        highpass_freq = lowcut

                        #create a matrix of 0s equal to the length of the timecourse
                        F = np.zeros((N))
                        
                        #define where on the list of 0s is the maximum freq
                        lowidx = int(N / 2) + 1
                        if lowpass_freq > 0:
                            lowidx = np.round(float(lowpass_freq) / fs * N)
                        
                        #define where on the list of 0s is the minimum freq
                        highidx = 0
                        if highpass_freq > 0:
                            highidx = np.round(float(highpass_freq) / fs * N)
                        
                        #put the frequencies between the low and highpoint as 1s (so they're accepted)
                        F[int(highidx):int(lowidx)] = 1
                        #also include the frequencies on the other end. So instead of spots 2:5 of 100, spots 95:98 of 100
                        F = ((F + F[::-1]) > 0).astype(int)


                        x = "Filtering data for " + person + " " + j
                        print(x)
                        log.append(x)
                        
                        numofvoxels = 0
                        numofmaskvoxels = 0
                        #loop over every possible voxel in 3D space
                        for dimi in range(dim_x):
                            print("Running for x dimension slice " + str(dimi + 1) + " of " + str(dim_x) + " for " + person + " " + j)
                            for dimj in range(dim_y):
                                for dimk in range(dim_z):
                                    #only filter if voxel is in brain mask
                                    if mask_data[dimi][dimj][dimk] == 1:
                                        currentseries = image_data[dimi][dimj][dimk]
                                        #this creates amplitude vs time data after a FFT filter. So FFT then an inverse FFT
                                        new_data[dimi][dimj][dimk] = np.real(ifft(fft(currentseries)*F))                                        
                                        numofvoxels = numofvoxels + 1
                                    else:
                                        new_data[dimi][dimj][dimk] = [0]*N
                                        numofmaskvoxels = numofmaskvoxels + 1
                        
                        #save image
                        regressor_img = nib.Nifti1Image(new_data, img.affine, img.header)
                        nib.save(regressor_img,output_file)
                        
                        x = "Number of voxels updated is " + str(numofvoxels)
                        print(x)
                        log.append(x)
                        
                        x = "Number of voxels in mask is " + str(numofmaskvoxels)
                        print(x)
                        log.append(x)                        
                        
                        #find the final time, save info to log
                        steptimer = round(time.time()-steptimer,3)
                        x = "Individual step took " + str(steptimer) + " s to run."
                        print(x)
                        log.append(x)
                        steptimermin = round(steptimer/60,3)
                        x = "(which is " + str(steptimermin) + " minutes)"
                        print(x)
                        log.append(x)
                        
                        x = "Voxels per second is " + str(numofvoxels/steptimer)
                        print(x)
                        log.append(x)
              

    if k == 'gs':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/" + j + "/func/"
                input_file = dir_in + regfolder + person + "_" + j + "_" + gsinput
                input_mask = dir_in + person + "_" + j + "_" + gsmask
                output_file = dir_in + regfolder + person + "_" + j + "_" + gsoutput
                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x) 
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file) == True:
                            x = "fslmeants did not run; file already exists for " + output_file
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        steptimer = time.time()
                        os.chdir(dir_in)
                        
                        x = "fslmeants will now try to run. Hopefully the mean time series is nice today."
                        print(x)
                        log.append(x)                        
                        try:
                            mygs = fsl.ImageMeants()
                            mygs.inputs.in_file = input_file
                            mygs.inputs.out_file = output_file  
                            mygs.inputs.mask = input_mask
                            mygs.run()
                            
                            x = "fslmeants probably created " + output_file
                            print(x)
                            log.append(x)
                        except:
                            x = "fslmeants failed."
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


    if k == 'ns':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/" + j + "/func/"
                input_file = dir_in + regfolder + person + "_" + j + "_" + nsinput
                input_csfmask = dir_in + person + "_" + j + "_" + nscsfmask
                input_wmmask = dir_in + person + "_" + j + "_" + nswmmask
                
                output_CSF = dir_in + regfolder + person + "_" + j + "_" + nsoutputCSF
                output_WM = dir_in + regfolder + person + "_" + j + "_" + nsoutputWM
                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x) 
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_WM) == True:
                            x = "fslmeants did not run; file already exists for " + output_WM
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        steptimer = time.time()
                        os.chdir(dir_in)
                        
                        x = "fslmeants will now try to run. Hopefully the mean time series is nice today."
                        print(x)
                        log.append(x)                        
                        try:
                            myns = fsl.ImageMeants()
                            myns.inputs.in_file = input_file
                            myns.inputs.out_file = output_CSF 
                            myns.inputs.mask = input_csfmask
                            myns.run()
                            
                            myns.inputs.out_file = output_WM 
                            myns.inputs.mask = input_wmmask
                            myns.run()
                            
                            x = "fslmeants probably created " + output_WM
                            print(x)
                            log.append(x)
                        except:
                            x = "fslmeants failed."
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


    if k == 'filterhmp':
        #at one point in an earlier version of this code, I experimented with interpolating over volumes marked for censoring
        #while this code no longer does that, there's some of that legacy in this filtering hmp step. The HMP are **not** interpolated
        #but I didn't want to rewrite all my code, so it does the 'interpolating' step here, but nothing happens
        
        
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                #define file names for this specific kid
                dir_in = dir_start + person + "/" + j + "/func/"
                headmotionfile = dir_in + person + "_" + j + "_" + filterhmpinput            
                output_file = dir_in + regfolder + person + "_" + j + "_" + filterhmpoutput 
                input_reg = dir_in + regfolder + person + "_" + j + "_" + rdreginput
                tmaskfile = dir_in + regfolder + person + "_" + j + "_" + rdtmaskname


                if os.path.isfile(headmotionfile) == False:
                    x = "This file doesn't exist: " + headmotionfile
                    print(x)
                    log.append(x) 
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file) == True:
                            x = "Filter HMP did not run; file already exists for " + output_file
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:                     
                        x = "We will now try to detrend+filter HMP"
                        print(x)
                        log.append(x)
                        
                        #find the current time                        
                        steptimer = time.time()
                        os.chdir(dir_in)

        
                        #read in the detrend regression data
                        regdata = pd.read_csv(input_reg, index_col=0)
                
                        #read in the temporal mask data
                        tmask = []
                        with open(tmaskfile, 'r') as file:
                            for line in file:
                                tmask.append(int(line))
                        
                        #create a dictionary of different types of motion signals
                        motiondict = {
                                'motionR_1' : [],
                                'motionR_2' : [],
                                'motionR_3' : [],
                                'motionR_4' : [],
                                'motionR_5' : [],
                                'motionR_6' : []   
                        }        
                
                        #read in head motion file, put data into dictionary
                        with open(headmotionfile) as file:
                            for line in file:
                                splitted = line.split()
                                #create head motion parameters and their  quadratic terms
                                motiondict['motionR_1'].append(float(splitted[0]))
                                motiondict['motionR_2'].append(float(splitted[1]))
                                motiondict['motionR_3'].append(float(splitted[2]))
                                motiondict['motionR_4'].append(float(splitted[3]))
                                motiondict['motionR_5'].append(float(splitted[4]))
                                motiondict['motionR_6'].append(float(splitted[5]))
                        
                        #define names of different types of motion data
                        rawmotion = ['motionR_1','motionR_2','motionR_3','motionR_4','motionR_5','motionR_6']
                        detmotion = ['motionR_1det','motionR_2det','motionR_3det','motionR_4det','motionR_5det','motionR_6det']
                        intmotion = ['motionR_1detint','motionR_2detint','motionR_3detint','motionR_4detint','motionR_5detint','motionR_6detint']
                        fltmotion = ['motionR_1detintflt','motionR_2detintflt','motionR_3detintflt','motionR_4detintflt','motionR_5detintflt','motionR_6detintflt']
                
                        timelist = list(range(0,len(motiondict['motionR_1'])))
                        
                        #split time into points that are censored and points that aren't                        
                        subtimelist = []
                        missingtime = []
                        
                        for data in range(len(timelist)):
                            if tmask[data] == 1:
                                subtimelist.append(timelist[data])
                            else:
                                missingtime.append(timelist[data])                            
                        fulltime = subtimelist+missingtime
                        
                        ###detrend the data###
                        for rr in rawmotion:
                            testseries = motiondict[rr]
                    
                            #divide the series up into points that are censored and points that aren't
                            subtestseries = []                
                            missingseries = []
                               
                            for data in range(len(testseries)):
                                if tmask[data] == 1:
                                    subtestseries.append(testseries[data])
                                else:
                                    missingseries.append(0)
                            
                            #timeseries
                            timeseriesDF = pd.DataFrame(
                                {'Time_Series': subtestseries
                                })  
                    
                            y = timeseriesDF["Time_Series"]
                                                                       
                            #create the model. Predict y (the time series) as a function of X (all the nuisance regressors)
                            model = sm.OLS(y, regdata).fit()
                            residuals = model.resid.tolist()
                            
                            #recreate the full data with the residuals + the points marked for censoring
                            fulldata = residuals+missingseries
                            fulldata = [fulldata for _,fulldata in sorted(zip(fulltime,fulldata))]
                            
                            #add the detrend data to the motion dictionary
                            motiondict[rr+'det'] = fulldata                            
                
                        ###interpolate the data###                
                        
                        #number of sample points
                        N = len(motiondict['motionR_1'])
            
                        #this spits out the timepoints. If fs=10 and N=500, then 0,0.1,0.2...49.8,49.9
                        t = np.linspace(0.0, N/fs-1/fs, N)
                        
                        #determine the timepoints marked for censoring
                        index = []
                        currentline = 0
                        with open(tmaskfile) as file:
                            for line in file:
                                if int(line) == 0:
                                    index.append(currentline)
                                currentline = currentline + 1
                        
                        #create the list of times that do not need censoring. To be fed into model
                        timesteps_subset = np.delete(t, index)
            
                        #missingtime is the timepoints that were interpolated. ie missing from timesteps_subset
                        #note this isn't the same missingtime I defined above. This is different. Yeah, sloppy code writing
                        #sue me. I'm too lazy to fix it
                        missingtime = []
                        for sec in t:
                            if sec not in list(timesteps_subset):
                                missingtime.append(sec)
                        myInt = 1/fs
                        timepoints = [int(x / myInt) for x in missingtime]
                        
                        #alltime is the timepoints not interpolated + timepoints interpolated. Interpolated times at the end
                        alltime = list(timesteps_subset) + missingtime                        
                        
               
                        #the frequencies to check for Lomb Scargle
                        frequency = np.linspace(0,0.2,700)
                        frequency = np.delete(frequency,0)
                            
                        for rr in detmotion:
                            testseries = motiondict[rr] 
                                                       

                            x = "We're not interpolating for " + person + " " + j
                            #print(x)
                            log.append(x)
                            motiondict[rr+'int'] = testseries

                                
                               
                                                                                                    
                        ###filter the data###
                           
                        #definte the lowpass and highpass                                                                   
                        lowpass_freq = highcut
                        highpass_freq = lowcut
                        
                        #create a matrix of 0s equal to the length of the timecourse
                        F = np.zeros((N))
                        
                        #define where on the list of 0s is the maximum freq
                        lowidx = int(N / 2) + 1
                        if lowpass_freq > 0:
                            lowidx = np.round(float(lowpass_freq) / fs * N)
                        
                        #define where on the list of 0s is the minimum freq
                        highidx = 0
                        if highpass_freq > 0:
                            highidx = np.round(float(highpass_freq) / fs * N)
                        
                        #put the frequencies between the low and highpoint as 1s (so they're accepted)
                        F[int(highidx):int(lowidx)] = 1
                        #also include the frequencies on the other end. So instead of spots 2:5 of 100, spots 95:98 of 100
                        F = ((F + F[::-1]) > 0).astype(int)
                        
                        for rr in intmotion:
                            testseries = motiondict[rr]                                                 
                            #this creates amplitude vs time data after a FFT filter. So FFT then an inverse FFT
                            repaireddata = np.real(ifft(fft(testseries)*F))
                            
                            #add the repaired data to the motion dictionary
                            motiondict[rr+'flt'] = repaireddata          

                        #create a sub dictionary of just the filtered data. Save it
                        filterdict = dict((k, motiondict[k]) for k in fltmotion)
                        pd.DataFrame(filterdict).to_csv(output_file, index=False)                    
         
                        #find the final time, save info to log
                        steptimer = round(time.time()-steptimer,3)
                        x = "Individual step took " + str(steptimer) + " s to run."
                        print(x)
                        log.append(x)
                        

    if k == 'makereg':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                #define file names for this specific kid
                dir_in = dir_start + person + "/" + j + "/func/"
                headmotionfile = dir_in + regfolder + person + "_" + j + "_" + regheadmotionname
                tmaskfile = dir_in + regfolder + person + "_" + j + "_" + regtmaskname
                wmfile = dir_in + regfolder + person + "_" + j + "_" + regwmname
                csffile = dir_in + regfolder + person + "_" + j + "_" + regcsfname
                globalsigfile = dir_in + regfolder + person + "_" + j + "_" + regglobalsigname
                regoutput = dir_in + regfolder + person + "_" + j + "_" + regname


                if os.path.isfile(headmotionfile) == False:
                    x = "This file doesn't exist: " + headmotionfile
                    print(x)
                    log.append(x)
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(regoutput) == True:
                            x = "Make regression data did not run; file already exists for " + regoutput
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        #find the current time
                        steptimer = time.time()
                                        
                        #framewise displacement
                        tmask = []
                        with open(tmaskfile) as file:
                            for line in file:
                                tmask.append(int(line))
                              
                        #create dataframe for single timepoint censoring
                        #initially place tmask into dataframe for correct indexing
                        censordf = pd.DataFrame({'tmask':tmask})
                        for i in range(len(tmask)):
                            if tmask[i] == 0:
                                dfcolumn = []
                                for j in range(len(tmask)):
                                    dfcolumn.append(0)
                                dfcolumn[i] = 1
                                header = 'motion' + str(i)
                                newdf = pd.DataFrame({header : dfcolumn})
                                censordf = censordf.join(newdf)
                        del censordf['tmask']
        
                        #create some empty lists. 2 = squared, t = previous time point
                        #pad previous time point parameters with a zero
        
                        globalsig = []
                        globalsig2 = []
                        globalsigt = [0]
                        globalsig2t = [0]                
                        wmsig = []
                        wmsig2 = []
                        wmsigt = [0]
                        wmsig2t = [0]
                        csfsig = []
                        csfsig2 = []
                        csfsigt = [0]
                        csfsig2t = [0]
                        
                        
                        #read in head motion data, create quadratic terms and temporal derivatives
                        data = pd.read_csv(headmotionfile)
                        
                        motionR_1 = list(data.motionR_1detintflt)
                        motionR_2 = list(data.motionR_2detintflt)
                        motionR_3 = list(data.motionR_3detintflt)
                        motionR_4 = list(data.motionR_4detintflt)
                        motionR_5 = list(data.motionR_5detintflt)
                        motionR_6 = list(data.motionR_6detintflt)
                        motionR2_1 = [i ** 2 for i in motionR_1]
                        motionR2_2 = [i ** 2 for i in motionR_2]
                        motionR2_3 = [i ** 2 for i in motionR_3]
                        motionR2_4 = [i ** 2 for i in motionR_4]
                        motionR2_5 = [i ** 2 for i in motionR_5]
                        motionR2_6 = [i ** 2 for i in motionR_6]
                        
                        motionRt_1 = list(set([0] + motionR_1[:-1]))
                        motionRt_2 = list(set([0] + motionR_2[:-1]))
                        motionRt_3 = list(set([0] + motionR_3[:-1]))
                        motionRt_4 = list(set([0] + motionR_4[:-1]))
                        motionRt_5 = list(set([0] + motionR_5[:-1]))
                        motionRt_6 = list(set([0] + motionR_6[:-1]))
                        motionR2t_1 = list(set([0] + motionR2_1[:-1]))
                        motionR2t_2 = list(set([0] + motionR2_2[:-1]))
                        motionR2t_3 = list(set([0] + motionR2_3[:-1]))
                        motionR2t_4 = list(set([0] + motionR2_4[:-1]))
                        motionR2t_5 = list(set([0] + motionR2_5[:-1]))
                        motionR2t_6 = list(set([0] + motionR2_6[:-1]))
                                        
                                                        
                        #read in global signal, creating the list globalsig and expanded versions
                        #also create a list of timepoints, ie 0, 1, 2, 3, 4, 5, etc
                        with open(globalsigfile, 'r') as file:
                            for line in file:
                                currentSig = float(line[:-1])
                                globalsig.append(currentSig)
                                globalsig2.append(currentSig**2)
                                globalsigt.append(currentSig)
                                globalsig2t.append(currentSig**2)
        
                        del globalsigt[-1]
                        del globalsig2t[-1]
        
                        #read in WM signal, creating the list wmsig and expanded versions
                        with open(wmfile, 'r') as file:
                            for line in file:
                                currentSig = float(line[:-1])
                                wmsig.append(currentSig)
                                wmsig2.append(currentSig**2)
                                wmsigt.append(currentSig)
                                wmsig2t.append(currentSig**2)
        
                        del wmsigt[-1]
                        del wmsig2t[-1]
        
                        #read in CSF signal, creating the list csfsig and expanded versions
                        with open(csffile, 'r') as file:
                            for line in file:
                                currentSig = float(line[:-1])
                                csfsig.append(currentSig)
                                csfsig2.append(currentSig**2)
                                csfsigt.append(currentSig)
                                csfsig2t.append(currentSig**2)
        
                        del csfsigt[-1]
                        del csfsig2t[-1]
                            

                        #create dataframes for different time series
                        gsDF = pd.DataFrame(
                            {
                             'Global_Signal': globalsig - np.mean(globalsig),
                             'Global_Signal2' : globalsig2 - np.mean(globalsig2),
                             'Global_Signalt' : globalsigt - np.mean(globalsigt),
                             'Global_Signal2t' : globalsig2t - np.mean(globalsig2t)
                            })                        
                        
                        WMDF = pd.DataFrame(
                            {
                             'WM_Signal' : wmsig - np.mean(wmsig),
                             'WM_Signal2' : wmsig2 - np.mean(wmsig2),
                             'WM_Signalt' : wmsigt - np.mean(wmsigt),
                             'WM_Signal2t' : wmsig2t - np.mean(wmsig2t)
                            })   
                            
                        CSFDF = pd.DataFrame(
                            {
                             'CSF_Signal' : csfsig - np.mean(csfsig),
                             'CSF_Signal2' : csfsig2 - np.mean(csfsig2),
                             'CSF_Signalt' : csfsigt - np.mean(csfsigt),
                             'CSF_Signal2t' : csfsig2t - np.mean(csfsig2t)
                            })
                            
                        HMPDF = pd.DataFrame(
                            {
                             'MotionR_1' : motionR_1 - np.mean(motionR_1),
                             'MotionR_2' : motionR_2 - np.mean(motionR_2),
                             'MotionR_3' : motionR_3 - np.mean(motionR_3),
                             'MotionR_4' : motionR_4 - np.mean(motionR_4),
                             'MotionR_5' : motionR_5 - np.mean(motionR_5),
                             'MotionR_6' : motionR_6 - np.mean(motionR_6),
                             'MotionR2_1' : motionR2_1 - np.mean(motionR2_1),
                             'MotionR2_2' : motionR2_2 - np.mean(motionR2_2),
                             'MotionR2_3' : motionR2_3 - np.mean(motionR2_3),
                             'MotionR2_4' : motionR2_4 - np.mean(motionR2_4),
                             'MotionR2_5' : motionR2_5 - np.mean(motionR2_5),
                             'MotionR2_6' : motionR2_6 - np.mean(motionR2_6),
                             'MotionRt_1' : motionRt_1 - np.mean(motionRt_1),
                             'MotionRt_2' : motionRt_2 - np.mean(motionRt_2),
                             'MotionRt_3' : motionRt_3 - np.mean(motionRt_3),
                             'MotionRt_4' : motionRt_4 - np.mean(motionRt_4),
                             'MotionRt_5' : motionRt_5 - np.mean(motionRt_5),
                             'MotionRt_6' : motionRt_6 - np.mean(motionRt_6),
                             'MotionR2t_1' : motionR2t_1 - np.mean(motionR2t_1),
                             'MotionR2t_2' : motionR2t_2 - np.mean(motionR2t_2),
                             'MotionR2t_3' : motionR2t_3 - np.mean(motionR2t_3),
                             'MotionR2t_4' : motionR2t_4 - np.mean(motionR2t_4),
                             'MotionR2t_5' : motionR2t_5 - np.mean(motionR2t_5),
                             'MotionR2t_6' : motionR2t_6 - np.mean(motionR2t_6)
                            })                        
                            

                        allregressorsDF = pd.DataFrame({'tmask':tmask})
                                               
                        
                        if regglobal == True:
                            allregressorsDF = allregressorsDF.join(gsDF)
                        if regWM == True:
                            allregressorsDF = allregressorsDF.join(WMDF)
                        if regCSF == True:
                            allregressorsDF = allregressorsDF.join(CSFDF)
                        if regHMP == True:
                            allregressorsDF = allregressorsDF.join(HMPDF)
                        if regvolumes == True:
                            allregressorsDF = allregressorsDF.join(censordf)
                        

                        #add a constant to dataframe
                        allregressorsDF = sm.add_constant(allregressorsDF)
                        del allregressorsDF['tmask'] 
                                                
                        #save regressors as a CSV file
                        allregressorsDF.to_csv(regoutput)
                        x = "All regressors saved to " + regoutput
                        log.append(x)
                        print(x)
                        
                        #find the final time, save info to log
                        steptimer = round(time.time()-steptimer,3)
                        x = "Individual step took " + str(steptimer) + " s to run."
                        print(x)
                        log.append(x)    
                
                    
    if k == 'runreg':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                #define file names for this specific kid
                dir_in = dir_start + person + "/" + j + "/func/"
                input_file = dir_in + regfolder + person + "_" + j + "_" + regimagename
                input_mask = dir_in + person + "_" + j + "_" + regmaskname
                input_reg = dir_in + regfolder + person + "_" + j + "_" + reginput
                output_file = dir_in + regfolder + person + "_" + j + "_" + regimagenameoutput

                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x)
                elif os.path.isfile(input_reg) == True:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file) == True:
                            x = "Regression did not run; file already exists for " + output_file
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:

                        #find the current time
                        steptimer = time.time()
                        
                        regdata = pd.read_csv(input_reg, index_col=0)
                        
                        #load the image using some package I found called NiBabel
                        img = nib.load(input_file)
                        image_data = img.get_fdata()
                        new_data = image_data.copy()
                              
                        #load the mask
                        img = nib.load(input_mask)
                        mask_data = img.get_fdata()
                        
                        #get shape of image data
                        shape = image_data.shape
                        dim_x = shape[0]
                        dim_y = shape[1]
                        dim_z = shape[2]
                            
                        x = "Running the regression for " + person + " " + j
                        print(x)
                        log.append(x)
                        
                        #loop over every possible voxel in 3D space
                        for dimi in range(dim_x):
                            print("Running for x dimension slice " + str(dimi + 1) + " of " + str(dim_x) + " for " + person + " " + j)
                            for dimj in range(dim_y):
                                for dimk in range(dim_z):
                                    #only create model if voxel is in brain mask
                                    if mask_data[dimi][dimj][dimk] == 1:
                                        #load the current series, put in data fram
                                        currentseries = image_data[dimi][dimj][dimk]
                                        timeseriesDF = pd.DataFrame(
                                            {'Time_Series': currentseries
                                            })  
                                        y = timeseriesDF["Time_Series"]                                        
                                        
                                        #create the model. Predict y (the time series) as a function of X (all the nuisance regressors)
                                        model = sm.OLS(y, regdata).fit()
                                        """
                                        print(model.summary())
                                        timelist = list(range(0,shape[3]))
                                        predictions = model.predict(regdata)
                                        plt.plot(timelist,currentseries, label='Series',linewidth = 0.75)
                                        plt.plot(timelist,predictions, label='Model',linewidth = 0.5)
                                        plt.legend()
                                        plt.show()
                                        """
                                        residuals = model.resid.tolist()
                                        new_data[dimi][dimj][dimk] = residuals
                                        
                                        #for testing, this makes every voxel equal to the volume:
                                        #new_data[dimi][dimj][dimk] = [qq for qq in range(len(new_data[dimi][dimj][dimk]))]
                                    else:
                                        new_data[dimi][dimj][dimk] = [0]*len(new_data[dimi][dimj][dimk])
                        
                        #save image
                        regressor_img = nib.Nifti1Image(new_data, img.affine, img.header)
                        nib.save(regressor_img,output_file)
        
                        #find the final time, save info to log
                        steptimer = round(time.time()-steptimer,3)
                        x = "Individual step took " + str(steptimer) + " s to run."
                        print(x)
                        log.append(x)
                        steptimermin = round(steptimer/60,3)
                        x = "(which is " + str(steptimermin) + " minutes)"
                        print(x)
                        log.append(x)   
                        
                else:
                    x = "This file doesn't exist: " + input_reg
                    print(x)
                    log.append(x)                    


    if k == 'remean':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/" + j + "/func/"
                input_file = dir_in + regfolder + person + "_" + j + "_" + remeanimagename
                input_mean = dir_in + regfolder + person + "_" + j + "_" + remeanmean
                output_file = dir_in + regfolder + person + "_" + j + "_" + remeanoutput
                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x) 
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file) == True:
                            x = "Remean did not run; file already exists for " + output_file
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        steptimer = time.time()
                        os.chdir(dir_in)
                        
                        x = "Remean will now try to run."
                        print(x)
                        log.append(x)                        
                        try:
                            mymath = fsl.ImageMaths()
                            mymath.inputs.in_file = input_file
                            mymath.inputs.out_file = output_file
                            mymath.inputs.args = "-add " + input_mean
                            mymath.run()
                            
                            x = "Remean probably created " + output_file
                            print(x)
                            log.append(x)
                        except:
                            x = "Remean failed."
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



#Wrap up the program

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


"""
Basic Functional Preprocessing Pipeline


Made by Kirk Graff
kirk.graff@ucalgary.ca

Please email me if you have any questions :)
I'm not the best programmer so apologies if something is coded oddly!


Make sure your scans are in BIDS format before running
Edit the things near the top, and the program should run fine!



"""




"""***********"""
"""RANDOM INFO"""
"""**************
To run every step of this program you probably need the following structural images:
Brain extracted structural image - eg T1wAbfcBe
Eroded CSF in native structural space - eg T1wAbfcBeCSF_Erode
Eroded WM in native structural space - eg T1wAbfcBeWM_Erode
WM binary in native structural space - eg T1wAbfcBeWM_binary

Run this program after determining the reference volume
    


If you're not sure which participants to use, type 'os.listdir(dir_start)'
If your participant of choice is the 2nd file listed, then set participants as
participants = [1]
If your participants of choice are the 100th and 101st files listed, then set participants as
participants = [99,100]

You can guess and check using: 
os.listdir(dir_start)[x]
(where x is some number, perhaps 20)


"""




"""***********************"""
"""GENERAL PROGRAM OPTIONS"""
"""***********************"""
#what directory are your images saved in?
dir_start = '/Users/example/example/directory_with_all_MRI_scans_in_BIDS_format/'


#the full pathway/name of the file that specifies the reference volumes for each 4D image
#these are created in find ref volume program
RefVolFile = '/Users/example/example/xrefvolumes.csv'


#What are the files called in the reference volume spreadsheet?
#ie if you open RefVolFile, what are the images referred to as?
filenamesinRefVolFile = "task-movie_boldMcFto0.nii.gz_rel.rms"


#what participants do you want this to run on? e.g. [1,2,3] or list(range(1,4))
#this is based on the files in the directory. 0 = first file in directory
participants = [8]


#do you want to run on ses-0, ses-12, or both? If both, type ["ses-0","ses-12"]
imagesession = ["ses-0","ses-12"]


#if True, it'll assume the anatomical image is in the same session as the functional. If false, it'll use the folder mentioned
samesesanat = True
diffsesanatfolder = 'ses-struct01'

#if replacer is false, the program won't run if output image already exists
#if replacer is true, the program will write over outputs that already exist
replacer = False

#name of log book that output is saved to
logname = 'xfunclogbook.txt'

#what steps do you want the program to run? The steps are run in the order listed
#for full preprocessing type:
#steps = ['mcflirt1','slicetime','mcflirt2','split','bet','betcons','bbr','cxfm','axfm','maskupdate','cleanup']

steps = ['mcflirt1','slicetime','mcflirt2','split','bet','betcons','bbr','cxfm','axfm','maskupdate','cleanup']



#mcflirt1 = generate motion estimates on 'uncorrected' data. ~1 minute per image
#slicetime = slicetime correction with FSL. Very fast
#mcflirt2 = rigid body realignment on slicetime corrected data. ~1 minute per image.
#split = split 4D volume into 3D volumes. Isolate reference volume. Very fast
#bet = use FSL Bet to remove non-brain data from reference volume. Very fast
#betcons = use FSL Bet to only remove what is definitely non-brain. More conservative than your one uncle
#bbr = warp EPI image to structural image using boundary based registration. Uses FLIRT. ~12 minutes per image.
#cxfm = reverses the transformation matrix from bbr step to instead warp structural to EPI. Uses FLIRT. 1s per scan
#axfm = warps the structural image to the functional image using the output of cxfm. Uses FLIRT. 30s per scan
#maskupdate = update CSF and WM masks (mostly CSF). 10s per scan
#cleanup - delete 'unnecessary' files that intermediate steps spit out


"""****************"""
"""MCFLIRT1 OPTIONS"""
"""****************"""
mcf1input = "task-movie_bold"
mcf1output = "task-movie_boldMcf"




"""*****************************"""
"""SLICE TIME CORRECTION OPTIONS"""
"""*****************************"""
stcinput = "task-movie_bold"
stcoutput = "task-movie_boldStc"





"""****************"""
"""MCFLIRT2 OPTIONS"""
"""****************"""
mcf2input = "task-movie_boldStc"
mcf2output = "task-movie_boldStcMcf"





"""*************"""
"""SPLIT OPTIONS"""
"""*************"""
splitinput = "task-movie_boldStcMcf"
splitoutput = "task-movie_boldStcRef"





"""***************"""
"""FSL BET OPTIONS"""
"""***************"""
betinput = "task-movie_boldStcRef"
betoutput = "task-movie_boldStcRefBet"
betfrac = 0.3


#the higher betfrac the more is removed along edges of an image
#will also spit out a mask using the output name with "_mask" on the end


"""****************************"""
"""FSL BET CONSERVATIVE OPTIONS"""
"""****************************"""
betcinput = "task-movie_boldStcRef"
betcoutput = "task-movie_boldStcRefConsbet"
betcfrac = 0.1




"""*****************"""
"""FLIRT BBR OPTIONS"""
"""*****************"""
bbrinput = "task-movie_boldStcRefBet"
bbroutput = "task-movie_boldStcRefBetBbr"
flirtoutput = "task-movie_boldStcRefBetFlt"



#bbrreference is the name of the brain extracted structural image
bbrreference = "T1wAbfcBe"
#bbrwm is a binary version of the white matter of the above listed brain extracted image
bbrwm = "T1wAbfcBeWM_binary"


"""*************************"""
"""cxfm: CONVERT XFM OPTIONS"""
"""*************************"""
cxfminput = "task-movie_boldStcRefBetBbr_mat"
cxfmoutput = "task-movie_boldStcRefBetBbr_matinv"


#this reverses a fsl formated transformation matrix using FLIRT


"""***********************"""
"""axfm: Apply XFM OPTIONS"""
"""***********************"""
#warp T1w to functional space
axfminput = "T1wAbfcBe"
axfmoutput = "T1wAbfcBe_func"
axfmreference = "task-movie_boldStcRefBet"
axfmmatrix = "task-movie_boldStcRefBetBbr_matinv"

#warp structural CSF to functional space
axfmcsfinput = "T1wAbfcBeCSF_Erode"
axfmcsfoutput = "T1wAbfcBeCSF_Erode_func"

#warp structural WM to functional space
axfmwminput = "T1wAbfcBeWM_Erode"
axfmwmoutput = "T1wAbfcBeWM_Erode_func"



"""******************"""
"""maskupdate OPTIONS"""
"""******************"""
mucsfinput = "T1wAbfcBeCSF_Erode_func"
mucsfoutput = "MASKCSF"

muwminput = "T1wAbfcBeWM_Erode_func"
muwmoutput = "MASKWM"

#whole brain mask
mumask = "task-movie_boldStcRefBet_mask"



"""*****************************************"""
"""ANYTHING BELOW HERE DOESN'T NEED CHANGING"""
"""**********(OR SO KIRK HOPES)*************"""
"""*****************************************"""

import nipype.interfaces.fsl as fsl
import nipype.interfaces.afni as afni
import nipype.interfaces.ants as ants
from nipype.interfaces.c3 import C3dAffineTool
import os
import pandas as pd
import time
import shutil
from shutil import copyfile


#get the current time
totaltimer = time.time()

#get a list of everything in the starting directory
participant_folders = os.listdir(dir_start)

#everything in log gets saved to the logbook. Text often gets appended to log
log = ["*************************************************"]
log.append('Starting log for ' + time.ctime())


#the big loop of steps. Each step follows the same basic format
#see comments for mcflirt1
for k in steps: 

    if k == 'mcflirt1':
        #df is the dataframe that is read in that states the reference volume for each 4D volume
        df = pd.read_csv(RefVolFile)
        files = list(df['File'])
        refframes = list(df['Ref_Volume'])
        #loop through all the participants listed
        for i in participants:
            person = participant_folders[i]
            #loop through all the sessions listed (ses-0, ses-12, or both)
            for j in imagesession:
                #define the reference volume for the particular 4D image
                reffer = person + "_" + j + "_" + filenamesinRefVolFile
                #define the directory for the particular 4D image
                dir_in = dir_start + person + "/" + j + "/func/"
                #what's the name of the input 4D volume?
                input_file = dir_in + person + "_" + j + "_" + mcf1input + ".nii.gz"
                #what's the name of the output 4D volume after motion realignment?
                output_file = dir_in + person + "_" + j + "_" + mcf1output + ".nii.gz"
                #check if the input file actually exists
                if os.path.isfile(input_file) == False:
                    #if not, check again with .nii instead of .nii.gz
                    #this is a way of accepting files named both .nii or .nii.gz
                    input_file = dir_in + person + "_" + j + "_" + mcf1input + ".nii"
                if os.path.isfile(input_file) == False:
                    #put in the log that the input file doesn't exist, so the step didn't run
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x)
                else:
                    #if this variable becomes false, the step won't run
                    doit = True
                    #check if we're supposed to replace files that already exist
                    if replacer == False:
                        if os.path.isfile(output_file) == True:
                            x = "McFlirt1 did not run; file already exists for " + output_file
                            print(x)
                            log.append(x)
                            #changing doit to false means the step won't run
                            doit = False
                    try:
                        #determine which line of the reference volume file has the kid in question
                        indexnumber = files.index(reffer)
                        refvolume = refframes[indexnumber]                    
                    except:
                        x = "McFlirt1 did not run. No reference volume specified."
                        print(x)
                        log.append(x)
                        doit = False
                    if doit == True:
                        #define the current time
                        steptimer = time.time()

                        x = "McFlirt1 is beginning to run."
                        print(x)
                        log.append(x)
                        try:
                            #change the directory
                            os.chdir(dir_in)
                            #woooo nipype code
                            mymcf = fsl.MCFLIRT()
                            mymcf.inputs.in_file = input_file
                            mymcf.inputs.out_file = output_file
                            mymcf.inputs.save_mats = True
                            mymcf.inputs.save_plots = True
                            mymcf.inputs.save_rms = True
                            mymcf.inputs.ref_vol = refvolume
                            mymcf.run()                        
                            
                            x = "McFlirt1 probably created " + output_file
                            print(x)
                            log.append(x)      
                        except:
                            #if something went wrong with all the nipype stuff, this keeps the program running
                            #so we can try other kids/steps without crashing the whole program
                            x = "McFlirt1 failed."
                            print(x)
                            log.append(x)
                        #calculate the time it took the program to run by taking the current time and subtracting the old time
                        #the '3' rounds it to 3 decimal places. Or maybe 3 sig digs. I forget
                        steptimer = round(time.time()-steptimer,3)
                        x = "Individual step took " + str(steptimer) + " s to run."
                        print(x)
                        log.append(x)
                        #convert the time to minutes
                        steptimermin = round(steptimer/60,3)
                        x = "(which is " + str(steptimermin) + " minutes)"
                        print(x)
                        log.append(x)


    if k == 'slicetime':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/" + j + "/func/"
                input_file = dir_in + person + "_" + j + "_" + stcinput + ".nii.gz"
                output_file = dir_in + person + "_" + j + "_" + stcoutput + ".nii.gz"
                if os.path.isfile(input_file) == False:
                    input_file = dir_in + person + "_" + j + "_" + stcinput + ".nii"
                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x)
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file) == True:
                            x = "Slicetime Correction did not run; file already exists for " + output_file
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        steptimer = time.time()

                        x = "Slice Time Correction is beginning to run."
                        print(x)
                        log.append(x)
                        try:
                            os.chdir(dir_in)
                            fslSlice = fsl.SliceTimer()
                            fslSlice.inputs.in_file = input_file
                            fslSlice.inputs.out_file = output_file
                            #apparently "interleaved" is how scans are collected at the ACH
                            fslSlice.inputs.interleaved = True

                            fslSlice.run()                      
                            
                            x = "Slice Time Correction probably created " + output_file
                            print(x)
                            log.append(x)      
                        except:
                            x = "Slice Time Correction failed."
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



    if k == 'mcflirt2':
        df = pd.read_csv(RefVolFile)
        files = list(df['File'])
        refframes = list(df['Ref_Volume'])
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                reffer = person + "_" + j + "_" + filenamesinRefVolFile
                dir_in = dir_start + person + "/" + j + "/func/"
                input_file = dir_in + person + "_" + j + "_" + mcf2input + ".nii.gz"
                output_file = dir_in + person + "_" + j + "_" + mcf2output + ".nii.gz"
                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x)
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file) == True:
                            x = "McFlirt2 did not run; file already exists for " + output_file
                            print(x)
                            log.append(x)
                            doit = False
                    try:
                        #determine which line of the reference volume file has the kid in question
                        indexnumber = files.index(reffer)
                        refvolume = refframes[indexnumber]                    
                    except:
                        x = "McFlirt2 did not run. No reference volume specified."
                        print(x)
                        log.append(x)
                        doit = False
                    if doit == True:
                        steptimer = time.time()

                        x = "McFlirt2 is beginning to run."
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
                            mymcf.inputs.ref_vol = refvolume
                            mymcf.run()                        
                            
                            x = "McFlirt2 probably created " + output_file
                            print(x)
                            log.append(x)      
                        except:
                            x = "McFlirt2 failed."
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
                        
  
    if k == 'split':
        df = pd.read_csv(RefVolFile)
        files = list(df['File'])
        refframes = list(df['Ref_Volume'])
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                reffer = person + "_" + j + "_" + filenamesinRefVolFile
                dir_in = dir_start + person + "/" + j + "/func/"
                input_file = person + "_" + j + "_" + splitinput + ".nii.gz"
                output_file = dir_in + person + "_" + j + "_" + splitoutput + ".nii.gz"
                if os.path.isfile(dir_in + input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x)
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file) == True:
                            x = "Split did not run; file already exists for " + output_file
                            print(x)
                            log.append(x)
                            doit = False
                    try:
                        #determine which line of the reference volume file has the kid in question
                        indexnumber = files.index(reffer)
                        refvolume = refframes[indexnumber]                    
                    except:
                        x = "Split did not run. No reference volume specified."
                        print(x)
                        log.append(x)
                        doit = False
                    if doit == True:
                        steptimer = time.time()

                        x = "Split is beginning to run."
                        print(x)
                        log.append(x)
                        try:
                            os.chdir(dir_in)
                            mysplit = fsl.Split()
                            mysplit.inputs.dimension = 't'
                            mysplit.inputs.in_file = input_file
                            #define a directory for the splitted 4D image
                            mysplit.inputs.out_base_name = dir_in + "split/" + input_file
    
                            #create the splitted directory, if it doesn't already exist
                            if not os.path.exists(dir_in + "split/"):
                                os.makedirs(dir_in + "split/")                      
        
                            mysplit.run()
                            
                            #copy the reference volume from the splitted directory to the main directory
                            copyfile(dir_in + "split/" + person + "_" + j + "_" + splitinput + "0" + str(refvolume) + ".nii.gz", output_file)

                            x = "Split probably created " + output_file
                            print(x)
                            log.append(x)      
                        except:
                            x = "Split failed."
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

                      
    if k == 'bet':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/" + j + "/func/"
                input_file = dir_in + person + "_" + j + "_" + betinput + ".nii.gz"
                output_file = dir_in + person + "_" + j + "_" + betoutput + ".nii.gz"
                output_mask = dir_in + person + "_" + j + "_" + betoutput + "_mask.nii.gz"
                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x)
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file) == True:
                            x = "BET did not run; file already exists for " + output_file
                            print(x)
                            log.append(x)
                            doit = False
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
                            mybet.inputs.frac = betfrac
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


    if k == 'betcons':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/" + j + "/func/"
                input_file = dir_in + person + "_" + j + "_" + betcinput + ".nii.gz"
                output_file = dir_in + person + "_" + j + "_" + betcoutput + ".nii.gz"
                output_mask = dir_in + person + "_" + j + "_" + betcoutput + "_mask.nii.gz"
                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x)
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file) == True:
                            x = "BET did not run; file already exists for " + output_file
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        steptimer = time.time()

                        x = "Place your BETs. Conservative BET is beginning to run."
                        print(x)
                        log.append(x)
                        try:
                            os.chdir(dir_in)
                            mybet = fsl.BET()
                            mybet.inputs.in_file = input_file
                            #specify the fractional intensity for BET
                            mybet.inputs.frac = betcfrac
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
                            
                            x = "BET conservative probably created " + output_file
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
                        
                        
    if k == 'bbr':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                

                dir_in = dir_start + person + "/" + j + "/func/"
                input_file = dir_in + person + "_" + j + "_" + bbrinput + ".nii.gz"

                output_file = dir_in + person + "_" + j + "_" + bbroutput + ".nii.gz"
                output_file2 = dir_in + person + "_" + j + "_" + flirtoutput + ".nii.gz"
                output_mask1 = dir_in + person + "_" + j + "_" + bbroutput + "_mask.nii.gz"
                output_mask2 = dir_in + person + "_" + j + "_" + flirtoutput + "_mask.nii.gz"

                #this program assumes the structural image and its WM are saved in a folder with BIDS naming setup
                if samesesanat == True:
                    input_reference = dir_start + person + "/" + j + "/anat/" + person + "_" + j + "_" + bbrreference + ".nii.gz"
                    input_wm = dir_start + person + "/" + j + "/anat/" + person + "_" + j + "_" + bbrwm + ".nii.gz"
                else:
                    input_reference = dir_start + person + "/" + diffsesanatfolder + "/anat/" + person + "_" + diffsesanatfolder + "_" + bbrreference + ".nii.gz"
                    input_wm = dir_start + person + "/" + diffsesanatfolder + "/anat/" + person + "_" + diffsesanatfolder + "_" + bbrwm + ".nii.gz"                    

               
                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x)
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file) == True:
                            x = "FLIRT did not run; file already exists for " + output_file
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        steptimer = time.time()
                        os.chdir(dir_in)

                        x = "FSL will now try to FLIRT with you"
                        print(x)
                        log.append(x)
                        try:
                            os.chdir(dir_in)
                            myflirt = fsl.FLIRT()
                            myflirt.inputs.in_file = input_file
                            myflirt.inputs.reference = input_reference
                            myflirt.inputs.out_file = output_file
                            #ciric et al says to use 9 DOF. Though FSL default is 12...
                            myflirt.inputs.dof = 9
                            myflirt.inputs.out_matrix_file = dir_in + person + "_" + j + "_" + bbroutput + "_mat"
                            #bbr = boundary based registration
                            myflirt.inputs.cost = "bbr"
                            myflirt.inputs.wm_seg = input_wm
                            myflirt.run()
                            
    
                            c3 = C3dAffineTool()
                            c3.inputs.source_file = input_file
                            c3.inputs.reference_file = input_reference
                            
                            c3.inputs.itk_transform = dir_in + person + "_" + j + "_" + bbroutput + ".h5"
                            c3.inputs.transform_file = dir_in + person + "_" + j + "_" + bbroutput + "_mat"
                            
                            c3.inputs.fsl2ras = True
                            c3.run()
    
    
                            myflirt = fsl.FLIRT()
                            myflirt.inputs.in_file = input_file
                            myflirt.inputs.reference = input_reference
                            myflirt.inputs.out_file = output_file2
                            #ciric et al says to use 9 DOF. Though FSL default is 12...
                            myflirt.inputs.dof = 9
                            myflirt.inputs.out_matrix_file = dir_in + person + "_" + j + "_" + flirtoutput + "_mat"
                            #bbr = boundary based registration
                            myflirt.run()
                            
    
                            c3 = C3dAffineTool()
                            c3.inputs.source_file = input_file
                            c3.inputs.reference_file = input_reference
                            
                            c3.inputs.itk_transform = dir_in + person + "_" + j + "_" + flirtoutput + ".h5"
                            c3.inputs.transform_file = dir_in + person + "_" + j + "_" + flirtoutput + "_mat"
                            
                            c3.inputs.fsl2ras = True
                            c3.run()                            
      
                            x = "FLIRT probably created " + output_file
                            print(x)
                            log.append(x)
                            x = "FLIRT probably created " + output_file2
                            print(x)
                            log.append(x)
                            
                            
                        except:
                            x = "You were shot down. FLIRT failed."
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


    if k == 'cxfm':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/" + j + "/func/"
                input_file = dir_in + person + "_" + j + "_" + cxfminput
                output_file = dir_in + person + "_" + j + "_" + cxfmoutput
                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x)
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file) == True:
                            x = "Convert XFM did not run; file already exists for " + output_file
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        steptimer = time.time()
                        os.chdir(dir_in)

                        x = "Convert XFM will now try to run."
                        print(x)
                        log.append(x)
                        try:
                            invt = fsl.ConvertXFM()
                            invt.inputs.in_file = input_file
                            invt.inputs.invert_xfm = True
                            invt.inputs.out_file = output_file
                            invt.run()
  
                            x = "Convert XFM probably created " + output_file
                            print(x)
                            log.append(x)
                        except:
                            x = "Convert XFM failed."
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


    if k == 'axfm':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                
                if samesesanat == True:
                    anatj = j
                else:
                    anatj = diffsesanatfolder               
                
                
                
                
                dir_in = dir_start + person + "/" + j + "/func/"
                dir_in_anat = dir_start + person + "/" + anatj + "/anat/"
                input_file1 = dir_in_anat + person + "_" + anatj + "_" + axfminput + ".nii.gz"
                output_file1 = dir_in + person + "_" + j + "_" + axfmoutput + ".nii.gz"
                        
                input_file2 = dir_in_anat + person + "_" + anatj + "_" + axfmcsfinput + ".nii.gz"
                intermediate2_1 = dir_in + person + "_" + j + "_" + axfmcsfoutput + "junk1.nii.gz" 
                intermediate2_2 = dir_in + person + "_" + j + "_" + axfmcsfoutput + "junk2.nii.gz" 
                output_file2 = dir_in + person + "_" + j + "_" + axfmcsfoutput + ".nii.gz" 
                
                input_file3 = dir_in_anat + person + "_" + anatj + "_" + axfmwminput + ".nii.gz"
                intermediate3_1 = dir_in + person + "_" + j + "_" + axfmwmoutput + "junk1.nii.gz"  
                intermediate3_2 = dir_in + person + "_" + j + "_" + axfmwmoutput + "junk2.nii.gz"  
                output_file3 = dir_in + person + "_" + j + "_" + axfmwmoutput + ".nii.gz"  
                
                input_matrix = dir_in + person + "_" + j + "_" + axfmmatrix
                input_reference = dir_in + person + "_" + j + "_" + axfmreference + ".nii.gz"
                if os.path.isfile(input_file1) == False:
                    x = "This file doesn't exist: " + input_file1
                    print(x)
                    log.append(x) 
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file3) == True:
                            x = "Apply XFM did not run; file already exists for " + output_file3
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        steptimer = time.time()
                        os.chdir(dir_in)
                        
                        x = "Apply XFM will now try to run."
                        print(x)
                        log.append(x)                        
                        try:
                            myflirt = fsl.FLIRT()
                            myflirt.inputs.reference = input_reference
                            myflirt.inputs.apply_xfm = True
                            myflirt.inputs.in_matrix_file = input_matrix
                            
                            myflirt.inputs.in_file = input_file1
                            myflirt.inputs.out_file = output_file1
                            myflirt.run()
                            
                            myflirt.inputs.in_file = input_file2
                            myflirt.inputs.out_file = intermediate2_1
                            myflirt.run()
                            
                            myflirt.inputs.in_file = input_file3
                            myflirt.inputs.out_file = intermediate3_1
                            myflirt.run()
                            
                            #after warping, remove low threshold for both CSF/WM
                            myrlt = fsl.Threshold()
                            myrlt.inputs.use_robust_range = True
                            myrlt.inputs.use_nonzero_voxels = True
                            
                            myrlt.inputs.thresh = 10
                            myrlt.inputs.in_file = intermediate2_1
                            myrlt.inputs.out_file = intermediate2_2
                            myrlt.run()
                            
                            myrlt.inputs.thresh = 60
                            myrlt.inputs.in_file = intermediate3_1
                            myrlt.inputs.out_file = intermediate3_2
                            myrlt.run()
                            
                            #convert images to binaries
                            mybin = fsl.UnaryMaths()
                            mybin.inputs.operation = 'bin'
                            mybin.inputs.in_file = intermediate2_2
                            mybin.inputs.out_file = output_file2
                            mybin.run()
                            
                            mybin.inputs.in_file = intermediate3_2
                            mybin.inputs.out_file = output_file3
                            mybin.run()
                            
                            x = "Apply XFM probably created " + output_file1
                            print(x)
                            log.append(x)
                        except:
                            x = "Apply XFM failed."
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


    if k == 'maskupdate':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/" + j + "/func/"
                input_csfmask = dir_in + person + "_" + j + "_" + mucsfinput + ".nii.gz"
                output_csfmask = dir_in + person + "_" + j + "_" + mucsfoutput + ".nii.gz"
                input_wmmask = dir_in + person + "_" + j + "_" + muwminput + ".nii.gz"
                output_wmmask = dir_in + person + "_" + j + "_" + muwmoutput + ".nii.gz"
                input_brainmask = dir_in + person + "_" + j + "_" + mumask + ".nii.gz"                
                
                input_brainmask_erode = dir_in + person + "_" + j + "_" + mumask + "erode.nii.gz"
                input_brainmask_upview = dir_in + person + "_" + j + "_" + mumask + "upview.nii.gz"
                input_brainmask_upview_down = dir_in + person + "_" + j + "_" + mumask + "junk.nii.gz"
                input_brainmask_upview_down_mat = dir_in + person + "_" + j + "_" + mumask + "upview_mat"
                                
                if os.path.isfile(input_csfmask) == False:
                    x = "This file doesn't exist: " + input_csfmask
                    print(x)
                    log.append(x) 
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_csfmask) == True:
                            x = "Update masks did not run; file already exists for " + output_csfmask
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        steptimer = time.time()
                        os.chdir(dir_in)
                        
                        x = "Update masks will now try to run."
                        print(x)
                        log.append(x)                        
                        try:
                            """
                            The first 6 steps are literally the stupidest fix, but the only one that would work.
                            Their purpose is to create an eroded whole brain mask to limit CSF to tissue near ventricle
                            -roi increases the field of view
                            -erosion then erodes the sides of the mask. The increased  field of view allows for the
                            bottom to also be eroded
                            -then myflirt1 warps the original expanded field of view image back to the original image
                            (this literally changes nothing, cause they're the same image, but gives us a transformation matrix)
                            -myflirt2 then warps the eroded image back into the same space as the original image
                            -rlt removes the low threshold artifact from the warping process
                            """
                            
                            roi = fsl.ExtractROI()
                            roi.inputs.in_file = input_brainmask
                            roi.inputs.roi_file = input_brainmask_upview
                            roi.inputs.x_min = -5
                            roi.inputs.x_size = 101
                            roi.inputs.y_min = -5
                            roi.inputs.y_size = 119
                            roi.inputs.z_min = -5
                            roi.inputs.z_size = 101
                            roi.run()
                            
                            erosionM = afni.MaskTool()
                            erosionM.inputs.in_file = input_brainmask_upview
                            erosionM.inputs.out_file = input_brainmask_erode
                            erosionM.inputs.outputtype = 'NIFTI_GZ'
                            erosionM.inputs.dilate_inputs = '-7'
                            erosionM.inputs.args = "-overwrite"
                            erosionM.run()
                            
                            myflirt1 = fsl.FLIRT()
                            myflirt1.inputs.reference = input_brainmask
                            myflirt1.inputs.in_file = input_brainmask_upview
                            myflirt1.inputs.out_file = input_brainmask_upview_down
                            myflirt1.inputs.out_matrix_file = input_brainmask_upview_down_mat
                            myflirt1.run()
                            
                            myflirt2 = fsl.FLIRT()
                            myflirt2.inputs.reference = input_brainmask
                            myflirt2.inputs.apply_xfm = True
                            myflirt2.inputs.in_matrix_file = input_brainmask_upview_down_mat                            
                            myflirt2.inputs.in_file = input_brainmask_erode
                            myflirt2.inputs.out_file = input_brainmask_erode
                            myflirt2.run()
                            
                            myrlt = fsl.Threshold()
                            myrlt.inputs.use_robust_range = True
                            myrlt.inputs.use_nonzero_voxels = True
                            myrlt.inputs.thresh = 1
                            myrlt.inputs.in_file = input_brainmask_erode
                            myrlt.inputs.out_file = input_brainmask_erode
                            myrlt.run()
                            
                            #create the CSF mask by multiplying the eroded brainmask by the original CSF mask
                            mymath = fsl.ImageMaths()
                            mymath.inputs.in_file = input_brainmask_erode
                            mymath.inputs.out_file = output_csfmask
                            mymath.inputs.args = "-mul " + input_csfmask
                            mymath.run()
                            
                            #create the WM mask by multiplying the original brainmask by the original WM mask
                            #this probably changes nothing, but perhaps there was a bad functional<-->structural alignment
                            mymath = fsl.ImageMaths()
                            mymath.inputs.in_file = input_brainmask
                            mymath.inputs.out_file = output_wmmask
                            mymath.inputs.args = "-mul " + input_wmmask
                            mymath.run()
                            
                            x = "Update masks probably created " + output_wmmask
                            print(x)
                            log.append(x)
                        except:
                            x = "Update masks failed."
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



    if k == 'cleanup':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/" + j + "/func/"
                x = "Now deleting junk extra files."
                print(x)
                log.append(x) 
                
                input_file = dir_in + person + "_" + j + '_' + axfmcsfinput + '_flirt.mat'
                if os.path.isfile(input_file) == True:
                    os.remove(input_file)

                input_file = dir_in + person + "_" + j + '_' + axfmwminput + '_flirt.mat'
                if os.path.isfile(input_file) == True:
                    os.remove(input_file)

                input_file = dir_in + person + "_" + j + '_' + axfminput + '_flirt.mat'
                if os.path.isfile(input_file) == True:
                    os.remove(input_file)
                                       
                input_file = dir_in + person + "_" + j + '_' + axfmcsfinput + '_funcjunk1.nii.gz'
                if os.path.isfile(input_file) == True:
                    os.remove(input_file)                    
                input_file = dir_in + person + "_" + j + '_' + axfmcsfinput + '_funcjunk2.nii.gz'
                if os.path.isfile(input_file) == True:
                    os.remove(input_file) 
    
                input_file = dir_in + person + "_" + j + '_' + axfmwminput + '_funcjunk1.nii.gz'
                if os.path.isfile(input_file) == True:
                    os.remove(input_file)                    
                input_file = dir_in + person + "_" + j + '_' + axfmwminput + '_funcjunk2.nii.gz'
                if os.path.isfile(input_file) == True:
                    os.remove(input_file) 


                input_file = dir_in + person + "_" + j + '_' + mcf2output + '.nii.gz_abs_mean.rms'
                if os.path.isfile(input_file) == True:
                    os.remove(input_file)
                input_file = dir_in + person + "_" + j + '_' + mcf2output + '.nii.gz_abs.rms'
                if os.path.isfile(input_file) == True:
                    os.remove(input_file)
                input_file = dir_in + person + "_" + j + '_' + mcf2output + '.nii.gz_rel_mean.rms'
                if os.path.isfile(input_file) == True:
                    os.remove(input_file)                    
                input_file = dir_in + person + "_" + j + '_' + mcf2output + '.nii.gz_rel.rms'
                if os.path.isfile(input_file) == True:
                    os.remove(input_file)
                input_file = dir_in + person + "_" + j + '_' + mcf2output + '.nii.gz.par'
                if os.path.isfile(input_file) == True:
                    os.remove(input_file)



                input_file = dir_in + person + "_" + j + '_' + mumask + 'erode_flirt.mat'
                if os.path.isfile(input_file) == True:
                    os.remove(input_file)
                input_file = dir_in + person + "_" + j + '_' + mumask + 'erode.nii.gz'
                if os.path.isfile(input_file) == True:
                    os.remove(input_file)
                input_file = dir_in + person + "_" + j + '_' + mumask + 'junk.nii.gz'
                if os.path.isfile(input_file) == True:
                    os.remove(input_file)
                input_file = dir_in + person + "_" + j + '_' + mumask + 'upview_mat'
                if os.path.isfile(input_file) == True:
                    os.remove(input_file)
                input_file = dir_in + person + "_" + j + '_' + mumask + 'upview.nii.gz'
                if os.path.isfile(input_file) == True:
                    os.remove(input_file)
                      
                dir_in_input = dir_in + "split"
                if os.path.exists(dir_in_input):
                    shutil.rmtree(dir_in_input)
                    
                dir_in_input = dir_in + person + "_" + j + "_" + mcf1output + ".nii.gz.mat"
                #print(dir_in_input)
                if os.path.exists(dir_in_input):
                    #print(dir_in_input)
                    shutil.rmtree(dir_in_input)

                dir_in_input = dir_in + person + "_" + j + "_" + mcf2output + ".nii.gz.mat"
                #print(dir_in_input)
                if os.path.exists(dir_in_input):
                    #print(dir_in_input)
                    shutil.rmtree(dir_in_input)
                        
                        
#We've escaped the big loop. Let's wrap up this program.

  

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


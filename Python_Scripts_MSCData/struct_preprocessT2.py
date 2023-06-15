#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 16:56:52 2020

@author: shefalirai
"""


"""
Update log: 
Use this file for T2 structural preprocessing
Updated the name of the code: struct_preprocessT2
Edited code for MSC dataset
July 2020

Originally Guinevere:
Structural Preprocessing Pipeline
Version 1.24

Update log: 
v1.24
Added comments to code. Yay best practice
Updated erosion
Made it so erosion can still occur even if file already exists
V1.23
Removed bad realignment


Location: Alberta Children's Hospital
Date: 2019-03-13

"""




"""***********"""
"""RANDOM INFO"""
"""**************

If you're not sure which participants to use, type 'os.listdir(dir_start)'
If your participant of choice is the 2nd file listed, then set participants as
participants = [1]
If your participants of choice are the 100th and 101st files listed, then set participants as
participants = [99,100]

You can guess and check using: 
os.listdir(dir_start)[x]
(where x is some number, perhaps 20)

Shefali's note: make sure you run Sypder through terminal and not the desktop Anaconda

Shefali notes:
For Afni it seems like you need to add to path always before running spyder. To avoid error: 3dmask_tool command not found 
Must type in bash: 
    bash-3.2$ export PATH=/usr/lib/afni/bin:$PATH
    bash-3.2$ spyder
Then run script

"""

"""***********************"""
"""GENERAL PROGRAM OPTIONS"""
"""***********************"""
#what directory are your images saved in?
dir_start = "/Users/shefalirai/Desktop/msc_processed/"

#what directory is your template saved in?
template_dir = "/Users/shefalirai/Desktop/mni/"

#what participants do you want this to run on? e.g. [1,2,3] or list(range(1,4))
#this is based on the files in the directory. 0 = first file in directory. 0 = DS_Store in my directory. 
participants = [1,2,3,4,5,6,7,8,9,10]
#participants = list(range(1, 59))


#if replacer is false, the program won't run if output image already exists
#if replacer is true, the program will write over outputs that already exist
replacer = False

#name of log book that output is saved to
logname = 'xstruct_logbook.txt'


#what steps do you want to run? For full preprocessing type:
steps = ['n4','abe','ar','atrop','segwarp','wmmask','erode']
#the steps are run in the order listed

#steps = ['filechecker']
#n4 = Use ANTs N4BiasFieldCorrection to correct for inhomogenities. ~7 minutes per image
#abe = Use ANTs BrainExtraction to remove skull and non-brain tissue. ~60 minutes per image
#ar = Use ANTs Registration to warp brain to a template. ~90 minutes per image
#atrop = Use ANTs ATROPOS to generate tissue segmentations. ~5 minutes per image.
#segwarp = Use ANTs Apply Transformations to warp segmentations back to native space. Very quick
#wmmask = Use fslmaths to generate a binary mask of the white matter. Used for BBR. Very quick
#erode = use AFNI to erode tissue segments. Very quick
#filechecker = checks if a file exists or not. Should probably be run independent of other steps


"""******************"""
"""SEND EMAIL OPTIONS"""
"""******************"""
#if sendemail is True, the program will email you the log book when it finishes doing what it's doing
sendemail = False

receiver_email = "shefali.s.rai@gmail.com"
subject = "Python Program Update"
body = "Python program finished running. See attached log."



"""**************************************"""
"""n4: ANTs N4BiasFieldCorrection OPTIONS"""
"""**************************************"""
n4input = "T2wFltmean"
n4output = "T2wFltmeanAbfc"


"""**********************************"""
"""abe: ANTs Brain Extraction OPTIONS"""
"""**********************************"""
abeinput = "T2wFltmeanAbfc"
abeoutput = "T2wFltmeanAbfcBe"

#specify what you want to use as a reference for brain extraction. MNI template. 
abetemplate = template_dir + "mni_icbm152_t2_tal_nlin_asym_09c.nii"
abetemplatemask = template_dir + "mni_icbm152_t1_tal_nlin_asym_09c_mask.nii"


"""****************************"""
"""ar: AntsRegistration OPTIONS"""
"""****************************"""
arinputmoving = "T2wFltmeanAbfcBe"
aroutput = "T2wFltmeanAbfcBeAr"

armatrixoutputname = "transformT2wFltmeantoMNI"
#the outputed matrix will add .h5 to the above name"
#you'll also generate the inverse matrix that has added inverse.h5 to the above name

#specify what you want to warp the input to. MNI template.
arinputfixedimage = template_dir + "mni_icbm152_t2_tal_nlin_asym_09c.nii"
arinputfixedmask = template_dir + "mni_icbm152_t1_tal_nlin_asym_09c_mask.nii"


"""***************************"""
"""atrop: ANTs Atropos OPTIONS"""
"""***************************"""
#your input should be in the same space as the tissue priors you're feeding in
atropinput = "T2wFltmeanAbfcBeAr"
atropCSFoutput = "T2wFltmeanAbfcBeArCSF"
atropGMoutput = "T2wFltmeanAbfcBeArGM"
atropWMoutput = "T2wFltmeanAbfcBeArWM"

#tt0 is a list with the tissue priors of a template
# CSF file = tissue1
# GM file = tissue2
# WM file = tissue3
tt0 = template_dir + "mni_icbm152_tissuet%02d.nii"


#template mask file
atropmask = template_dir + "mni_icbm152_t1_tal_nlin_asym_09c_mask.nii"


"""*******************************************"""
"""segwarp: ANTs Apply Transformations OPTIONS"""
"""*******************************************"""
segwarpinput1 = "T2wFltmeanAbfcBeArCSF"
segwarpoutput1 = "T2wFltmeanAbfcBeCSF"

segwarpinput2 = "T2wFltmeanAbfcBeArGM"
segwarpoutput2 = "T2wFltmeanAbfcBeGM"

segwarpinput3 = "T2wFltmeanAbfcBeArWM"
segwarpoutput3 = "T2wFltmeanAbfcBeWM"

#what matrix file warps the inputs to the outputs?
segwarpmatrix = "transformT2wFltmeantoMNIinverse.h5" 

#give a reference image for the output files. Presumably the native space image
segwarpreference = "T2wFltmeanAbfcBe"


"""*************************"""
"""wmmask: fslmaths OPTIONS"""
"""*************************"""
wmmaskinput = "T2wFltmeanAbfcBeWM"
wmmaskoutput = "T2wFltmeanAbfcBeWM_binary"

#removes everything below this threshold (a percentage)
wmmasklowthreshold = 25


"""*****************************"""
"""erode: AFNI Mask Tool OPTIONS"""
"""*****************************"""
erodeinput1 = "T2wFltmeanAbfcBeCSF"
erodeoutput1 = "T2wFltmeanAbfcBeCSF_Erode"

erodeinput2 = "T2wFltmeanAbfcBeGM"
erodeoutput2 = "T2wFltmeanAbfcBeGM_Erode"

erodeinput3 = "T2wFltmeanAbfcBeWM"
erodeoutput3 = "T2wFltmeanAbfcBeWM_Erode"


"""*******************"""
"""filechecker OPTIONS"""
"""*******************"""
#this checks if files exist or not. Useful to see if you've run a program already
#or not
filecheckerfile = "T2wFltmeanAbfcBeWM_Erode.nii.gz"

filecheckerbids = True
#if the above is True, the program will tack on the ID# and session before
#checking the file. If False, it will only check for the file name as specified



"""*****************************************"""
"""ANYTHING BELOW HERE DOESN'T NEED CHANGING"""
"""**********(OR SO KIRK HOPES)*************"""
"""*****************************************"""

import nipype.interfaces.fsl as fsl
import nipype.interfaces.afni as afni
import nipype.interfaces.ants as ants
import os
import time
# import smtplib, ssl
# from email import encoders
# from email.mime.base import MIMEBase
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText


#options for sending an email. Best practice says not to store a password in plain text,
#but I don't care about the email address "kirkpython". If this program ever leaves the lab,
#use your own email address. Or don't - I don't care that much
# sender_email = "kirkpython@gmail.com"
# password = "TheScream"
# message = MIMEMultipart()
# message["From"] = sender_email
# message["To"] = receiver_email
# message["Subject"] = subject
# message.attach(MIMEText(body, "plain"))
# filename = logname


#get the current time
totaltimer = time.time()

#get a list of everything in the starting directory
participant_folders = sorted(os.listdir(dir_start))

log = ["*************************************************"]
log.append('Starting log for ' + time.ctime())
logexist = ['The images listed below exist: ']
lognoexist = ['The images listed below do not exist: ']


#The Big For Loop. Holding the bulk of code in this program
#loop through all steps specified
#most of these steps are similar. See comments for n4
for k in steps:

    # if k == 'filechecker':
    #     for i in participants:
    #         person = participant_folders[i]
    #         for j in imagesession:
    #             dir_in = dir_start + person + "/" + j + "/anat/"
    #             if filecheckerbids == True:
    #                 input_file = dir_in + person + "_" + j + "_" + filecheckerfile
    #             else:
    #                 input_file = dir_in + filecheckerfile
    #             if os.path.isfile(input_file) == False:
    #                 lognoexist.append(input_file)
    #             else:
    #                 logexist.append(input_file)

    
    if k == 'n4':
        for i in participants:
            person = participant_folders[i]
            dir_in = dir_start + person + "/" + "anat/"
            input_file = dir_in + person + "_" + n4input + ".nii.gz"
            output_file = dir_in + person + "_" + n4output + ".nii.gz"
                #check if the input_file actually exists
            if os.path.isfile(input_file) == False:
                #if it doesn't exist, try .nii instead of .nii.gz
                input_file = dir_in + person + "_" + n4input + ".nii"
                #check again if the input_file exists
            if os.path.isfile(input_file) == False:
                #if it doesn't exist, put this info in the log
                x = "This file doesn't exist: " + input_file
                print(x)
                log.append(x)
            else:
                #nipype code only runs if doit is true. Various checks turn it off
                doit = True
                if replacer == False:
                    #check if output_file already exists
                    if os.path.isfile(output_file) == True:
                         x = "N4BiasFieldCorrection did not run; file already exists for " + output_file + ".nii.gz"
                         print(x)
                         log.append(x)
                #prevent the preprocessing from happening if replacer==False and the output already exists
                         doit = False                    
                    if doit == True:
                    #determine the current time
                        steptimer = time.time()
                        x = "ANTs N4BiasFieldCorrection is beginning to run. You're N4 a treat!"
                        print(x)
                        log.append(x)
                    #nipype code is put in a try statement so that if it fails the rest of the program can still run
                        try:
                        #woooo nipype code
                            myabfc = ants.N4BiasFieldCorrection()
                            myabfc.inputs.input_image = input_file
                            myabfc.inputs.output_image = output_file            
                            myabfc.run()
                            x = "N4BiasFieldCorrection probably created " + output_file
                            print(x)
                            log.append(x)      
                        # except:
                        #     x = "N4BiasFieldCorrection failed."
                        #     print(x)
                        #     log.append(x)
                        except Exception as e: print(e)
                        #determine how long the program took by subtracting the current time from the old time
                        steptimer = round(time.time()-steptimer,3)
                        x = "Individual step took " + str(steptimer) + " s to run."
                        print(x)
                        log.append(x)
                        #convert time to minutes
                        steptimermin = round(steptimer/60,3)
                        x = "(which is " + str(steptimermin) + " minutes)"
                        print(x)
                        log.append(x)
    
                  
    if k == 'abe':
        for i in participants:
            person = participant_folders[i]
            # for j in imagesession:
            dir_in = dir_start + person + "/" + "anat/"
            input_file = dir_in + person + "_" + abeinput + ".nii.gz"
            output_file = dir_in + person + "_" + abeoutput + ".nii.gz"
            if os.path.isfile(input_file) == False:
                x = "This file doesn't exist: " + input_file
                print(x)
                log.append(x)
            else:
                doit = True
                if replacer == False:
                    if os.path.isfile(output_file) == True:
                          x = "ANTs Brain Extraction did not run; file already exists for " + output_file + ".nii.gz"
                          print(x)
                          log.append(x)
                          doit = False
                    if doit == True:                    
                        steptimer = time.time()
                        os.chdir(dir_in)

                        x = "ANTs BrainExtraction will now try to run. Ants have tiny, hard to extract, brains."
                        print(x)
                        log.append(x)
                        try:
                            myabe = ants.BrainExtraction()
                            myabe.inputs.anatomical_image = input_file
                            myabe.inputs.brain_probability_mask = abetemplatemask
                            myabe.inputs.brain_template = abetemplate
                            myabe.inputs.out_prefix = output_file
                        
                            myabe.run()
                            os.rename(output_file + 'BrainExtractionBrain.nii.gz', output_file) #shefali removed ' + ".nii.gz"' after the output_file because creating double .nii.gz at the end 
                            x = "BrainExtraction probably created " + output_file + ".nii.gz"
                            print(x)
                            log.append(x)
                        # except:
                        #     x = "ANTs Brain Extraction failed."
                        #     print(x)
                        #     log.append(x)
                        except Exception as e: print(e)
                        steptimer = round(time.time()-steptimer,3)
                        x = "Individual step took " + str(steptimer) + " s to run."
                        log.append(x)
                        print(x)
                        steptimermin = round(steptimer/60,3)
                        x = "(which is " + str(steptimermin) + " minutes)"
                        print(x)
                        log.append(x)
                        

    if k == 'ar':
        for i in participants:
            person = participant_folders[i]
            dir_in = dir_start + person + "/" + "anat/"
            input_file = dir_in + person + "_" + arinputmoving + ".nii.gz"
            output_file = dir_in + person + "_" + aroutput + ".nii.gz"
            if os.path.isfile(input_file) == False:
                x = "This file doesn't exist: " + input_file
                print(x)
                log.append(x)
            else:
                doit = True
                if replacer == False:
                    if os.path.isfile(output_file) == True:
                        x = "Ants Registration did not run; file already exists for " + output_file
                        print(x)
                        log.append(x)
                        doit = False
                    if doit == True:
                        steptimer = time.time()
                        os.chdir(dir_in)

                        x = "ANTs Registration will now try to run. Registration? I prefer Regisphilbin."
                        print(x)
                        log.append(x)
                        try:
                            myar = ants.Registration()
                            myar.inputs.fixed_image = arinputfixedimage
                            myar.inputs.fixed_image_masks = arinputfixedmask
                            myar.inputs.moving_image = input_file
                            # myar.inputs.output_warped_image = output_file
                            #for some reason, this decided to stop working??? So now I rename the default output
                        
                            #kirk barely understands anything in this section
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
                            #rename all the output names from their defaults to names we've specified
                            os.rename('transform_Warped.nii.gz',output_file)
                            os.rename('transformComposite.h5',armatrixoutputname + '.h5')
                            os.rename('transformInverseComposite.h5',armatrixoutputname + 'inverse.h5')
                            os.rename('transform_InverseWarped.nii.gz',armatrixoutputname + 'inverse.nii.gz')    
                            x = "ANTs Registration probably created " + output_file
                            print(x)
                            log.append(x)
                        except Exception as e: print(e)
                            # x = "ANTs Registration failed."
                            # print(x)
                            # log.append(x)
                        steptimer = round(time.time()-steptimer,3)
                        steptimermin = round(steptimer/60,3)
                        x = "Individual step took " + str(steptimer) + " s to run."
                        log.append(x)
                        print(x)
                        x = "(which is " + str(steptimermin) + " minutes)"
                        print(x)
                        log.append(x)
                        

    if k == 'atrop':
        for i in participants:
            person = participant_folders[i]
            dir_in = dir_start + person + "/" + "anat/"
            input_file = dir_in + person + "_" + atropinput + ".nii.gz"
            output_fileCSF = dir_in + person + "_" + atropCSFoutput + ".nii.gz"
            output_fileGM = dir_in + person + "_" + atropGMoutput + ".nii.gz"
            output_fileWM = dir_in + person + "_" + atropWMoutput + ".nii.gz"
            if os.path.isfile(input_file) == False:
                x = "This file doesn't exist: " + input_file
                print(x)
                log.append(x)
            else:
                doit = True
                if replacer == False:
                    if os.path.isfile(output_fileWM) == True:
                            x = "Ants Atropos did not run; file already exists for " + output_fileWM
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        steptimer = time.time()
                        os.chdir(dir_in)

                        x = "ANTs Atropos will now try to run. Atropos was one of the Three Fates who ended the life of mortals. Fitting?"
                        print(x)
                        log.append(x)
                        try:
                            myatrop = ants.Atropos()
                            myatrop.inputs.intensity_images = input_file
                            myatrop.inputs.mask_image = atropmask
                            myatrop.inputs.prior_image = tt0
                    
                            #kirk barely understands anything in this section
                            myatrop.inputs.dimension = 3
                            myatrop.inputs.initialization = 'PriorProbabilityImages'
                            myatrop.inputs.number_of_tissue_classes = 3
                            myatrop.inputs.prior_weighting = 0.8
                            myatrop.inputs.prior_probability_threshold = 0.0000001
                            myatrop.inputs.likelihood_model = 'Gaussian'
                            myatrop.inputs.mrf_smoothing_factor = 0.2
                            myatrop.inputs.mrf_radius = [1, 1, 1]
                            myatrop.inputs.n_iterations = 5
                            myatrop.inputs.convergence_threshold = 0.000001
                            myatrop.inputs.posterior_formulation = 'Socrates'
                            myatrop.inputs.use_mixture_model_proportions = True
                            myatrop.inputs.save_posteriors = True                            
                            
                            myatrop.run()
                            #rename outputs from their default to names we've specified
                            os.rename('POSTERIOR_01.nii.gz',output_fileCSF)
                            os.rename('POSTERIOR_02.nii.gz',output_fileGM)
                            os.rename('POSTERIOR_03.nii.gz',output_fileWM)   
                            x = "ANTs Atropos probably created " + output_fileWM
                            print(x)
                            log.append(x)
                        except Exception as e: print(e)
                            # x = "ANTs Atropos failed."
                            # print(x)
                            # log.append(x)
                        steptimer = round(time.time()-steptimer,3)
                        steptimermin = round(steptimer/60,3)
                        x = "Individual step took " + str(steptimer) + " s to run."
                        log.append(x)
                        print(x)
                        x = "(which is " + str(steptimermin) + " minutes)"
                        print(x)
                        log.append(x)                       


    if k == 'segwarp':
        for i in participants:
            person = participant_folders[i]
            dir_in = dir_start + person + "/" + "anat/"
            input_file1 = dir_in + person + "_" + segwarpinput1 + ".nii.gz"
            output_file1 = dir_in + person + "_" + segwarpoutput1 + ".nii.gz"
            input_file2 = dir_in + person + "_" + segwarpinput2 + ".nii.gz"
            output_file2 = dir_in + person + "_" + segwarpoutput2 + ".nii.gz"
            input_file3 = dir_in + person + "_" + segwarpinput3 + ".nii.gz"
            output_file3 = dir_in + person + "_" + segwarpoutput3 + ".nii.gz"
            if os.path.isfile(input_file1) == False:
                x = "This file doesn't exist: " + input_file1
                print(x)
                log.append(x) 
            else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file1) == True:
                            x = "Ants ApplyTransforms did not run; file already exists for " + output_file1
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        steptimer = time.time()
                        os.chdir(dir_in)
                        
                        x = "ANTs ApplyTransforms will now try to run. Don't transform yourself to fit someone else's expectations."
                        print(x)
                        log.append(x)                        
                        try:
                            myaat = ants.ApplyTransforms()
                            myaat.inputs.reference_image = dir_in + person + "_" + segwarpreference + ".nii.gz"
                            myaat.inputs.transforms = segwarpmatrix                            
                            myaat.inputs.input_image = input_file1                        
                            myaat.inputs.output_image = output_file1
                            myaat.run()
                            
                            myaat.inputs.input_image = input_file2                        
                            myaat.inputs.output_image = output_file2
                            myaat.run()
                            
                            myaat.inputs.input_image = input_file3                        
                            myaat.inputs.output_image = output_file3
                            myaat.run()
                            
                            x = "ANTs ApplyTransforms probably created " + output_file1
                            print(x)
                            log.append(x)
                        except Exception as e: print(e)
                            # x = "ANTs ApplyTransforms failed."
                            # print(x)
                            # log.append(x)
                        steptimer = round(time.time()-steptimer,3)
                        steptimermin = round(steptimer/60,3)
                        x = "Individual step took " + str(steptimer) + " s to run."
                        log.append(x)
                        print(x)
                        x = "(which is " + str(steptimermin) + " minutes)"
                        print(x)
                        log.append(x)

                    
    if k == 'wmmask':
        for i in participants:
            person = participant_folders[i]
            dir_in = dir_start + person + "/" + "anat/"
            input_file = dir_in + person + "_" + wmmaskinput + ".nii.gz"
            intermediate = dir_in + person + "_" + "_WhiteMatterT2_rlt.nii.gz"
            output_file = dir_in + person + "_" + wmmaskoutput + ".nii.gz"
            if os.path.isfile(input_file) == False:
                x = "This file doesn't exist: " + input_file
                print(x)
                log.append(x)
            else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file) == True:
                            x = "WM Mask did not run; file already exists for " + output_file
                            print(x)
                            log.append(x)
                            doit = False                    
                    if doit == True:
                        steptimer = time.time()
                        
                        myrlt = fsl.Threshold()
                        x = "WM Mask will now try to run. Woop woop"
                        print(x)
                        log.append(x)
                        try:
                            myrlt.inputs.in_file = input_file
                            myrlt.inputs.out_file = intermediate
                            myrlt.inputs.use_robust_range = True
                            myrlt.inputs.thresh = wmmasklowthreshold
                            myrlt.inputs.use_nonzero_voxels = True
                            myrlt.run()

                            #this converts what's left into a binary
                            mybin = fsl.UnaryMaths()
                            mybin.inputs.in_file = intermediate
                            mybin.inputs.out_file = output_file
                            mybin.inputs.operation = 'bin'
                            mybin.run()

                            x = "WM Mask probably created " + output_file
                            print(x)
                            log.append(x)    
                        except:
                            x = "WM Mask failed."
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




    if k == 'erode':
        for i in participants:
            person = participant_folders[i]
            dir_in = dir_start + person + "/" + "anat/"
            input_file1 = dir_in + person + "_" + erodeinput1 + ".nii.gz"
            intermediate1 = dir_in + person + "_" + "_csfthreshT2.nii.gz"
            output_file1 = dir_in + person + "_" + erodeoutput1 + ".nii.gz"
            input_file2 = dir_in + person + "_" + erodeinput2 + ".nii.gz"
            intermediate2 = dir_in + person + "_" + "_gmthreshT2.nii.gz"
            output_file2 = dir_in + person + "_" + erodeoutput2 + ".nii.gz"
            input_file3 = dir_in + person + "_" + erodeinput3 + ".nii.gz"
            output_file3 = dir_in + person + "_" + erodeoutput3 + ".nii.gz"
            intermediate3 = dir_in + person + "_" + "_wmthreshT2.nii.gz"
            if os.path.isfile(input_file1) == False:
                x = "This file doesn't exist: " + input_file1
                print(x)
                log.append(x) 
            else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(output_file1) == True:
                            x = "Erode did not run; file already exists for " + output_file1
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        steptimer = time.time()
                        os.chdir(dir_in)
                        
                        x = "We will now try to erode tissue."
                        print(x)
                        log.append(x)                        
                        try:
                            #first remove low threshold
                            threshold = fsl.Threshold()
                            threshold.inputs.in_file = input_file1
                            threshold.inputs.out_file = intermediate1
                            threshold.inputs.use_robust_range = True
                            #lowest 10% removed
                            threshold.inputs.thresh = 10
                            threshold.inputs.use_nonzero_voxels = True
                            threshold.run()
                            
                            threshold.inputs.in_file = input_file2
                            threshold.inputs.out_file = intermediate2
                            threshold.run()
                            
                            threshold.inputs.in_file = input_file3
                            threshold.inputs.out_file = intermediate3
                            threshold.run()                           

                            #erode CSF
                            erosionCSF = afni.MaskTool()
                            erosionCSF.inputs.in_file = intermediate1
                            erosionCSF.inputs.out_file = output_file1
                            erosionCSF.inputs.outputtype = 'NIFTI_GZ'
                            #2 rounds of erosion
                            erosionCSF.inputs.dilate_inputs = '-2'
                            erosionCSF.inputs.args = "-overwrite"
                            erosionCSF.run()
 
                            #erode GM
                            erosionGM = afni.MaskTool()
                            erosionGM.inputs.in_file = intermediate2
                            erosionGM.inputs.out_file = output_file2
                            erosionGM.inputs.outputtype = 'NIFTI_GZ'
                            #7 rounds of erosion
                            erosionGM.inputs.dilate_inputs = '-7'
                            erosionGM.inputs.args = "-overwrite"
                            erosionGM.run()
                            
                            #erode WM
                            erosionWM = afni.MaskTool()
                            erosionWM.inputs.in_file = intermediate3
                            erosionWM.inputs.out_file = output_file3
                            erosionWM.inputs.outputtype = 'NIFTI_GZ'
                            #7 rounds of erosion
                            erosionWM.inputs.dilate_inputs = '-7'
                            erosionWM.inputs.args = "-overwrite"
                            erosionWM.run()                            
                            
                            x = "Erosion probably created " + output_file1
                            print(x)
                            log.append(x)
                        except Exception as e: print(e)
                            # x = "Erosion failed."
                            # print(x)
                            # log.append(x)
                        steptimer = round(time.time()-steptimer,3)
                        steptimermin = round(steptimer/60,3)
                        x = "Individual step took " + str(steptimer) + " s to run."
                        log.append(x)
                        print(x)
                        x = "(which is " + str(steptimermin) + " minutes)"
                        print(x)
                        log.append(x)
                        
            
#We escaped the Big For Loop. Time to wrap up what this program does   

if 'filechecker' in steps:
    for item in logexist:
        x = item
        print(x)
        log.append(x)
    log.append('')
    for item in lognoexist:
        x = item
        print(x)
        log.append(x)   
    log.append('***')
    log.append('')                  
 

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
        
# if sendemail == True:
#     # Open PDF file in binary mode
#     with open(filename, "rb") as attachment:
#         # Add file as application/octet-stream
#         # Email client can usually download this automatically as attachment
#         part = MIMEBase("application", "octet-stream")
#         part.set_payload(attachment.read())

#     # Encode file in ASCII characters to send by email    
#     encoders.encode_base64(part)

#     # Add header as key/value pair to attachment part
#     part.add_header(
#         "Content-Disposition",
#         f"attachment; filename= {filename}",
#     )

#     # Add attachment to message and convert message to string
#     message.attach(part)
#     text = message.as_string()

#     # Log in to server using secure context and send email
#     context = ssl.create_default_context()
#     with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, text)

#     print("Email was sent to " + receiver_email + " containing " + logname)                    
                    
  
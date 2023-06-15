
"""

Script for linear registration.

Lines up T1s together and the T2s together

Created on Tue Jul 14 11:37:42 2020

@author: shefalirai

Notes:
c3d_affine_tool must be installed beforehand. See link: 
http://miykael.github.io/nipype-beginner-s-guide/normalize.html

Before starting spyder in terminal type:
    export PATH=/Applications/Convert3DGUI.app/Contents/bin:$PATH
Depending on Mac permissions, may have to open the GUI from applications folder first

"""


dir_start = '/Users/shefalirai/Desktop/msc_preprocessed/'

steps = ["linregisT1", "linregisT2", "meanT1", "meanT2", "linregis_meanT1T2"]


#linregisT1 = register all 3 T1 MSC images to the reference T1 image chosen. Uses FLIRT.
#linregisT2 = register all 3 T2 MSC images to the reference T2 image chosen. Uses FLIRT. 
#linregis_meanT1 = average all 4 T1 images together to create 1 T1fltmean image. Uses FSL MultiImageMaths. 
#linregis_meanT2 = average all 4 T2 images together to create 1 T2fltmean image. Uses FSL MultiImageMaths. 
#linregis_meanT1T2 = Warp the T2 averaged(T2fltmean) and T1 averaged(T1fltmean) using FLIRT linear registration again. 

participants = [1,2,3,4,5,6,7,8,9,10]

# Naming from original MSC dataset
# reference_T1w = sub-MSC#_ses-struct01_run-01_T#w.nii
# struct2 = sub-MSC#_ses-struct01_run-02_T#w.nii
# struct3 = sub-MSC#_ses-struct02_run-01_T#w.nii
# struct4 = sub-MSC#_ses-struct02_run-02_T#w.nii

imagesession = ["ses-struct01_run-02","ses-struct02_run-01", "ses-struct02_run-02"]
flirtreferenceT1 = "ses-struct01_run-01_T1w"
flirtreferenceT2 = "ses-struct01_run-01_T2w"

import nipype.interfaces.fsl as fsl
from nipype.interfaces.c3 import C3dAffineTool
from nipype.interfaces.fsl import MultiImageMaths
import os
import time

participant_folders = sorted(os.listdir(dir_start))

"""*****************"""
"""T1 FLIRT OPTIONS"""
"""*****************"""
flirtinputT1 = "T1w"
flirtoutputT1 = "T1wFlt"

"""*****************"""
"""T2 FLIRT OPTIONS"""
"""*****************"""
flirtinputT2 = "T2w"
flirtoutputT2 = "T2wFlt"

"""*****************"""
"""FSLMATHS T1MEAN OPTIONS"""
"""*****************"""

meanoutputT1 = "T1wFltmean"

"""*****************"""
"""FSLMATHS T2MEAN OPTIONS"""
"""*****************"""

meanoutputT2 = "T2wFltmean"

"""*****************"""
"""T1&T2MEAN FLIRT OPTIONS"""
"""*****************"""
flirtinputT2mean = "T2wFltmean"
flirtinputT1mean = "T1wFltmean"
flirtoutputT1T2mean = "T1T2wFltmean"


for k in steps: 
    
    if k == 'linregisT1':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/anat/"
                input_file = dir_in + person + "_" + j + "_" + flirtinputT1 + ".nii.gz"
                output_file = dir_in + person + "_" + j + "_" + flirtoutputT1 + ".nii.gz"
                input_reference = dir_start + person + "/anat/" + person + "_" + flirtreferenceT1 + ".nii.gz"

                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                else:
                    doit = True
                    if os.path.isfile(output_file) == True:
                            x = "FLIRT did not run; file already exists for " + output_file
                            print(x)
                            doit = False
                    if doit == True:
                        steptimer = time.time()
                        os.chdir(dir_in)

                        x = "FSL will now try to FLIRT with you"
                        print(x)
                        try:
                            os.chdir(dir_in)
                            myflirt = fsl.FLIRT()
                            myflirt.inputs.in_file = input_file
                            myflirt.inputs.reference = input_reference
                            myflirt.inputs.out_file = output_file
                            #ciric et al says to use 9 DOF. Though FSL default is 12...some say 6 for high quality T1s
                            myflirt.inputs.dof = 6
                            myflirt.inputs.out_matrix_file = dir_in + person + "_" + j + "_" + flirtoutputT1 + "_mat"
                            myflirt.run()
    
                            c3 = C3dAffineTool()
                            c3.inputs.source_file = input_file
                            c3.inputs.reference_file = input_reference
                            
                            c3.inputs.itk_transform = dir_in + person + "_" + j + "_" + flirtoutputT1 + ".h5"
                            c3.inputs.transform_file = dir_in + person + "_" + j + "_" + flirtoutputT1 + "_mat"
                            
                            c3.inputs.fsl2ras = True
                            c3.run()                            
      
                            x = "FLIRT probably created " + output_file
                            print(x)
                            
                        except Exception as e: print(e)
                        
                        steptimer = round(time.time()-steptimer,3)
                        steptimermin = round(steptimer/60,3)
                        x = "Individual step took " + str(steptimer) + " s to run."
                        print(x)
                        x = "(which is " + str(steptimermin) + " minutes)"
                        print(x)
                        
                        
    if k == 'linregisT2':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/anat/"
                input_file = dir_in + person + "_" + j + "_" + flirtinputT2 + ".nii.gz"
                output_file = dir_in + person + "_" + j + "_" + flirtoutputT2 + ".nii.gz"
                input_reference = dir_start + person + "/anat/" + person + "_" + flirtreferenceT2 + ".nii.gz"

                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                else:
                    doit = True
                    if os.path.isfile(output_file) == True:
                            x = "FLIRT did not run; file already exists for " + output_file
                            print(x)
                            doit = False
                    if doit == True:
                        steptimer = time.time()
                        os.chdir(dir_in)

                        x = "FSL will now try to FLIRT with you"
                        print(x)
                        try:
                            os.chdir(dir_in)
                            myflirt = fsl.FLIRT()
                            myflirt.inputs.in_file = input_file
                            myflirt.inputs.reference = input_reference
                            myflirt.inputs.out_file = output_file
                            #ciric et al says to use 9 DOF. Though FSL default is 12...some say 6 for high quality T1s
                            myflirt.inputs.dof = 6
                            myflirt.inputs.out_matrix_file = dir_in + person + "_" + j + "_" + flirtoutputT2 + "_mat"
                            myflirt.run()
    
                            c3 = C3dAffineTool()
                            c3.inputs.source_file = input_file
                            c3.inputs.reference_file = input_reference
                            
                            c3.inputs.itk_transform = dir_in + person + "_" + j + "_" + flirtoutputT2 + ".h5"
                            c3.inputs.transform_file = dir_in + person + "_" + j + "_" + flirtoutputT2 + "_mat"
                            
                            c3.inputs.fsl2ras = True
                            c3.run()                            
      
                            x = "FLIRT probably created " + output_file
                            print(x)
                            
                        except Exception as e: print(e)
                        
                        steptimer = round(time.time()-steptimer,3)
                        steptimermin = round(steptimer/60,3)
                        x = "Individual step took " + str(steptimer) + " s to run."
                        print(x)
                        x = "(which is " + str(steptimermin) + " minutes)"
                        print(x)

    if k == 'meanT1':
        for i in participants:
            person = participant_folders[i]
            dir_in = dir_start + person + "/anat/"
            input_file = dir_in + person + "_" + flirtreferenceT1 + ".nii.gz"
            output_file = dir_in + person + "_" + meanoutputT1 + ".nii.gz"

            if os.path.isfile(input_file) == False:
                x = "This file doesn't exist: " + input_file
                print(x)
            else:
                doit = True
                if os.path.isfile(output_file) == True:
                    x = "FSLMATHS Mean did not run; file already exists for " + output_file
                    print(x)
                    doit = False
                if doit == True:
                    steptimer = time.time()
                    os.chdir(dir_in)
                    
                    x = "FSL will now try to be mean to you."
                    print(x)
                    try:
                        os.chdir(dir_in)
                        mymean = fsl.MultiImageMaths()
                        mymean.inputs.in_file = input_file
                        mymean.inputs.op_string = "-add %s -add %s -add %s -div 4"
                        mymean.inputs.operand_files = [person + '_ses-struct01_run-02_T1wflt.nii.gz', person + '_ses-struct02_run-01_T1wflt.nii.gz', person + '_ses-struct02_run-02_T1wflt.nii.gz']
                        mymean.inputs.out_file = output_file
                        mymean.run()

                        x = "MEANT1 probably created " + output_file
                        print(x)
                            
                    except Exception as e: print(e)
                        
                    steptimer = round(time.time()-steptimer,3)
                    steptimermin = round(steptimer/60,3)
                    x = "Individual step took " + str(steptimer) + " s to run."
                    print(x)
                    x = "(which is " + str(steptimermin) + " minutes)"
                    print(x)                
                        

    if k == 'meanT2':
        for i in participants:
            person = participant_folders[i]
            dir_in = dir_start + person + "/anat/"
            input_file = dir_in + person + "_" + flirtreferenceT2 + ".nii.gz"
            output_file = dir_in + person + "_" + meanoutputT2 + ".nii.gz"

            if os.path.isfile(input_file) == False:
                x = "This file doesn't exist: " + input_file
                print(x)
            else:
                doit = True
                if os.path.isfile(output_file) == True:
                    x = "FSLMATHS Mean did not run; file already exists for " + output_file
                    print(x)
                    doit = False
                if doit == True:
                    steptimer = time.time()
                    os.chdir(dir_in)
                    
                    x = "FSL will now try to be mean to you."
                    print(x)
                    try:
                        os.chdir(dir_in)
                        mymean = fsl.MultiImageMaths()
                        mymean.inputs.in_file = input_file
                        mymean.inputs.op_string = "-add %s -add %s -add %s -div 4"
                        mymean.inputs.operand_files = [person +'_ses-struct01_run-02_T2wflt.nii.gz', person +'_ses-struct02_run-01_T2wflt.nii.gz', person + '_ses-struct02_run-02_T2wflt.nii.gz']
                        mymean.inputs.out_file = output_file
                        mymean.run()

                        x = "MEANT2 probably created " + output_file
                        print(x)
                            
                    except Exception as e: print(e)
                        
                    steptimer = round(time.time()-steptimer,3)
                    steptimermin = round(steptimer/60,3)
                    x = "Individual step took " + str(steptimer) + " s to run."
                    print(x)
                    x = "(which is " + str(steptimermin) + " minutes)"
                    print(x)                
                        

    if k == 'linregis_meanT1T2':
        for i in participants:
            person = participant_folders[i]
            dir_in = dir_start + person + "/anat/"
            input_file = dir_in + person + "_" + flirtinputT2mean + ".nii.gz"
            output_file = dir_in + person + "_" + flirtoutputT1T2mean + ".nii.gz"
            input_reference = dir_start + person + "/anat/" + person + "_" + flirtinputT1mean + ".nii.gz"
            
            if os.path.isfile(input_file) == False:
                x = "This file doesn't exist: " + input_file
                print(x)
            else:
                doit = True
                if os.path.isfile(output_file) == True:
                    x = "FLIRT did not run; file already exists for " + output_file
                    print(x)
                    doit = False
                if doit == True:
                    steptimer = time.time()
                    os.chdir(dir_in)
                    
                    x = "FSL will now try to FLIRT with you"
                    print(x)
                    try:
                        os.chdir(dir_in)
                        myflirt = fsl.FLIRT()
                        myflirt.inputs.in_file = input_file
                        myflirt.inputs.reference = input_reference
                        myflirt.inputs.out_file = output_file
                        #ciric et al says to use 9 DOF. Though FSL default is 12...some say 6 for high quality T1s
                        myflirt.inputs.dof = 6
                        myflirt.inputs.out_matrix_file = dir_in + person + "_" + flirtoutputT1T2mean + "_mat"
                        myflirt.run()
                        
                        c3 = C3dAffineTool()
                        c3.inputs.source_file = input_file
                        c3.inputs.reference_file = input_reference
                        
                        c3.inputs.itk_transform = dir_in + person + "_" + flirtoutputT1T2mean + ".h5"
                        c3.inputs.transform_file = dir_in + person + "_" + flirtoutputT1T2mean + "_mat"
                            
                        c3.inputs.fsl2ras = True
                        c3.run()                            
      
                        x = "FLIRTT1T2MEAN probably created " + output_file
                        print(x)
                            
                    except Exception as e: print(e)
                        
                    steptimer = round(time.time()-steptimer,3)
                    steptimermin = round(steptimer/60,3)
                    x = "Individual step took " + str(steptimer) + " s to run."
                    print(x)
                    x = "(which is " + str(steptimermin) + " minutes)"
                    print(x)
                        
                        
                        
                        
                        
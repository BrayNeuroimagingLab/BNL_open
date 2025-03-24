


"""***********************"""
"""GENERAL PROGRAM OPTIONS"""
"""***********************"""
#what directory are your images saved in?
dir_start = '/Users/ivy/Desktop/Test_EEG/Test_MRI_rawfiles_BIDS/'

#what directory is your template saved in?
#template_dir = '/Users/ivy/Desktop/Graff_fMRI_stuff/xnihpd_asym_04.5-08.5_nifti/nihpd_asym_07.0-11.0_nifti/'

template_dir_c = '/Users/ivy/Desktop/Test_EEG/Test_MRI_templates/mni_icbm152_nlin_asym_09c/'
template_dir_p = '/Users/ivy/Desktop/Test_EEG/Test_MRI_templates/nihpd_asym_07.0-11.0_nifti/'


#participants and their sessions
parses = [['sub-1973003C','ses-1','ses-2','ses-3','ses-4'],
          ]




#if replacer is false, the program won't run if output image already exists
#if replacer is true, the program will write over outputs that already exist
replacer = False





"""**************************************"""
"""n4: ANTs N4BiasFieldCorrection OPTIONS"""
"""**************************************"""
n4input = "T1w"
n4output = "T1wAbfc"


"""**********************************"""
"""abe: ANTs Brain Extraction OPTIONS"""
"""**********************************"""
abeinput = "T1wAbfc"
abeoutput = "T1wAbfcBe"

#specify what you want to use as a reference for brain extraction. Presumably the NIHPD template?


abetemplate_p = template_dir_p + "mni_icbm152_t1_tal_nlin_asym_09c.nii"
abetemplatemask_p = template_dir_p + "mni_icbm152_t1_tal_nlin_asym_09c_mask.nii"


abetemplate_c = template_dir_c + 'nihpd_asym_07.0-11.0_t1w.nii'
abetemplatemask_c = template_dir_c + 'nihpd_asym_07.0-11.0_mask.nii'


"""****************************"""
"""ar: AntsRegistration OPTIONS"""
"""****************************"""
arinputmoving = "T1wAbfcBe"
aroutput = "T1wAbfcBeAr"

armatrixoutputname = "transformT1wFltmeantoMNI"
outputexists = "transformT1wFltmeantoMNIinverse.h5"

#the outputed matrix will add .h5 to the above name"
#you'll also generate the inverse matrix that has added inverse.h5 to the above name

#specify what you want to warp the input to. Presumably the NIHPD template?

arinputfixedimage_p = template_dir_p + "mni_icbm152_t1_tal_nlin_asym_09c.nii"
arinputfixedmask_p = template_dir_p + "mni_icbm152_t1_tal_nlin_asym_09c_mask.nii"

arinputfixedimage_c = template_dir_c + 'nihpd_asym_07.0-11.0_t1w.nii'
arinputfixedmask_c = template_dir_c + 'nihpd_asym_07.0-11.0_mask.nii'







"""*****************************************"""
"""ANYTHING BELOW HERE DOESN'T NEED CHANGING"""
"""**********(OR SO KIRK HOPES)*************"""
"""*****************************************"""

import nipype.interfaces.ants as ants
import os
import time


#get the current time
totaltimer = time.time()

#get a list of everything in the starting directory
participant_folders = os.listdir(dir_start)



#loop through all the participants wanted
for i in parses:
    person = i[0]
    page = person[-1]
    #loop through the image sessions, ie ses-0 and/or ses-12
    
    if page == 'C':
        abetemplatemask = abetemplatemask_c
        abetemplate = abetemplate_c
    if page == 'P':
        abetemplatemask = abetemplatemask_p
        abetemplate = abetemplate_p

    if page == 'C':
        arinputfixedmask = arinputfixedmask_c
        arinputfixedimage = arinputfixedimage_c
    if page == 'P':
        arinputfixedmask = arinputfixedmask_p
        arinputfixedimage = arinputfixedimage_p
            
            
    for j in i[1:]:
        #the directory where images are saved for that person
        dir_in = dir_start + person + "/" + j + "/anat/"
        input_file = dir_in + person + "_" + j + "_" + n4input + ".nii.gz"
        output_file = dir_in + person + "_" + j + "_" + n4output + ".nii.gz"
        #check if the input_file actually exists
        if os.path.isfile(input_file) == False:
            #if it doesn't exist, try .nii instead of .nii.gz
            input_file = dir_in + person + "_" + j + "_" + n4input + ".nii"
        #check again if the input_file exists
        if os.path.isfile(input_file) == False:
            #if it doesn't exist, put this info in the log
            x = "This file doesn't exist: " + input_file
            print(x)
        else:
            #nipype code only runs if doit is true. Various checks turn it off
            doit = True
            if replacer == False:
                #check if output_file already exists
                if os.path.isfile(output_file) == True or os.path.isfile(dir_in + outputexists):
                    x = "N4BiasFieldCorrection did not run; file already exists for " + output_file
                    print(x)
                    #prevent the preprocessing from happening if replacer==False and the output already exists
                    doit = False                    
            if doit == True:
                #determine the current time
                steptimer = time.time()

                x = "ANTs N4BiasFieldCorrection is beginning to run. You're N4 a treat!"
                print(x)
                #nipype code is put in a try statement so that if it fails the rest of the program can still run
                try:
                    #woooo nipype code
                    myabfc = ants.N4BiasFieldCorrection()
                    myabfc.inputs.input_image = input_file
                    myabfc.inputs.output_image = output_file
                    
                    myabfc.run()
                    x = "N4BiasFieldCorrection probably created " + output_file
                    print(x)    
                except:
                    x = "N4BiasFieldCorrection failed."
                    print(x)
                #determine how long the program took by subtracting the current time from the old time
                steptimer = round(time.time()-steptimer,3)
                x = "Individual step took " + str(steptimer) + " s to run."
                print(x)
                #convert time to minutes
                steptimermin = round(steptimer/60,3)
                x = "(which is " + str(steptimermin) + " minutes)"
                print(x)

          
        dir_in = dir_start + person + "/" + j + "/anat/"
        input_file = person + "_" + j + "_" + abeinput + ".nii.gz"
        output_file = person + "_" + j + "_" + abeoutput
        if os.path.isfile(dir_in + input_file) == False:
            x = "This file doesn't exist: " + input_file
            print(x)
        else:
            doit = True
            if replacer == False:
                if os.path.isfile(dir_in + output_file + ".nii.gz") == True:
                    x = "ANTs Brain Extraction did not run; file already exists for " + output_file + ".nii.gz"
                    print(x)
                    doit = False
            if doit == True:                    
                steptimer = time.time()
                os.chdir(dir_in)

                x = "ANTs BrainExtraction will now try to run. Ants have tiny, hard to extract, brains."
                print(x)
                
                x = 'Using ' + abetemplatemask
                print(x)
                
                x = 'Using ' + abetemplate
                print(x)
                try:
                    myabe = ants.BrainExtraction()
                    myabe.inputs.anatomical_image = input_file
                    myabe.inputs.brain_probability_mask = abetemplatemask
                    myabe.inputs.brain_template = abetemplate
                    myabe.inputs.out_prefix = output_file
                
                    myabe.run()
                    os.rename(output_file + 'BrainExtractionBrain.nii.gz', output_file + '.nii.gz')
                    x = "BrainExtraction probably created " + output_file + ".nii.gz"
                    print(x)
                except:
                    x = "ANTs Brain Extraction failed."
                    print(x)
                steptimer = round(time.time()-steptimer,3)
                x = "Individual step took " + str(steptimer) + " s to run."
                print(x)
                steptimermin = round(steptimer/60,3)
                x = "(which is " + str(steptimermin) + " minutes)"
                print(x)
                

        dir_in = dir_start + person + "/" + j + "/anat/"
        input_file = dir_in + person + "_" + j + "_" + arinputmoving + ".nii.gz"
        output_file = dir_in + person + "_" + j + "_" + aroutput + ".nii.gz"
        if os.path.isfile(input_file) == False:
            x = "This file doesn't exist: " + input_file
            print(x)
        else:
            doit = True
            if replacer == False:
                if os.path.isfile(output_file) == True:
                    x = "Ants Registration did not run; file already exists for " + output_file
                    print(x)
                    doit = False
            if doit == True:
                steptimer = time.time()
                os.chdir(dir_in)

                x = "ANTs Registration will now try to run. Registration? I prefer Regisphilbin."
                print(x)
                
                x = 'Using ' + arinputfixedmask
                print(x)
                
                x = 'Using ' + arinputfixedimage
                print(x)
                try:
                    myar = ants.Registration()
                    myar.inputs.fixed_image = arinputfixedimage
                    myar.inputs.fixed_image_masks = arinputfixedmask
                    myar.inputs.moving_image = input_file
                    #myar.inputs.output_warped_image = output_file
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
                except:
                    x = "ANTs Registration failed."
                    print(x)
                steptimer = round(time.time()-steptimer,3)
                steptimermin = round(steptimer/60,3)
                x = "Individual step took " + str(steptimer) + " s to run."
                print(x)
                x = "(which is " + str(steptimermin) + " minutes)"
                print(x)


                


#subtract the new current time from the old current time. Also convert to minutes. Add to log
totaltimer = round(time.time()-totaltimer,3)
totaltimermin = round(totaltimer/60,3)
totaltimerhour = round(totaltimermin/60,3)
x = "All steps took " + str(totaltimer) + " s to run."
print(x)
x = "(which is " + str(totaltimermin) + " minutes)"
print(x)
x = "(which is " + str(totaltimerhour) + " hours)"
print(x)
x = 'The end date/time is ' + time.ctime()
print(x)

os.chdir(dir_start)

  
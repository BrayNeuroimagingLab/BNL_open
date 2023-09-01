#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 12:58:28 2022

This script carries out a very convoluted set of transformations in order to fix the problem of 'inner skull outside inner skull'
Basically, it creates a whole new inner skull estimate that should be better


@author: Kirk
"""




import numpy as np
import os.path as op
import os
import subprocess

import shutil
from shutil import copyfile

import mne
from mne.surface import read_surface
from mne.bem import _ico_downsample

import nibabel as nib
import nipype.interfaces.ants as ants
import nipype.interfaces.fsl as fsl


from figureoutfailure5_functions import closest_points,adj_surface2,adj_surface_alt,new_combined_surface,new_within_surface


#replace outputs that already exist?
replacer = True




mnimask_c = '/Users/ivy/Desktop/Test_EEG/Test_MRI_templates/nihpd_asym_07.0-11.0_nifti/nihpd_asym_07.0-11.0_mask.nii'
mnimask_p = '/Users/ivy/Desktop/Test_EEG/Test_MRI_templates/nihpd_asym_07.0-11.0_nifti/nihpd_asym_07.0-11.0_mask_adultspace.nii'


subjects_dir = '/Users/ivy/Desktop/Test_EEG/Test_MRI_ARCfiles/'


subjecthere = 'all'
#subjecthere = '26C'


#when combining the brain_mask_mni and brain_mask_orig, how much to adjust at a time. This adjustment happens twice, once towards brain center, once towards other surface
inneradj = 0.125

#when expanding the combined brain mask to make the new inner skull, how much to grow. This happens twice, once towards old inner skull, once away from brain center
skulladj = 1.25

#how much to squeeze in the outer skull, happens once, away from closest skin point
outerskullsqueeze = 0.6

#how much to move inner skull when outside the outer skull. This happens twice, once towards brain center, once towards closest brain mask
inneradjfinal = 0.5


#how much to move the outer skull outward. Note that this # is different than the others. It is the fraction distance between outer skin and outer skull
#so if you use 0.5, it'll move half the distance from outer skull to outer skin
outerskullstretch = 0.25



#get a list of everything in the starting directory
folders = os.listdir(subjects_dir)
folders.sort()

if subjecthere != 'all':
    folders2 = []
    for folder in folders:
        if folder.startswith('sub') and not folder.endswith('fif'):
            if subjecthere in folder:
                folders2.append(folder)
    folders = folders2



for folder in folders:
    if folder.startswith('sub') and not folder.endswith('fif'):
              
        gogo = True
        subject = folder
        
        subject_dir = op.join(subjects_dir, subject)
        ants_dir = op.join(subject_dir, 'ANTS_fun')
        bem_dir = op.join(subject_dir, 'bem')


        if 'C' in folder:
            output_file1 = ants_dir + '/nihpd_asym_07.0-11.0_mask_warp_orig.nii.gz'
            output_file2 = ants_dir + '/nihpd_asym_07.0-11.0_mask_warp.nii.gz'  
            mnimask = mnimask_c
        elif 'P' in folder:
            output_file1 = ants_dir + '/nihpd_asym_07.0-11.0_mask_warp_adultspace_orig.nii.gz'
            output_file2 = ants_dir + '/nihpd_asym_07.0-11.0_mask_warp_adultspace.nii.gz'    
            mnimask = mnimask_p
        else:
            print("Not specified age properly")
            gogo = False


        if gogo:
            
            #structural preprocessing outputs. These must exist in the ANTs dir
            refimage = ants_dir + '/transformT1wFltmeantoMNIinverse.nii.gz'
            segwarpmatrix = ants_dir + '/transformT1wFltmeantoMNIinverse.h5'
            
            #bem outputs
            inner_skull_bem = op.join(bem_dir, 'inner_skull.surf')
            outer_skull_bem = op.join(bem_dir, 'outer_skull.surf')
            brain_bem = op.join(bem_dir, 'brain.surf')
            outer_skin_bem = op.join(bem_dir, 'outer_skin.surf')
            
            #this file must exist, created by Freesurfer
            transform_file = subject_dir + '/mri/transforms/talairach.xfm'
            
            
            #brain estimate, for viewing purposes
            brainmask_file = subject_dir + '/mri/brainmask.mgz'
            
            
            #various outputs
    
            refmasked2 = ants_dir + '/transformT1wFltmeantoMNIinverse_masked.nii.gz'
            refmaskedconvert2 = ants_dir + '/transformT1wFltmeantoMNIinverse_masked.mgz'
            
            altsubdir_parent = subject_dir + '_alt/'
            altsubdir = altsubdir_parent + 'mri/'
            
            segheadfile = altsubdir[:-4] + '/surf/lh.seghead'
            segheadcopy2 = ants_dir + '/lh.seghead_brain_mni'
            
            smoothname2 = 'transformT1wFltmeantoMNIinverse_smooth.mgz'
            refmaskedsmooth2 = ants_dir + '/' + smoothname2
            refmaskedsmooth_copy2 = altsubdir + smoothname2
            
            brain_mni_surface = op.join(ants_dir, 'brain_mni.surf')
            brain_combined_surface = op.join(ants_dir, 'brain_combined.surf')
            inner_skull_new_estimate = op.join(ants_dir, 'inner_skull_new.surf')
            outer_skull_close = op.join(ants_dir, 'outer_skull_close.surf')
            inner_skull_final = op.join(ants_dir, 'inner_skull_final.surf')
            outer_skull_stretch = op.join(ants_dir, 'outer_skull_expanded.surf')
            
            
            #copy some original files for convenience, make new dir
            innerskull_copy = op.join(ants_dir, 'inner_skull_orig.surf')
            outerskull_copy = op.join(ants_dir, 'outer_skull_orig.surf')
            brain_copy = op.join(ants_dir, 'brain_orig.surf')
            outer_skin_copy = op.join(ants_dir, 'outer_skin_orig.surf')
            
            if os.path.isfile(inner_skull_final) and replacer == False:
                    print("Output files already exist for " + subject)
                    
            elif not os.path.isfile(inner_skull_bem):
                print("Necessary files do not exist for " + subject)
                
            elif not os.path.isfile(refimage):
                print("Necessary files do not exist for " + subject)
                
            else:
                copyfile(inner_skull_bem, innerskull_copy)
                copyfile(brain_bem, brain_copy)
                copyfile(outer_skull_bem, outerskull_copy)
                copyfile(outer_skin_bem,outer_skin_copy)
                if not os.path.exists(altsubdir):
                    os.makedirs(altsubdir)  
                    
                    
                
                
                print("For " + subject + ", running ANTs transform: MNI mask to subject space")
                myaat = ants.ApplyTransforms()
                myaat.inputs.reference_image = refimage
                myaat.inputs.transforms = segwarpmatrix                            
                
                myaat.inputs.input_image = mnimask               
                myaat.inputs.output_image = output_file1
                myaat.run()
                
                

                print("For " + subject + ", turning mask (now in subj space) into binary")
                img = nib.load(output_file1)
                image_data = img.get_fdata()
                new_data = image_data.copy()
                
                shape = image_data.shape
                dim_x = shape[0]
                dim_y = shape[1]
                dim_z = shape[2]
                
                for dimi in range(dim_x):
                    for dimj in range(dim_y):
                        for dimk in range(dim_z):                              
                            if new_data[dimi][dimj][dimk] > 0.75:
                                new_data[dimi][dimj][dimk] = 1
                            else:
                                new_data[dimi][dimj][dimk] = 0
                
                regressor_img = nib.Nifti1Image(new_data, img.affine, img.header, img.extra, img.file_map, img.get_data_dtype() )
                nib.save(regressor_img,output_file2)
                
                
                print("For " + subject + ", running FSL math - making sure it's a binary, removing any potential rounding errors")
                
                mybin = fsl.UnaryMaths()
                mybin.inputs.in_file = output_file2
                mybin.inputs.out_file = output_file2
                mybin.inputs.operation = 'bin'
                mybin.run()
                
                
                print("For " + subject + ", running FSL math - creating masked version of MNI brain in subj space")
                
                matharg = "-mul " + output_file2
                mymath = fsl.ImageMaths()
                mymath.inputs.in_file = refimage
                mymath.inputs.out_file = refmasked2
                mymath.inputs.args = matharg
                mymath.run()
                
                
                print("For " + subject + ", you created " + refmasked2)
                print("")
                
                
                
                c7 = 'mri_convert ' + refmasked2 + ' ' + refmaskedconvert2 + ' --conform'
                c8 = 'mri_add_xform_to_header -c ' + transform_file + ' ' + refmaskedconvert2 + ' ' + refmaskedconvert2
                
                
                c7 = c7.split(' ')
                c8 = c8.split(' ')
                
                
                subprocess.run(c7)
                subprocess.run(c8)
                
                
                #smooth the brain
                print("For " + subject + ", smoothing the masked MNI brain")
                
                c9 = 'mri_convert --fwhm 4 ' + refmaskedconvert2 + ' ' + refmaskedsmooth2
                
                c9 = c9.split(' ')
                subprocess.run(c9)
                
                
                #copying file to temporary folder, so make_scalp_surfaces can create a bunch of outputs that we can just discard later easily
                copyfile(refmaskedsmooth2, refmaskedsmooth_copy2)
                
                print("For " + subject + ", making surface for masked MNI brain")
                mne.bem.make_scalp_surfaces(subject=subject+'_alt',subjects_dir=subjects_dir,mri=smoothname2,no_decimate=True,overwrite=True)
                
                print("For " + subject + ", decimating surface and saving it")
                seghead = read_surface(segheadfile, return_dict=True)[-1]
                
                
                  
                
                try:
                    seghead_shrunk = mne.decimate_surface(seghead['rr'],seghead['tris'],20480,method='sphere')
                                    
                except:
                    print("")
                    print("Seghead shrunk failed, trying backup")
                    seghead_shrunk = mne.decimate_surface(seghead['rr'],seghead['tris'],20480)
                    print("")
                    
                if len(seghead_shrunk[1]) != 20480:
     
                    print("")
                    print("Seghead shrunk failed, trying backup backup")
                    print("")
                    seghead_shrunk = mne.decimate_surface(seghead['rr'],seghead['tris'],20480*3)
                    seghead_shrunk = mne.decimate_surface(seghead_shrunk[0],seghead_shrunk[1],20481)
                    
                    
                if len(seghead_shrunk[1]) == 20480:
                    print("Seghead shrunk has right number of triangles")
                    
                    mne.write_surface(brain_mni_surface, seghead_shrunk[0], seghead_shrunk[1], overwrite=True)
                    
                    
                    #saving original segheadfile, seems useful to keep. Deleting the temporary folder
                    copyfile(segheadfile, segheadcopy2)
                    shutil.rmtree(altsubdir_parent)
                    
                    
                    print("For " + subject + ", creating combined brain surface, based on the original brain surface and the MNI brain surface")
                    #the final MNI brain surface is mostly internal to the original brain surface, so we will designate them as such
                    innersurf = read_surface(brain_mni_surface, return_dict=True)[-1]
                    outersurf = read_surface(brain_copy, return_dict=True)[-1]
                    
                    
        
                    #we will use the MNI brain's to generate brain midpoint values
                    brainpoints = innersurf['rr']
                    brainpointst = brainpoints.T
                    midx = np.mean(brainpointst[0])
                    midy = np.mean(brainpointst[1])
                    midz = np.mean(brainpointst[2])
                    
                    #create combined brain mask
                    
                    new_combined_surface(brain_combined_surface,innersurf,outersurf,inneradj,midx,midy,midz)
                    #new_combined_surface(brain_combined_surface,outersurf,innersurf,inneradj,midx,midy,midz)
                    
                    
                    print("For " + subject + ", creating new inner skull estimate based on the combined brain surface")
                    #the combined brain is (or should be) internal to the original inner skull layer
                    innersurf = read_surface(brain_combined_surface, return_dict=True)[-1]
                    outersurf = read_surface(innerskull_copy, return_dict=True)[-1]
                    
                    fros = innersurf['rr'].copy()
                    adjfros = innersurf['rr'].copy()
                    
                    #for each point on the combined brain, get the closest inner skull point
                    closestpoints = closest_points(fros,outersurf['rr'])
                     
                    #for each point on the combined brain, move slightly away from mid brain and slightly towards closest inner skull point
                    #we're doing both in case on the other estimate is weird. This will be our new inner skull estimate, which should be slightly closer to the brain
                    for bn in range(len(fros)):
                        badpoint = fros[bn]
                        closestpoint = closestpoints[bn]
                        badpoint2 = adj_surface2(badpoint,skulladj,closestpoint[0],closestpoint[1],closestpoint[2])
                        badpoint3 = adj_surface_alt(badpoint2,skulladj,midx,midy,midz)
                        adjfros[bn] = badpoint3
                        
                    #save our new inner skull estimate
                    mne.write_surface(inner_skull_new_estimate, adjfros, innersurf['tris'], overwrite=True)
                    
                    
                    
                    print("For " + subject + ", stretching out the outer skull")
                    #the outer skull is (or should be) internal to the outer skin
                    innersurf = read_surface(outerskull_copy, return_dict=True)[-1]
                    outersurf = read_surface(outer_skin_copy, return_dict=True)[-1]
                    
                    fros = innersurf['rr'].copy()
                    adjfros = innersurf['rr'].copy()
                    
                    #for each point on the outer skull, get the closest point on the outer skin
                    closestpoints = closest_points(fros,outersurf['rr'])
                    
                    #for each point on the outer skull, move towards outer skin
                    for bn in range(len(fros)):
                        badpoint = fros[bn]
                        closestpoint = closestpoints[bn]
                        diff = badpoint-closestpoint
                        dist = (sum(diff**2))**0.5
                        badpoint2 = adj_surface2(badpoint,dist*outerskullstretch,closestpoint[0],closestpoint[1],closestpoint[2])
                        adjfros[bn] = badpoint2
                        
                    #save our new outer skull estimate
                    mne.write_surface(outer_skull_stretch, adjfros, innersurf['tris'], overwrite=True)
                    
                    
                    print("For " + subject + ", downsampling outer skull and moving it towards brain, in order to better estimate the inner skull")
                    #take the outer skull, downsample it, and move it slightly closer to the brain. This will ensure the final estimate of the inner skull is definitely
                    #inside the outer skull, and is not super close to the outer skull. This new outer skull exists only for adjusting the inner skull
                    surf_shrunk = _ico_downsample(innersurf , dest_grade=4)
                    fros = surf_shrunk['rr'].copy()
                    
                    #refind the closest points, now that we downsampled
                    closestpoints = closest_points(fros,outersurf['rr'])
                    
                    for bn in range(len(fros)):
                        badpoint = fros[bn]
                        closestpoint = closestpoints[bn]
                        #move away from the skin
                        badpoint2 = adj_surface2(badpoint,-1*outerskullsqueeze,closestpoint[0],closestpoint[1],closestpoint[2])
                        fros[bn] = badpoint2
                        
                    #save the outer skull downsampled
                    mne.write_surface(outer_skull_close, fros, surf_shrunk['tris'], overwrite=True)
                    
                    
                    print("For " + subject + ", creating final inner skull estimate")
                    innersurf = read_surface(inner_skull_new_estimate, return_dict=True)[-1]
                    outersurf = read_surface(outer_skull_close, return_dict=True)[-1]
                    closersurf = read_surface(brain_combined_surface, return_dict=True)[-1]
                    
                    new_within_surface(inner_skull_final,outersurf,innersurf,closersurf,inneradjfinal,midx,midy,midz)
                    
                    print("")
                    print("")
                    print("Successfully created final surface for " + subject)
                    print("")
                    print("")
                    
                    
                
                else:
                    
                    print("")
                    print("")
                    print("Oh no!!!!!!!")       
                    print("")
                    print("")
                    print("Oh no!!!!!!!")       
                    print("Oh no!!!!!!!")      
                    print("Oh no!!!!!!!")      
                    print("")
                    print("")
                    print("Oh no!!!!!!!")       
                    print("")
                    print("")    
        
    
    
    
    
    

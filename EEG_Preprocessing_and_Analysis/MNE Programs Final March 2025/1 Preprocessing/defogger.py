#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This removes fog
"""


import nibabel as nib

import nipype.interfaces.fsl as fsl
import pandas as pd
import math
import os
import subprocess



subjects_dir = '/Users/ivy/Desktop/Test_EEG/Test_MRI_beadless_BIDS/'

subjecthere = '03C'

#replace output files that already exist?
replacer = False

#what to remove with the sweep from each direction
lowthres = 300


#input specific coordinates for bad voxels. This program will remove these voxels and try to remove neighboring ones
badvoxels = []

#example of what bad voxels should look like
#badvoxels = [[204,68,81],[188,58,81],[188,57,86],[201,65,89]]


#what to remove with the looking for ghosts and stuff
#definitely remove
defthres = 474
#possibly remove
thres = 350
#must have a neighbor this high to be important
neighborthres = 500
#definitely keep
defkeep = 475




#get a list of everything in the starting directory
folders = os.listdir(subjects_dir)

folders2 = []
for folder in folders:
    if folder.startswith('sub') and not folder.endswith('fif'):
        if subjecthere in folder:
            folders2.append(folder)
folders = folders2


for folder in folders:
    if folder.startswith('sub') and not folder.endswith('fif'):
        subject = folder
        
        input_file = subjects_dir + subject + '/' + subject + '_T1w.nii.gz'
        output_file = subjects_dir + subject + '/' + subject + '_T1w_defog.nii.gz'

        if not (replacer == False and os.path.isfile(output_file)):
            
            if os.path.isfile(input_file):

                print("loading data for " + subject)
                img = nib.load(input_file)
                image_data = img.get_fdata()
                new_data = image_data.copy()

            
                shape = image_data.shape
                dim_x = shape[0]
                dim_y = shape[1]
                dim_z = shape[2]
                

                      
                print("Now checking bad voxels")    
                for abadvoxel in badvoxels:
                    
                    danger = False
                    
                    print("Checking bad voxel " + str(abadvoxel))
            
                    voxelstocheck = [abadvoxel]
                    
                    voxelsalreadychecked = []
                    thresofthose = []
                    voxelschanged = 0
                    voxelsunchanged = 0
                    
                    voxelstozero = []
                    
         
                    
                    #check voxel
                    
                    print("checking voxels")
                    while len(voxelstocheck) > 0:
                        voxelc = voxelstocheck[0]
                        
                        if voxelc in voxelsalreadychecked:
                            voxelstocheck.remove(voxelc)
                        
                        else:
                            if len(voxelsalreadychecked) > 0 and len(voxelsalreadychecked) % 250 == 0:
                                print('Checked 250 voxels. If this gets over 2000 or so, bad things have happened')
                            if len(voxelsalreadychecked) > 0 and len(voxelsalreadychecked) % 10000 == 0:
                                print('Checked 5000 voxels. UH OH')
                                danger = True     
                                voxelstocheck = []
                            
                            voxelval = new_data[voxelc[0]][voxelc[1]][voxelc[2]]
                            
                            thresofthose.append(voxelval)
                            voxelsalreadychecked.append(voxelc)
                            if not danger:
                                voxelstocheck.remove(voxelc)
                            
                            removed = False
                            
                            if voxelval > defthres and voxelval < defkeep:
                                removed = True
                                
                            elif voxelval > thres:
                                removed = True
                                xabove1 = new_data[voxelc[0]+1][voxelc[1]][voxelc[2]]
                                xbelow1 = new_data[voxelc[0]-1][voxelc[1]][voxelc[2]]                      
                                
                                if voxelval < xabove1 and voxelval < xbelow1:
                                    removed = False                       
    
                                yabove1 = new_data[voxelc[0]][voxelc[1]+1][voxelc[2]]
                                ybelow1 = new_data[voxelc[0]][voxelc[1]-1][voxelc[2]]
                 
                                if voxelval < yabove1 and voxelval < ybelow1:
                                    removed = False     
                                           
                                zabove1 = new_data[voxelc[0]][voxelc[1]][voxelc[2]+1]
                                zbelow1 = new_data[voxelc[0]][voxelc[1]][voxelc[2]-1]

                                if voxelval < zabove1 and voxelval < zbelow1:
                                    removed = False     
        
                    
                            else:
                                voxelsunchanged = voxelsunchanged + 1
        
        
                            if removed:    
                                voxelstozero.append(voxelc)
                            
                                
                                #new_data[voxelc[0]][voxelc[1]][voxelc[2]] = 0
                                voxelschanged = voxelschanged + 1
                                
                                newvoxelc = voxelc.copy()
                                newvoxelc[0] = newvoxelc[0]+1
                                voxelstocheck.append(newvoxelc)
                                
                                newvoxelc = voxelc.copy()
                                newvoxelc[0] = newvoxelc[0]-1
                                voxelstocheck.append(newvoxelc)            
                                
                    
                                newvoxelc = voxelc.copy()
                                newvoxelc[1] = newvoxelc[1]+1
                                voxelstocheck.append(newvoxelc)
                                
                                newvoxelc = voxelc.copy()
                                newvoxelc[1] = newvoxelc[1]-1
                                voxelstocheck.append(newvoxelc)     
                                
                                
                                
                                newvoxelc = voxelc.copy()
                                newvoxelc[2] = newvoxelc[2]+1
                                voxelstocheck.append(newvoxelc)
                                
                                newvoxelc = voxelc.copy()
                                newvoxelc[2] = newvoxelc[2]-1
                                voxelstocheck.append(newvoxelc)  
                                
                                if danger:
                                    voxelstocheck = []
                                
                                
        
        
                    
                    if danger:
                        print("Did not create output. You ran into danger")
                        print('')
                        
                    else:    
                        for voxelc in voxelstozero:
                            new_data[voxelc[0]][voxelc[1]][voxelc[2]] = 0
                    
                    
                        print("You checked " + str(len(voxelsalreadychecked)) + ' voxels')
                        
                        
                        
                        print("cleaning up")
                        for voxelc in voxelsalreadychecked:
                            
                            voxelval = new_data[voxelc[0]][voxelc[1]][voxelc[2]]
                            if voxelval > 0.1:
                            
                                meaningfulneighbors = 0
                                
                                newvoxelc = voxelc.copy()
                                newvoxelc[0] = newvoxelc[0]+1
                                neighborval = new_data[newvoxelc[0]][newvoxelc[1]][newvoxelc[2]]
                                if neighborval > neighborthres:
                                    meaningfulneighbors = meaningfulneighbors + 1
                                
                                newvoxelc = voxelc.copy()
                                newvoxelc[0] = newvoxelc[0]-1
                                neighborval = new_data[newvoxelc[0]][newvoxelc[1]][newvoxelc[2]]
                                if neighborval > neighborthres:
                                    meaningfulneighbors = meaningfulneighbors + 1    
                            
                                newvoxelc = voxelc.copy()
                                newvoxelc[1] = newvoxelc[1]+1
                                neighborval = new_data[newvoxelc[0]][newvoxelc[1]][newvoxelc[2]]
                                if neighborval > neighborthres:
                                    meaningfulneighbors = meaningfulneighbors + 1
                                
                                newvoxelc = voxelc.copy()
                                newvoxelc[1] = newvoxelc[1]-1
                                neighborval = new_data[newvoxelc[0]][newvoxelc[1]][newvoxelc[2]]
                                if neighborval > neighborthres:
                                    meaningfulneighbors = meaningfulneighbors + 1   
                            
                                newvoxelc = voxelc.copy()
                                newvoxelc[2] = newvoxelc[2]+1
                                neighborval = new_data[newvoxelc[0]][newvoxelc[1]][newvoxelc[2]]
                                if neighborval > neighborthres:
                                    meaningfulneighbors = meaningfulneighbors + 1
                                
                                newvoxelc = voxelc.copy()
                                newvoxelc[2] = newvoxelc[2]-1
                                neighborval = new_data[newvoxelc[0]][newvoxelc[1]][newvoxelc[2]]
                                if neighborval > neighborthres:
                                    meaningfulneighbors = meaningfulneighbors + 1   
                            
                            
                                if meaningfulneighbors == 0:
                                    new_data[voxelc[0]][voxelc[1]][voxelc[2]] = 0
                                    voxelschanged = voxelschanged + 1
                                    voxelsunchanged = voxelsunchanged - 1
                            

 
                for dimi in range(dim_x):

                    if (dimi+1) % 10 == 0:
                        print("For " + subject + ", making adjustments for slice " + str(dimi+1) + " of " + str(dim_x))                    

                    #from top, straight down
                    for dimk in range(dim_z):
                        keepchecking = True
                        for dimj in range(dim_y):
                            value = new_data[dimi][dimj][dimk]
                            if keepchecking:
                                if value < lowthres:
                                    new_data[dimi][dimj][dimk] = 0
                                else:
                                    keepchecking = False

                    
                    #from bottom, straight up
                    for dimk in range(dim_z):
                        keepchecking = True
                        for dimj in reversed(range(dim_y)):
                            value = new_data[dimi][dimj][dimk]
                            if keepchecking:
                                if value < lowthres:
                                    new_data[dimi][dimj][dimk] = 0
                                else:
                                    keepchecking = False
                
                   
                    #from left, straight right
                    for dimj in range(dim_y):
                        keepchecking = True
                        for dimk in range(dim_z):
                            value = new_data[dimi][dimj][dimk]
                            if keepchecking:
                                if value < lowthres:
                                    new_data[dimi][dimj][dimk] = 0
                                else:
                                    keepchecking = False
                    
                    
                    #from right, straight left
                    for dimj in range(dim_y):
                        keepchecking = True
                        for dimk in reversed(range(dim_z)):
                            value = new_data[dimi][dimj][dimk]
                            if keepchecking:
                                if value < lowthres:
                                    new_data[dimi][dimj][dimk] = 0
                                else:
                                    keepchecking = False          
                                                     
                             
                    #from top, down right
                    for dimk in range(dim_z):
                        keepchecking = True
                        for dimj in range(dim_y):
                            if dimk+dimj < dim_z:
                                value = new_data[dimi][dimj][dimk+dimj]
                                if keepchecking:
                                    if value < lowthres:
                                        new_data[dimi][dimj][dimk+dimj] = 0
                                    else:
                                        keepchecking = False
                    
                    #from top, down left
                    for dimk in range(dim_z):
                        keepchecking = True
                        for dimj in range(dim_y):
                            if dimk-dimj >= 0:
                                value = new_data[dimi][dimj][dimk-dimj]
                                if keepchecking:
                                    if value < lowthres:
                                        new_data[dimi][dimj][dimk-dimj] = 0
                                    else:
                                        keepchecking = False
                    
                    #from bottom, diagonal right
                    for dimk in range(dim_z):
                        keepchecking = True
                        for dimj in reversed(range(dim_y)):
                            if dimk + (dim_y-dimj-1) < dim_z:
                                value = new_data[dimi][dimj][dimk+(dim_y-dimj-1)]
                                if keepchecking:
                                    if value < lowthres:
                                        new_data[dimi][dimj][dimk+(dim_y-dimj-1)] = 0
                                    else:
                                        keepchecking = False
                    
                    #from bottom, diagonal left
                    for dimk in range(dim_z):
                        keepchecking = True
                        for dimj in reversed(range(dim_y)):
                            if dimk - (dim_y-dimj-1) >= 0:
                                value = new_data[dimi][dimj][dimk-(dim_y-dimj-1)]
                                if keepchecking:
                                    if value < lowthres:
                                        new_data[dimi][dimj][dimk-(dim_y-dimj-1)] = 0
                                    else:
                                        keepchecking = False
                        
                        
                    #from left, diagonal down
                    for dimj in range(dim_y):
                        keepchecking = True
                        for dimk in range(dim_z):
                            if dimj + dimk < dim_y:
                                value = new_data[dimi][dimj+dimk][dimk]
                                if keepchecking:
                                    if value < lowthres:
                                        new_data[dimi][dimj+dimk][dimk] = 0
                                    else:
                                        keepchecking = False
                    
                    #from left, diagonal up
                    for dimj in range(dim_y):
                        keepchecking = True
                        for dimk in range(dim_z):
                            if dimj - dimk >= 0:
                                value = new_data[dimi][dimj-dimk][dimk]
                                if keepchecking:
                                    if value < lowthres:
                                        new_data[dimi][dimj-dimk][dimk] = 0
                                    else:
                                        keepchecking = False
                    
                    #from right, diagonal down
                    for dimj in range(dim_y):
                        keepchecking = True
                        for dimk in reversed(range(dim_z)):
                            if dimj+(dim_z-dimk-1) < dim_y:
                                value = new_data[dimi][dimj+(dim_z-dimk-1)][dimk]
                                if keepchecking:
                                    if value < lowthres:
                                        new_data[dimi][dimj+(dim_z-dimk-1)][dimk] = 0
                                    else:
                                        keepchecking = False
                        
                    #from right, diagonal up
                    for dimj in range(dim_y):
                        keepchecking = True
                        for dimk in reversed(range(dim_z)):
                            if dimj-(dim_z-dimk-1) >= 0:
                                value = new_data[dimi][dimj-(dim_z-dimk-1)][dimk]
                                if keepchecking:
                                    if value < lowthres:
                                        new_data[dimi][dimj-(dim_z-dimk-1)][dimk] = 0
                                    else:
                                        keepchecking = False                        

 
                print("Turning into binary")                        
                for dimi in range(dim_x):
                    for dimj in range(dim_y):
                        for dimk in range(dim_z):                              
                            if new_data[dimi][dimj][dimk] != 0:
                                new_data[dimi][dimj][dimk] = 1
                
                
                print("saving outputs")
                regressor_img = nib.Nifti1Image(new_data, img.affine, img.header, img.extra, img.file_map, img.get_data_dtype() )
                nib.save(regressor_img,output_file)
                

                print("Running FSL math")
                
                mybin = fsl.UnaryMaths()
                mybin.inputs.in_file = output_file
                mybin.inputs.out_file = output_file
                mybin.inputs.operation = 'bin'
                mybin.run()
                
                
                matharg = "-mul " + output_file
                mymath = fsl.ImageMaths()
                mymath.inputs.in_file = input_file
                mymath.inputs.out_file = output_file
                mymath.inputs.args = matharg
                mymath.run()
                
                print("You created " + output_file)
                print("")
                
                






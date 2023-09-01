#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nibabel as nib

import nipype.interfaces.fsl as fsl
import math
import os



input_base = '/Users/ivy/Desktop/Test_EEG/Test_MRI_rawfiles_BIDS/'
output_base = '/Users/ivy/Desktop/Test_EEG/Test_MRI_beadless_BIDS/'

subjecthere = 'sub-1973003C_ses-3'


#change this number if you run into trouble
thres = 200

beadlocation = [156,213,136]



defthres = 900
neighborthres = 500

#replace output files that already exist?
replacer = False



subj = subjecthere
subjsplit = subj.split('_')
participant = subjsplit[0]
ses = subjsplit[1]

input_file = input_base + participant + '/' + ses + '/anat/' + participant + '_' + ses + '_T1w.nii.gz'
output_dir = output_base + participant + '/' + ses + '/anat/'
output_file = output_dir + participant + '_' + ses + '_T1w.nii.gz'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

go = True
if not os.path.isfile(input_file):
    print('Does not exist: ' + input_file)
    go = False
if os.path.isfile(output_file):
    if replacer == False:
        print('Output file already exists, not overwriting for: ' + output_file)
        go = False
    else:
        print('Output file already exists. Overwriting')
    
    
    
if go:

    danger = False
    print("Now creating " + output_file)

    
    abadvoxel = beadlocation

  
    
    voxelstocheck = [abadvoxel]
    
    voxelsalreadychecked = []
    thresofthose = []
    voxelschanged = 0
    voxelsunchanged = 0
    
    voxelstozero = []
    
    
    print("loading data")
    img = nib.load(input_file)
    image_data = img.get_fdata()
    
    new_data = image_data.copy()
    
    
    #check voxel
    
    print("checking voxels")
    while len(voxelstocheck) > 0:
        voxelc = voxelstocheck[0]
        
        if voxelc in voxelsalreadychecked:
            voxelstocheck.remove(voxelc)
        
        else:
            if len(voxelsalreadychecked) > 0 and len(voxelsalreadychecked) % 250 == 0:
                print('Checked 250 voxels. If this gets over 1500 or so, bad things have happened')
            if len(voxelsalreadychecked) > 0 and len(voxelsalreadychecked) % 2000 == 0:
                print('Checked 2000 voxels. UH OH')
                danger = True     
                voxelstocheck = []
            
            voxelval = new_data[voxelc[0]][voxelc[1]][voxelc[2]]
            
            thresofthose.append(voxelval)
            voxelsalreadychecked.append(voxelc)
            if not danger:
                voxelstocheck.remove(voxelc)
            
            removed = False
            
            if voxelval > defthres:
                removed = True
                
            elif voxelval > thres:
                removed = True
                xabove1 = new_data[voxelc[0]+1][voxelc[1]][voxelc[2]]
                xabove2 = new_data[voxelc[0]+2][voxelc[1]][voxelc[2]]
                
                xbelow1 = new_data[voxelc[0]-1][voxelc[1]][voxelc[2]]
                xbelow2 = new_data[voxelc[0]-2][voxelc[1]][voxelc[2]]                        
                
                #if (voxelval < xabove1 or voxelval < xabove2) and (voxelval < xbelow1 or voxelval < xbelow2):
                #    removed = False
                    
                if voxelval < xabove1 and voxelval < xbelow1:
                    removed = False                       


                yabove1 = new_data[voxelc[0]][voxelc[1]+1][voxelc[2]]
                yabove2 = new_data[voxelc[0]][voxelc[1]+2][voxelc[2]]
                
                ybelow1 = new_data[voxelc[0]][voxelc[1]-1][voxelc[2]]
                ybelow2 = new_data[voxelc[0]][voxelc[1]-2][voxelc[2]]                        
                
                #if (voxelval < yabove1 or voxelval < yabove2) and (voxelval < ybelow1 or voxelval < ybelow2):
                #    removed = False

                if voxelval < yabove1 and voxelval < ybelow1:
                    removed = False     
                    
                    
                zabove1 = new_data[voxelc[0]][voxelc[1]][voxelc[2]+1]
                zabove2 = new_data[voxelc[0]][voxelc[1]][voxelc[2]+2]
                
                zbelow1 = new_data[voxelc[0]][voxelc[1]][voxelc[2]-1]
                zbelow2 = new_data[voxelc[0]][voxelc[1]][voxelc[2]-2]                        
                
                #if (voxelval < zabove1 or voxelval < zabove2) and (voxelval < zbelow1 or voxelval < zbelow2):
                #    removed = False

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
            
            
        print("Turning into binary")
        shape = image_data.shape
        dim_x = shape[0]
        dim_y = shape[1]
        dim_z = shape[2]
        
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
        
        






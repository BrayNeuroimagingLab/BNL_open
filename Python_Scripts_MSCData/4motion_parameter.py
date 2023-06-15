#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 10:47:42 2019

@author: Kirk
"""

"""
Looks at Motion Parameters





"""

"""***********************"""
"""GENERAL PROGRAM OPTIONS"""
"""***********************"""
#what directory are your images saved in?
dir_start = "/Volumes/LaCie/msc_motor1/"


#what participants do you want this to run on? e.g. [1,2,3] or list(range(1,4))
#this is based on the files in the directory. 0 = first file in directory
#participants = list(range(1,55))
participants = [1]


#do you want to run on ses-0, ses-12, or both? If both, type ["ses-0","ses-12"]
imagesession = ["ses-func01", "ses-func02", "ses-func03","ses-func04","ses-func05","ses-func06","ses-func07","ses-func08","ses-func09","ses-func10"]
#text file with 6 head alignment estimates
filterhmpinput = 'task-Dora5_boldMcf.nii.gz.par'

#mcflirt FD values. For comparison
fdfileinput = 'task-Dora5_boldMcf.nii.gz_rel.rms'

#Power FD output with filtering
fdfileoutput = 'PowerFD.csv'

fs = 0.4

#filtering threshold. Anything within this range is what you want to keep
# highcut = 0.08
highcut = 0.1
lowcut = 0

#threshold for fdmcflirt. 0.2 or 0.25 are good choices
fd1thres = 0.2
#threshold for fdpower. double fdmcflirt is good
fd2thres = 0.2




"""*****************************************"""
"""ANYTHING BELOW HERE DOESN'T NEED CHANGING"""
"""**********(OR SO KIRK HOPES)*************"""
"""*****************************************"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from scipy.stats import linregress
from scipy.fftpack import fft, ifft

os.chdir(dir_start)


#get a list of everything in the starting directory
participant_folders = sorted(os.listdir(dir_start))


badvolsFD_flirt = []
badvolsFD_power = []
badvolsFD_poweryflt = []
subj = []
seslist = []




for i in participants:
    person = participant_folders[i]
    for j in imagesession:
        subj.append(person)
        seslist.append(j)
        #define file names for this specific kid
        dir_in = dir_start + person + "/" + j + "/func/"
        headmotionfile = dir_in + person + "_" + j + "_" + filterhmpinput            
        fdfile = dir_in + person + "_" + j + "_" + fdfileinput 
        fdsavefile = dir_in + person + "_" + j + "_" + fdfileoutput 

        rawmotion = ['rot_x','rot_y','rot_z','trans_x','trans_y','trans_z']
                
        md = {
                'rot_x' : [],
                'rot_y' : [],
                'rot_z' : [],
                'trans_x' : [],
                'trans_y' : [],
                'trans_z' : []   
        }

        mdc =  {
                'rot_x' : [],
                'rot_y' : [],
                'rot_z' : [],
                'trans_x' : [],
                'trans_y' : [],
                'trans_z' : [],
                'trans_yflt' : []
        }
        
        currentline = 0
        with open(headmotionfile) as file:
            for line in file:
                #if currentline < 434:
                splitted = line.split()
                #create head motion parameters
                md['rot_x'].append(float(splitted[0]))
                md['rot_y'].append(float(splitted[1]))
                md['rot_z'].append(float(splitted[2]))
                md['trans_x'].append(float(splitted[3]))
                md['trans_y'].append(float(splitted[4]))
                md['trans_z'].append(float(splitted[5]))
                currentline = currentline + 1
                    
        N = len(md['rot_x'])
        
        tf = np.linspace(0.0,fs/2,int(N/2))
        alltime = list(range(0,N))        
   
       


        os.chdir(dir_in)



        
                                                                                    
        ###filter the data###
           
        #define the lowpass and highpass                                                                   
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
        
        for rr in rawmotion:
            testseries = md[rr]                                                 
            #this creates amplitude vs time data after a FFT filter. So FFT then an inverse FFT
            repaireddata = np.real(ifft(fft(testseries)*F))
            
            #add the repaired data to the motion dictionary
            md[rr+'flt'] = repaireddata          
           
        
        timelist = list(range(0,N))
        timelist2 = list(range(0,N))
        alltime = list(range(0,N))
        
        #calculate change in HMP from timepoint to timepoint. Convert angles (in radians) to mm by assuming 50 mm head radius
        for i in timelist:
            mdc['rot_x'].append(abs((md['rot_x'][i]-md['rot_x'][i-1])*50))
            mdc['rot_y'].append(abs((md['rot_y'][i]-md['rot_y'][i-1])*50))
            mdc['rot_z'].append(abs((md['rot_z'][i]-md['rot_z'][i-1])*50))
            mdc['trans_x'].append(abs(md['trans_x'][i]-md['trans_x'][i-1]))
            mdc['trans_y'].append(abs(md['trans_y'][i]-md['trans_y'][i-1]))
            mdc['trans_z'].append(abs(md['trans_z'][i]-md['trans_z'][i-1]))
            mdc['trans_yflt'].append(abs(md['trans_yflt'][i]-md['trans_yflt'][i-1]))            
        
        
        
        #calculate FD both with and without filtered y
        FD = []
        FD2 = []       
        for i in timelist2:
            FD.append(mdc['rot_x'][i]+mdc['rot_y'][i]+mdc['rot_z'][i]+mdc['trans_x'][i]+mdc['trans_y'][i]+mdc['trans_z'][i])
            FD2.append(mdc['rot_x'][i]+mdc['rot_y'][i]+mdc['rot_z'][i]+mdc['trans_x'][i]+mdc['trans_yflt'][i]+mdc['trans_z'][i])
        
        FDnewdf = pd.DataFrame({'FD':FD2})
        FDnewdf.to_csv(fdsavefile)
        

        #import FLIRT FD calculation
        fdflirt = []
        with open(fdfile) as file:
            for line in file:
                fdflirt.append(float(line))
        
        #count the number of bad volumes for each way of calculating FD
        badvolsFD = 0
        badvolsFD2 = 0
        #badvolsFD3 = 0
        badvolsFDflirt = 0
        for i in range(len(FD)):
            if FD[i] > fd2thres:
                badvolsFD = badvolsFD + 1
        for i in range(len(FD2)):
            if FD2[i] > fd2thres:
                badvolsFD2 = badvolsFD2 + 1                
        for i in range(len(fdflirt)):
            if fdflirt[i] > fd1thres:
                badvolsFDflirt = badvolsFDflirt + 1
                
        badvolsFD_flirt.append(badvolsFDflirt)
        badvolsFD_power.append(badvolsFD)
        badvolsFD_poweryflt.append(badvolsFD2)
   
    
badvoldf = pd.DataFrame({'person':subj,'ses':seslist,'BadvolMCFLIRT':badvolsFD_flirt,'BadvolPower':badvolsFD_power,'BadvolPowerFltY':badvolsFD_poweryflt})    

badvoldf['diff'] = badvoldf['BadvolPower']-badvoldf['BadvolPowerFltY']


print(badvoldf.to_string())
    
    
    

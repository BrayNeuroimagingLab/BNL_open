#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 14:27:58 2023

@author: Kirk
"""

import os
import pandas as pd
import numpy as np
from scipy.stats.stats import pearsonr  
import matplotlib.pyplot as plt


#where are your connectomes saved
connectomefolder = '/Users/path/to/connectomes/'

#average motion for each connectome
motiondf = '/Users/path/to/avgmotiondf.csv'

#do you wish to carry out a Fisher z transform on your connectome to better approximate a normal distribution?
#(select False if this was already carried out previously)
fisherz = True






participant_files = os.listdir(connectomefolder)
subfiles = [file for file in participant_files if file.endswith('csv')]

motiondf = pd.read_csv(motiondf)


FCallvec = []
avgmotlist = []
veclen = []

for file in subfiles:

    print("Loading " + file)
    rawdata = pd.read_csv(connectomefolder + file, index_col=0)

    if not list(rawdata.columns) == list(rawdata.index):
        print("Connectome index does not match columns")
    else:
        
        #check if motion info is available
        avgmot = motiondf.loc[motiondf['filename'] == file]['avgmotion']
        
        if not len(avgmot) == 1:
            print("Motion data not available for connectome")
        else:
        
            #vectorize the connectome
            FCm = np.squeeze(np.asarray(rawdata))
        
            vec = []
            for ii in range(1, FCm.shape[0]):
                for jj in range(ii):
                    vec.append(FCm[ii, jj])
                    
            if fisherz:
                vec = np.arctanh(vec)
                    
            FCallvec.append(np.asarray(vec))
            avgmotlist.append(float(avgmot))
            veclen.append(len(vec))


if not len(set(veclen)) == 1:
    print("Your connectomes are not all the same size")
else:

    print("Calculating QC-FC")
    transposedcorrelations = list(map(list, zip(*FCallvec)))
    
    numedges = len(transposedcorrelations)
    numedges10 = int(len(transposedcorrelations)/10)
    
    edgemotcorr = []
    pvalist = []
    for conn in range(len(transposedcorrelations)):
        #I get unhappy if I don't know how close my program is to being done, so this tells you that
        if conn % numedges10 == 0:
            print('Edge',conn,'of',numedges)
        
        #is edge correlated with motion?
        somecorrelation = transposedcorrelations[conn]                
        pc = pearsonr(somecorrelation,avgmotlist)
        edgemotcorr.append(pc[0])
        pvalist.append(pc[1])
    
    sigedges = sum(i < 0.05 for i in pvalist)
    sigedgepercent = sigedges/len(pvalist)*100
    strsigedgepercent = str(round(sigedgepercent,2))
    
    print(strsigedgepercent + '% of your edges are significantly (p < 0.05) correlated with average head motion')
    print("The histogram shows the correlation (between edge strength and motion) for all edges")
    
    plt.hist(edgemotcorr)
    plt.show()
    









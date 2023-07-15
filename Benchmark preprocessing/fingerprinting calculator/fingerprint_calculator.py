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
from scipy import stats


#where are your connectomes saved
connectomefolder = '/Users/path/to/connectomes/'

#your connectomes must be named participantid + separator + whatever else + .csv
#e.g., subject-001_ses-1_movie-1.csv
nameseparator = '_'


#do you wish to carry out a Fisher z transform on your connectome to better approximate a normal distribution?
#(select False if this was already carried out previously)
fisherz = True






participant_files = os.listdir(connectomefolder)
subfiles = [file for file in participant_files if file.endswith('csv')]


FCallvec = []
participantlist = []
labellist = []
veclen = []

for filen in range(len(subfiles)):
    
    file = subfiles[filen]
    
    fnames = file.find(nameseparator)
    participantid = file[:fnames]

    print("Loading " + file)
    rawdata = pd.read_csv(connectomefolder + file, index_col=0)

    if not list(rawdata.columns) == list(rawdata.index):
        print("Connectome index does not match columns")
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
        veclen.append(len(vec))
        participantlist.append(participantid)
        labellist.append(participantid + nameseparator + str(filen) + 'x')


if not len(set(veclen)) == 1:
    print("Your connectomes are not all the same size")
else:

    print("")
    print("Creating correlation matrix between connectomes")
    

    corrlol = []
    numlabels = len(labellist)
    numlabels10 = int(len(labellist)/10)
    
    for i in range(len(labellist)):
        
        if i % numlabels10 == 0:
            print('Checking connectome',i+1,'of',numlabels)
        
        FC1vec = FCallvec[i]
        corrlist = []

        
        for l in range(len(labellist)):
            if i > l:  
            
                FC2vec = FCallvec[l]       
                corre = pearsonr(FC1vec,FC2vec)
                finalcorr = np.arctanh(corre[0])  

            else:
                finalcorr = 0   

            corrlist.append(finalcorr) 

        corrlol.append(corrlist)
        
    
    corrdf = pd.DataFrame(data=corrlol)
    corrdf = corrdf + corrdf.T
    
    corrdf.columns = labellist
    corrdf.index = labellist


    print("")
    print("Fingerprint matching!")
        
    meanselfcomp = []
    meanothercomp = []
    indiv = []
    percentile = []
    matchlist = []
    filelist = []


    for i in range(len(labellist)):
        
        if i % numlabels10 == 0:
            print('Checking connectome',i+1,'of',numlabels)
            
        label1 = labellist[i]
        person1 = participantlist[i]
        
        #get self-self correlations, but not the trivial same scan to same scan
        personcolumns1 = [col for col in labellist if person1 in col]
        personcolumnsother = [col for col in personcolumns1 if label1 not in col]
        
        #correlations to others
        nonpersoncolumns = [col for col in labellist if person1 not in col]
        
        selfdf = corrdf[label1].loc[personcolumnsother]
        selfdflist = list(selfdf)
        othersdf = corrdf[label1].loc[nonpersoncolumns]   
        othersdflist = list(othersdf)
        
        #check that there are multiple files from participant
        if len(selfdflist) > 0:
            meanselfcomp.append(np.mean(selfdflist))
            meanothercomp.append(np.mean(othersdflist))
            indiv.append(np.mean(selfdflist)-np.mean(othersdflist))
            
            compval = 0
            numbetter = []
            for selfcomp in selfdflist:
                comp = sum(np.array(othersdflist) > selfcomp)
                if comp == 0:
                    #if none of the other comparisons are higher than this self comparison, then it's a match
                    compval = compval + 1
                numbetter.append(stats.percentileofscore(othersdflist, selfcomp))
            #average match rate across # of comparisons
            adjcompval = compval / len(selfdflist)
            avgnumbetter = np.mean(numbetter)
                        
            matchlist.append(adjcompval)
            percentile.append(avgnumbetter)
            filelist.append(subfiles[i])
            
        
        
        
    resultdf = pd.DataFrame({'file':filelist,'match':matchlist,'percentile':percentile,'stability':meanselfcomp,'similarity':meanothercomp,'indiv':indiv})
    resultdf = resultdf.sort_values(by=['file'])    
    
    print("")
    print(resultdf.to_string())
    print("")
    print("")
    
    matches = [match for match in matchlist if match >= 1]
    nummatches = len(matches)
    matchpercent = nummatches/len(matchlist)*100
    
    print("Number of matches:",nummatches,'/',len(matchlist),'(',round(matchpercent,2),'%)')
    print("Average match rate:",round(np.average(matchlist),2),'(this is the same as match percent if only 2 scans per participant)')
    print("Average percentile:",round(np.average(percentile),2),'(self-stability relative to similarity-to-others; 100% = all matches)')
    print("Average self-stability",round(np.average(meanselfcomp),2))
    print("Average similarity-to-others",round(np.average(meanothercomp),2))
    print("Average individualization",round(np.average(indiv),2))
        
    




















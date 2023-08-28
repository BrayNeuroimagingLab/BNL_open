#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 14:27:58 2023

@author: Kirk

This calculates ICC2 for every edge
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pingouin as pg


#where are your connectomes saved
connectomefolder = '/Users/ivy/Desktop/Test_Data/connectomes/'

#your connectomes must be named participantid + separator + way of judging reliability (e.g. by session) + separator + whatever else + .csv
#e.g., subject-001_ses-1_movie-1.csv
nameseparator = '_'


#do you wish to carry out a Fisher z transform on your connectome to better approximate a normal distribution?
#(select False if this was already carried out previously)
fisherz = True

#if False, will only test the first 250 edges, for speed
testalledges = False




participant_files = os.listdir(connectomefolder)
subfiles = [file for file in participant_files if file.endswith('csv')]


FCallvec = []
veclen = []
participantlist = []
rawnamelist = []
sessionlist = []

for filen in range(len(subfiles)):
    
    file = subfiles[filen]
    
    fnames = file.split(nameseparator)
    participantid = fnames[0]
    participantses = fnames[1]

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
        rawnamelist.append(participantid + '_' + participantses)
        sessionlist.append(participantses)

if not len(set(veclen)) == 1:
    print("Your connectomes are not all the same size")
else:

    print("Making edge df")
    listofparcels = list(rawdata.columns)
    connections = []
    for ii in range(1, rawdata.shape[0]):
        for jj in range(ii):
            #connections.append(str(ii)+'-'+str(jj))    
            connections.append(listofparcels[ii]+'-'+listofparcels[jj])


    edgedata = pd.DataFrame({'images':rawnamelist,'person':participantlist,'ses':sessionlist})
    edgeydata = pd.DataFrame(data=FCallvec)
    edgeydata.columns = connections
    edgedata = edgedata.join(edgeydata)    


    iccs = []
    edgesused = []

    numedges = len(connections)
    
    if testalledges:
        testlen = numedges
    else:
        testlen = 250
    
    for edgenum in range(testlen):
        if edgenum % 1000 == 0:
            print('For ICC, working on edge ' + str(edgenum))
        edge = connections[edgenum]
        
        icc_df = pg.intraclass_corr(data=edgedata,targets='person',raters='ses',ratings=edge)
        iccval = float(icc_df[icc_df['Type']=='ICC2']['ICC'])
        
        
        #modelstr = 'Q("' + edge + '") ~ C(person) + C(ses)'
        #model = ols(modelstr, data=edgedata).fit()
        #summary = sm.stats.anova_lm(model)
        
        #MSp = summary['mean_sq'][0]
        #MSe = summary['mean_sq'][2]
        #MSs = summary['mean_sq'][1]
        
        #ICC2
        #ICCx = (MSp - MSe)/(MSp+(nr-1)*MSe+nr/nc*(MSs-MSe))
        
        #ICC3
        #ICCx = (MSp-MSe)/(MSp+(nr-1)*MSe)
        
        iccs.append(iccval)
        edgesused.append(edge)

    iccdf = pd.DataFrame({'edge':edgesused,'icc2':iccs})
    
    print("")
    print(iccdf)
    print('')
    print("Tested",testlen,'edges')
    print("Average ICC2 is",np.mean(iccs))
    
    print("The histogram shows the distribution of ICC values")
    
    plt.hist(iccs)
    plt.show()








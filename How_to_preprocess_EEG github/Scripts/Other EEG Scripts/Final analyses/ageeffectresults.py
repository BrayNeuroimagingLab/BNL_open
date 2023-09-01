#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Looking at age effects...

For each different specific video (e.g., Dora3, Dora6, Dora9, RX2, etc) 
I ran a paired t-test for each edge, comparing child FC to their parent FC. 
I then averaged the absolute t-statistic across all edges. This gave me 11 different 
averages per frequency band per FC measure. (Why 11 and not 12? Participants only had 3 Dora videos in common). 
Results were similar across frequency bands. Here are the alpha band averages across tasks:
    
psi: 0.921
pli: 0.974
wpli: 0.978
imcoh: 1.15
coh: 1.76
plv: 1.69


This program specifically loads up the t-test df's, calculates the average (absolute) t stat, then spits that out, basically

"""



import numpy as np
import pandas as pd
import os
from scipy.stats.stats import pearsonr
from scipy.stats import ttest_rel



from scipy import stats


#folder where outputs are saved
savesumdir = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/xresults/parentvchild_ttest/'


conmethods = ['psi','pli','wpli','imcoh','coh','plv']
fbandhere = '8.0-13.0'
#fbandhere = '13.0-30.0'
#fbandhere = '2.5-45.0'

conmethodlist = []
fbandlist = []
stasklist = []
avgtlist = []

filestoread = os.listdir(savesumdir)

for filetoread in filestoread:

    if filetoread.endswith('.csv'):
        sfile = filetoread.split('_')
        conmethod = sfile[1]
        fband = sfile[2]
        stask = sfile[3][:-4]
        
        ttestdf = pd.read_csv(savesumdir+filetoread,index_col=0)
    
        abst = abs(ttestdf['tval'])
        avgabst = np.mean(abst)
        
        conmethodlist.append(conmethod)
        fbandlist.append(fband)
        stasklist.append(stask)
        avgtlist.append(avgabst)
    
summarydf = pd.DataFrame({'fband':fbandlist,'task':stasklist,'conmethod':conmethodlist,'avgt':avgtlist})

subdf = summarydf[summarydf['fband'] == fbandhere]

for conmethod in conmethods:
    subsubdf = subdf[subdf['conmethod'] == conmethod]
        
    avgthere = np.mean(subsubdf['avgt'])
    minthere = np.min(subsubdf['avgt'])
    maxthere = np.max(subsubdf['avgt'])
    print(conmethod,avgthere)
    
    #print(conmethod,minthere,maxthere)
    
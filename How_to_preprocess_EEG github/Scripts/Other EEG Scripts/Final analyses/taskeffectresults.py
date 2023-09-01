#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This program specifically loads up the F-test df's, calculates the average F stat, then spits that out, basically

"""



import numpy as np
import pandas as pd
import os
from scipy.stats.stats import pearsonr
from scipy.stats import ttest_rel



from scipy import stats


#folder where outputs are saved
savesumdir = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/xresults/avgtask_anova/'
savesumdir = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/xresults/task_anova/'


conmethods = ['psi','pli','wpli','imcoh','coh','plv']
fbandhere = '8.0-13.0'
#fbandhere = '13.0-30.0'
#fbandhere = '2.5-45.0'

conmethodlist = []
fbandlist = []
avgtlist = []

filestoread = os.listdir(savesumdir)

for filetoread in filestoread:

    if filetoread.endswith('.csv'):
        sfile = filetoread.split('_')
        conmethod = sfile[1]
        fband = sfile[2][:-4]
        
        anovadf = pd.read_csv(savesumdir+filetoread,index_col=0)
        
        Fval = anovadf['Fval']
        avgabst = np.mean(Fval)
        
        conmethodlist.append(conmethod)
        fbandlist.append(fband)
        avgtlist.append(avgabst)
    
summarydf = pd.DataFrame({'fband':fbandlist,'conmethod':conmethodlist,'avgt':avgtlist})

subdf = summarydf[summarydf['fband'] == fbandhere]

for conmethod in conmethods:
    subsubdf = subdf[subdf['conmethod'] == conmethod]
        
    valuehere = float(subsubdf['avgt'])
    
    print(conmethod,valuehere)



"""
testdf1 = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/xresults/task_anova/taskanova_plv_8.0-13.0.csv'
testdf2 = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/xresults/task_anova/taskanova_imcoh_8.0-13.0.csv'

plvdf = pd.read_csv(testdf1,index_col=0)
plvF = list(plvdf['Fval'])
imcohdf = pd.read_csv(testdf2,index_col=0)
imcohF = list(imcohdf['Fval'])

tres = ttest_rel(plvF,imcohF)
"""
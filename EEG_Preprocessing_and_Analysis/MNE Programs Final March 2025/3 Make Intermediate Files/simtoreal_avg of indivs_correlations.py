#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
After running simtoreal_correlations, this program averages all of them together
That way the simtoreal for average connectomes and simtoreal for average of all the connectomes are in a similar format

If I were starting over, this program is kinda unnecessary and could just be tacked onto the end of simtoreal_correlations
"""

import pandas as pd
import numpy as np


#output of simtoreal_correlations
dfloc = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/results_august2024/individualfilecorrelations100/corrdf.csv'


df = pd.read_csv(dfloc,index_col=0,low_memory=False)

fbands = list(set(df['fband']))
conmethods = list(set(df['conmethod']))
abstypes = list(set(df['abs']))
comparisons = list(set(df['comparison']))


corrfband = []
corrconmethod = []
corrabs = []
corrcomparison = []
corrcomparisonspecific = []
corrcorrspearman = []
corrcorrpearson = []

corrcorrspearmanabs = []
corrcorrpearsonabs = []

count = 0
speclist = []

for fband in fbands:
    for conmethod in conmethods:
        for abstype in abstypes:
            for comparison in comparisons:
                subdf = df[(df['fband'] == fband) &
                           (df['conmethod'] == conmethod) &
                           (df['abs'] == abstype) &
                           (df['comparison'] == comparison)
                           ]
                
                compspecifics = list(set(subdf['compspecific']))
                
                for compspecific in compspecifics:
                    if count % 50 == 0:
                        print(count)
                    xsubdf = subdf[subdf['compspecific'] == compspecific]
                    if len(xsubdf) != 581:
                        print("OH NO")
                    else:
                        count = count + 1
                        pcorrs = list(xsubdf['Pearson'])
                        scorrs = list(xsubdf['Spearman'])
                        
                        if all([i>0.999 for i in pcorrs]):
                            meanpcorr = 1
                        
                        else:
                            pcorrs = np.arctanh(pcorrs)
                            adjpcorrs = []
                            specialp = False
 
                            for val in pcorrs:
                                if val != np.inf and val != np.nan:
                                    adjpcorrs.append(val)
                                else:
                                    specialp = True
                            
                            if specialp:
                                speclist.append([fband,conmethod,abstype,comparison,compspecific,'Pearson'])                           
                            
                            meanpcorr = np.mean(adjpcorrs)
                            meanpcorr = np.tanh(meanpcorr)
                            
                            absadjpcorrs = [abs(x) for x in adjpcorrs]
                            absmeanpcorr = np.mean(absadjpcorrs)
                            absmeanpcorr = np.tanh(absmeanpcorr)
                            
                            
                            
                        if all([i>0.999 for i in scorrs]):
                            meanscorr = 1
                        else:
                            scorrs = np.arctanh(scorrs)
                            adjscorrs = []
                            specials = False
 
                            for val in scorrs:
                                if val != np.inf and val != np.nan:
                                    adjscorrs.append(val)     
                                else:
                                    specials = True

                            if specials:
                                speclist.append([fband,conmethod,abstype,comparison,compspecific,'Spearman'])
    
                           
                            meanscorr = np.mean(adjscorrs)
                            meanscorr = np.tanh(meanscorr)
                            
                            
                            absadjscorrs = [abs(x) for x in adjscorrs]
                            absmeanscorr = np.mean(absadjscorrs)
                            absmeanscorr = np.tanh(absmeanscorr)
                        
                        
                        corrfband.append(fband)
                        corrconmethod.append(conmethod)
                        corrabs.append(abstype)
                        corrcomparison.append(comparison)
                        corrcomparisonspecific.append(compspecific)
                        corrcorrpearson.append(meanpcorr)
                        corrcorrspearman.append(meanscorr)
                        
                        corrcorrpearsonabs.append(absmeanpcorr)
                        corrcorrspearmanabs.append(absmeanscorr)
                        


resultdf = pd.DataFrame({'fband':corrfband,
                         'conmethod':corrconmethod,
                         'abs':corrabs,
                         'comparison':corrcomparison,
                         'compspecific':corrcomparisonspecific,
                         'Pearson':corrcorrpearson,
                         'Spearman':corrcorrspearman,
                         'Pearson_abs':corrcorrpearsonabs,
                         'Spearman_abs':corrcorrspearmanabs
                         })


resultdf.to_csv('/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/results_august2024/individualfilecorrelations100/corrdf_avgsofindivs.csv')






































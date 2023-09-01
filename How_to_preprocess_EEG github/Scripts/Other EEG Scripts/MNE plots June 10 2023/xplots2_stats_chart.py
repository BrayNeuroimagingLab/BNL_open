#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 16:13:06 2023

@author: Kirk
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal
from scipy.stats import ttest_rel
import math


usesensor = False
usesameses = False

figbasename = 'fig2-stats'
savefolder = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/yresult_folder/'


savesumdir = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/xfingerprint/'
sensorsumdir = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/xfingerprint_sensor/'






conmethods = ['psi','pli','wpli','imcoh','coh','plv']


fbands_all = [[8.0,13.0],[13.0,30.0],[2.5,45.0]]

fbandslist = [[0]]

rowdatas_all = ['stability','similarity','individualization','match','percentile']
rowtitles_all = ['Self-Stability','Similarity-to-Others','Individualization','Match Rate (%)','Self-Stability Percentile']

rowdataslist = [[0,2,3,4]]
rowdataslist = [[0,1,2,3,4]]






colorlist = ['#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00']
cmap = 'summer' 

colorsinboxes = ['#ECF39E','#A4C3B2','w','silver' ]


outputname = figbasename
if usesensor:
    outputname = outputname + '_sensor'
if usesameses:
    outputname = outputname + '_sameses'
outputname = outputname + '.png'


    
    

def round_sig(x,sig):

    format_string = '{{:.{}g}}'.format(sig)
    roundtext = format_string.format(x)
    
    adjroundtext = roundtext.replace(".", "").lstrip("0")
    if adjroundtext != '':
        while len(adjroundtext) < sig:
            if '.' in roundtext:
                roundtext = roundtext + '0' 
            else:
                roundtext = roundtext + '.0'
            adjroundtext = roundtext.replace(".", "").lstrip("0")    

        if abs(float(roundtext)) >= 10**sig:
            format_string = '{{:.{}E}}'.format(sig-1)
            xroundtext = format_string.format(Decimal(x))
            xroundtext = xroundtext.split('E')
            roundtext = xroundtext[0] + 'e' + str(int(xroundtext[1]))
        
        elif abs(float(roundtext)) < 1/(10**(sig)):
            format_string = '{{:.{}E}}'.format(sig-1)
            xroundtext = format_string.format(Decimal(x))
            xroundtext = xroundtext.split('E')
            roundtext = xroundtext[0] + 'e' + str(int(xroundtext[1]))
    
    return roundtext



for fbs in fbandslist:
    outputnameband = figbasename + '_fb-'
    fbands = []
    for fb in fbs:
        fbandhere = fbands_all[fb]
        fbands.append(fbandhere)
        if str(fbandhere) == '[2.5, 45.0]':
            outputnameband = outputnameband + 'br'
        elif str(fbandhere) == '[8.0, 13.0]':
            outputnameband = outputnameband + 'al'
        elif str(fbandhere) == '[13.0, 30.0]':
            outputnameband = outputnameband + 'be'

    for rds in rowdataslist:
        outputnamerow = outputnameband + '_r'
        rowdatas = []
        rowtitles = []
        for rd in rds:
            rowdatas.append(rowdatas_all[rd])
            rowtitles.append(rowtitles_all[rd])
            outputnamerow = outputnamerow + str(rd)


        outputname = outputnamerow
        if usesensor:
            outputname = outputname + '_sensor'
        if usesameses:
            outputname = outputname + '_sameses'
        outputname = outputname + '.png'
        
        
        columns = len(fbands)
        if columns < 2:
            columns = 2
        rows = len(rowdatas)
        lastrow = len(rowdatas)-1
        
        if rows < 2:
            rows = 2


        #fig, axs = plt.subplots(rows, columns,figsize=(2.7*columns,2.125*rows),dpi=200)
        fig, axs = plt.subplots(rows, columns,figsize=(2.9*columns,1.125*rows),dpi=300)
        

        pltthingsthingsthings = []
        
        for fi in range(len(fbands)):
        
            fband = fbands[fi]
            fbandstr = str(fband[0]) + '-' + str(fband[1])
            fmin = fband[0]
            fmax = fband[1]    
            title = fbandstr + ' Hz'
            
            pltthingsthings = []
            
            for coni in range(len(conmethods)):          
                conmethod = conmethods[coni]
                
                if usesensor:
                    logname = sensorsumdir + 'fingerprint_' + conmethod + '_' + fbandstr + '.csv'
                else:
                    logname = savesumdir + 'fingerprint_' + conmethod + '_' + fbandstr + '.csv'
                resultdf = pd.read_csv(logname,index_col=0)
                
                if usesameses:
                    matchrate = list(resultdf['match_sameses'])
                    percentiles = list(resultdf['percentile_sameses'])
                    stabilities = list(resultdf['stab_sameses_avg'])
                    similarities = list(resultdf['sim_avg'])
                    indivs = list(resultdf['stab_sameses_avg']-resultdf['sim_avg'])  
                else:
                    matchrate = list(resultdf['match'])
                    percentiles = list(resultdf['percentile'])
                    stabilities = list(resultdf['stab_avg'])
                    similarities = list(resultdf['sim_avg'])
                    indivs = list(resultdf['stab_avg']-resultdf['sim_avg'])
        
        
                matchrate = [x*100 for x in matchrate]

                pltthings = []
                
                for rowdata in rowdatas:
                    if rowdata == 'stability':
                        pltthings.append(stabilities)
                    if rowdata == 'similarity':
                        pltthings.append(similarities)
                    if rowdata == 'individualization':
                        pltthings.append(indivs)
                    if rowdata == 'match':
                        pltthings.append(matchrate)
                    if rowdata == 'percentile':
                        pltthings.append(percentiles)      
                
                
                pltthingsthings.append(pltthings)
            
            pltthingsthingsthings.append(pltthingsthings)     
               
            if len(fbands) > 1:   
                axs[0,fi].text(0.5,1.2,title,horizontalalignment='center', verticalalignment='center',transform=axs[0,fi].transAxes,fontsize=12)
        

        pltarar = np.array(pltthingsthingsthings)
        pltarar = np.transpose(pltarar, (2, 0, 1, 3))
        
        for x0 in range(len(rowdatas)):  
            comparisonz = pltarar[x0]
            
            for fi in range(len(fbands)):
                comparisonslist = comparisonz[fi]
        
                pvallistlist = []
                diffa0listlist = []
                colorlistlist = []
                
                for n1 in range(5):
                    
                    pvallist = []
                    diffa0list = []
                    colorlist = []
                    
                    for n2 in range(1,6):
                        
                        if n1 >= n2:
                            pval = ''
                            pvallist.append(pval)
                            diffa0list.append(pval)
                            colorlist.append(colorsinboxes[3])
                            
                        else:
                            
                             list1 = comparisonslist[n1]
                             list2 = comparisonslist[n2]
                             diff = [a_i - b_i for a_i, b_i in zip(list2, list1)]
                             diff_quantity = sum(i > 0 for i in diff)
                             diff_quantity = int(diff_quantity)
                                                  
                             pval = ttest_rel(list1,list2)[1]
                             
                             #'#999999', '#e41a1c', '#dede00'
                             
                             if pval < 0.05/15:
                                 colorlist.append(colorsinboxes[0])
                             elif pval < 0.05:
                                 colorlist.append(colorsinboxes[1])
                             else:
                                 colorlist.append(colorsinboxes[2])
                            
                             
                             dval = abs(np.mean(diff)/np.std(diff))            
                             
                             strhere = 'p: ' + round_sig(pval,2) + '\n' + 'c>r: ' + str(diff_quantity) + '/50'
                             strhere = 'p: ' + round_sig(pval,2)
                             
                             #pvallist.append('p = ' + round_sig(pval,2))
                             pvallist.append(strhere)
                             diffa0list.append('>0 = ' + str(diff_quantity))
                             
                    
                    pvallistlist.append(pvallist)
                    diffa0listlist.append(diffa0list)
                    colorlistlist.append(colorlist)


                #'#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3'        

                table = axs[x0,fi].table(cellText=pvallistlist,
                  cellLoc='center',
                  rowLabels=['psi','pli','wpli','imcoh','coh'],
                  colLabels=['pli','wpli','imcoh','coh','plv'],
                  rowLoc='center',
                  #rowColours=['linen','linen','linen','linen','linen'],
                  #colColours=['linen','linen','linen','linen','linen'],
                  rowColours=['#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628'],
                  colColours=['#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3'],
                  bbox = [0, 0, 1, 1],
                  cellColours=colorlistlist,
                  )      
                
                cellDict = table.get_celld()
                for i in range(0,5):
                    cellDict[(0,i)].set_height(.1)        
                
                #table.auto_set_font_size(False)
                table.set_fontsize(12)
                #table.auto_set_column_width(col=list(range(5)))
                axs[x0,fi].axis("off")  



        for rn in range(len(rowdatas)):
            #axs[rn,0].set_ylabel(rowtitles[rn])    
            axs[rn,0].text(-0.12,0.5,rowtitles[rn],horizontalalignment='center', verticalalignment='center',transform=axs[rn,0].transAxes,fontsize=6,rotation=90)


        if len(rowdatas) == 1:
            for y in range(columns):
                fig.delaxes(axs[1][y])
        
        if len(fbands) == 1:
            for x in range(len(rowdatas)):
                fig.delaxes(axs[x][1])
        
                
        plt.subplots_adjust(top=0.94)
        plt.tight_layout()
        
        

        
        plt.savefig(savefolder + outputname)
        print("Saving " + savefolder + outputname)
        plt.show()
        
        
        
        
        
        
        
        
        






            
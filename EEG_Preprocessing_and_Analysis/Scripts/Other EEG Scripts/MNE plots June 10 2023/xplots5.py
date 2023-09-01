#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 11:27:12 2023

@author: Kirk
"""

import pandas as pd
import matplotlib.pyplot as plt


figbasename = 'fig5'

percentofmaxmode = False




readin1 = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/xfingerprint_time/fingerprintsummary.csv'
readin2 = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/xfingerprint_time_comb/fingerprintsummary.csv'
readin3 = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/xfingerprint_time_comb_12/fingerprintsummary.csv'

readinlist = [readin1,readin2]
readinlist = [readin3]



savefolder = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/yresult_folder/'
savefolder = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/yresult_ohbm/'


titlelist = ['separate tasks', 'combined tasks','mega combined']



con_list = ['psi','pli','wpli','imcoh','coh','plv']
#con_list = ['psi','pli']



colorlist = ['#377eb8', '#ff7f00', '#4daf4a','#999999', '#e41a1c', '#984ea3']
colorlist = ['#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00']




conmethods = ['psi','pli','wpli','imcoh','coh','plv']


fbands_all = [[8.0,13.0],[13.0,30.0],[2.5,45.0]]


fbandslist = [[0]]

rowdatas_all = ['stability','similarity','individualization','match','percentile']
rowtitles_all = ['Self-Stability','Similarity-to-Others','Participant Identifiability','Match Rate (%)','Self-Stability Percentile']
#rowtitles_all = ['Self-Stability','Similarity-to-Others','Individualization','Match Rate (%)','Self-Stability Percentile']

rowdataslist = [[2]]
#rowdataslist = [[0,1,2]]





for fbs in fbandslist:
    outputnameband = figbasename + '_fb-'
    fbands = []
    for fb in fbs:
        fbandhere = fbands_all[fb]
        fbands.append(fbandhere)
        bandhere = str(fbandhere[0]) + '-' + str(fbandhere[1])
        if str(fbandhere) == '[2.5, 45.0]':
            outputnameband = outputnameband + 'br'
        elif str(fbandhere) == '[8.0, 13.0]':
            outputnameband = outputnameband + 'al'
        elif str(fbandhere) == '[13.0, 30.0]':
            outputnameband = outputnameband + 'be'

    if len(readinlist) == 2:
        outputnameband = outputnameband + '_both'
    elif 'comb/' in readinlist[0]:
        outputnameband = outputnameband + '_comb'
    elif 'comb_12' in readinlist[0]:
        outputnameband = outputnameband + '_comb12'        
    else:
        outputnameband = outputnameband + '_sep'
    
    if percentofmaxmode:
        outputnameband = outputnameband + '_percentmax'


    for rds in rowdataslist:
        outputnamerow = outputnameband + '_r'
        rowdatas = []
        rowtitles = []
        for rd in rds:
            rowdatas.append(rowdatas_all[rd])
            rowtitles.append(rowtitles_all[rd])
            outputnamerow = outputnamerow + str(rd)


        outputname = outputnamerow + '.png'
        
        
        columns = len(readinlist)
        if columns < 2:
            columns = 2
        rows = len(rowdatas)
        lastrow = len(rowdatas)-1
        lastcolumn = len(readinlist)-1
        
        if rows < 2:
            rows = 2
        
        fig, axs = plt.subplots(rows, columns,figsize=(4*columns,2.125*rows),dpi=300)
        
        maxn = [0]*rows
        minn = [100]*rows




        
        for i in range(len(readinlist)):
            sumdf = pd.read_csv(readinlist[i],index_col=0)
            sumdf['indiv'] = sumdf['stability'] - sumdf['similarity']
        
            title = titlelist[i]
            
            
            for j in range(len(con_list)):
                con_section = con_list[j]
                
                
                
                band = bandhere
                
            
                subdf = sumdf[sumdf['con'] == con_section]
                age = 'all'
                subsubdf = subdf[subdf['age'] == age]
                subsubsubdf = subsubdf[subsubdf['band'] == band]
                
                epochs = list(subsubsubdf['epochs'])
                epochs = [x*2/60 for x in epochs]
                matchrate = list(subsubsubdf['match'])
                percentiles = list(subsubsubdf['percentile'])
                stabilities = list(subsubsubdf['stability'])
                similarities = list(subsubsubdf['similarity'])
                indivs = list(subsubsubdf['indiv'])
                
                matchratemax = max(matchrate)
                percentilesmax = max(percentiles)
                stabilitiesmax = max(stabilities)
                similaritiesmax = max(similarities)
                indivsmax = max(indivs)
                
                if percentofmaxmode:
                    matchrate = [x/matchratemax*100 for x in matchrate]
                    percentiles = [x/percentilesmax*100 for x in percentiles]
                    stabilities = [x/stabilitiesmax*100 for x in stabilities]
                    similarities = [x/similaritiesmax*100 for x in similarities]
                    indivs = [x/indivsmax*100 for x in indivs]                
                
        

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

                
                    
                for x0 in range(len(rowdatas)):
                    plthere = pltthings[x0].copy()
                    axs[x0,i].scatter(epochs,plthere,marker=".",color=colorlist[j])
                    axs[x0,i].plot(epochs,plthere,color=colorlist[j],label=con_section) 
        
                    maxval = max(plthere)
                    if maxval > maxn[x0]:
                        maxn[x0] = maxval
                    minval = min(plthere)
                    if minval < minn[x0]:
                        minn[x0] = minval   
        
        
            if len(readinlist) > 1:
                axs[0,i].text(0.5,1.05,title,horizontalalignment='center', verticalalignment='center',transform=axs[0,i].transAxes,fontsize=12)
        
        
        
        

        for rn in range(len(rowdatas)):
            axs[rn,0].set_ylabel(rowtitles[rn])   
        
        
        for y in range(columns):
            axs[lastrow,y].set_xlabel('2 Sec Epochs Included')    
            axs[lastrow,y].set_xlabel('Data Included (min)')    
        
        if len(rds) > 1:
            for y in range(columns):
                for x in range(rows-1):
                    #axs[x,y].set_xticks([])
                    axs[x,y].set_xticklabels([])
        
        for y in range(columns):
            for x in range(rows):
                axs[x,y].spines['right'].set_visible(False)
                axs[x,y].spines['top'].set_visible(False)
                axs[x,y].yaxis.grid(False)
        
        #for x in range(rows):
        #    rangehere = maxn[x]-minn[x]
        #    for y in range(columns):
        #        axs[x,y].set_ylim(minn[x]-rangehere/10,maxn[x]+rangehere/10)  
        

        if len(rowdatas) == 1:
            for y in range(columns):
                fig.delaxes(axs[1][y])
        
        if len(readinlist) == 1:
            for x in range(len(rowdatas)):
                fig.delaxes(axs[x][1])
              
        
        
        
        lgd = axs[0,lastcolumn].legend(bbox_to_anchor=(1.02,0.99),loc='upper left')
        plt.subplots_adjust(top=0.94)
        plt.tight_layout()
        
        print("Saving " + savefolder + outputname)
        #plt.savefig(savefolder + outputname)
        plt.savefig(savefolder + outputname,transparent=True)
        plt.show()
        
        
        










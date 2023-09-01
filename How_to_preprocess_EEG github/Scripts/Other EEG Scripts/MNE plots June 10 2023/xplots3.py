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
from scipy.stats import ttest_rel,sem
from scipy import stats
from matplotlib.font_manager import FontProperties


figbasename = 'fig3'
savefolder = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/yresult_folder/'
savefolder = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/yresult_ohbm/'



savesumdir = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/xfingerprint/'



conmethods = ['psi','pli','wpli','imcoh','coh','plv']


fbands_all = [[8.0,13.0],[13.0,30.0],[2.5,45.0]]

fbandslist = [[0]]

rowdatas_all = ['stability','similarity','individualization','match','percentile']
rowtitles_all = ['Δ Self-Stability','Δ Similarity-to-Others','Δ Individualization','Δ Match Rate (%)','Δ Self-Stability Percentile']
#rowtitles_all = ['Task Sensitivity','Δ Similarity-to-Others','Δ Individualization','Δ Match Rate (%)','Δ Self-Stability Percentile']

#rowdataslist = [[0,1,2,3,4]]
rowdataslist = [[0,1]]
rowdataslist = [[0]]


colorsinboxes = ['#ECF39E','#A4C3B2','w','silver' ]
colorlist = ['#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00']
barwi = 0.33
wi = 0.4 #spread of points  
cs = 13 #point size?
edgecolor = 'black'
avgcolor = 'grey'



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
        outputname = outputname + '.png'
        
        
        columns = len(fbands)
        if columns < 2:
            columns = 2
        rows = len(rowdatas)
        lastrow = len(rowdatas)-1
        
        if rows < 2:
            rows = 2
        
        fig, axs = plt.subplots(rows, columns,figsize=(4*columns,2.125*rows),dpi=300)
        
        maxn = [0]*rows
        minn = [100]*rows
        
        for fi in range(len(fbands)):
        
            fband = fbands[fi]
            fbandstr = str(fband[0]) + '-' + str(fband[1])
            fmin = fband[0]
            fmax = fband[1]    
            title = fbandstr + ' Hz'
            
            pltthingsthings = []
            pltthingsthingsp = []
            
            for coni in range(len(conmethods)):          
                conmethod = conmethods[coni]
                
                logname = savesumdir + 'fingerprint_' + conmethod + '_' + fbandstr + '.csv'
                resultdf = pd.read_csv(logname,index_col=0)
                
                
                matchrate = list(resultdf['match_sametask']-resultdf['match_difftask'])
                percentiles = list(resultdf['percentile_sametask']-resultdf['percentile_difftask'])
                stabilities = list(resultdf['stab_sametask']-resultdf['stab_difftask'])
                similarities = list(resultdf['sim_sametask']-resultdf['sim_difftask'])
                indivs = list(resultdf['stab_sametask']-resultdf['sim_sametask']-resultdf['stab_difftask']+resultdf['sim_difftask'])
                
                matchratep = ttest_rel(resultdf['match_sametask'],resultdf['match_difftask'])[1]
                percentilesp = ttest_rel(resultdf['percentile_sametask'],resultdf['percentile_difftask'])[1]
                stabilitiesp = ttest_rel(resultdf['stab_sametask'],resultdf['stab_difftask'])[1]
                similaritiesp = ttest_rel(resultdf['sim_sametask'],resultdf['sim_difftask'])[1]
                indivsp = ttest_rel(resultdf['stab_sametask']-resultdf['sim_sametask'],resultdf['stab_difftask']-resultdf['sim_difftask'])[1]
        
        
                matchrate = [x*100 for x in matchrate]
                pltthings = []
                pltthingsp = []
                
                for rowdata in rowdatas:
                    if rowdata == 'stability':
                        pltthings.append(stabilities)
                        pltthingsp.append(stabilitiesp)
                    if rowdata == 'similarity':
                        pltthings.append(similarities)
                        pltthingsp.append(similaritiesp)
                    if rowdata == 'individualization':
                        pltthings.append(indivs)
                        pltthingsp.append(indivsp)
                    if rowdata == 'match':
                        pltthings.append(matchrate)
                        pltthingsp.append(matchratep)
                    if rowdata == 'percentile':
                        pltthings.append(percentiles)  
                        pltthingsp.append(percentilesp)
                        
                pltthingsthings.append(pltthings)
                pltthingsthingsp.append(pltthingsp)
                        
                xs = np.random.normal(coni, 0.11, len(matchrate))
                xs = np.random.random_sample((len(matchrate),))
                xs = [x*wi+coni-0.5*wi for x in xs]
                xs[-1] = coni
                xs[0] = coni
                
                
                for x0 in range(len(rowdatas)):
                    plthere = pltthings[x0].copy()
                    plthere.sort()
                    axs[x0,fi].scatter(xs,plthere,s=cs,marker='o',color=colorlist[coni],edgecolors=edgecolor,zorder=2)
                    axs[x0,fi].plot([coni-barwi,coni+barwi],[np.mean(plthere)]*2,color=avgcolor,linewidth=3,zorder=1)  
                    se = sem(plthere)
                    tval = stats.t.ppf(1-0.025,49)
                    lval = np.mean(plthere) - se*tval
                    hval = np.mean(plthere) + se*tval
                    #axs[x0,fi].plot([coni-barwi/2,coni+barwi/2],[lval]*2,color=avgcolor,linewidth=3,zorder=1)  
                    #axs[x0,fi].plot([coni-barwi/2,coni+barwi/2],[hval]*2,color=avgcolor,linewidth=3,zorder=1) 
                    
                        
                    matchtext = round_sig(np.mean(plthere),3) 
                    if len(matchtext) > 4:
                        matchtext = 'μ = ' + round_sig(np.mean(plthere),2)   
                        
                    #axs[x0,fi].text(coni,1.0,matchtext,horizontalalignment='center', verticalalignment='bottom',fontsize=11,transform=axs[x0,fi].get_xaxis_transform())             
        
                    maxval = max(plthere)
                    if maxval > maxn[x0]:
                        maxn[x0] = maxval
                    minval = min(plthere)
                    if minval < minn[x0]:
                        minn[x0] = minval   

            pltar = np.array(pltthingsthings)
            pltar = np.transpose(pltar, (1, 0, 2))    
            
            pltarp = np.array(pltthingsthingsp)
            pltarp = np.transpose(pltarp, (1,0))
            for row in range(len(rowdatas)):                        
                datahere = pltar[row]
                means = []
                meansp = []
                for dat in datahere:
                    matchtext = round_sig(np.mean(dat),2)  
                    means.append(matchtext)

                datap = pltarp[row]
                colorlist = []
                colorlistlist = [['w','w','w','w','w','w']]
                boldlist = []
                for dat in datap:
                    matchtext = round_sig(np.mean(dat),2)  
                    
                    if dat < 0.05/6:
                        colorlist.append(colorsinboxes[0])
                        boldlist.append('b')
                    elif dat < 0.05:
                        colorlist.append(colorsinboxes[1])
                        boldlist.append('i')
                    else:
                        colorlist.append(colorsinboxes[2])
                        boldlist.append('n')
                        
                    meansp.append(matchtext)
                    
                colorlistlist.append(colorlist)
                    

                tabdata = [means,meansp]

                table = axs[row,fi].table(cellText=tabdata,
                  cellLoc='center',
                  rowLabels=[' μ Δ ',' p '],
                  rowLoc='center',
                  rowColours=['linen','linen'],
                  colWidths=[1.113/6.226]+[1/6.226]*4+[1.113/6.226],
                  #cellColours=colorlistlist,
                  cellColours=[['#FF000000']*6]*2,
                  bbox = [0, 1.035, 1, 0.22])
                for (row, col), cell in table.get_celld().items():
                    if row == 1:
                        if boldlist[col] == 'b':
                            cell.set_text_props(fontproperties=FontProperties(weight='bold'))
                        elif boldlist[col] == 'i':
                            cell.set_text_props(fontstyle='italic')
                            #cell.set_text_props(fontproperties=FontProperties(weight='semibold'))
                  
                
                
            if len(fbands) > 1:   
                axs[0,fi].text(0.5,1.2,title,horizontalalignment='center', verticalalignment='center',transform=axs[0,fi].transAxes,fontsize=12)
        
        
        for rn in range(len(rowdatas)):
            axs[rn,0].set_ylabel(rowtitles[rn])    
            axs[rn,0].axhline(y=0, color='black', linestyle=':', linewidth=0.75)
          
        for y in range(columns):
            for x in range(rows-1):
                axs[x,y].set_xticks([])
                axs[x,y].set_xticklabels([])
        
        for y in range(columns):
            axs[lastrow,y].set_xticks(range(len(conmethods)))
            axs[lastrow,y].set_xticklabels(conmethods)
            
        
        for y in range(columns):
            for x in range(rows):
                axs[x,y].spines['right'].set_visible(False)
                axs[x,y].spines['top'].set_visible(False)
                axs[x,y].yaxis.grid(False)
        
        for x in range(rows):
            rangehere = maxn[x]-minn[x]
            for y in range(columns):
                axs[x,y].set_ylim(minn[x]-rangehere/10,maxn[x]+rangehere/10) 
                
        axs[0,0].get_xlim()
        
        
        if len(rowdatas) == 1:
            for y in range(columns):
                fig.delaxes(axs[1][y])
        
        if len(fbands) == 1:
            for x in range(len(rowdatas)):
                fig.delaxes(axs[x][1])
              
        
        plt.subplots_adjust(top=0.94)
        plt.tight_layout()
        
        
        plt.savefig(savefolder + outputname, transparent=True)
        print("Saving " + savefolder + outputname)
        plt.show()
        
        
        





















            
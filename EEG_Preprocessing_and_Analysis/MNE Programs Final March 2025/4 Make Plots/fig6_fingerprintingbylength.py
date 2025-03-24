#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This creates a figure for fingerprinting stats by file length
"""

import pandas as pd
import matplotlib.pyplot as plt
import os


figbasename = 'Fig6'


#where is the data saved that we are plotting?
readin = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/results_august2024/x_fingerprint_timesubset/fingerprintsummary.csv'


#where to save the figure
savefolder = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/results_lol2025probably/figures_mar2025/'



conmethodsx = ['coh','plv','ciplv','ecso','ecpwo','imcoh','wpli','pli','psi']
colorlistx = ['#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00']



saveoutputs = False



fbands_all = [[8.0,13.0],[13.0,30.0],[2.5,45.0]]
#which frequency band to plot, based on the above variable
fbandnum = 2


rowdatas_all = ['stability','similarity','individualization']
rowtitles_all = ['Self-Stability','Similarity-to-Others','Participant Identifiability']





fbandhere = fbands_all[fbandnum]
fbandstr = str(fbandhere[0]) + '-' + str(fbandhere[1])
fmin = fbandhere[0]
fmax = fbandhere[1]

dataname = str(fmin)+'-'+str(fmax)


outputname = figbasename + '_' + dataname + '_stability.png'


columns = 2


rows = len(rowdatas_all)
fig, axs = plt.subplots(rows, columns,figsize=(4*columns,2.125*rows),dpi=300)

for rds in range(columns):
    
    if rds == 0:
        con_list = conmethodsx[:5]
        colorlist = colorlistx[:5]
    if rds == 1:
        con_list = conmethodsx[5:]
        colorlist = colorlistx[5:]
        

    
    
    
    rowdatas = rowdatas_all
    rowtitles = rowtitles_all
    

    lastrow = len(rowdatas)-1
    lastcolumn = columns-1
    

    
    
    maxn = [0]*rows
    minn = [100]*rows




    
    sumdf = pd.read_csv(readin,index_col=0)
    sumdf['indiv'] = sumdf['stability'] - sumdf['similarity']

    
    
    for j in range(len(con_list)):
        con_section = con_list[j]
        
        
                    
    
        subdf = sumdf[sumdf['con'] == con_section]
        age = 'all'
        subsubdf = subdf[subdf['age'] == age]
        subsubsubdf = subsubdf[subsubdf['band'] == dataname]
        
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
            axs[x0,rds].scatter(epochs,plthere,marker=".",color=colorlist[j])
            axs[x0,rds].plot(epochs,plthere,color=colorlist[j],label=con_section) 

            maxval = max(plthere)
            if maxval > maxn[x0]:
                maxn[x0] = maxval
            minval = min(plthere)
            if minval < minn[x0]:
                minn[x0] = minval   



    

for rn in range(len(rowdatas)):
    axs[rn,0].set_ylabel(rowtitles[rn])   


for y in range(columns):
    axs[lastrow,y].set_xlabel('2 Sec Epochs Included')    
    axs[lastrow,y].set_xlabel('Data Included (minutes)')    


for y in range(columns):
    for x in range(rows-1):
        #axs[x,y].set_xticks([])
        axs[x,y].set_xticklabels([])

for y in range(columns):
    for x in range(rows):
        axs[x,y].spines['right'].set_visible(False)
        axs[x,y].spines['top'].set_visible(False)
        axs[x,y].yaxis.grid(False)

axs[0,0].set_title('Vulnerable and Semi-Vulnerable')
axs[0,1].set_title('Minimally Vulnerable')


axs[0,0].yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
axs[1,0].yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
axs[2,0].yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))

if fbandnum == 2:
    axs[0,0].yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
    axs[1,0].yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
    axs[2,0].yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))    

    
    
#lgd = axs[0,lastcolumn].legend(bbox_to_anchor=(1.02,0.99),loc='upper left')
lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
fig.legend(lines[:9], labels[:9],bbox_transform=fig.transFigure,bbox_to_anchor=(1.12,1))


#plt.subplots_adjust(right=0.94)
plt.tight_layout()

if saveoutputs:
    print("Saving graph")
    
    savefolderx = savefolder + fbandstr + '/'
    if not os.path.exists(savefolderx):
        os.makedirs(savefolderx)




    print("Saving " + savefolder + outputname)
    plt.savefig(savefolderx + outputname,bbox_inches='tight')
#plt.savefig(savefolder + outputname,transparent=True)
plt.show()
    
    
    










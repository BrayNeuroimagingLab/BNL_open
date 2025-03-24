#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This creates a figure for the consistency of the age effect (ses12 vs ses34) by amount of data
"""

import pandas as pd
import matplotlib.pyplot as plt
import os


figbasename = 'Fig7'


#where is the data saved that we are plotting?
readin2 = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/results_lol2025probably/splithalf/frontvbackage_nov.csv'




#save figure where?
savefolder = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/results_lol2025probably/figures_mar2025/'


conmethodsx = ['coh','plv','ciplv','ecso','ecpwo','imcoh','wpli','pli','psi']
colorlistx = ['#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00']



saveoutputs = False



fbands_all = [[8.0,13.0],[13.0,30.0],[2.5,45.0]]
#which frequency bands to plot? Based on the above variable
fbandnum = 2

rowdatas_all = ['s']
rowtitles_all = ['Split-Half Correlation']






fbandhere = fbands_all[fbandnum]
fbandstr = str(fbandhere[0]) + '-' + str(fbandhere[1])
fmin = fbandhere[0]
fmax = fbandhere[1]

dataname = str(fmin)+'-'+str(fmax)


outputname = figbasename + '_' + dataname + '_agelength.png'


columns = 1
rows = 2
fig, axs = plt.subplots(rows, columns,figsize=(4*columns,2.125*rows),dpi=300)

for rds in range(rows):
    
    if rds == 0:
        con_list = conmethodsx[:5]
        colorlist = colorlistx[:5]
    if rds == 1:
        con_list = conmethodsx[5:]
        colorlist = colorlistx[5:]
        

    
    
    
    rowdatas = rowdatas_all
    rowtitles = rowtitles_all
    
    
    maxn = [0]*rows
    minn = [100]*rows



    sumdf2 = pd.read_csv(readin2,index_col=0)

    for j in range(len(con_list)):
        con_section = con_list[j]
        
    
        sumdf = sumdf2.copy()
    
        subdf = sumdf[sumdf['conmethod'] == con_section]
        subsubsubdf = subdf[subdf['fband'] == dataname]
        
        epochs = list(subsubsubdf['epochs'])
        epochs = [x*2/60 for x in epochs]
        
        pltthings = []
        avgts = list(subsubsubdf['corr'])
        pltthings.append(avgts)            
        
    
        plthere = pltthings[0].copy()
        axs[rds].scatter(epochs,plthere,marker=".",color=colorlist[j])
        axs[rds].plot(epochs,plthere,color=colorlist[j],label=con_section) 
    
        maxval = max(plthere)
        if maxval > maxn[0]:
            maxn[0] = maxval
        minval = min(plthere)
        if minval < minn[0]:
            minn[0] = minval   
    
    
    

for rn in range(2):
    axs[rn].set_ylabel(rowtitles[0])   


axs[1].set_xlabel('Data Included (minutes)')    

axs[0].set_xticklabels([])


for x in range(rows):
    axs[x].spines['right'].set_visible(False)
    axs[x].spines['top'].set_visible(False)
    axs[x].yaxis.grid(False)


axs[0].set_title('Vulnerable and Semi-Vulnerable')
axs[1].set_title('Minimally Vulnerable')


axs[0].yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
axs[1].yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))

    
    
#lgd = axs[0,lastcolumn].legend(bbox_to_anchor=(1.02,0.99),loc='upper left')
lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
fig.legend(lines[:9], labels[:9],bbox_transform=fig.transFigure,bbox_to_anchor=(1.25,1))


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
    
    
    










#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This makes plots based on self-stability, similarity-to-others, and other individualization stats
for both real and simulated data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal
import os

#if this is False, it uses the simulated data instead of the real data
usereal = False
usereal = True


#where to save the outputs
savefolder = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/results_lol2025probably/figures_mar2025/'


#where is the fingerprint data for both the real data and the simulated data?
savesumdir_sim = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/results_august2024/x_fingerprint_onlysim100/'
savesumdir_real = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/results_august2024/x_fingerprint/'




saveoutputs = False


conmethodsx = ['coh','plv','ciplv','ecso','ecpwo','imcoh','wpli','pli','psi']
colorlistx = ['#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00']




fbands_all = [[8.0,13.0],[13.0,30.0],[2.5,45.0]]

#which frequency band to use right now? based on the above variable
fb = 2

#what data do we want to plot? 0/1/2 makes the main figures, 3/4 makes the sup figures
rowdataslist = [[3,4]]
#rowdataslist = [[0,1,2]]


rowdatas_all = ['stability','similarity','individualization','match','percentile']
rowtitles_all = ['Self-Stability','Similarity-to-Others','Participant Identifiability','Match Rate (%)','Self-Stability Percentile']
analyses_title = ['Vulnerable','Semi-Vulnerable','Minimally Vulnerable']




if usereal == False:
    figbasename = 'Fig4'
if usereal == True:
    figbasename = 'Fig5'
if rowdataslist == [[3,4]]:
    figbasename = figbasename + '_Sup1'



figsizebase = 1.7
barwi = 0.4
wi = 0.6   
cs = 13
edgecolor = 'black'
avgcolor = 'grey'



#round numbers for putting them in the plot
def round_sig(x,sig):

    format_string = '{{:.{}g}}'.format(sig)
    roundtext = format_string.format(x)
    
    #print(x,roundtext)
    
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
    
    if sig == 1 and roundtext[-2:] == '-2':
        roundtext = str(round(x,2))
        
        print('test',roundtext,x)
    
    return roundtext






fbandhere = fbands_all[fb]
fbandstr = str(fbandhere[0]) + '-' + str(fbandhere[1])
fmin = fbandhere[0]
fmax = fbandhere[1]

dataname = str(fmin)+'-'+str(fmax)


if usereal:
    outputname = figbasename + '_' + dataname + '_realidentifiability.png'
else:
    outputname = figbasename + '_' + dataname + '_simulatedidentifiability.png'




for rds in rowdataslist:
    rowdatas = []
    rowtitles = []
    for rd in rds:
        rowdatas.append(rowdatas_all[rd])
        rowtitles.append(rowtitles_all[rd])
    
    
columns = 3
rows = len(rowdatas)
lastrow = len(rowdatas)-1

if rows < 2:
    rows = 2
    
maxn = [0]*rows
minn = [100]*rows


fig, axs = plt.subplots(rows, columns,figsize=(4*figsizebase,2.125*rows),dpi=300,width_ratios=[2,3,4])



for fi in range(3):
    

    if fi == 0:
        conmethods = conmethodsx[:2]
        colorlist = colorlistx[:2]
    if fi == 1:
        conmethods = conmethodsx[2:5]
        colorlist = colorlistx[2:5]
    if fi == 2:
        conmethods = conmethodsx[5:]
        colorlist = colorlistx[5:]
        
    ncm = len(conmethods)
        

    fband = fbandhere
    fbandstr = str(fband[0]) + '-' + str(fband[1])
    fmin = fband[0]
    fmax = fband[1]    
    title = analyses_title[fi]
    pltthingsthings = []
    
    for coni in range(len(conmethods)):          
        conmethod = conmethods[coni]
        
        if usereal:
            logname = savesumdir_real + 'fingerprint_' + conmethod + '_' + fbandstr + '.csv'
        else:
            logname = savesumdir_sim + 'fingerprint_' + conmethod + '_' + fbandstr + '.csv'

        resultdf = pd.read_csv(logname,index_col=0)
        
        matchrate = list(resultdf['match'])
        percentiles = list(resultdf['percentile'])
        stabilities = list(resultdf['stab_avg'])
        similarities = list(resultdf['sim_avg'])
        indivs = list(resultdf['stab_avg']-resultdf['sim_avg'])


        matchrate = [x*100 for x in matchrate]
        pltthings = []
        rowmaxs = []
        
        for rowdata in rowdatas:
            if rowdata == 'stability':
                pltthings.append(stabilities)
                #rowmaxs.append()
            if rowdata == 'similarity':
                pltthings.append(similarities)
            if rowdata == 'individualization':
                pltthings.append(indivs)
            if rowdata == 'match':
                pltthings.append(matchrate)
            if rowdata == 'percentile':
                pltthings.append(percentiles)                
              
        pltthingsthings.append(pltthings)
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
                
                
            maxval = max(plthere)
            if maxval > maxn[x0]:
                maxn[x0] = maxval
            minval = min(plthere)
            if minval < minn[x0]:
                minn[x0] = minval   
        
    pltar = np.array(pltthingsthings)
    pltar = np.transpose(pltar, (1, 0, 2))    
    for row in range(len(rowdatas)): 
                               
        datahere = pltar[row]
        means = []
        for dat in datahere:
            matchtext = round_sig(np.mean(dat),3) 
            if len(matchtext) > 4:
                matchtext = round_sig(np.mean(dat),2) 
                if len(matchtext) > 4:
                    matchtext = round_sig(np.mean(dat),1)                 
            means.append(matchtext)

        tabdata = [means]
        edgeextra = 0
        total = ncm+edgeextra*2
        edgevalues = 1+edgeextra

        cells = axs[row,fi].table(cellText=tabdata,
          cellLoc='center',
          rowLabels=[' μ '],
          #rowLoc='center',
          rowColours=['linen','linen'],
          cellColours=[['#FF000000']*ncm],
          #colWidths=[1.113/6.226]+[1/6.226]*4+[1.113/6.226],
          #colWidths=[1.213/6.426]+[1/6.426]*(ncm-2)+[1.213/6.426],          
          colWidths=[edgevalues/total]+[1/total]*(ncm-2)+[edgevalues/total],
          bbox = [0, 1.035, 1, 0.11])
        
        for ii in range(len(tabdata[0])):
            cells[0,ii].set_text_props(va='center_baseline')


    axs[0,fi].text(0.5,1.215,title,horizontalalignment='center', verticalalignment='center',transform=axs[0,fi].transAxes,fontsize=12)


    axs[lastrow,fi].set_xticks(range(len(conmethods)))
    axs[lastrow,fi].set_xticklabels(conmethods)
        
    xmax = len(conmethods)-0.5
    for x in range(rows):
        axs[x,fi].set_xlim(-0.5,xmax) 
    for x in range(rows):
        lim = axs[x,fi].get_ylim()
        ymax = lim[1]*1.01
        ymin = lim[0]
        if ymin > 0:
            ymin = 0
        if ymax-ymin > 100:
            ymax = ymax*1.01
        
        axs[x,fi].set_ylim(ymin,ymax)
    

#jankyfix. Cause it's now a year and half since I finished my PhD and I ain't doing this in a more future-proof way
if fb == 0 and rowdataslist == [[0,1,2]] and usereal == False:
    print('janky correct applied')
    axs[0,2].set_ylim(-0.06,0.06)
    axs[0,0].set_yticklabels(['0.0','1.0','2.0','3.0','4.0'])
if fb == 1 and rowdataslist == [[0,1,2]] and usereal == False:
    print('janky correct applied')
    print(axs[2,2].get_ylim())
    axs[0,2].set_ylim(-0.033,0.045)
    axs[2,2].set_ylim(-0.033,0.045)
    axs[0,0].set_yticklabels(['0.0','1.0','2.0','3.0','4.0'])
    axs[2,0].set_yticklabels(['0.0','1.0','2.0'])
if fb == 2 and rowdataslist == [[0,1,2]] and usereal == False:
    axs[0,0].yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
    axs[2,0].yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
    axs[0,1].yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
if usereal and fb == 0 and rowdataslist == [[0,1,2]]:
    axs[0,0].yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
    axs[1,0].yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
    axs[2,0].yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))



for rn in range(len(rowdatas)):
    axs[rn,0].set_ylabel(rowtitles[rn])    
    
  
for y in range(columns):
    for x in range(rows-1):
        axs[x,y].set_xticks([])
        axs[x,y].set_xticklabels([])



for y in range(columns):
    for x in range(rows):
        axs[x,y].spines['right'].set_visible(False)
        axs[x,y].spines['top'].set_visible(False)
        axs[x,y].yaxis.grid(False)




if len(rowdatas) == 1:
    for y in range(columns):
        fig.delaxes(axs[1][y])


if usereal:
    fig.suptitle('Real Connectomes')
else:
    fig.suptitle('Simulated Connectomes')

plt.subplots_adjust(top=0.94)
plt.tight_layout()

if saveoutputs:
    print("Saving graph")
    
    savefolderx = savefolder + dataname + '/'
    if not os.path.exists(savefolderx):
        os.makedirs(savefolderx)


    #plt.savefig(savefolderx + outputname, transparent=True)
    plt.savefig(savefolderx + outputname)
print("Saving " + savefolder + outputname)
plt.show()
























            
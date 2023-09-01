#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This makes the plots of the average connectomes

"""



import numpy as np
import mne
import pandas as pd
import os

import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
import statsmodels.api as sm






#folder with all the participant folders and EEG outputs
dir_start = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/prepro1/'

subjects_dir = '/Users/ivy/Desktop/Graff_EEG_stuff/ZPrecise2_MRI_fixed_rename_FS'

loaddir = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/yavg/'
savedir = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/yresult_folder/'

networklabels = '/Users/ivy/Desktop/Graff_EEG_stuff/Desikankilliany/dklabels.csv'




saveoutputs = True




#aparc doesn't work right now
parc = 'aparc.a2009s'
parc = 'aparc'

#this calculates connectivity in 0.5 Hz bands then averages them. 2-3.5 means 2-2.5,2.5-3,3-3.5,3.5-4
fbands = [[4.0,7.5],[8.0,12.5],[13.0,29.5],[2.5,44.5],[30.0,44.5]]


conmethodsload = ['psi_nonabs']
conmethodsload = ['psi_nonabs','psi_abs','pli_nonabs','wpli_nonabs','imcoh_nonabs','imcoh_abs','coh_nonabs','plv_nonabs']
conmethodstitle = ['psi','psi (abs)','pli','wpli','imcoh','imcoh (abs)','coh','plv']

conmethodstitle_space = ['    psi    ','    psi (abs)    ','    pli    ','    wpli    ','    imcoh    ','    imcoh (abs)    ','    coh    ','    plv    ']
conmethodstitle_space2 = [' psi ',' psi (abs) ',' pli ',' wpli ',' imcoh ',' imcoh (abs) ',' coh ',' plv ']
#conmethodstitle_space2 = ['psi','psi (abs)','pli','wpli','imcoh','imcoh (abs)','coh','plv']



conmethodsaltorder = ['imcoh','psi','imcoh (abs)','pli','wpli','psi (abs)','coh','plv']
conmethodsaltorder = ['psi','psi (abs)','pli','wpli','imcoh','imcoh (abs)','coh','plv']

conmethodscolor = ['#377eb8', '#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#f781bf', '#a65628', '#984ea3']



fbands = [[8.0,13.0]]
fbands = [[2.5,45.0]]
fbands = [[13.0,30.0]]





locationlist = ['A','B','C','D','E','F','G','H']


def highlight_cell(x,y, ax=None, **kwargs):
    rect = plt.Rectangle((x-.5, y-.5), 1,1, fill=False, **kwargs)
    ax = ax or plt.gca()
    ax.add_patch(rect)
    return rect


#get a list of everything in the starting directory
folders = os.listdir(subjects_dir)
subjectlist = []
for folder in folders:
    if folder.startswith('sub') and not folder.endswith('fif'):
        if '001' not in folder: 
            subject = folder
            subjectlist.append(subject)

mastersubj = subjectlist[0]
labels_parc = mne.read_labels_from_annot(mastersubj, parc=parc,subjects_dir=subjects_dir)                          
label_names = [label.name for label in labels_parc]   

ypos_lists = []
xpos_lists = []
zpos_lists = []

for subject in subjectlist:
    labels_parc = mne.read_labels_from_annot(subject, parc=parc,subjects_dir=subjects_dir)                          

    label_ypos = list()
    label_xpos = list()
    label_zpos = list()
    for name in label_names:
        idx = label_names.index(name)
        xpos = np.mean(labels_parc[idx].pos[:, 0])
        ypos = np.mean(labels_parc[idx].pos[:, 1])
        zpos = np.mean(labels_parc[idx].pos[:, 2])
        label_ypos.append(ypos)
        label_xpos.append(xpos)
        label_zpos.append(zpos)
    
    ypos_lists.append(label_ypos)
    xpos_lists.append(label_xpos)    
    zpos_lists.append(label_zpos)
    
yposarrays = [np.array(x) for x in ypos_lists]
xposarrays = [np.array(x) for x in xpos_lists]
zposarrays = [np.array(x) for x in zpos_lists]

y_pos_avg = [np.mean(k) for k in zip(*yposarrays)]
x_pos_avg = [np.mean(k) for k in zip(*xposarrays)]
z_pos_avg = [np.mean(k) for k in zip(*zposarrays)]




netdf = pd.read_csv(networklabels,index_col=0)
ogid = list(netdf['id_num'])



labnames = netdf['label']
#testdf = pd.DataFrame({'label':labnames,'network':labz,'ypos':label_ypos,'idnum':ogid})
testdf = pd.DataFrame({'label':labnames,'ypos':y_pos_avg,'xpos':x_pos_avg,'zpos':z_pos_avg,'idnum':ogid})
testdf['hemi'] = testdf['label'].str[-2:]

testdf = testdf.sort_values(by=['hemi','ypos'])

subtestdf = testdf[testdf['hemi'] == 'lh']
neutlabel = subtestdf['label'].str[:-3]
lhlabel = neutlabel + '-lh'
lhlabel = list(lhlabel)
rhlabel = neutlabel + '-rh'
rhlabel = list(rhlabel)
neutlabel = list(neutlabel)

newlabel = lhlabel + rhlabel


testdf.label = testdf.label.astype("category")
testdf.label = testdf.label.cat.set_categories(newlabel)
testdf = testdf.sort_values(by=['label'])


#testdf = testdf.sort_values(by=['hemi','ypos'])
labelz = testdf['label']





  


zero_data = np.zeros(shape=(len(labels_parc),len(labels_parc)))
zerodf = pd.DataFrame(data=zero_data)
zerodf.columns=label_names
zerodf.index=label_names


print("Loading dataframes")
for fband in fbands:
    fbandstr = str(fband[0]) + '-' + str(fband[1])
    fmin = fband[0]
    fmax = fband[1]
    
    avgdflist = []
    
    dataname = str(fmin)+'-'+str(fmax)
    
    fig, axs = plt.subplot_mosaic("AB;CD;EF;GH;JJ",dpi=300,figsize=(9.5,20))
    #fig, axs = plt.subplots(3,2,figsize=(10,15),dpi=200)    
    
    veclist = []
    
    
    for cn in range(len(conmethodsload)):  
        
        conmethodload = conmethodsload[cn]
        
        conmethodtitle = conmethodstitle_space[cn]
        
        conmethodcolor = conmethodscolor[cn]

        avgname_abs = loaddir + 'avg_' + fbandstr + '_' + conmethodload + '.csv'
        #avgname_nonabs = savedir + 'avg_' + fbandstr + '_' + conmethodload + '.csv'

        avgdf = pd.read_csv(avgname_abs,index_col=0)

        lx = locationlist[cn]
        
        adjdf = np.array(avgdf)
        maxval = np.max(adjdf)
        
        graphdfx = avgdf.reindex(columns=labelz)
        graphdfx = graphdfx.reindex(index=labelz)
        
        #test test
        #graphdfx['cuneus-lh']['cuneus-lh'] = 5
           
        altavgdf = np.array(graphdfx) + np.identity(len(graphdfx)) 
        
        vec = []
        for ii in range(1, altavgdf.shape[0]):
            for jj in range(ii):
                vec.append(altavgdf[ii, jj])
        
        veclist.append(vec)
        
        x = [list(x) for x in np.array(altavgdf)]
        minlist = []
        for my_list in x:
            xx = [min(x for x in my_list if x > 0.0001)]
            minlist.append(xx)
        altminvalhere = np.min(minlist)
        
        minval = min(np.min(graphdfx))
        maxval = max(np.max(graphdfx))
        absmin = abs(minval)
        
        if absmin > maxval:
            newmax = absmin
        else:
            newmax = maxval
        
            
        if minval < 0:
            cmap = 'coolwarm'
            cmap = 'RdBu_r'
            chartmin = -1*newmax
            chartmax = newmax                
             
        else:
            cmap = 'YlGnBu'
            cmap = 'viridis'
            #cmap = 'Reds'
            chartmin = altminvalhere
            chartmax = newmax
        
        
        x = list(testdf['hemi'])
        change = [i-0.5 for i in range(1,len(x)) if x[i]!=x[i-1] ]
                
        cs = axs[lx].matshow(graphdfx,cmap=cmap,vmin=chartmin, vmax=chartmax)        
        
        axs[lx].set_yticks([])
        axs[lx].set_yticklabels('', fontsize=8)    
          
        axs[lx].set_xticks([])
        axs[lx].set_xticklabels('', fontsize=8,rotation=90)                                    
        
        axs[lx].xaxis.set_ticks_position('bottom')
        axs[lx].yaxis.grid(False)
        axs[lx].xaxis.grid(False) 
            
        axs[lx].set_xlim(-0.5,len(graphdfx)-0.5)
        axs[lx].set_ylim(len(graphdfx)-0.5,-0.5)
        
        for num in change:   
            axs[lx].axvline(x=num,c='black')
            axs[lx].axhline(y=num,c='black')
        

        cbar = fig.colorbar(cs,ax=axs[lx])
        cbar.ax.tick_params(labelsize=12)
        
        props = dict(boxstyle="Square, pad=0.2", facecolor=conmethodcolor, alpha=0.75)
        
        axs[lx].text(0.5,1.03,conmethodtitle,horizontalalignment='center', verticalalignment='bottom',transform=axs[lx].transAxes,fontsize=16,c='black', bbox=props)        
        
        axs[lx].text(-0.05,0.75,'L',rotation=90,horizontalalignment='center', verticalalignment='center',transform=axs[lx].transAxes,fontsize=13,c='black',weight='bold')        
        axs[lx].text(-0.05,0.25,'R',rotation=90,horizontalalignment='center', verticalalignment='center',transform=axs[lx].transAxes,fontsize=13,c='black',weight='bold')        
        
        axs[lx].text(0.25,-0.05,'L',horizontalalignment='center', verticalalignment='center',transform=axs[lx].transAxes,fontsize=13,c='black',weight='bold')        
        axs[lx].text(0.75,-0.05,'R',horizontalalignment='center', verticalalignment='center',transform=axs[lx].transAxes,fontsize=13,c='black',weight='bold')        
        
        axs[lx].text(-0.04,0.96,'P',rotation=90,horizontalalignment='center', verticalalignment='center',transform=axs[lx].transAxes,fontsize=10,c='black')        
        axs[lx].text(-0.04,0.54,'A',rotation=90,horizontalalignment='center', verticalalignment='center',transform=axs[lx].transAxes,fontsize=10,c='black')        
        axs[lx].text(-0.04,0.46,'P',rotation=90,horizontalalignment='center', verticalalignment='center',transform=axs[lx].transAxes,fontsize=10,c='black')        
        axs[lx].text(-0.04,0.04,'A',rotation=90,horizontalalignment='center', verticalalignment='center',transform=axs[lx].transAxes,fontsize=10,c='black')        
        
        axs[lx].text(0.04,-0.04,'P',horizontalalignment='center', verticalalignment='center',transform=axs[lx].transAxes,fontsize=10,c='black')        
        axs[lx].text(0.46,-0.04,'A',horizontalalignment='center', verticalalignment='center',transform=axs[lx].transAxes,fontsize=10,c='black')        
        axs[lx].text(0.54,-0.04,'P',horizontalalignment='center', verticalalignment='center',transform=axs[lx].transAxes,fontsize=10,c='black')        
        axs[lx].text(0.96,-0.04,'A',horizontalalignment='center', verticalalignment='center',transform=axs[lx].transAxes,fontsize=10,c='black')        
        


    vecdf = pd.DataFrame(data=veclist)
    vecdf = vecdf.T
    vecdf.columns = conmethodstitle
    
    vecdf = vecdf.reindex(columns=conmethodsaltorder)
    
    veccorr = vecdf.corr()
    
    rlistlist = []
            
    for n1 in range(7):
        
        rlist = []
        corr1 = conmethodsaltorder[n1]
        

        for n2 in range(1,8):
            
            corr2 = conmethodsaltorder[n2]
            
            if n1 >= n2:
                rval = np.nan
                rlist.append(rval)
                
            else:
                rval = veccorr[corr1].loc[corr2]
                rlist.append(rval)                
                 
        
        rlistlist.append(rlist)
    



    rlistdf = pd.DataFrame(data=rlistlist)
    rlistdf.columns = conmethodsaltorder[1:]
    rlistdf.index = conmethodsaltorder[:-1]
    
    
    cmap = 'RdBu_r'
    #cs4 = axs[x0,fi].matshow(rlistlist,cmap=cmap,vmin=min_value,vmax=max_value)
    cs4 = axs['J'].matshow(rlistdf,cmap=cmap,vmin=-1,vmax=1)
    cbar = fig.colorbar(cs4,ax=axs['J'])
    cbar.ax.tick_params(labelsize=12)    
          
    # add text annotations to each box
    #for i in range(rlistdf.shape[0]):
    #    for j in range(rlistdf.shape[1]):
    #        if not np.isnan(rlistdf.iloc[i,j]):
    #            pval = rlistdf.iloc[i, j]
    #            texthere = round(pval,2)
    #            axs['J'].text(j, i, texthere, ha="center", va="center", color="black",fontsize=9)


    axs['J'].set_xticks(range(7))
    #axs['J'].xaxis.set_ticks_position('none') 
    axs['J'].set_xticklabels(conmethodstitle_space2[1:], fontsize=12,rotation=90)
    
    axs['J'].set_yticks(range(7))
    #axs['J'].yaxis.set_ticks_position('none') 
    axs['J'].set_yticklabels(conmethodstitle_space2[:-1], fontsize=12)

    axs['J'].xaxis.set_ticks_position('bottom')
    axs['J'].xaxis.grid(False)     
    axs['J'].yaxis.grid(False)
    axs['J'].set_xlim(-0.5,6.5)
    axs['J'].set_ylim(6.5,-0.5)   
    
    axs['J'].tick_params(axis=u'both', which=u'both',length=0, pad=7)

    for ln in range(7):
        label = axs['J'].get_xticklabels()[ln]
        conmethodcolor = conmethodscolor[ln+1]
        label.set_fontsize(15)
        label.set_bbox(dict(facecolor=conmethodcolor, edgecolor='white', alpha=0.75,pad=6))

    for ln in range(7):
        label = axs['J'].get_yticklabels()[ln]
        conmethodcolor = conmethodscolor[ln]
        label.set_fontsize(15)
        label.set_bbox(dict(facecolor=conmethodcolor, edgecolor='white', alpha=0.75,pad=6))
    

    for row in range(len(rlistdf)):
        for col in range(len(rlistdf)):
            if not np.isnan(rlistdf.iloc[row][col]):
                highlight_cell(col,row, color="black", linewidth=1.5)
    
    #fig.delaxes(axs['I'])


    plt.tight_layout()
    plt.subplots_adjust(top=0.94)
        
    if saveoutputs:
        print("Saving graph")

        plt.savefig(savedir + 'fig1_' + dataname + '_avgcorrmatrix.png')
    
    print("Showing graph")
    plt.show()



        
        
















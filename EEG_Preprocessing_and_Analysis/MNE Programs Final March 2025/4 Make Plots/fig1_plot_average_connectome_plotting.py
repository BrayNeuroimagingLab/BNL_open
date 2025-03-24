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



#folder with all the participant folders and EEG outputs
dir_start = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/prepro1/'
subjects_dir = '/Users/ivy/Desktop/Graff_EEG_stuff/ZPrecise2_MRI_fixed_rename_FS'

#where are the averaged connectomes saved?
loaddir = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/results_august2024/avg100/'

#where are the correlation files saved?
corrfreqdf = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/results_august2024/individualfilecorrelations100/corrdf_avgs.csv'
corrfreqdf2 = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/results_august2024/individualfilecorrelations100/corrdf_avgsofindivs.csv'

#where to output files to?
savedir = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/results_lol2025probably/figures_mar2025/'


saveoutputs = False

networklabels = '/Users/ivy/Desktop/Graff_EEG_stuff/Desikankilliany/dklabels.csv'
parc = 'aparc'


#this is a number from 0-2 for the different connectivity measures. 0 plots coh + plv, 1 plots ciplv, ecso, ecpwo, 2 plots the rest
fi = 2

figbasename = 'Fig' + str(fi+1)

conmethodsx = ['coh','plv','ciplv','ecso','ecpwo','imcoh','wpli','pli','psi']
colorlistx = ['#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00']

if fi == 0:
    corrlist = conmethodsx[:2]
    ogconmethodscolor = colorlistx[:2]
if fi == 1:
    corrlist = conmethodsx[2:5]
    ogconmethodscolor = colorlistx[2:5]
if fi == 2:
    corrlist = conmethodsx[5:]
    ogconmethodscolor = colorlistx[5:]





conmethodsload = []
conmethodstitle_space = []
conmethodscolor = []

for ci in range(len(corrlist)):
    conmethod = corrlist[ci]
    conmethodsload.append(conmethod+'_nonsim_nonabs')
    conmethodsload.append(conmethod+'_sim_nonabs')
    conmethodstitle_space.append('    '+conmethod+' - real    ')
    conmethodstitle_space.append('    '+conmethod+' - simulated    ')
    conmethodscolor.append(ogconmethodscolor[ci])
    conmethodscolor.append(ogconmethodscolor[ci])



#which frequency band do we want to look at?
#fbands = [[8.0,13.0]]
fbands = [[2.5,45.0]]
#fbands = [[13.0,30.0]]




corrfreq = pd.read_csv(corrfreqdf,index_col=0)
corrfreq2 = pd.read_csv(corrfreqdf2,index_col=0)


locationlist = ['A','B','D','E','G','H','J','K','M','N']
locationlist_corr = ['C','F','I','L','O']
corrlabels = ['real to simulated\navg connectome','real to simulated\navg of each recording','distance dependence\navg connectome','distance dependence\navg of each recording']



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
labelz = list(testdf['label'])


  


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
    
    if len(corrlist) == 5:
        fig, axs = plt.subplot_mosaic("ABC;DEF;GHI;JKL;MNO",dpi=300,figsize=(16,17.5*5/4))  
    elif len(corrlist) == 4:
        fig, axs = plt.subplot_mosaic("ABC;DEF;GHI;JKL",dpi=300,figsize=(16,17.5))  
    elif len(corrlist) == 2:
        fig, axs = plt.subplot_mosaic("ABC;DEF",dpi=300,figsize=(16,17.5*2/4))  
    elif len(corrlist) == 3:
        fig, axs = plt.subplot_mosaic("ABC;DEF;GHI",dpi=300,figsize=(16,17.5*3/4))                  
        
        
    
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
        

           
        altavgdf = np.array(graphdfx) + np.identity(len(graphdfx)) 
        
        
        x = [list(x) for x in np.array(altavgdf)]
        minlist = []
        for my_list in x:
            xx = [min(x for x in my_list if x > 0.0001)]
            minlist.append(xx)
        altminvalhere = np.min(minlist)
        
        minval = np.min(graphdfx)
        maxval = np.max(graphdfx)
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
        

        cbar = fig.colorbar(cs,ax=axs[lx],fraction=0.046, pad=0.04)
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
        
        

    
    corrfreqband = corrfreq[corrfreq['fband'] == fbandstr]
    corrfreqband2 = corrfreq2[corrfreq2['fband'] == fbandstr]
    
    
    
    
    cmap = 'RdBu_r'
    
    
    for cn in range(len(corrlist)): 
        lx = locationlist_corr[cn]
        
        
        
        conmethod = corrlist[cn]
        
        subcorrfreqx = corrfreqband[corrfreqband['conmethod'] == conmethod]
        subcorrfreq = subcorrfreqx[subcorrfreqx['abs'] == 'nonabs']
        subcorrfreq_abs = subcorrfreqx[subcorrfreqx['abs'] == 'abs']
        simtoreal = subcorrfreq[subcorrfreq['comparison'] == 'sim'].iloc[0]['Spearman']
        distancedep = subcorrfreq_abs[subcorrfreq_abs['comparison'] == 'distance'].iloc[0]['Spearman']
        
        subcorrfreq2x = corrfreqband2[corrfreqband2['conmethod'] == conmethod]
        subcorrfreq2 = subcorrfreq2x[subcorrfreq2x['abs'] == 'nonabs']
        subcorrfreq2_abs = subcorrfreq2x[subcorrfreq2x['abs'] == 'abs']
        simtoreal_avgofindiv = subcorrfreq2[subcorrfreq2['comparison'] == 'sim'].iloc[0]['Spearman']
        distancedep_avgofindiv = subcorrfreq2_abs[subcorrfreq2_abs['comparison'] == 'distance'].iloc[0]['Spearman']        
        
        
        newdf = pd.DataFrame({'test':[simtoreal,simtoreal_avgofindiv,distancedep,distancedep_avgofindiv]})
        vals_og = list(newdf['test'])
        vals = [str(round(x,2)) for x in vals_og]
    
        cs4 = axs[lx].matshow(newdf,cmap=cmap,vmin=-1,vmax=1)
        
        for xn in range(len(vals)):
            valog = vals_og[xn]
            val = vals[xn]
            split = val.split('.')
            if len(split[1]) == 1:
                val = val + '0'
            if abs(valog) > 0.5:
                axs[lx].text(0, xn, val, ha='center', va='center',fontsize=16,c='white',fontweight='bold')   
            else:
                axs[lx].text(0, xn, val, ha='center', va='center',fontsize=16,c='black',fontweight='bold')   
        
        axs[lx].set_yticks(range(4))
        axs[lx].set_yticklabels(corrlabels, fontsize=12)
        axs[lx].yaxis.set_ticks_position('right')
        
        axs[lx].set_xticks([])
        axs[lx].set_xticklabels([])        
    
        axs[lx].xaxis.grid(False)     
        axs[lx].yaxis.grid(False)
        axs[lx].set_ylim(3.5,-0.5)

    
        axs[lx].tick_params(axis=u'both', which=u'both',length=0, pad=7)

 

    if len(corrlist) == 4:
        titlez = 'Minimally Vulnerable Connectivity Measures'
        titlepos = 0.95
    elif len(corrlist) == 3:
        titlez = 'Semi-Vulnerable Connectivity Measures'
        titlepos = 0.96
    elif len(corrlist) == 2:
        titlez = 'Vulnerable Connectivity Measures'
        titlepos = 0.99
        
    fig.suptitle(titlez,y=titlepos,fontsize=16)


    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
        
    if saveoutputs:
        print("Saving graph")
        
        savefolder = savedir + dataname + '/'
        if not os.path.exists(savefolder):
            os.makedirs(savefolder)
            
        #plt.subplots_adjust(top=0.1)

        plt.savefig(savefolder + figbasename + '_' + dataname + '_avgcorrmatrix_' + '-'.join(corrlist) + '.png')
    
    print("Showing graph")
    plt.show()



        
        
















#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

After running makeavg_to_plot_average_connectome, we can calculate the correlation between the average connectomes for real to sim

"""



import numpy as np
import mne
import pandas as pd
import os
import math
from scipy.stats import spearmanr
from scipy.stats import pearsonr





#folder where the averaged connectomes live
avg_dir = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/results_august2024/avg100/'

#structural data
subjects_dir = '/Users/ivy/Desktop/Graff_EEG_stuff/ZPrecise2_MRI_fixed_rename_FS'



#parcellation
parc = 'aparc'

#which frequency bands and FC measures to use
fbands = [[8.0,13.0],[13.0,30.0],[2.5,45.0]]
conmethods = ['wpli','imcoh','coh','pli','plv','psi','ciplv','ecso','ecpwo']






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


edgelen = []
for ii in range(1, len(label_names)):
    x1 = label_xpos[ii]
    y1 = label_ypos[ii]
    z1 = label_zpos[ii]
    
    for jj in range(ii):
        x2 = label_xpos[jj]
        y2 = label_ypos[jj]
        z2 = label_zpos[jj]                            
        
        xdiff = abs(x1-x2)
        ydiff = abs(y1-y2)
        zdiff = abs(z1-z2)
        
        ss = xdiff*xdiff+ydiff*ydiff+zdiff*zdiff
        sr = math.sqrt(ss)
        
        edgelen.append(sr)   





corrfband = []
corrconmethod = []
corrabs = []
corrcomparison = []
corrcomparisonspecific = []
corrcorrspearman = []
corrcorrpearson = []


veclist = []
vecnamelist = []
                            
for fband in fbands:
    fbandstr = str(fband[0]) + '-' + str(fband[1])
    fmin = fband[0]
    fmax = fband[1]
                 
    for cn in range(len(conmethods)):  
        conmethod = conmethods[cn]
        
        saveconnectome_sim_nonabs = avg_dir + 'avg_' + str(fmin) + '-' + str(fmax) + '_' + conmethod + '_sim_nonabs.csv'
        saveconnectome_nonsim_nonabs = avg_dir + 'avg_' + str(fmin) + '-' + str(fmax) + '_' + conmethod + '_nonsim_nonabs.csv'
        saveconnectome_sim_abs = avg_dir + 'avg_' + str(fmin) + '-' + str(fmax) + '_' + conmethod + '_sim_abs.csv'
        saveconnectome_nonsim_abs = avg_dir + 'avg_' + str(fmin) + '-' + str(fmax) + '_' + conmethod + '_nonsim_abs.csv'
        
        if os.path.isfile(saveconnectome_sim_nonabs):

            print("Loading " + saveconnectome_sim_nonabs) 
            parceldata1 = pd.read_csv(saveconnectome_sim_nonabs,index_col=0)            
            FCm = np.squeeze(np.asarray(parceldata1))
            #FCm = np.arctanh(FCm)

            newvec = []
            for ii in range(1, FCm.shape[0]):
                for jj in range(ii):
                    newvec.append(FCm[ii, jj])
                    
            newvec = np.asarray(newvec)
            
            
            
            veclist.append(newvec)
            vecnamelist.append(conmethod + '_' + fbandstr + '_simnonabs')   


            print("Loading " + saveconnectome_sim_abs) 
            parceldata1 = pd.read_csv(saveconnectome_sim_abs,index_col=0)            
            FCm = np.squeeze(np.asarray(parceldata1))
            #FCm = np.arctanh(FCm)

            newvec = []
            for ii in range(1, FCm.shape[0]):
                for jj in range(ii):
                    newvec.append(FCm[ii, jj])
                    
            newvec = np.asarray(newvec)
            
            veclist.append(newvec)
            vecnamelist.append(conmethod + '_' + fbandstr + '_simabs')   


            print("Loading " + saveconnectome_nonsim_nonabs) 
            parceldata1 = pd.read_csv(saveconnectome_nonsim_nonabs,index_col=0)            
            FCm = np.squeeze(np.asarray(parceldata1))
            #FCm = np.arctanh(FCm)

            newvec = []
            for ii in range(1, FCm.shape[0]):
                for jj in range(ii):
                    newvec.append(FCm[ii, jj])
                    
            newvec = np.asarray(newvec)
            
            veclist.append(newvec)
            vecnamelist.append(conmethod + '_' + fbandstr + '_realnonabs') 


            print("Loading " + saveconnectome_nonsim_abs) 
            parceldata1 = pd.read_csv(saveconnectome_nonsim_abs,index_col=0)            
            FCm = np.squeeze(np.asarray(parceldata1))
            #FCm = np.arctanh(FCm)

            newvec = []
            for ii in range(1, FCm.shape[0]):
                for jj in range(ii):
                    newvec.append(FCm[ii, jj])
                    
            newvec = np.asarray(newvec)
            
            veclist.append(newvec)
            vecnamelist.append(conmethod + '_' + fbandstr + '_realabs') 
        

                      



print("")
print("")
print("")
print("Checking comparisons for avg")
print("")
print("")
print("")
if len(veclist) > 1:
    veclist.append(np.asarray(edgelen))
    vecnamelist.append('distance')  
    
    abslist = ['abs','nonabs']
    
    for fband in fbands:
        fbandstr = str(fband[0]) + '-' + str(fband[1])
        
        fbands2 = fbands.copy()
        fbands2.remove(fband)

        for cn in range(len(conmethods)):  
            conmethod = conmethods[cn]    
            
            conmethods2 = conmethods.copy()
            conmethods2.remove(conmethod)
            
            for abstype in abslist:
                
                if abstype == 'abs':
                    otherabs = 'nonabs'
                else:
                    otherabs = 'abs'
                    
            
                vecname1 = conmethod + '_' + fbandstr + '_real' + abstype
                indexval1 = vecnamelist.index(vecname1)
                vec1 = veclist[indexval1]
                
            
            
            
            
                vecname2 = 'distance'
                indexval2 = vecnamelist.index(vecname2)
                vec2 = veclist[indexval2]
                
                
                nas = np.logical_or(np.logical_or(np.isinf(vec1),np.isinf(vec2)),np.logical_or(np.isnan(vec1),np.isnan(vec2)))
                pcorr = pearsonr(vec1[~nas],vec2[~nas])[0]
                scorr = spearmanr(vec1[~nas],vec2[~nas])[0]
                
                
                corrfband.append(fbandstr)
                corrconmethod.append(conmethod)
                corrabs.append(abstype)
                corrcomparison.append('distance')
                corrcorrpearson.append(pcorr)
                corrcorrspearman.append(scorr)
                corrcomparisonspecific.append('distance')
                


                vecname2 = conmethod + '_' + fbandstr + '_sim' + abstype
                indexval2 = vecnamelist.index(vecname2)
                vec2 = veclist[indexval2]
                
                
                nas = np.logical_or(np.logical_or(np.isinf(vec1),np.isinf(vec2)),np.logical_or(np.isnan(vec1),np.isnan(vec2)))
                pcorr = pearsonr(vec1[~nas],vec2[~nas])[0]
                scorr = spearmanr(vec1[~nas],vec2[~nas])[0]
                
                

                corrfband.append(fbandstr)
                corrconmethod.append(conmethod)
                corrabs.append(abstype)
                corrcomparison.append('sim')
                corrcorrpearson.append(pcorr)
                corrcorrspearman.append(scorr)
                corrcomparisonspecific.append('sim')
                
                
                
                vecname2 = conmethod + '_' + fbandstr + '_real' + otherabs
                indexval2 = vecnamelist.index(vecname2)
                vec2 = veclist[indexval2]
                
                
                nas = np.logical_or(np.logical_or(np.isinf(vec1),np.isinf(vec2)),np.logical_or(np.isnan(vec1),np.isnan(vec2)))
                pcorr = pearsonr(vec1[~nas],vec2[~nas])[0]
                scorr = spearmanr(vec1[~nas],vec2[~nas])[0]
                
                
                corrfband.append(fbandstr)
                corrconmethod.append(conmethod)
                corrabs.append(abstype)
                corrcomparison.append('abs_comp')
                corrcorrpearson.append(pcorr)
                corrcorrspearman.append(scorr)    
                corrcomparisonspecific.append(otherabs)
                


                for conmethod2 in conmethods2:
                    
                    for abstype2 in abslist:
                    
                        vecname2 = conmethod2 + '_' + fbandstr + '_real' + abstype2
                        indexval2 = vecnamelist.index(vecname2)
                        vec2 = veclist[indexval2]
                        
                        
                        nas = np.logical_or(np.logical_or(np.isinf(vec1),np.isinf(vec2)),np.logical_or(np.isnan(vec1),np.isnan(vec2)))
                        pcorr = pearsonr(vec1[~nas],vec2[~nas])[0]
                        scorr = spearmanr(vec1[~nas],vec2[~nas])[0]
                        
                        
                        corrfband.append(fbandstr)
                        corrconmethod.append(conmethod)
                        corrabs.append(abstype)
                        corrcomparison.append('conmethod')
                        corrcorrpearson.append(pcorr)
                        corrcorrspearman.append(scorr)      
                        corrcomparisonspecific.append(conmethod2+'_'+abstype2)




                for fband2 in fbands2:
                    fbandstr2 = str(fband2[0]) + '-' + str(fband2[1])
                    vecname2 = conmethod + '_' + fbandstr2 + '_real' + abstype
                    indexval2 = vecnamelist.index(vecname2)
                    vec2 = veclist[indexval2]
                    
                    
                    nas = np.logical_or(np.logical_or(np.isinf(vec1),np.isinf(vec2)),np.logical_or(np.isnan(vec1),np.isnan(vec2)))
                    pcorr = pearsonr(vec1[~nas],vec2[~nas])[0]
                    scorr = spearmanr(vec1[~nas],vec2[~nas])[0]
                    
                    

                    corrfband.append(fbandstr)
                    corrconmethod.append(conmethod)
                    corrabs.append(abstype)
                    corrcomparison.append('fband')
                    corrcorrpearson.append(pcorr)
                    corrcorrspearman.append(scorr)  
                    corrcomparisonspecific.append(fbandstr2)








resultdf = pd.DataFrame({'fband':corrfband,
                         'conmethod':corrconmethod,
                         'abs':corrabs,
                         'comparison':corrcomparison,
                         'compspecific':corrcomparisonspecific,
                         'Pearson':corrcorrpearson,
                         'Spearman':corrcorrspearman
                         })

resultdf.to_csv('/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/results_august2024/individualfilecorrelations100/corrdf_avgs.csv')
























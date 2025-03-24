

#this program calculates the correlation in t values between the ses12 t values and the ses34 t values, to see if the same
#edges show age effects


import pandas as pd
from scipy.stats import pearsonr
#import os
#import numpy as np


#where are the t values saved
taskfolder = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/results_lol2025probably/parentvchild_ttest_timesubset/'

#where to output the data
outputfolder = '/Users/ivy/Desktop/Graff_EEG_stuff/precise_KIDS_final/results_lol2025probably/splithalf/'


#which frequency bands and FC measures to use
fbands = [[8.0,13.0],[13.0,30.0],[2.5,45.0]]
conmethods = ['coh','plv','imcoh','ciplv','pli','wpli','psi','ecpwo','ecso']




subsections = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,20,25,30,35,40,45,50,60,70,80,90,100,110,120,130,140,150]



fbandlist = []
conmethodlist = []
subsectionlist = []
corrlist = []


for timesubx in subsections:
    epochs = int(timesubx*5)
    for fband in fbands:
        fbandstr = str(fband[0]) + '-' + str(fband[1])
        for conmethod in conmethods:    
            fmin = fband[0]
            fmax = fband[1]
            
            print("Checking",fband,conmethod,epochs,'epochs')
            
            file12 = taskfolder + 'aget_' + conmethod + '_' + fbandstr + '_' + str(epochs) + 'e12.csv'
            file34 = taskfolder + 'aget_' + conmethod + '_' + fbandstr + '_' + str(epochs) + 'e34.csv'
            
            t12 = pd.read_csv(file12,index_col=0)
            t34 = pd.read_csv(file34,index_col=0)
    
            corr = pearsonr(t12['tval'],t34['tval'])[0]
            #corr = np.arctanh(corr)
            corrlist.append(corr)

            fbandlist.append(fbandstr)
            conmethodlist.append(conmethod)
            subsectionlist.append(epochs)            
                    
    
resultdf = pd.DataFrame({'fband':fbandlist,'conmethod':conmethodlist,'epochs':subsectionlist,'corr':corrlist})
resultdf = resultdf.sort_values(by=['fband','conmethod','epochs'])                
    
print(resultdf)                   
 
           
resultdf.to_csv(outputfolder+'frontvbackage_nov.csv')   





















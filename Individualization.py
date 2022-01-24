"""

This program calculates individualization stats for young children
See Graff et al 2022


Modify the code near the top (up to line 150), choose what results you want to calculate, then hopefully it'll run!


This program assumes you have
-A dataframe containing the age of each participant at time of scan
-A folder containing a file for each participant that lists their mean FD. Your preprocessing pipeline should generate these
-A folder containing a csv for each participant of their parcellated time courses
-MIST_PARCEL_ORDER.csv, or some equivalent csv file that tells you what network each parcel belongs to

Your data should contain exactly two scans per participant. Designed for data collected 1ish year apart, but might still work otherwise

Made by Kirk Graff
kirk.graff@ucalgary.ca

Please email me if you have any questions :)
I'm a mostly self-taught programmer so apologies if something is coded oddly!


"""



import time
import random
import statsmodels.api as sm
from scipy.stats.stats import pearsonr
import csv
import pandas as pd
import numpy as np
import os
import operator as op
from functools import reduce



#number of timepoints you want to use, to match scan length after censoring
#you can set it to 'all' if you don't want to match scan length
scanlength = 273
#number of nodes your parcellation has
numparcels = 1095
#how many networks are you interested in?
mistofinterest = 12

#semi-optional, depending what you're running. Do you want to calculate stats for internetwork edges? Do you want to work with split half data?
#(you don't need separate csv files for split half data. This program will make them based off of the parcellated files you have)
includeinternetwork = True
loadsplithalfdata = True



#folder where all parcellated time courses are stored
dir_start = '/Users/ivy/Desktop/Current Data Individualization/54BCensorGSR_1095/' #1095

#which participant files do you want to load? I've been working with 73 participants, each scanned twice, for 146 files
#these are loaded out of dir_start
participants = list(range(-146,0))








#what network does each parcel belong to?
hierarchyfile = '/Users/ivy/Desktop/Graff_fMRI_stuff/Release/Hierarchy/MIST_PARCEL_ORDER.csv'


#where things are outputted
baseoutputfolder = '/Users/ivy/Desktop/Current Results Individualization 3/new summary data/'

#where random numbers are saved
baserandomfolder = '/Volumes/June_2020_Graff/RandomNumbersIndiv3/'
randomfolder = 'randomlists/'


#how many random iterations do you want to generate numbers for
numrandlists = 1000

#how many random numbers do you want to actually use
numrandliststouse = 1000

#how many parcels per random iteration
numrandparcels = 36

#folder where motion info is stored 
motioninfo = '/Users/ivy/Desktop/Misc_Graff_Things/Old Data Pre Error Caught/indivfiles6/'
#name of files in the motion info folder
motionfilename = 'task-movie_boldMcf.nii.gz_rel_mean.rms'

#df where participants' age is stored
agedfloc = '/Users/ivy/Desktop/Misc_Graff_Things/QCStuff/agedfplus.csv'



#array where matrices are saved. This is outputted by program
arraydatalistname = '/Users/ivy/Desktop/Current Results Individualization 3/arraydata'

#regenerate array even if it already exists?
replacer = False





#this program does a number of different individualization calculations that can be run more or less independently
#pick what outputs you want this program to spit out, or put all these things into the resulttype list


resulttype = [
              'makerandomnumstype2','makerandomnumstype3','makenetworkmatchrandtype2','makenetworkmatchrandtype3','loadnetworkmatchrand',
              'networkmatchstats',
              'networkage',
              'networkagerand',
              'networkchangestats',
              'networkageed',
              'networkmatchstatssplithalf',
              'splithalfage',
              'networkage2',
              ]


#makerandomnumstype2 = randomly pick x # of parcels for each network, sampled y # of times
#makerandomnumstype3 = randomly pick x #/2 of parcels for each pair of networks, sampled y # of times. Used for internetwork analyses
#makenetworkmatchrandtype2 = actually do the individualization calculations on the random subsets
#makenetworkmatchrandtype3 = actually do the individualization calculations on the random subsets
#loadnetworkmatchrand = go through all the random subsets of data generated in previous steps, and summarize them in smaller df (instead of having 1000s of dfs)

#networkmatchstats = stats for whole networks
#networkage = age stats for whole networks. networkmatchstats must be run first
#networkagerand = age stats for random subsets. Loadnetworkmatchrand must be run first
#networkchangestats = calculate mean change in edge strength across two scans from same participant. And some other calculations
#networkageed = age stats for networkchangestats
#networkmatchstatssplithalf = individualization stats for split half data
#splithalfage = age effects for split half correlations
#networkage2 = similarity calculated using a MEM that compares all pairs of scans








#if your data is arranged properly, nothing below here should need to be changed


#read in agedf
agedf = pd.read_csv(agedfloc,index_col=0)

#read in hierarchy data, to know which network each parcel belongs to
hdf = pd.read_csv(hierarchyfile)
hdf = hdf.rename(columns={'sATOM': 's1095'})



totaltimer = time.time()




#this calculates match rate, correlation to self, correlation to others, and self minus others
def fpfaster(FCallnames,parcelcolumns,parcelrows,edgeslist,shortidlist,personnumlist):

    FCallvec = []
    comppearson = []
    noncomppearson = []
    meannoncomppearson = []
    pearsonmatch = []
    pearsuccess = []
    pearsuccessmean = []            

    numscans = len(FCallnames)

    #loop through all scans, saving vectorized data to a list
    for num in range(numscans):
        FCm = FCallnames[num]
        FCmsub = FCm[parcelcolumns].loc[parcelrows]
        
        FCmsub = np.squeeze(np.asarray(FCmsub))

        if parcelcolumns == parcelrows:
            
            tri = np.tril(FCmsub, -1)
        
            vec = []
            for ii in range(1, tri.shape[0]):
                for jj in range(ii):
                    vec.append(tri[ii, jj])
              
            if edgeslist == 'all':
                FCallvec.append(np.asarray(vec))
            
            else:
                FCallvec.append(np.asarray([vec[inde] for inde in edgeslist]))
            
        else:
            
            vec = []
            for ii in range(0, FCmsub.shape[0]):
                for jj in range(0, FCmsub.shape[1]):
                    vec.append(FCmsub[ii, jj])
                    
            if edgeslist == 'all':
                FCallvec.append(np.asarray(vec))
            
            else:
                FCallvec.append(np.asarray([vec[inde] for inde in edgeslist]))
            
            
    numedges = len(FCallvec[0])
    
    #for each scan, calculate correlation to self and to others
    for i in range(len(shortidlist)):
        person1 = personnumlist[i]
        otherpearson = []
        
        
        FC1vec = FCallvec[i]
        
        for l in range(len(shortidlist)):
            if i != l:  
                
                person2 = personnumlist[l]
    
                FC2vec = FCallvec[l]          
                
                corre = pearsonr(FC1vec,FC2vec)
                
                if person1 == person2:
                    comppearson.append(np.arctanh(corre[0]))                    
                else:
                    otherpearson.append(np.arctanh(corre[0]))
                       
        noncomppearson.append(max(otherpearson))
        meannoncomppearson.append(np.mean(otherpearson))
                       
         
    for i in range(len(shortidlist)):
        psucc = comppearson[i] - noncomppearson[i]
    
        psuccmean = comppearson[i] - meannoncomppearson[i]
    
        pearsuccess.append(psucc)
    
        pearsuccessmean.append(psuccmean)
    
        
        if comppearson[i] > noncomppearson[i]:
            pearsonmatch.append(1)
        else:
            pearsonmatch.append(0)
                

    #create df of output
    summarydf = pd.DataFrame({'ID':shortidlist,'stability':comppearson,'nearest neighbor':noncomppearson,'stab minus nn':pearsuccess,'matchtotal':pearsonmatch,'mean similarity':meannoncomppearson,'stab minus sim':pearsuccessmean}) 
    summarydf['ses'] = summarydf['ID'].astype(str).str[4:]

    return summarydf,numedges;        



#similar to fpfaster, but with split-half correlations
def fpfastersplithalf(FCallnamessplit1,FCallnamessplit2,parcelcolumns,parcelrows,edgeslist,shortidlist,personnumlist):

    FCallvechalf1 = []
    FCallvechalf2 = []
    
    splitpearson = []
    comppearson = []
    noncomppearson = []
    meannoncomppearson = []
    pearsonmatch = []
    pearsuccess = []
    pearsuccessmean = []            

    numscans = len(FCallnamessplit1)

    for num in range(numscans):
        #print(num)
        FCm = FCallnamessplit1[num]
        FCmsub = FCm[parcelcolumns].loc[parcelrows]
        #print(FCmsub)
        
        FCmsub = np.squeeze(np.asarray(FCmsub))

        if parcelcolumns == parcelrows:
            #print("TESTING")
            
            tri = np.tril(FCmsub, -1)
        
            vec = []
            for ii in range(1, tri.shape[0]):
                for jj in range(ii):
                    vec.append(tri[ii, jj])
              
            if edgeslist == 'all':
                FCallvechalf1.append(np.asarray(vec))
            
            else:
                FCallvechalf1.append(np.asarray([vec[inde] for inde in edgeslist]))
            
        else:
            
            vec = []
            for ii in range(0, FCmsub.shape[0]):
                for jj in range(0, FCmsub.shape[1]):
                    vec.append(FCmsub[ii, jj])
                    
            if edgeslist == 'all':
                FCallvechalf1.append(np.asarray(vec))
            
            else:
                FCallvechalf1.append(np.asarray([vec[inde] for inde in edgeslist]))
            


    for num in range(numscans):
        #print(num)
        FCm = FCallnamessplit2[num]
        FCmsub = FCm[parcelcolumns].loc[parcelrows]
        #print(FCmsub)
        
        FCmsub = np.squeeze(np.asarray(FCmsub))

        if parcelcolumns == parcelrows:
            #print("TESTING")
            
            tri = np.tril(FCmsub, -1)
        
            vec = []
            for ii in range(1, tri.shape[0]):
                for jj in range(ii):
                    vec.append(tri[ii, jj])
              
            if edgeslist == 'all':
                FCallvechalf2.append(np.asarray(vec))
            
            else:
                FCallvechalf2.append(np.asarray([vec[inde] for inde in edgeslist]))
            
        else:
            
            vec = []
            for ii in range(0, FCmsub.shape[0]):
                for jj in range(0, FCmsub.shape[1]):
                    vec.append(FCmsub[ii, jj])
                    
            if edgeslist == 'all':
                FCallvechalf2.append(np.asarray(vec))
            
            else:
                FCallvechalf2.append(np.asarray([vec[inde] for inde in edgeslist]))

         
    numedges = len(FCallvechalf1[0])

    
    for i in range(len(shortidlist)):
        person1 = personnumlist[i]
        otherpearson = []
        
        
        FC1vechalf1 = FCallvechalf1[i]
        FC1vechalf2 = FCallvechalf2[i]        
        
        corre = pearsonr(FC1vechalf1,FC1vechalf2)

        splitpearson.append(np.arctanh(corre[0]))
        
        for l in range(len(shortidlist)):
            if i != l:  
                
                person2 = personnumlist[l]
    
                FC2vechalf1 = FCallvechalf1[l]
                FC2vechalf2 = FCallvechalf2[l]                
                          
                #two scans per participant, each divided into two halves, gives 4 potential correlations
                corre1 = pearsonr(FC1vechalf1,FC2vechalf1)
                corre2 = pearsonr(FC1vechalf1,FC2vechalf2)
                corre3 = pearsonr(FC1vechalf2,FC2vechalf1)
                corre4 = pearsonr(FC1vechalf2,FC2vechalf2)
                
                corre1 = np.arctanh(corre1[0])
                corre2 = np.arctanh(corre2[0])
                corre3 = np.arctanh(corre3[0])
                corre4 = np.arctanh(corre4[0])   
                
                correavg = (corre1+corre2+corre3+corre4)/4
                
                if person1 == person2:
                    comppearson.append(correavg)                    
                else:
                    otherpearson.append(correavg)
                       
        noncomppearson.append(max(otherpearson))
        meannoncomppearson.append(np.mean(otherpearson))
                       
         
    for i in range(len(shortidlist)):
        psucc = comppearson[i] - noncomppearson[i]
    
        psuccmean = comppearson[i] - meannoncomppearson[i]
    
        pearsuccess.append(psucc)
    
        pearsuccessmean.append(psuccmean)

      
        if (splitpearson[i] > noncomppearson[i]) & (splitpearson[i] > comppearson[i]) :
            pearsonmatch.append(1)
        else:
            pearsonmatch.append(0)
            


    
    summarydf = pd.DataFrame({'ID':shortidlist,'splithalf':splitpearson,'stability':comppearson,'nearest neighbor':noncomppearson,'stab minus nn':pearsuccess,'matchtotal':pearsonmatch,'mean similarity':meannoncomppearson,'stab minus sim':pearsuccessmean}) 
    summarydf['ses'] = summarydf['ID'].astype(str).str[4:]

    return summarydf,numedges;  




#calculate age associations with a metric of interest
def ageeffects(summarydf,columnofinterest):
    subsummarydf0 = summarydf.loc[summarydf['ses'] == 'ses-0'].copy()
    subsummarydf12 = summarydf.loc[summarydf['ses'] == 'ses-12'].copy()
    sublist0 = list(subsummarydf0[columnofinterest])
    sublist12 = list(subsummarydf12[columnofinterest])
    dataindiv = np.array([sublist0,sublist12])
    dataavg = np.average(dataindiv, axis=0)
    
    indep = pd.DataFrame({'Score':list(dataavg)})
    indepz = (indep['Score'] - indep['Score'].mean())/indep['Score'].std(ddof=0)

    #create the model. Predict y (the time series) as a function of X (all the nuisance regressors)
    model = sm.OLS(indep,regdf).fit()
    ageparam = model.params['avgage']
    ageparamlow = model.conf_int(alpha=0.05, cols=None)[0]['avgage']
    ageparamhigh = model.conf_int(alpha=0.05, cols=None)[1]['avgage']
    
    agepvalue = model.pvalues['avgage']

    #model with standardized data
    model = sm.OLS(indepz,regdf).fit()
    ageparamz = model.params['avgage']
    ageparamzlow = model.conf_int(alpha=0.05, cols=None)[0]['avgage']
    ageparamzhigh = model.conf_int(alpha=0.05, cols=None)[1]['avgage']

    
    r2_w_age = model.rsquared
         
    #model without age to calculate cohen's f2
    model = sm.OLS(indep,regdf2).fit()  
    r2_wo_age = model.rsquared
    f2 = (r2_w_age - r2_wo_age)/(1-r2_w_age)
    
    return [agepvalue,f2,ageparam,ageparamlow,ageparamhigh,ageparamz,ageparamzlow,ageparamzhigh];


#calculate edge stats, e.g. mean change between two sessions
def changestatsfaster(FCallnames,parcelcolumns,parcelrows,edgeslist,shortidlist,personnumlist):

    FCallvec = []    
    diffbypersonlist = []
    stdlist = []
    diffstdlist = []
    meanstrlist = []
           

    numscans = len(FCallnames)

    for num in range(numscans):
        FCm = FCallnames[num]
        FCmsub = FCm[parcelcolumns].loc[parcelrows]
        
        FCmsub = np.squeeze(np.asarray(FCmsub))

        #vectorize edges
        if parcelcolumns == parcelrows:
            
            tri = np.tril(FCmsub, -1)
        
            vec = []
            for ii in range(1, tri.shape[0]):
                for jj in range(ii):
                    vec.append(tri[ii, jj])
              
            if edgeslist == 'all':
                FCallvec.append(np.asarray(vec))
            
            else:
                FCallvec.append(np.asarray([vec[inde] for inde in edgeslist]))
            
        else:
            
            vec = []
            for ii in range(0, FCmsub.shape[0]):
                for jj in range(0, FCmsub.shape[1]):
                    vec.append(FCmsub[ii, jj])
                    
            if edgeslist == 'all':
                FCallvec.append(np.asarray(vec))
            
            else:
                FCallvec.append(np.asarray([vec[inde] for inde in edgeslist]))
            
       
    numedges = len(FCallvec[0])
    
    #calculate mean difference, std of difference, mean edge strength, and std of edge strength
    for i in range(len(shortidlist)):
        person1 = personnumlist[i]            
        FC1vec = FCallvec[i]
        
        for l in range(len(shortidlist)):
            if i != l:  
                
                person2 = personnumlist[l]
                FC2vec = FCallvec[l]          
                                
                if person1 == person2:
                    
                    difflist = abs(FC1vec - FC2vec)
                    meandiff = np.mean(difflist)
                    diffbypersonlist.append(meandiff)
                    
                    diffstd = np.std(difflist)
                    diffstdlist.append(diffstd)
                    
                    std0 = np.std(FC1vec)       
                    stdlist.append(std0)
                    
                    meanstr = np.mean(FC1vec)
                    meanstrlist.append(meanstr)
                       

    
    summarydf = pd.DataFrame({'ID':shortidlist,'meandiff':diffbypersonlist,'stddiff':diffstdlist,'edgestd':stdlist,'meanedge':meanstrlist}) 
    summarydf['ses'] = summarydf['ID'].astype(str).str[4:]

    return summarydf,numedges;   


#calculate similarity with mem that compares every pair of participants
def similaritymem(FCallnames,parcelcolumns,parcelrows,edgeslist,shortidlist,personnumlist):

    FCallvec = []       

    numscans = len(FCallnames)

    print("Vectorizing")
    for num in range(numscans):
        FCm = FCallnames[num]
        FCmsub = FCm[parcelcolumns].loc[parcelrows]
        
        FCmsub = np.squeeze(np.asarray(FCmsub))

        if parcelcolumns == parcelrows:
            
            tri = np.tril(FCmsub, -1)
        
            vec = []
            for ii in range(1, tri.shape[0]):
                for jj in range(ii):
                    vec.append(tri[ii, jj])
              
            if edgeslist == 'all':
                FCallvec.append(np.asarray(vec))
            
            else:
                FCallvec.append(np.asarray([vec[inde] for inde in edgeslist]))
            
        else:
            
            vec = []
            for ii in range(0, FCmsub.shape[0]):
                for jj in range(0, FCmsub.shape[1]):
                    vec.append(FCmsub[ii, jj])
                    
            if edgeslist == 'all':
                FCallvec.append(np.asarray(vec))
            
            else:
                FCallvec.append(np.asarray([vec[inde] for inde in edgeslist]))
            

    print("Generating correlations")            
    
    corrtootherslists = []
    for i in range(len(shortidlist)):
        person1 = personnumlist[i]
        otherpearson = []
        
        
        FC1vec = FCallvec[i]
        
        for l in range(len(shortidlist)):
                
            person2 = personnumlist[l]

            if person1 == person2:
                otherpearson.append(0)                    
            else:

                FC2vec = FCallvec[l]          
                
                corre = pearsonr(FC1vec,FC2vec)
                otherpearson.append(np.arctanh(corre[0]))
        
                       
        corrtootherslists.append(otherpearson)

    corrtodf = pd.DataFrame(data=corrtootherslists)

    corrtodf.columns = list(persondf['ID'])
    corrtodf.index = list(persondf['ID'])    
                       
         
    person1list = []
    person2list = []
    pairsex = []
    pairavgmotion = []
    pairavgage = []
    pairagediff = []
    
    zagelist = list(persondf['age'])
    zavgmotion = list(persondf['fd'])
    
    #for each pair of scans, calculate sex of pair, avg motion of pair, avg age of pair, age diff of pair
    for ii in range(146):
        age1 = zagelist[ii]
        motion1 = zavgmotion[ii]
        pers1 = personnumlist[ii]
        for jj in range(146):
            age2 = zagelist[jj]
            motion2 = zavgmotion[jj]
            pers2 = personnumlist[jj]
            
            person1list.append(pers1)
            person2list.append(pers2)
            
           
            if pers1[0] == '0':
                if pers2[0] == '0':
                    pairsex.append('FF')
                else:
                    pairsex.append('FM')
            elif pers2[0] == '0':
                pairsex.append('FM')
            else:
                pairsex.append('MM')
                                    
            ageavg = age1/2+age2/2
            pairavgage.append(ageavg)
            
            agediff = abs(age1-age2)
            pairagediff.append(agediff)
            
            pairavgmotion.append(motion1/2+motion2/2)


    df_stack = corrtodf.stack().reset_index()
    
    #rename the columns
    df_stack.columns = ['Scan 1', 'Scan 2', 'Corr']
    
    df_stack['Corr_z'] = (df_stack['Corr'] - df_stack['Corr'].mean())/df_stack['Corr'].std(ddof=0)
    
   
    df_stack['person1'] = person1list
    df_stack['person2'] = person2list
    df_stack['sex'] = pairsex
    df_stack['avgmotion'] = pairavgmotion
    df_stack['avgage'] = pairavgage
    df_stack['agediff'] = pairagediff
    
    
    #drop pairs that are duplicates or correlation to self
    keepdrop = []
    for ii in range(146):
        for jj in range(146):
            if ii >= jj:
                keepdrop.append(0)
            else:
                keepdrop.append(1)
    
    keepdrop = [i for i, x in enumerate(keepdrop) if x == 1]

    df_stack_short = df_stack.iloc[keepdrop]
    
    #the correlation code above artifically set correlations from the same participant to be equal to 0
    #in theory your results will be messed up if two scans have anti-correlated FC estimates. If that happens, your data quality is weird!
    #or something else weird is up. Scans just aren't that dissimilar in my experience
    df_stack_short = df_stack_short[df_stack_short['Corr'] > 0]
    

    #generate age effects on similarity
    df = df_stack_short.copy()                                                                                                                                                
    df["group"] = 1                                                                                                            
                                                                                                                               
    vcf = {"person1": "0 + C(person1)", "person2": "0 + C(person2)"}                                                         
    model = sm.MixedLM.from_formula("Corr ~ avgage + agediff + avgmotion + sex", groups="group",vc_formula=vcf, re_formula="0", data=df)                                                   
    result = model.fit()  
    
    avgagepvalue = result.pvalues['avgage']    
    avgageparam = result.params['avgage']
    
    agediffpvalue = result.pvalues['agediff']    
    agediffparam = result.params['agediff']    

    avgageparamlow = result.conf_int(alpha=0.05, cols=None)[0]['avgage']
    avgageparamhigh = result.conf_int(alpha=0.05, cols=None)[1]['avgage']  
    
    agediffparamlow = result.conf_int(alpha=0.05, cols=None)[0]['agediff']
    agediffparamhigh = result.conf_int(alpha=0.05, cols=None)[1]['agediff']      


    model = sm.MixedLM.from_formula("Corr_z ~ avgage + agediff + avgmotion + sex", groups="group",vc_formula=vcf, re_formula="0", data=df)                                                   
    result = model.fit()  
    
    avgagepvaluez = result.pvalues['avgage']    
    avgageparamz = result.params['avgage']
    
    agediffpvaluez = result.pvalues['agediff']    
    agediffparamz = result.params['agediff']    

    avgageparamlowz = result.conf_int(alpha=0.05, cols=None)[0]['avgage']
    avgageparamhighz = result.conf_int(alpha=0.05, cols=None)[1]['avgage']  
    
    agediffparamlowz = result.conf_int(alpha=0.05, cols=None)[0]['agediff']
    agediffparamhighz = result.conf_int(alpha=0.05, cols=None)[1]['agediff'] 



    return [avgageparam,avgagepvalue,agediffparam,agediffpvalue,avgageparamlow,avgageparamhigh,agediffparamlow,agediffparamhigh,
            avgageparamz,avgagepvaluez,agediffparamz,agediffpvaluez,avgageparamlowz,avgageparamhighz,agediffparamlowz,agediffparamhighz];     





participant_files = os.listdir(dir_start)


#get parcel names
parcels = list(range(1,numparcels+1))
networks7 = []
networks12 = []

parcelnames = []
for parcel in parcels:
    curname = 'parcel' + str(parcel)
    parcelnames.append(curname)


#for each parcel, search it in hierarchy data and find its network
for parce in parcels:
    x = hdf.loc[hdf['s'+str(numparcels)] == parce]['s7'].iloc[0]
    networks7.append(x)
    x = hdf.loc[hdf['s'+str(numparcels)] == parce]['s12'].iloc[0]
    networks12.append(x)    
    
    
#create dataframe of parcels and their networks, their location, and their neighbours
parcelinfodf = pd.DataFrame({'parcel':parcelnames,'network7':networks7,'network12':networks12})


idlist = []
shortidlist = []
scannumlist = []
scanseslist = []
agelist = []
avgmotion = []
compidlist = []
avgmotioncomp = []
agecomplist = []
sex = []
personnumlist = []


#get info for each participant
for i in participants:
    fileid1 = participant_files[i]
    #parcellationfile1 = dir_start + fileid1
    idparts = fileid1.split('_')
    person1 = idparts[0]
    personnum1 = person1[-3:]
    j1 = idparts[1]
    if j1 == 'ses-0':
        j2 = 'ses-12'
    else:
        j2 = 'ses-0'
    if personnum1[0] == '0':
        sex.append(0)
    else:
        sex.append(1)
    
    personnumlist.append(personnum1)
    
    personid1 = person1 + '_' + j1
    shortpersonid1 = personnum1 + '_' + j1
    personid2 = person1 + '_' + j2
    idlist.append(personid1)
    shortidlist.append(shortpersonid1)
    scannumlist.append(person1)
    scanseslist.append(j1)
    compidlist.append(personid2)

for identity in idlist:
    age = float(agedf[agedf['scan'] == identity]['age'])
    
    
    agelist.append(age)
    avgmotionfile = motioninfo + identity + '_' + motionfilename
    with open(avgmotionfile) as file:
        for line in file:
            avgmotion.append(float(line))

for identity in compidlist:
    age = float(agedf[agedf['scan'] == identity]['age'])
    agecomplist.append(age)
    avgmotionfile = motioninfo + identity + '_' + motionfilename
    with open(avgmotionfile) as file:
        for line in file:
            avgmotioncomp.append(float(line))
    
    
#create df of participants' characteristics
persondf = pd.DataFrame({'ID':shortidlist,'sex':sex,'person':personnumlist,'ses':scanseslist,'age':agelist,'fd':avgmotion,'agecomp':agecomplist,'fdcomp':avgmotioncomp})
persondf['avgage'] = persondf['age']/2 + persondf['agecomp']/2
persondf['agediff'] = persondf['agecomp']-persondf['age']
persondf['avgavgmot'] = persondf['fd']/2 + persondf['fdcomp']/2


#create df for only ses-0 data
mdf = persondf.loc[persondf['ses'] == 'ses-0'].copy()
mdf = mdf.reset_index(drop=True)

#create df used for linear regression
regdf = mdf[['avgavgmot','agediff','avgage','sex']]
regdf = sm.add_constant(regdf)

#df without age, for calculating cohen's f2
regdf2 = mdf[['avgavgmot','agediff','sex']]
regdf2 = sm.add_constant(regdf2)

#standardized regression df
regdfz = regdf.copy()
regdfz['avgavgmot'] = (regdfz['avgavgmot'] - regdfz['avgavgmot'].mean())/regdfz['avgavgmot'].std(ddof=0)
regdfz['agediff'] = (regdfz['agediff'] - regdfz['agediff'].mean())/regdfz['agediff'].std(ddof=0)
regdfz['avgage'] = (regdfz['avgage'] - regdfz['avgage'].mean())/regdfz['avgage'].std(ddof=0)

#standardized regression df without age
regdf2z = regdf2.copy()
regdf2z['avgavgmot'] = (regdf2z['avgavgmot'] - regdf2z['avgavgmot'].mean())/regdf2z['avgavgmot'].std(ddof=0)
regdf2z['agediff'] = (regdf2z['agediff'] - regdf2z['agediff'].mean())/regdf2z['agediff'].std(ddof=0)



shortidlist = list(persondf['ID'])
personnumlist = list(persondf['person'])



idlist = []

FCall = []
FCallsplit1 = []
FCallsplit2 = []



arraydatalist = arraydatalistname + '_' + str(numparcels) + 'parcels_' + str(scanlength) + 'time.npz'

arraydatalistsplit1 = arraydatalistname + '_' + str(numparcels) + 'parcels_' + str(scanlength) + 'time_half1.npz'
arraydatalistsplit2 = arraydatalistname + '_' + str(numparcels) + 'parcels_' + str(scanlength) + 'time_half2.npz'


doit = True
if replacer == False:
    if os.path.isfile(arraydatalist) == True:
        doit = False

#save all parcellation csv files into an array, if they don't already exist
if doit == True:      
    print("Starting creating matrices and stuff")
    for i in participants:
        fileid1 = participant_files[i]
        print("Generating for " + fileid1)
        
        idparts = fileid1.split('_')
        person1 = idparts[0]
        personnum1 = person1[-3:]
        j1 = idparts[1]
        personid1 = personnum1 + '_' + j1     
    
        parcellationfile1 = dir_start + fileid1
        parceldata1 = pd.read_csv(parcellationfile1, index_col=0)
        
        subdoit = True
        
        if scanlength == 273:
            subparceldata1 = parceldata1[0:273]
        elif scanlength == 'all':
            subparceldata1 = parceldata1
        else:
            print("Your scan length settings are messed up.")
            subdoit = False
    
        if subdoit:

            idlist.append(personid1)   
            
            FCm = subparceldata1.corr()
            FCm = np.squeeze(np.asarray(FCm))
            FCm = FCm - np.identity(len(FCm))
        
            
            FCm = np.arctanh(FCm)
            FCall.append(FCm)   

   
    np.savez(arraydatalist,FCall)


#load parcellated data if it already exists              
else:
    print("Loading matrices")
    FCallload = np.load(arraydatalist)
    FCall = [FC for FC in FCallload['arr_0']]


if loadsplithalfdata:

    doit = True
    if replacer == False:
        if os.path.isfile(arraydatalistsplit1) == True:
            if os.path.isfile(arraydatalistsplit2) == True:
                doit = False

    #save split half data into an array if it doesn't already exist
    if doit == True:      
        print("Starting creating split half matrices and stuff")
        for i in participants:
            fileid1 = participant_files[i]
            print("Generating for " + fileid1)
            
            idparts = fileid1.split('_')
            person1 = idparts[0]
            personnum1 = person1[-3:]
            j1 = idparts[1]
            personid1 = personnum1 + '_' + j1     
        
            parcellationfile1 = dir_start + fileid1
            parceldata1 = pd.read_csv(parcellationfile1, index_col=0)
            
            subdoit = True
            
            if scanlength == 273:
                subparceldata1of2 = parceldata1[0:136]
                subparceldata2of2 = parceldata1[136:272]
                
            elif scanlength == 'all':
                
                scanlengthhere = len(parceldata1)
                subparceldata1of2 = parceldata1[0:int(scanlengthhere/2)] 
                subparceldata2of2 = parceldata1[int(scanlengthhere/2):] 
            else:
                print("Your scan length settings are messed up.")
                subdoit = False
        
            if subdoit:
    
                idlist.append(personid1)   
                
                FCm = subparceldata1of2.corr()
                FCm = np.squeeze(np.asarray(FCm))
                FCm = FCm - np.identity(len(FCm))
            
                FCm = np.arctanh(FCm)
                FCallsplit1.append(FCm)   
                
                
                FCm = subparceldata2of2.corr()
                FCm = np.squeeze(np.asarray(FCm))
                FCm = FCm - np.identity(len(FCm))
            
                FCm = np.arctanh(FCm)
                FCallsplit2.append(FCm)                       
                
                
        np.savez(arraydatalistsplit1,FCallsplit1)
        np.savez(arraydatalistsplit2,FCallsplit2)  


    #load split half data if it already exists as an array
    else:
        print("Loading splithalf matrices")
        FCallload = np.load(arraydatalistsplit1)
        FCallsplit1 = [FC for FC in FCallload['arr_0']]
    
        FCallload = np.load(arraydatalistsplit2)
        FCallsplit2 = [FC for FC in FCallload['arr_0']]


#put parcel names into matrices
print("Adjusting matrices with parcel names")
FCallnames = []
for FC in FCall:
    FCm = pd.DataFrame(data=FC)
    FCm.columns = parcelnames
    FCm.index = parcelnames
    FCallnames.append(FCm)


if loadsplithalfdata:
    
    FCallnamessplit1 = []
    for FC in FCallsplit1:
        FCm = pd.DataFrame(data=FC)
        FCm.columns = parcelnames
        FCm.index = parcelnames
        FCallnamessplit1.append(FCm)
    
    FCallnamessplit2 = []
    for FC in FCallsplit2:
        FCm = pd.DataFrame(data=FC)
        FCm.columns = parcelnames
        FCm.index = parcelnames
        FCallnamessplit2.append(FCm)







networksnum = list(range(1,mistofinterest+1))

networkparcels = []

#create lists of all the parcels in each network
for network in networksnum:
    parcelsnet = list(parcelinfodf[parcelinfodf['network' + str(mistofinterest)] == network]['parcel'])
    networkparcels.append(parcelsnet)


#create output folder based on parcellation, scan length, which network scheme you're using
outputfolder = baseoutputfolder + str(numparcels) + 'parcels_' + str(scanlength) + 'length_' + str(mistofinterest) + 'networks/'
outputfolderrand = baserandomfolder + str(numparcels) + 'parcels_' + str(scanlength) + 'length_' + str(mistofinterest) + 'networks/'

if not os.path.exists(outputfolder):
    os.makedirs(outputfolder)        




#code below here only runs based on what steps you put into resulttype
#see top of code for what each step does


if 'networkmatchstats' in resulttype:
    
    edgetype = []
    matchtotallist = []
    matchpercentlist = []
    meancomplist = []
    meanbestnoncomplist = []
    meannoncomplist = []
    meancmblist = []
    meancmmlist = []
    numedgeslist = []
    randcount = []
    intrainter = []
    
    for network1 in networksnum:
        net1 = network1-1
        parcelcolumns = networkparcels[net1]

        if includeinternetwork:
            subnetworks = networksnum
        else:
            subnetworks = [network1]
        
        for network2 in subnetworks:
            if network2 >= network1:
                net2 = network2-1
                parcelrows = networkparcels[net2]            
                
                edgesname = str(net1+1)+'to'+str(net2+1)

                if network2 == network1:
                    intrainter.append('intra')
                else:
                    intrainter.append('inter')

                print("Investigating " + edgesname)
    
                fpresults = fpfaster(FCallnames,parcelcolumns,parcelrows,'all',shortidlist,personnumlist)
                
                savefile = outputfolder + 'fpnetworks_' + edgesname + '.csv'
                fpresults[0].to_csv(savefile)
                
                edgetype.append(edgesname)
                matchtotallist.append(sum(fpresults[0]['matchtotal']))
                matchpercentlist.append(sum(fpresults[0]['matchtotal'])/len(fpresults[0])*100)
                meancomplist.append(np.mean(fpresults[0]['stability']))
                meanbestnoncomplist.append(np.mean(fpresults[0]['nearest neighbor']))
                meannoncomplist.append(np.mean(fpresults[0]['mean similarity']))
                meancmblist.append(np.mean(fpresults[0]['stab minus nn']))
                meancmmlist.append(np.mean(fpresults[0]['stab minus sim']))
                numedgeslist.append(fpresults[1])

    parcelrows = parcelnames
    parcelcolumns = parcelnames
    intrainter.append('whole')
    edgetype.append('whole')
    
    print("Investigating whole")
    fpresults = fpfaster(FCallnames,parcelcolumns,parcelrows,'all',shortidlist,personnumlist)
    matchtotallist.append(sum(fpresults[0]['matchtotal']))
    matchpercentlist.append(sum(fpresults[0]['matchtotal'])/len(fpresults[0])*100)
    meancomplist.append(np.mean(fpresults[0]['stability']))
    meanbestnoncomplist.append(np.mean(fpresults[0]['nearest neighbor']))
    meannoncomplist.append(np.mean(fpresults[0]['mean similarity']))
    meancmblist.append(np.mean(fpresults[0]['stab minus nn']))
    meancmmlist.append(np.mean(fpresults[0]['stab minus sim']))
    numedgeslist.append(fpresults[1])    
    
    savefile = outputfolder + 'fpnetworks_whole.csv'
    fpresults[0].to_csv(savefile)
           
    overallsummarydf = pd.DataFrame({'networks':edgetype,'edgetype':intrainter,'numedges':numedgeslist,'matchtotal':matchtotallist,'matchpercent':matchpercentlist,'comp':meancomplist,'bestnoncomp':meanbestnoncomplist,'avgnoncomp':meannoncomplist,'cmb':meancmblist,'cmm':meancmmlist})
    print(overallsummarydf.to_string())
    print("")    

    if includeinternetwork:
        switchdf = overallsummarydf[overallsummarydf['edgetype'] == 'inter'].copy()
        switchernets = list(switchdf['networks'])
        switchernets = [x[-1]+'to'+x[0] for x in switchernets]
        switchdf['networks'] = switchernets
        
        totaloverallsummarydf = overallsummarydf.append(switchdf)
        totaloverallsummarydf = totaloverallsummarydf.sort_values('networks')
        totaloverallsummarydf = totaloverallsummarydf.reset_index(drop=True)
        
        savefile = outputfolder + 'fp_overallsummary_expanded.csv'
        totaloverallsummarydf.to_csv(savefile)

    savefile = outputfolder + 'fp_overallsummary.csv'
    overallsummarydf.to_csv(savefile)


  




if 'makerandomnumstype2' in resulttype:
    
    #this picks nodes from the network
    
    savespot = outputfolderrand + randomfolder

    if not os.path.exists(savespot):
        os.makedirs(savespot)     
 
    for num in range(len(networksnum)):
        parcelshere = networkparcels[num]

        networkhere = str(num + 1)
        
            
        if len(parcelshere) >= numrandparcels:
        
            savedoc = savespot + 'type2_' + networkhere + 'to' + networkhere + '_' + str(numrandparcels) + 'intra.csv'     
            
            randlists = []
            for num2 in range(numrandlists):
                randlist = random.sample(parcelshere,numrandparcels)
                randlists.append(randlist)
                    
            with open(savedoc,"w") as f:
                wr = csv.writer(f)
                wr.writerows(randlists) 
                    

    parcelshere = parcelnames

    networkhere = 'whole'
    
        
    if len(parcelshere) >= numrandparcels:
    
        savedoc = savespot + 'type2_' + networkhere + '_' + str(numrandparcels) + 'intra.csv'     
        
        randlists = []
        for num2 in range(numrandlists):
            randlist = random.sample(parcelshere,numrandparcels)
            randlists.append(randlist)
                
        with open(savedoc,"w") as f:
            wr = csv.writer(f)
            wr.writerows(randlists)                         



if 'makerandomnumstype3' in resulttype:
    
    #this picks nodes/2 from the two networks
    
    savespot = outputfolderrand + randomfolder

    if not os.path.exists(savespot):
        os.makedirs(savespot)     


    for num1 in range(len(networksnum)):
        net1 = str(num1 + 1)   
        parcelshere1 = networkparcels[num1]
    
        for num2 in range(len(networksnum)):
            net2 = str(num2 + 1)                    
            parcelshere2 = networkparcels[num2]
            
            if num2 == num1:
                    
                if len(parcelshere1) >= numrandparcels:
                
                    savedoc1 = savespot + 'type3_' + net1 + 'to' + net2 + '_' + str(numrandparcels) + '_1.csv' 
                    savedoc2 = savespot + 'type3_' + net1 + 'to' + net2 + '_' + str(numrandparcels) + '_2.csv' 
                    
                    randlistsA = []
                    randlistsB = []
                    for num in range(numrandlists):
                        randlist = random.sample(parcelshere1,numrandparcels)
                        
                        randlistA = randlist[:len(randlist)//2]
                        randlistB = randlist[len(randlist)//2:]
                        
                        randlistsA.append(randlistA)
                        randlistsB.append(randlistB)
                            
                    with open(savedoc1,"w") as f:
                        wr = csv.writer(f)
                        wr.writerows(randlistsA) 

                    with open(savedoc2,"w") as f:
                        wr = csv.writer(f)
                        wr.writerows(randlistsB) 
                    
            if num2 > num1:
             
                    
                if len(parcelshere1) >= numrandparcels/2:
                    if len(parcelshere2) >= numrandparcels/2:
                
                        savedoc1 = savespot + 'type3_' + net1 + 'to' + net2 + '_' + str(numrandparcels) + '_1.csv' 
                        savedoc2 = savespot + 'type3_' + net1 + 'to' + net2 + '_' + str(numrandparcels) + '_2.csv' 
                        
                        randlistsA = []
                        randlistsB = []
                        for num in range(numrandlists):
                            randlistA = random.sample(parcelshere1,numrandparcels//2)
                            randlistB = random.sample(parcelshere2,numrandparcels//2)
                            
                            randlistsA.append(randlistA)
                            randlistsB.append(randlistB)
                                
                        with open(savedoc1,"w") as f:
                            wr = csv.writer(f)
                            wr.writerows(randlistsA) 

                        with open(savedoc2,"w") as f:
                            wr = csv.writer(f)
                            wr.writerows(randlistsB) 


    parcelshere1 = parcelnames

    networkhere = 'whole'
    
    
    if len(parcelshere1) >= numrandparcels:
        
        savedoc1 = savespot + 'type3_whole_' + str(numrandparcels) + '_1.csv' 
        savedoc2 = savespot + 'type3_whole_' + str(numrandparcels) + '_2.csv' 
        
        randlistsA = []
        randlistsB = []
        for num in range(numrandlists):
            randlist = random.sample(parcelshere1,numrandparcels)
            
            randlistA = randlist[:len(randlist)//2]
            randlistB = randlist[len(randlist)//2:]
            
            randlistsA.append(randlistA)
            randlistsB.append(randlistB)
                
        with open(savedoc1,"w") as f:
            wr = csv.writer(f)
            wr.writerows(randlistsA) 

        with open(savedoc2,"w") as f:
            wr = csv.writer(f)
            wr.writerows(randlistsB)  



if 'makenetworkmatchrandtype2' in resulttype:
    
    edgetype = []
    matchtotallist = []
    matchpercentlist = []
    meancomplist = []
    meanbestnoncomplist = []
    meannoncomplist = []
    meancmblist = []
    meancmmlist = []
    numedgeslist = []
    numparcelslist = []
    randcount = []
    intrainter = []
    
    grnetworks = networksnum + ['whole']
    
    for network in grnetworks:

        if network != 'whole':
            netz = str(network) + 'to' + str(network)
        else:
            netz = 'whole'
        

        loadspot = outputfolderrand + randomfolder
        loaddoc = loadspot + 'type2_' + netz + '_' + str(numrandparcels) + 'intra.csv'     

        if os.path.isfile(loaddoc):
            randlistsr = []
            with open(loaddoc) as csvfile:
                 spamreader = csv.reader(csvfile)        
                 for row in spamreader:
                     randlistsr.append(row)

            savefolder = outputfolder + 'type2_random_' + netz + '_' + str(numrandparcels) + 'intra/'
            if not os.path.exists(savefolder):
                os.makedirs(savefolder)

            edgesname = netz
            lastfile = savefolder + 'fpnetworks_' + edgesname + '_iteration_' + str(numrandliststouse) + '_of_' + str(numrandliststouse) + '.csv'
            if not os.path.isfile(lastfile):
    
                for randlist in range(numrandliststouse):
                    savefile = savefolder + 'fpnetworks_' + edgesname + '_iteration_' + str(randlist+1) + '_of_' + str(numrandliststouse) + '.csv'
                    
                    if not os.path.isfile(savefile):
                    
                        parcelcolumns = randlistsr[randlist]
                        parcelrows = randlistsr[randlist]
                    
                        
                        intrainter.append('intra')
            
                        print("Investigating " + netz + ' (' + str(numrandparcels) + ' parcels) iteration ' + str(randlist+1) + ' of ' + str(numrandliststouse))
            
                    
                        fpresults = fpfaster(FCallnames,parcelcolumns,parcelrows,'all',shortidlist,personnumlist)
                        
                        fpresults[0].to_csv(savefile)
                        
                        randcount.append(randlist+1)
                        edgetype.append(edgesname)
                        matchtotallist.append(sum(fpresults[0]['matchtotal']))
                        matchpercentlist.append(sum(fpresults[0]['matchtotal'])/len(fpresults[0])*100)
                        meancomplist.append(np.mean(fpresults[0]['stability']))
                        meanbestnoncomplist.append(np.mean(fpresults[0]['nearest neighbor']))
                        meannoncomplist.append(np.mean(fpresults[0]['mean similarity']))
                        meancmblist.append(np.mean(fpresults[0]['stab minus nn']))
                        meancmmlist.append(np.mean(fpresults[0]['stab minus sim']))
                        numedgeslist.append(fpresults[1])
                        numparcelslist.append(numrandparcels)

           
    overallsummarydf = pd.DataFrame({'networks':edgetype,'edgetype':intrainter,'randcount':randcount,'numparcels':numparcelslist,'numedges':numedgeslist,'matchtotal':matchtotallist,'matchpercent':matchpercentlist,'comp':meancomplist,'bestnoncomp':meanbestnoncomplist,'avgnoncomp':meannoncomplist,'cmb':meancmblist,'cmm':meancmmlist})
    print(overallsummarydf.to_string())
    print("")    
    

if 'makenetworkmatchrandtype3' in resulttype:
    
    edgetype = []
    matchtotallist = []
    matchpercentlist = []
    meancomplist = []
    meanbestnoncomplist = []
    meannoncomplist = []
    meancmblist = []
    meancmmlist = []
    numedgeslist = []
    numparcelslist = []
    randcount = []
    intrainter = []



    netlist = []
    intrainterlist = []
    for num1 in range(len(networksnum)):
        net1 = str(num1 + 1) 
        for num2 in range(len(networksnum)):
            net2 = str(num2 + 1)   
            if num2 == num1:
                intrainterlist.append('intra')
            elif num2 > num1:
                intrainterlist.append('inter')
            
        
            if num2 >= num1:
                networkhere = net1 + 'to' + net2
                netlist.append(networkhere)
    netlist.append('whole')
    intrainterlist.append('whole')
    
    loadspot = outputfolderrand + randomfolder
    
    for netnum in range(len(netlist)):
        
        network = netlist[netnum]
        
        doit = True
        if includeinternetwork == False:
            if intrainterlist[netnum] == 'inter':
                doit = False
        
        if doit:
        

            loaddoc1 = loadspot + 'type3_' + network + '_' + str(numrandparcels) + '_1.csv' 
            loaddoc2 = loadspot + 'type3_' + network + '_' + str(numrandparcels) + '_2.csv'   

            if os.path.isfile(loaddoc1):
                randlistsr1 = []
                with open(loaddoc1) as csvfile:
                     spamreader = csv.reader(csvfile)        
                     for row in spamreader:
                         randlistsr1.append(row)

                randlistsr2 = []
                with open(loaddoc2) as csvfile:
                     spamreader = csv.reader(csvfile)        
                     for row in spamreader:
                         randlistsr2.append(row)


                savefolder = outputfolder + 'type3_random_' + network + '_' + str(numrandparcels) + '/'
                if not os.path.exists(savefolder):
                    os.makedirs(savefolder)
        
                for randlist in range(numrandliststouse):
                    parcelcolumns = randlistsr1[randlist]
                    parcelrows = randlistsr2[randlist]
                
                    edgesname = network
                    intrainter.append(intrainterlist[netnum])
        
                    print("Investigating " + network + ' (' + str(numrandparcels) + ' parcels) iteration ' + str(randlist+1) + ' of ' + str(numrandliststouse))
        
        
                    fpresults = fpfaster(FCallnames,parcelcolumns,parcelrows,'all',shortidlist,personnumlist)
                    
                    savefile = savefolder + 'fpnetworks_' + edgesname + '_iteration_' + str(randlist+1) + '_of_' + str(numrandliststouse) + '.csv'
                    fpresults[0].to_csv(savefile)
                    
                    randcount.append(randlist+1)
                    edgetype.append(edgesname)
                    matchtotallist.append(sum(fpresults[0]['matchtotal']))
                    matchpercentlist.append(sum(fpresults[0]['matchtotal'])/len(fpresults[0])*100)
                    meancomplist.append(np.mean(fpresults[0]['stability']))
                    meanbestnoncomplist.append(np.mean(fpresults[0]['nearest neighbor']))
                    meannoncomplist.append(np.mean(fpresults[0]['mean similarity']))
                    meancmblist.append(np.mean(fpresults[0]['stab minus nn']))
                    meancmmlist.append(np.mean(fpresults[0]['stab minus sim']))
                    numedgeslist.append(fpresults[1])
                    numparcelslist.append(numrandparcels)

           
    overallsummarydf = pd.DataFrame({'networks':edgetype,'edgetype':intrainter,'randcount':randcount,'numparcels':numparcelslist,'numedges':numedgeslist,'matchtotal':matchtotallist,'matchpercent':matchpercentlist,'comp':meancomplist,'bestnoncomp':meanbestnoncomplist,'avgnoncomp':meannoncomplist,'cmb':meancmblist,'cmm':meancmmlist})
    print(overallsummarydf.to_string())
    print("")    





if 'loadnetworkmatchrand' in resulttype:
    
    randtypelist = ['type2','type3']  
    
    edgetype = []
    matchtotallist = []
    matchpercentlist = []
    meancomplist = []
    meanbestnoncomplist = []
    meannoncomplist = []
    meancmblist = []
    meancmmlist = []
    numedgeslist = []
    #randcount = []
    intrainter = []
    randtypelisthere = []

    netlist = []
    intrainterlist = []
    for num1 in range(len(networksnum)):
        net1 = str(num1 + 1) 
        for num2 in range(len(networksnum)):
            net2 = str(num2 + 1)   
            if num2 == num1:
                intrainterlist.append('intra')
            elif num2 > num1:
                intrainterlist.append('inter')
                
            if num2 >= num1:
                networkhere = net1 + 'to' + net2
                netlist.append(networkhere)

    netlist.append('whole')
    intrainterlist.append('whole')
    
    netlist.append('inter')
    intrainterlist.append('inter')
    
    netlist.append('intra')
    intrainterlist.append('intra')                
    
    
    for randtype in randtypelist:

        for num in range(len(netlist)):
                                         
            if randtype != 'type3':
                numedges = int(reduce(op.mul, range(numrandparcels, numrandparcels-2, -1), 1)/reduce(op.mul, range(1, min(2,numrandparcels-2)+1), 1))
            else:
                numedges = (numrandparcels/2)**2
            
            networkshere = netlist[num]

            #numedges = numedgeslistload[num]
            
            if randtype != 'type2':
                loadfolder = outputfolder + randtype + '_random_' + networkshere + '_' + str(numrandparcels) + '/'
                outputsavefile = outputfolder + 'output_' + randtype + '_random_' + networkshere + '_' + str(numrandparcels) + '.csv'
            else:
                loadfolder = outputfolder + randtype + '_random_' + networkshere + '_' + str(numrandparcels) + 'intra/'
                outputsavefile = outputfolder + 'output_' + randtype + '_random_' + networkshere + '_' + str(numrandparcels) + 'intra.csv'
             
            
            lastfile = loadfolder + 'fpnetworks_' + networkshere + '_iteration_' + str(numrandliststouse) + '_of_' + str(numrandliststouse) + '.csv'

            if not os.path.isfile(outputsavefile):
                if os.path.isfile(lastfile):

                    edgetype = []
                    matchtotallist = []
                    matchpercentlist = []
                    meancomplist = []
                    meanbestnoncomplist = []
                    meannoncomplist = []
                    meancmblist = []
                    meancmmlist = []
                    numedgeslist = []
                    intrainter = []
                    randtypelisthere = []  
                         
                    for randlistnum in range(numrandliststouse):
                        
                        if ((randlistnum+1)%100) == 1:
                            print("Investigating " + networkshere + ' (' + str(numrandparcels) + ' parcels) iteration ' + str(randlistnum+1) + ' of ' + str(numrandliststouse))
                        loadfile = loadfolder + 'fpnetworks_' + networkshere + '_iteration_' + str(randlistnum+1) + '_of_' + str(numrandliststouse) + '.csv'
                
                        fpresults = pd.read_csv(loadfile, index_col=0)
                        
                        intrainter.append(intrainterlist[num])  
                        edgetype.append(networkshere)
                        matchtotallist.append(sum(fpresults['matchtotal']))
                        matchpercentlist.append(sum(fpresults['matchtotal'])/len(fpresults)*100)
                        meancomplist.append(np.mean(fpresults['stability']))
                        meanbestnoncomplist.append(np.mean(fpresults['nearest neighbor']))
                        meannoncomplist.append(np.mean(fpresults['mean similarity']))
                        meancmblist.append(np.mean(fpresults['stab minus nn']))
                        meancmmlist.append(np.mean(fpresults['stab minus sim']))
                        numedgeslist.append(numedges)
                        randtypelisthere.append(randtype)
                        
                    overallsummarydf = pd.DataFrame({'networks':edgetype,'edgetype':intrainter,'randtype':randtypelisthere,'numedges':numedgeslist,'matchtotal':matchtotallist,'matchpercent':matchpercentlist,'comp':meancomplist,'bestnoncomp':meanbestnoncomplist,'avgnoncomp':meannoncomplist,'cmb':meancmblist,'cmm':meancmmlist})
                    print(overallsummarydf) 
                    print("")
                    overallsummarydf.to_csv(outputsavefile)




    

if 'networkage' in resulttype:
    edgetype = []
    fpmeasure = []
    agecoef = []
    agepval = []
    f2 = []
    intrainter = []
    numedgeslist = []

    agecoeflow = []
    agecoefhigh = []
    
    agecoefz = []
    agecoefzlow = []
    agecoefzhigh = []

    loadfile = outputfolder + 'fp_overallsummary.csv'
    netedgedf = pd.read_csv(loadfile, index_col=0)

    netlist = list(netedgedf['networks'])
    numedgeslistload = list(netedgedf['numedges'])
    intrainterlist = list(netedgedf['edgetype'])


    for num in range(len(netlist)):
        
        #num = 4
        
        networks = netlist[num]
        numedges = numedgeslistload[num]
    
        loadfile = outputfolder + 'fpnetworks_' + networks + '.csv'
        
        netdf = pd.read_csv(loadfile, index_col=0)
     
        columnsofinterest = ['stability', 'nearest neighbor', 'stab minus nn','mean similarity', 'stab minus sim']
        
        for columnofinterest in columnsofinterest:
            agestuff = ageeffects(netdf,columnofinterest)
            
            intrainter.append(intrainterlist[num])  
            numedgeslist.append(numedges)
            edgetype.append(networks)
            fpmeasure.append(columnofinterest)
            agecoef.append(agestuff[2])
            agepval.append(agestuff[0])
            f2.append(agestuff[1])   
 
            agecoeflow.append(agestuff[3])   
            agecoefhigh.append(agestuff[4])   
            
            agecoefz.append(agestuff[5])   
            agecoefzlow.append(agestuff[6])   
            agecoefzhigh.append(agestuff[7])   

            

    ageeffectdf = pd.DataFrame({'networks':edgetype,'numedges':numedgeslist,'edgetype':intrainter,'fpmeasure':fpmeasure,'agepval':agepval,'age f2':f2,'agecoef':agecoef,'agecoef_low':agecoeflow,'agecoef_high':agecoefhigh,'agecoefz':agecoefz,'agecoefz_low':agecoefzlow,'agecoefz_high':agecoefzhigh})
    
    ageeffectdf = ageeffectdf.sort_values(['fpmeasure','networks'])
    
    print(ageeffectdf.to_string())
        
    savefile = outputfolder + 'age_overallsummary.csv'
    ageeffectdf.to_csv(savefile)





if 'networkagerand' in resulttype:

    randtypelist = ['type2','type3']    

    edgetype = []
    fpmeasure = []
    agecoef = []
    agepval = []
    f2 = []
    intrainter = []
    numedgeslist = []
    uniqcols = []
    randtypelisthere = []  

    agecoeflow = []
    agecoefhigh = []
    
    agecoefz = []
    agecoefzlow = []
    agecoefzhigh = []


    netlist = []
    intrainterlist = []
    for num1 in range(len(networksnum)):
        net1 = str(num1 + 1) 
        for num2 in range(len(networksnum)):
            net2 = str(num2 + 1)   
            if num2 == num1:
                intrainterlist.append('intra')
            elif num2 > num1:
                intrainterlist.append('inter')
                
            if num2 >= num1:
                networkhere = net1 + 'to' + net2
                netlist.append(networkhere)

    netlist.append('whole')
    intrainterlist.append('whole')
    
    #netlist = ['whole']
    

    netlist.append('inter')
    intrainterlist.append('inter')
    
    netlist.append('intra')
    intrainterlist.append('intra')  

    
    for randtype in randtypelist:

        for num in range(len(netlist)):
                                    
            
            if randtype != 'type3':
                numedges = int(reduce(op.mul, range(numrandparcels, numrandparcels-2, -1), 1)/reduce(op.mul, range(1, min(2,numrandparcels-2)+1), 1))
            else:
                numedges = (numrandparcels/2)**2
            
            networkshere = netlist[num]

            
            if randtype != 'type2':
                loadfolder = outputfolder + randtype + '_random_' + networkshere + '_' + str(numrandparcels) + '/'
                outputsavefile = outputfolder + 'outputage_' + randtype + '_random_' + networkshere + '_' + str(numrandparcels) + '_age_rand_fulllist.csv'
                outputsavefile2 = outputfolder + 'outputage_' + randtype + '_random_' + networkshere + '_' + str(numrandparcels) + '_age_rand_overallsummary.csv'
            else:
                loadfolder = outputfolder + randtype + '_random_' + networkshere + '_' + str(numrandparcels) + 'intra/'
                outputsavefile = outputfolder + 'outputage_' + randtype + '_random_' + networkshere + '_' + str(numrandparcels) + '_intra_age_rand_fulllist.csv'
                outputsavefile2 = outputfolder + 'outputage_' + randtype + '_random_' + networkshere + '_' + str(numrandparcels) + '_intra_age_rand_overallsummary.csv'
             
            
            lastfile = loadfolder + 'fpnetworks_' + networkshere + '_iteration_' + str(numrandliststouse) + '_of_' + str(numrandliststouse) + '.csv'

            if not os.path.isfile(outputsavefile):
                if os.path.isfile(lastfile):

                    edgetype = []
                    fpmeasure = []
                    agecoef = []
                    agepval = []
                    f2 = []
                    intrainter = []
                    numedgeslist = []
                    uniqcols = []
                    randtypelisthere = []  

                    agecoeflow = []
                    agecoefhigh = []
                    
                    agecoefz = []
                    agecoefzlow = []
                    agecoefzhigh = []
                         
                    for randlistnum in range(numrandliststouse):
                        
                        if ((randlistnum+1)%100) == 1:
                            print("Investigating " + networkshere + ' (' + str(numrandparcels) + ' parcels) iteration ' + str(randlistnum+1) + ' of ' + str(numrandliststouse))
                        loadfile = loadfolder + 'fpnetworks_' + networkshere + '_iteration_' + str(randlistnum+1) + '_of_' + str(numrandliststouse) + '.csv'
                
                        fpresults = pd.read_csv(loadfile, index_col=0)

                        columnsofinterest = ['stability', 'nearest neighbor', 'stab minus nn','mean similarity', 'stab minus sim']
                        
                        for columnofinterest in columnsofinterest:
                            agestuff = ageeffects(fpresults,columnofinterest)
                            
                            uniqcol = randtype + '_' + networkshere + '_' + str(numrandparcels) + '_' + columnofinterest
                            uniqcols.append(uniqcol)
                            intrainter.append(intrainterlist[num])  
                            numedgeslist.append(numedges)
                            edgetype.append(networkshere)
                            fpmeasure.append(columnofinterest)
                            randtypelisthere.append(randtype)

                            agecoef.append(agestuff[2])
                            agepval.append(agestuff[0])
                            f2.append(agestuff[1])   
                 
                            agecoeflow.append(agestuff[3])   
                            agecoefhigh.append(agestuff[4])   
                            
                            agecoefz.append(agestuff[5])   
                            agecoefzlow.append(agestuff[6])   
                            agecoefzhigh.append(agestuff[7]) 


                    
                    ageeffectranddf = pd.DataFrame({'networks':edgetype,'numedges':numedgeslist,'edgetype':intrainter,'randtype':randtypelisthere,'fpmeasure':fpmeasure,'type':uniqcols,'agepval':agepval,'age f2':f2,'agecoef':agecoef,'agecoef_low':agecoeflow,'agecoef_high':agecoefhigh,'agecoefz':agecoefz,'agecoefz_low':agecoefzlow,'agecoefz_high':agecoefzhigh})
                    ageeffectranddf = ageeffectranddf.sort_values(['fpmeasure','networks'])
                                                            
                    ageeffectranddf.to_csv(outputsavefile)


                    
                    uniqfeatures = list(set(uniqcols))
                
                    print("Summarizing the data")
                
                    edgetype = []
                    fpmeasure = []
                    agecoef = []
                    agepval = []
                    f2 = []
                    intrainter = []
                    numedgeslist = []
                    uniqcols = []
                    randtypelisthere = []  
                    randcount = []

                    agecoeflow = []
                    agecoefhigh = []
                    
                    agecoefz = []
                    agecoefzlow = []
                    agecoefzhigh = []
                
                    for nummy in range(len(uniqfeatures)):
                                
                        feature = uniqfeatures[nummy]
                        
                        features = feature.split('_')
                
                        netties = features[1].split('to')
                        
                        if len(netties) == 1:
                            intrainter.append('whole')
                        elif netties[0] == netties[1]:
                            intrainter.append('intra')
                        else:
                            intrainter.append('inter')
                        
                        
                        netageeffectranddf = ageeffectranddf[ageeffectranddf['type'] == feature]
                
                        randcount.append(len(netageeffectranddf))
                        
                        #intrainter.append(intrainterlist[num])  
                        numedgeslist.append(int(np.mean(netageeffectranddf['numedges'])))
                        edgetype.append(features[1])
                        fpmeasure.append(features[3])
                        randtypelisthere.append(features[0])

                        agepval.append(np.mean(netageeffectranddf['agepval']))
                        f2.append(np.mean(netageeffectranddf['age f2']))  
                        
                        agecoef.append(np.mean(netageeffectranddf['agecoef']))
                        agecoeflow.append(np.mean(netageeffectranddf['agecoef_low']))        
                        agecoefhigh.append(np.mean(netageeffectranddf['agecoef_high']))        
                 
                        agecoefz.append(np.mean(netageeffectranddf['agecoefz']))
                        agecoefzlow.append(np.mean(netageeffectranddf['agecoefz_low']))        
                        agecoefzhigh.append(np.mean(netageeffectranddf['agecoefz_high']))   
            
                                    
                        
                    avgageeffectranddf = pd.DataFrame({'randtype':randtypelisthere,'networks':edgetype,'edgetype':intrainter,'fpmeasure':fpmeasure,'randcount':randcount,'numedges':numedgeslist,'agepval':agepval,'age f2':f2,'agecoef':agecoef,'agecoef_low':agecoeflow,'agecoef_high':agecoefhigh,'agecoefz':agecoefz,'agecoefz_low':agecoefzlow,'agecoefz_high':agecoefzhigh})
                  
                    avgageeffectranddf = avgageeffectranddf.sort_values(['fpmeasure','networks'])
                    
                    print(avgageeffectranddf.to_string())
                    
                    avgageeffectranddf.to_csv(outputsavefile2)
                        




if 'networkchangestats' in resulttype:
    
    edgetype = []
    numedgeslist = []
    intrainter = []
    adiffbypersonlist = []
    astdlist = []
    adiffstdlist = []
    ameanstrlist = []                
    
    
    for network1 in networksnum:
        net1 = network1-1
        parcelcolumns = networkparcels[net1]

        if includeinternetwork:
            subnetworks = networksnum
        else:
            subnetworks = [network1]
        
        for network2 in subnetworks:
            if network2 >= network1:
                net2 = network2-1
                parcelrows = networkparcels[net2]            
                
                edgesname = str(net1+1)+'to'+str(net2+1)

                if network2 == network1:
                    intrainter.append('intra')
                else:
                    intrainter.append('inter')

                print("Investigating " + edgesname)
    
                chresults = changestatsfaster(FCallnames,parcelcolumns,parcelrows,'all',shortidlist,personnumlist)
                                       
                savefile = outputfolder + 'ednetworks_' + edgesname + '.csv'
                
                chresults[0].to_csv(savefile)
                
                edgetype.append(edgesname)
                
                adiffbypersonlist.append(np.mean(chresults[0]['meandiff']))
                astdlist.append(np.mean(chresults[0]['edgestd']))
                adiffstdlist.append(np.mean(chresults[0]['stddiff']))
                ameanstrlist.append(np.mean(chresults[0]['meanedge']))
                numedgeslist.append(chresults[1])

    parcelrows = parcelnames
    parcelcolumns = parcelnames
    intrainter.append('whole')
    edgetype.append('whole')
    
    print("Investigating whole")


    chresults = changestatsfaster(FCallnames,parcelcolumns,parcelrows,'all',shortidlist,personnumlist)
                           
    savefile = outputfolder + 'ednetworks_whole.csv'
    chresults[0].to_csv(savefile)
    
    adiffbypersonlist.append(np.mean(chresults[0]['meandiff']))
    astdlist.append(np.mean(chresults[0]['edgestd']))
    adiffstdlist.append(np.mean(chresults[0]['stddiff']))
    ameanstrlist.append(np.mean(chresults[0]['meanedge']))
    numedgeslist.append(chresults[1])


           
    eoverallsummarydf = pd.DataFrame({'networks':edgetype,'edgetype':intrainter,'numedges':numedgeslist,'meanmeandiff':adiffbypersonlist,'meanstddiff':adiffstdlist,'meanstd':astdlist,'meanmeanstrength':ameanstrlist})
    print(eoverallsummarydf.to_string())
    print("")    

    if includeinternetwork:
        switchdf = eoverallsummarydf[eoverallsummarydf['edgetype'] == 'inter'].copy()
        switchernets = list(switchdf['networks'])
        switchernets = [x[-1]+'to'+x[0] for x in switchernets]
        switchdf['networks'] = switchernets
        
        etotaloverallsummarydf = eoverallsummarydf.append(switchdf)
        etotaloverallsummarydf = etotaloverallsummarydf.sort_values('networks')
        etotaloverallsummarydf = etotaloverallsummarydf.reset_index(drop=True)
        
        savefile = outputfolder + 'ed_overallsummary_expanded.csv'
        etotaloverallsummarydf.to_csv(savefile)

    savefile = outputfolder + 'ed_overallsummary.csv'
    eoverallsummarydf.to_csv(savefile)




if 'networkageed' in resulttype:
    edgetype = []
    fpmeasure = []
    agecoef = []
    agepval = []
    f2 = []
    intrainter = []
    numedgeslist = []

    agecoeflow = []
    agecoefhigh = []
    
    agecoefz = []
    agecoefzlow = []
    agecoefzhigh = []




    loadfile = outputfolder + 'ed_overallsummary.csv'
    netedgedf = pd.read_csv(loadfile, index_col=0)

    netlist = list(netedgedf['networks'])
    numedgeslistload = list(netedgedf['numedges'])
    intrainterlist = list(netedgedf['edgetype'])


    for num in range(len(netlist)):
        
        #num = 4
        
        networks = netlist[num]
        numedges = numedgeslistload[num]
    
        loadfile = outputfolder + 'ednetworks_' + networks + '.csv'
        
        netdf = pd.read_csv(loadfile, index_col=0)
     
        columnsofinterest = ['meandiff','stddiff','edgestd','meanedge']
        
        for columnofinterest in columnsofinterest:
            agestuff = ageeffects(netdf,columnofinterest)
            
            intrainter.append(intrainterlist[num])  
            numedgeslist.append(numedges)
            edgetype.append(networks)
            fpmeasure.append(columnofinterest)
            agecoef.append(agestuff[2])
            agepval.append(agestuff[0])
            f2.append(agestuff[1])   
 
            agecoeflow.append(agestuff[3])   
            agecoefhigh.append(agestuff[4])   
            
            agecoefz.append(agestuff[5])   
            agecoefzlow.append(agestuff[6])   
            agecoefzhigh.append(agestuff[7])   

            

    ageeffectdf = pd.DataFrame({'networks':edgetype,'numedges':numedgeslist,'edgetype':intrainter,'fpmeasure':fpmeasure,'agepval':agepval,'age f2':f2,'agecoef':agecoef,'agecoef_low':agecoeflow,'agecoef_high':agecoefhigh,'agecoefz':agecoefz,'agecoefz_low':agecoefzlow,'agecoefz_high':agecoefzhigh})
    
    ageeffectdf = ageeffectdf.sort_values(['fpmeasure','networks'])
        
    print(ageeffectdf.to_string())
        
    savefile = outputfolder + 'age_edgesummary.csv'
    
    ageeffectdf.to_csv(savefile)     



if 'networkmatchstatssplithalf' in resulttype:
    
    edgetype = []
    matchtotallist = []
    matchpercentlist = []
    meancomplist = []
    meansplitlist = []
    meanbestnoncomplist = []
    meannoncomplist = []
    meancmblist = []
    meancmmlist = []
    numedgeslist = []
    randcount = []
    intrainter = []
    
    for network1 in networksnum:
        net1 = network1-1
        parcelcolumns = networkparcels[net1]

        if includeinternetwork:
            subnetworks = networksnum
        else:
            subnetworks = [network1]
        
        for network2 in subnetworks:
            if network2 >= network1:
                net2 = network2-1
                parcelrows = networkparcels[net2]            
                
                edgesname = str(net1+1)+'to'+str(net2+1)

                if network2 == network1:
                    intrainter.append('intra')
                else:
                    intrainter.append('inter')

                print("Investigating " + edgesname)
    
                fpresults = fpfastersplithalf(FCallnamessplit1,FCallnamessplit2,parcelcolumns,parcelrows,'all',shortidlist,personnumlist)
                
                savefile = outputfolder + 'half_fpnetworks_' + edgesname + '.csv'
                fpresults[0].to_csv(savefile)
                
                edgetype.append(edgesname)
                matchtotallist.append(sum(fpresults[0]['matchtotal']))
                matchpercentlist.append(sum(fpresults[0]['matchtotal'])/len(fpresults[0])*100)
                meancomplist.append(np.mean(fpresults[0]['stability']))
                meansplitlist.append(np.mean(fpresults[0]['splithalf']))
                meanbestnoncomplist.append(np.mean(fpresults[0]['nearest neighbor']))
                meannoncomplist.append(np.mean(fpresults[0]['mean similarity']))
                meancmblist.append(np.mean(fpresults[0]['stab minus nn']))
                meancmmlist.append(np.mean(fpresults[0]['stab minus sim']))
                numedgeslist.append(fpresults[1])

    parcelrows = parcelnames
    parcelcolumns = parcelnames
    intrainter.append('whole')
    edgetype.append('whole')
    
    print("Investigating whole")
    fpresults = fpfastersplithalf(FCallnamessplit1,FCallnamessplit2,parcelcolumns,parcelrows,'all',shortidlist,personnumlist)
    matchtotallist.append(sum(fpresults[0]['matchtotal']))
    matchpercentlist.append(sum(fpresults[0]['matchtotal'])/len(fpresults[0])*100)
    meancomplist.append(np.mean(fpresults[0]['stability']))
    meansplitlist.append(np.mean(fpresults[0]['splithalf']))
    meanbestnoncomplist.append(np.mean(fpresults[0]['nearest neighbor']))
    meannoncomplist.append(np.mean(fpresults[0]['mean similarity']))
    meancmblist.append(np.mean(fpresults[0]['stab minus nn']))
    meancmmlist.append(np.mean(fpresults[0]['stab minus sim']))
    numedgeslist.append(fpresults[1])    
    
    savefile = outputfolder + 'half_fpnetworks_whole.csv'
    fpresults[0].to_csv(savefile)
           
    overallsummarydf = pd.DataFrame({'networks':edgetype,'edgetype':intrainter,'numedges':numedgeslist,'matchtotal':matchtotallist,'matchpercent':matchpercentlist,'split':meansplitlist,'comp':meancomplist,'bestnoncomp':meanbestnoncomplist,'avgnoncomp':meannoncomplist,'cmb':meancmblist,'cmm':meancmmlist})
    print(overallsummarydf.to_string())
    print("")    

    if includeinternetwork:
        switchdf = overallsummarydf[overallsummarydf['edgetype'] == 'inter'].copy()
        switchernets = list(switchdf['networks'])
        switchernets = [x[-1]+'to'+x[0] for x in switchernets]
        switchdf['networks'] = switchernets
        
        totaloverallsummarydf = overallsummarydf.append(switchdf)
        totaloverallsummarydf = totaloverallsummarydf.sort_values('networks')
        totaloverallsummarydf = totaloverallsummarydf.reset_index(drop=True)
        
        savefile = outputfolder + 'half_fp_overallsummary_expanded.csv'
        totaloverallsummarydf.to_csv(savefile)

    savefile = outputfolder + 'half_fp_overallsummary.csv'
    overallsummarydf.to_csv(savefile)




if 'splithalfage' in resulttype:
    

    networklistgra = ['1to1','2to2','3to3','4to4','5to5','6to6','7to7','8to8','9to9','10to10','11to11','12to12','whole'] 
    
    agecoef = []
    agepval = []
    f2 = []
    intrainter = []
    numedgeslist = []

    agecoeflow = []
    agecoefhigh = []
    
    agecoefz = []
    agecoefzlow = []
    agecoefzhigh = []    
    
    networkgralist = []
    
    motionpval = []


    for networkgra in networklistgra:
        
        print("Checking network " + networkgra)
        
            
        networkgralist.append(networkgra)
        
        splitdffile = outputfolder + 'half_fpnetworks_' + networkgra + '.csv'
        splitdf = pd.read_csv(splitdffile, index_col=0)    


        indepz = (splitdf['splithalf'] - splitdf['splithalf'].mean())/splitdf['splithalf'].std(ddof=0)

        df = persondf[['person','sex','age','fd']].copy()
        df['Corr'] = splitdf['splithalf']                                                                                                                                                
        df["group"] = 1                                                                                                                
                                                                                                                                   
        vcf = {"person": "0 + C(person)"}                                                                                                       
        model = sm.MixedLM.from_formula("Corr ~ age + fd + sex", groups="group",vc_formula=vcf, re_formula="0", data=df)    
        
        result = model.fit()  
        
        agepvalue = result.pvalues['age']
        ageparam = result.params['age']
        
        motionpval.append(result.pvalues['fd'])
 
        ageparamlow = result.conf_int(alpha=0.05, cols=None)[0]['age']
        ageparamhigh = result.conf_int(alpha=0.05, cols=None)[1]['age']       
 
        agepval.append(agepvalue)
        agecoef.append(ageparam)
        agecoeflow.append(ageparamlow)
        agecoefhigh.append(ageparamhigh)    
        
  
        #do it again with standardized estimates
        df = persondf[['person','sex','age','fd']].copy()
        df['Corr'] = indepz                                                                                                                                             
        df["group"] = 1                                                                                                                
                                                                                                                                   
        vcf = {"person": "0 + C(person)"}                                                                                                        
        model = sm.MixedLM.from_formula("Corr ~ age + fd + sex", groups="group",vc_formula=vcf, re_formula="0", data=df)    
        
        result = model.fit()  

        ageparam = result.params['age']
 
        ageparamlow = result.conf_int(alpha=0.05, cols=None)[0]['age']
        ageparamhigh = result.conf_int(alpha=0.05, cols=None)[1]['age']   

        agecoefz.append(ageparam)
        agecoefzlow.append(ageparamlow)
        agecoefzhigh.append(ageparamhigh)   


        
        df['agez'] = (df['age'] - df['age'].mean())/df['age'].std(ddof=0)
        model = sm.MixedLM.from_formula("Corr ~ agez + fd + sex", groups="group",vc_formula=vcf, re_formula="0", data=df)    
        
        result = model.fit()  

        ageparam = result.params['agez']




    print(motionpval)
    checkdf = pd.DataFrame({'networks':networkgralist,'agepval':agepval,'agecoef':agecoef,'agecoef_low':agecoeflow,'agecoef_high':agecoefhigh,'agecoefz':agecoefz,'agecoefz_low':agecoefzlow,'agecoefz_high':agecoefzhigh})
    checkdf.to_csv(outputfolder + "splithalfagedata.csv")

    print(checkdf.to_string())





if 'networkage2' in resulttype:
    edgetype = []
    
    avgagecoefmem = []
    avgagepvalmem = []
    agediffcoefmem = []
    agediffpvalmem = []
    
    avgagecoefmemlow = []
    avgagecoefmemhigh = []
    agediffcoefmemlow = []
    agediffcoefmemhigh = []
    
    intrainter = []
    numedgeslist = []

    avgagecoefmemz = []
    avgagepvalmemz = []
    agediffcoefmemz = []
    agediffpvalmemz = []
    
    avgagecoefmemlowz = []
    avgagecoefmemhighz = []
    agediffcoefmemlowz = []
    agediffcoefmemhighz = []



    loadfile = outputfolder + 'fp_overallsummary.csv'
    netedgedf = pd.read_csv(loadfile, index_col=0)
    
    if includeinternetwork:
        subnetedgedf = netedgedf
    else:
        subnetedgedf = netedgedf[netedgedf['edgetype'] != 'inter']

    netlist = list(subnetedgedf['networks'])
    numedgeslistload = list(subnetedgedf['numedges'])
    intrainterlist = list(subnetedgedf['edgetype'])
    

    networkparcels1 = []
    networkparcels2 = []

    networkslist = list(range(1,mistofinterest+1))

    for network1 in networkslist:
        net1 = network1-1
        parcelcolumns = networkparcels[net1]

        if includeinternetwork:
            subnetworks = networkslist
        else:
            subnetworks = [network1]
        
        for network2 in subnetworks:
            if network2 >= network1:
                net2 = network2-1
                parcelrows = networkparcels[net2]   
                
                networkparcels1.append(parcelcolumns)
                networkparcels2.append(parcelrows)
                
    for num in range(len(netlist)):
    #for num in range(2):
        
        networks = netlist[num]
        numedges = numedgeslistload[num]
        
        print("Checking network " + networks)

        if networks != 'whole':
            parcelcolumns = networkparcels1[num]
            parcelrows = networkparcels2[num]
        else:
            parcelcolumns = parcelnames
            parcelrows = parcelnames
    
        loadfile = outputfolder + 'fpnetworks_' + networks + '.csv'
        
        netdf = pd.read_csv(loadfile, index_col=0)
     
        edgetype.append(networks)
        numedgeslist.append(numedges)
        intrainter.append(intrainterlist[num])  
        
        agestuff3 = similaritymem(FCallnames,parcelcolumns,parcelrows,'all',shortidlist,personnumlist)
        avgagecoefmem.append(agestuff3[0])
        avgagepvalmem.append(agestuff3[1])
        agediffcoefmem.append(agestuff3[2])
        agediffpvalmem.append(agestuff3[3])
            
        avgagecoefmemlow.append(agestuff3[4])
        avgagecoefmemhigh.append(agestuff3[5])
        
        agediffcoefmemlow.append(agestuff3[6])
        agediffcoefmemhigh.append(agestuff3[7])
            
 
        avgagecoefmemz.append(agestuff3[8])
        avgagepvalmemz.append(agestuff3[9])
        agediffcoefmemz.append(agestuff3[10])
        agediffpvalmemz.append(agestuff3[11])
        
        avgagecoefmemlowz.append(agestuff3[12])
        avgagecoefmemhighz.append(agestuff3[13])
        agediffcoefmemlowz.append(agestuff3[14])
        agediffcoefmemhighz.append(agestuff3[15])
     
    
    ageeffectdf = pd.DataFrame({'networks':edgetype,'numedges':numedgeslist,'edgetype':intrainter,
                                'avgagepvalmem':avgagepvalmem,'avgagecoefmem':avgagecoefmem,'avgagecoefmem_low':avgagecoefmemlow,'avgagecoefmem_high':avgagecoefmemhigh,
                                'agediffpvalmem':agediffpvalmem,'agediffcoefmem':agediffcoefmem,'agediffcoefmem_low':agediffcoefmemlow,'agediffcoefmem_high':agediffcoefmemhigh,
                                })
    

    print(ageeffectdf.to_string())


    ageeffectdfz = pd.DataFrame({'networks':edgetype,'numedges':numedgeslist,'edgetype':intrainter,
                                'avgagepvalmemz':avgagepvalmemz,'avgagecoefmemz':avgagecoefmemz,'avgagecoefmemz_low':avgagecoefmemlowz,'avgagecoefmemz_high':avgagecoefmemhighz,
                                'agediffpvalmemz':agediffpvalmemz,'agediffcoefmemz':agediffcoefmemz,'agediffcoefmemz_low':agediffcoefmemlowz,'agediffcoefmemz_high':agediffcoefmemhighz,
                                })
    

    print(ageeffectdfz.to_string())

        
    savefile = outputfolder + 'age_multimodel2.csv'
    ageeffectdf.to_csv(savefile)  

    savefile = outputfolder + 'age_multimodel2_z.csv'
    ageeffectdfz.to_csv(savefile)  








print("")
totaltimer = round(time.time()-totaltimer,3)
totaltimermin = round(totaltimer/60,3)
totaltimerhour = round(totaltimermin/60,3)
x = "All steps took " + str(totaltimer) + " s to run."
print(x)
x = "(which is " + str(totaltimermin) + " minutes)"
print(x)












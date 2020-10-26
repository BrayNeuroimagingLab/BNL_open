"""
Fingerprinter program
This program takes an individual's list of correlations, then tries to identify
which other list of correlations is most similar to it. Ideally it should be a second
scan from the same individual


Inputs into this program are generated from 06fittoparcellation

Made by Kirk Graff
kirk.graff@ucalgary.ca

Please email me if you have any questions :)
I'm not the best programmer so apologies if something is coded oddly!

"""




"""***********************"""
"""GENERAL PROGRAM OPTIONS"""
"""***********************"""
#what directory are your images saved in?
dir_start = '/Users/example/example/directory_with_all_MRI_scans_in_BIDS_format/'

#where do you want to save outputs of fingerprinting tests
saveoutputs = '/Users/example/example/fpoutputs/'


#if replacer is false, the program won't run if output image already exists
#if replacer is true, the program will write over outputs that already exist
replacer = False


#first item is the reg folder, second item is the file type in that folder
regfolders = [       
            ['BandpassCensorGSR/','YCDetFltRgwchvRemArBetPar325'],
            ['BandpassNoCensorGSR/','NCDetFltRgwchRemArBetPar325']
            ]



hierarchyfile = '/Users/example/example/Release/Hierarchy/MIST_PARCEL_ORDER.csv'
avgmotionname = 'task-movie_boldMcf.nii.gz_rel_mean.rms'
motionname = 'task-movie_boldMcf.nii.gz_rel.rms'

avgmotionaftercensor = 'task-movie_boldMcf.nii.gz_rel_mean_after_censor.rms'
avgmotionofcensor = 'task-movie_boldMcf.nii.gz_rel_mean_of_censored.rms'

agedf = '/Users/example/example/agedf.csv'


participants = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
imagesession = ["ses-0","ses-12"]


steps = ['groupcompare','groupcompareresults','matchbymotion']



numparcels = 325



#what files do you want to run through the fingerprinter?

#the first is the name of the file. The second is the folder it is in. Use 'main' if it's the main folder
#put !!! in the name instead of the number of parcels
fingerprintfiles = [
                   ['CorrForPar!!!_alltime_allnetworks.csv','main'],
                   ]




#only use the first fingerprint test? Gives expanded information
onefiletype = False




"""*****************************************"""
"""ANYTHING BELOW HERE DOESN'T NEED CHANGING"""
"""**********(OR SO KIRK HOPES)*************"""
"""*****************************************"""
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr  
import statsmodels.api as sm

participant_folders = os.listdir(dir_start)

if os.path.isdir(saveoutputs) == False:
    os.makedirs(saveoutputs)

hdf = pd.read_csv(hierarchyfile)
filetypes = []
filetypesnoq = []
filefolders = []
fileparcels = []
for types in fingerprintfiles:
    filetypes.append(types[0])
    filefolders.append(types[1])
    fileparcels.append(np.nan)
    



matchlist = []
ages = pd.read_csv(agedf,index_col=0)

if onefiletype == True:
    filetypes = [filetypes[0]]


for k in steps:
    if k == 'groupcompare':
        

        numscans = len(participants)*2
        matchrate = []
        matchpercent = []
        compcorr = []
        compcorrsd = []
        cmb = []
        acmb = []
        cmm = []
        cmmsd = []
        noncompmean = []
        noncompmeansd = []
        numconnections = []
        pipe = []
        tests = []  
        meancomprank = []                  
        
        
        
        for pipeline in regfolders:
            regfolder=pipeline[0]
            imgtype=pipeline[1]
        
        
        

            for filenum in range(len(filetypes)):
                filetype = filetypes[filenum]
                filetype = filetype.replace('!!!',str(numparcels))
                savefile = saveoutputs + 'fp_' + regfolder[:-1] + "_" + filetype
                
                doit = True
                if replacer == False:
                    if os.path.isfile(savefile) == True:
                        x = "Group compare did not run; file already exists for " + savefile
                        print(x)
                        doit = False
                if doit == True:
                    filetypes[filenum] = filetype
                    imgtype = imgtype.replace('!!!',str(numparcels))
                    scanlist = []
                    seslist = []
                    matchsuccess = []
                    matchbin = []
                    i = participants[0]
                    person = participant_folders[i]
                    j = imagesession[0]
                    if filefolders[filenum] == 'main':
                        datalink = dir_start + person + "/" + j + "/func/" + regfolder + imgtype + "/" + person + "_" + j + "_" + filetype
                    else:
                        datalink = dir_start + person + "/" + j + "/func/" + regfolder + imgtype + "/" + filefolders[filenum] + "/" + person + "_" + j + "_" + filetype
                    
                    if os.path.isfile(datalink) == False:
                        doit = False
                        print("Group compare did not run; file does not exist for " + datalink)
                    
                if doit == True:
                    print("Now running fingerprinting for " + regfolder + " " + filetype)
                    data = list(pd.read_csv(datalink)['distance'])
                    datadf = pd.DataFrame({'distance':data})
            
                    try:
                        for i in participants:
                            person = participant_folders[i]
                            for j in imagesession:
                                if filefolders[filenum] == 'main':
                                    datalink = dir_start + person + "/" + j + "/func/" + regfolder + imgtype + "/" + person + "_" + j + "_" + filetype
                                else:
                                    datalink = dir_start + person + "/" + j + "/func/" + regfolder + imgtype + "/" + filefolders[filenum] + "/" + person + "_" + j + "_" + filetype
                                
                                data = list(pd.read_csv(datalink)['weight'])
                                tempdf = pd.DataFrame({str(i) + j:data})
                                scanlist.append(str(i) + j)
                                seslist.append(j)
                                datadf = datadf.join(tempdf)
                    except:
                        print("Group compare did not run. You have a missing file somewhere, or something.")
                        doit = False
                    
                if doit == True:   
                    del datadf['distance']        
                    
                    for i in participants:
                        for j in imagesession:
                            datadf[str(i) + j] = np.arctanh(datadf[str(i) + j])
                    
            
                    numconnections.append(len(data))
                    #find correlations of each scan to every other scan
                    fpdf = datadf.corr()
                    
                    #ignore the correlations along the diagonal. Doesn't matter that scan1's corr with scan1 is 1.0
                    fpdf[fpdf==1] = 0
                    #convert to Fisher z score
                    fpdf = np.arctanh(fpdf)
                    matches = 0
                    fails = 0
                    complementscore = []
                    bestnoncomplementscore = []
                    meannoncomplementscore = []
                    compminusbestnon = []
                    adjcompminusbestnon = []
                    compminusmean = []
                    avgmotion = []
                    avgmotioncomp = []               
                    
                    agelist = []
                    agelistcomp = []
                    compwhere = []
                    
                    sexlist = []
                    tdlist = []
                    
                    for i in participants:
                        person = participant_folders[i]
                        for j in imagesession:
                            if j == 'ses-0':
                                altsession = 'ses-12'
                            if j == 'ses-12':
                                altsession = 'ses-0'
                            
                            if person[-3] == '6':
                                sexlist.append(0)
                                tdlist.append(1)
                            if person[-3] == '0':
                                sexlist.append(1)
                                tdlist.append(1)
                            
                            age = float(ages.loc[ages['scan'] == person + "_" + j]['age'])
                            agecomp = float(ages.loc[ages['scan'] == person + "_" + altsession]['age'])
                            agelist.append(age)
                            agelistcomp.append(agecomp)
                            avgmotionfile = dir_start + person + "/" + j + "/func/" + person + "_" + j + "_" + avgmotionname
                            avgmotionfilecomp = dir_start + person + "/" + altsession + "/func/" + person + "_" + altsession + "_" + avgmotionname
                            with open(avgmotionfile) as file:
                                for line in file:
                                    avgmotion.append(float(line))   
                            with open(avgmotionfilecomp) as file:
                                for line in file:
                                    avgmotioncomp.append(float(line)) 


                            
                            #for each scan, find its highest correlation                   
                            themax = fpdf[str(i)+j].idxmax()
                            #find the scan's correlation to its complement scan (2nd scan from same person)
                            comscore = fpdf[str(i)+j][str(i)+altsession]
                            complementscore.append(comscore)
                            scores = list(fpdf[str(i)+j])
                            scores.sort(reverse=True)
                            scores.remove(0)
                            compwhere.append(scores.index(comscore))
                            scores.remove(fpdf[str(i)+j][str(i)+altsession])
                            bestnoncomplementscore.append(scores[0])
                            meannoncomplementscore.append(sum(scores)/len(scores))
                            
                            #if the highest corr is also the corr to the complement, then it's a match!
                            if themax == str(i) + altsession:
                                #print("Match! For " + person + " " + j + " the best match is " + person + " " + altsession)
                                matchsuccess.append("Yes: " + themax)
                                matches = matches + 1
                                matchbin.append(1)
                             
                            #this part is a bit janky. Some of the scans had a 1 digit ID #, some had a 2 digit #.
                            #e.g. participant 5 vs participant 16
                            #This accounts for that    
                            else:
                                if themax[1] == 's':
                                    thekid = participant_folders[int(themax[0])]
                                    theses = (themax[1:])
                                    matchsuccess.append("No: " + themax)
                                    matchbin.append(0)
                                    #print("Fail! For " + person + " " + j + " the best match is " + thekid + " " + theses)
                                elif themax[2] == 's':
                                    thekid = participant_folders[int(themax[0:2])]
                                    theses = (themax[2:])
                                    matchsuccess.append("No: " + themax)
                                    matchbin.append(0)
                                    #print("Fail! For " + person + " " + j + " the best match is " + thekid + " " + theses)   
                                fails = fails + 1
                    
                    for item in range(len(complementscore)):
                        compminusbestnon.append(complementscore[item]-bestnoncomplementscore[item])
                        adjcompminusbestnon.append((complementscore[item]-bestnoncomplementscore[item])*400+50)
                        compminusmean.append(complementscore[item]-meannoncomplementscore[item])
                        
                    matchdf = pd.DataFrame({'scan':scanlist,'session':seslist,'complement':complementscore,'match?':matchsuccess,'comprank':compwhere,'matchbin':matchbin,'bestnoncomp':bestnoncomplementscore,'mean':meannoncomplementscore,'compminusbestnon':compminusbestnon,'adjcompminusbestnon':adjcompminusbestnon,'compminusmean':compminusmean,'avgmotion':avgmotion,'avgmotioncomp':avgmotioncomp,'age':agelist,'agecomp':agelistcomp,'sex':sexlist,'td':tdlist})

                    matchdf.to_csv(savefile,index=False)
                    print("Data saved to " + savefile)
                                            
                        
    if k == 'groupcompareresults':                        
                        
        numscans = len(participants)*2
        matchrate = []
        matchpercent = []
        compcorr = []
        compcorrsd = []
        cmb = []
        acmb = []
        cmm = []
        cmmsd = []
        bestnoncomp = []
        noncompmean = []
        noncompmeansd = []
        numconnections = []
        pipe = []
        tests = []  
        meancomprank = []                  
        
           
        for pipeline in regfolders:
            regfolder=pipeline[0]
            imgtype=pipeline[1]
              

            for filenum in range(len(filetypes)):
                filetype = filetypes[filenum]
                filetype = filetype.replace('!!!',str(numparcels))
                imgtype = imgtype.replace('!!!',str(numparcels))
                
                #this is the saved matchdf
                openfile = saveoutputs + 'fp_' + regfolder[:-1] + "_" + filetype                        

                #check if the matchdf exists
                if os.path.isfile(openfile) == False:
                    x = "Group compare results did not run; this file doesn't exist " + openfile
                    print(x)
                else:
                    
                    #get how many connections by opening up the first file and counting how many connections there are
                    person = participant_folders[participants[0]]
                    j = imagesession[0]
                    if filefolders[filenum] == 'main':
                        datalink = dir_start + person + "/" + j + "/func/" + regfolder + imgtype + "/" + person + "_" + j + "_" + filetype
                    else:
                        datalink = dir_start + person + "/" + j + "/func/" + regfolder + imgtype + "/" + filefolders[filenum] + "/" + person + "_" + j + "_" + filetype
                    data = list(pd.read_csv(datalink)['weight'])
                    numconnections.append(len(data)) 
                    
                    #read in the already saved match df
                    matchdf = pd.read_csv(openfile)    
                
                    meancompminusbestnon = sum(matchdf['compminusbestnon'])/len(matchdf['compminusbestnon'])
                    meanadjcompminusbestnon = sum(matchdf['adjcompminusbestnon'])/len(matchdf['adjcompminusbestnon'])
                    meancompminusmean = sum(matchdf['compminusmean'])/len(matchdf['compminusmean'])
                    meancomplement = sum(matchdf['complement'])/len(matchdf['complement'])
                    meangroup = sum(matchdf['mean'])/len(matchdf['mean'])
                                    
                    totaltests = len(matchdf['matchbin'])
            
                    bestnoncomp.append(sum(matchdf['bestnoncomp'])/len(matchdf['bestnoncomp']))
                    matchrate.append(str(sum(matchdf['matchbin'])) + "/" + str(totaltests))
                    matchpercent.append(sum(matchdf['matchbin'])/totaltests*100)
                    compcorr.append(meancomplement)
                    compcorrsd.append(np.std(matchdf['complement']))
                    cmb.append(meancompminusbestnon)
                    acmb.append(meanadjcompminusbestnon)
                    cmm.append(meancompminusmean)
                    cmmsd.append(np.std(matchdf['compminusmean']))
                    noncompmean.append(meangroup)
                    noncompmeansd.append(np.std(matchdf['mean']))
                    pipe.append(regfolder)
                    tests.append(filetype)
                    meancomprank.append(sum(matchdf['comprank'])/len(matchdf['comprank']))
        
                    if onefiletype == True:
                        print("")
                        #matchdf = matchdf.loc[matchdf['session'] == 'ses-0'] 
                        print(matchdf.to_string())
                        print("")
                        matchdfcorr = matchdf.corr()
                        print(matchdfcorr.to_string())
        
        if len(pipe) > 0:
            testdf = pd.DataFrame({'pipe':pipe,'test':tests,'match rate':matchrate,'match%':matchpercent,'comp rank':meancomprank,'bestnoncomp':bestnoncomp,'complement corr':compcorr,'complement sd':compcorrsd,'group corr':noncompmean,'group sd':noncompmeansd,'complement-best':cmb,'adjcomp-best':acmb,'complement-mean':cmm,'cmmsd':cmmsd,'connections':numconnections})        
    
            
            matchscore = testdf['match%']
            
            print(round(testdf.sort_values(by=['test','pipe']),3).to_string())
            
            for pipeline in regfolders:
                regfolder=pipeline[0]
                xx = testdf.loc[testdf['pipe'] == regfolder]
                fpmean = sum(xx['match%'])/len(xx['match%'])
                print("For pipe " + regfolder + " mean match rate is " + str(fpmean))
    

            print("")


    if k == 'matchbymotion':                        
                        

        motcmb = []
        motcmm = []

        omotcmb = []
        omotcmm = []
        cmotcmb = []
        cmotcmm = []
        
        modelr2 = []
        modelavgmot = []
        modelcavgmot = []
        summodelmot = []
        cmmnomot = []
        cmmmedmot = []
        cmm3rdmot = []

        pipe = []
        tests = []  
        cmwhat = []
             

        regfolder = regfolders[0][0]
        imgtype = regfolders[0][1]
        filetype = filetypes[0]
        filetype = filetype.replace('!!!',str(numparcels))
        imgtype = imgtype.replace('!!!',str(numparcels))        

        openfile = saveoutputs + 'fp_' + regfolder[:-1] + "_" + filetype                        

        #check if the matchdf exists
        if os.path.isfile(openfile) == False:
            x = "Group compare results did not run; this file doesn't exist " + openfile
            print(x)
        else:
            
            #get how many connections by opening up the first file and counting how many connections there are
            person = participant_folders[participants[0]]
            j = imagesession[0]
            if filefolders[filenum] == 'main':
                datalink = dir_start + person + "/" + j + "/func/" + regfolder + imgtype + "/" + person + "_" + j + "_" + filetype
            else:
                datalink = dir_start + person + "/" + j + "/func/" + regfolder + imgtype + "/" + filefolders[filenum] + "/" + person + "_" + j + "_" + filetype
            data = list(pd.read_csv(datalink)['weight'])
            numconnections.append(len(data)) 
            
            #read in the already saved match df
            matchdf = pd.read_csv(openfile)
            cmbpipedf = matchdf[["avgmotion", "avgmotioncomp"]].copy()
            cmbpipedf['worstmot'] = cmbpipedf[["avgmotion", "avgmotioncomp"]].max(axis=1)            


        for pipeline in regfolders:
            regfolder=pipeline[0]
            imgtype=pipeline[1]
              

            for filenum in range(len(filetypes)):
                filetype = filetypes[filenum]
                filetype = filetype.replace('!!!',str(numparcels))
                imgtype = imgtype.replace('!!!',str(numparcels))
                
                #this is the saved matchdf
                openfile = saveoutputs + 'fp_' + regfolder[:-1] + "_" + filetype                        

                #check if the matchdf exists
                if os.path.isfile(openfile) == False:
                    x = "Group compare results did not run; this file doesn't exist " + openfile
                    print(x)
                else:
                    
                    #get how many connections by opening up the first file and counting how many connections there are
                    person = participant_folders[participants[0]]
                    j = imagesession[0]
                    if filefolders[filenum] == 'main':
                        datalink = dir_start + person + "/" + j + "/func/" + regfolder + imgtype + "/" + person + "_" + j + "_" + filetype
                    else:
                        datalink = dir_start + person + "/" + j + "/func/" + regfolder + imgtype + "/" + filefolders[filenum] + "/" + person + "_" + j + "_" + filetype
                    data = list(pd.read_csv(datalink)['weight'])
                    numconnections.append(len(data)) 
                    
                    #read in the already saved match df
                    matchdf = pd.read_csv(openfile)
                    
                    medmotion = np.percentile(matchdf['avgmotion'],50)
                    thirdquartmotion = np.percentile(matchdf['avgmotion'],75)
                    
                    
                    omotcmmcorr = pearsonr(matchdf['avgmotion'],matchdf['compminusmean'])[0]
                    omotcmbcorr = pearsonr(matchdf['avgmotion'],matchdf['compminusbestnon'])[0]
                    cmotcmmcorr = pearsonr(matchdf['avgmotioncomp'],matchdf['compminusmean'])[0]
                    cmotcmbcorr = pearsonr(matchdf['avgmotioncomp'],matchdf['compminusbestnon'])[0]

                    omotcmb.append(omotcmbcorr)
                    omotcmm.append(omotcmmcorr)
                    cmotcmb.append(cmotcmbcorr)
                    cmotcmm.append(cmotcmmcorr)      
                
                    ses0mot = []
                    ses12mot = []
                    ses0cmb = []
                    ses12cmb = []
                    ses0cmm = []
                    ses12cmm = []


                    matchdf['worstmot'] = matchdf[["avgmotion", "avgmotioncomp"]].max(axis=1)

                    cmblist = list(matchdf['compminusbestnon'])
                    tempdf = pd.DataFrame({regfolder:cmblist})
                    cmbpipedf = cmbpipedf.join(tempdf)





                    regdf = matchdf[['avgmotion','avgmotioncomp']].copy()
                    regdf = sm.add_constant(regdf)
                    
                    #create the model. Predict y (the time series) as a function of X (all the nuisance regressors)
                    model = sm.OLS(matchdf[['compminusmean']],regdf).fit()
                    
                    
                    yintercept = model.params['const']
                    motparam = model.params['avgmotion']     
                    cmotparam = model.params['avgmotioncomp']
                    motparamsum = motparam + cmotparam
                    r2_model = model.rsquared

                    modelr2.append(r2_model)
                    modelavgmot.append(motparam)
                    modelcavgmot.append(cmotparam)
                    summodelmot.append(motparamsum)
                    
                    cmmnomot.append(yintercept)
                    cmmmedmot.append(yintercept + motparam*medmotion + cmotparam*medmotion)
                    cmm3rdmot.append(yintercept + motparam*thirdquartmotion + cmotparam*thirdquartmotion)

                    pipe.append(regfolder)
                    tests.append(filetype)
                    cmwhat.append('compminusmean')

                    model = sm.OLS(matchdf[['compminusmean']],regdf).fit()
                    
                    
                    #create the model. Predict y (the time series) as a function of X (all the nuisance regressors)
                    model = sm.OLS(matchdf[['compminusbestnon']],regdf).fit()                    
                    yintercept = model.params['const']
                    motparam = model.params['avgmotion']     
                    cmotparam = model.params['avgmotioncomp']
                    motparamsum = motparam + cmotparam
                    r2_model = model.rsquared

                    modelr2.append(r2_model)
                    modelavgmot.append(motparam)
                    modelcavgmot.append(cmotparam)
                    summodelmot.append(motparamsum)
                    
                    cmmnomot.append(yintercept)
                    cmmmedmot.append(yintercept + motparam*medmotion + cmotparam*medmotion)
                    cmm3rdmot.append(yintercept + motparam*thirdquartmotion + cmotparam*thirdquartmotion)

                    pipe.append(regfolder)
                    tests.append(filetype)
                    cmwhat.append('compminusbest')
        
        
                    if onefiletype == True:
                        print("")
                        print(matchdf.to_string())
                        print("")
        
        plt.show()
        if len(pipe) > 0:
            #testdf = pd.DataFrame({'pipe':pipe,'test':tests,'corr avg motion vs avg cmm':motcmm,'corr avg motion vs avg cmb':motcmb,'corr motion vs cmb':omotcmb,'corr motion vs cmm':omotcmm,'corr comp motion vs cmb':cmotcmb,'corr comp motion vs cmm':cmotcmm})        
            testdf = pd.DataFrame({'pipe':pipe,'test':tests,'comparison':cmwhat,'motion r2':modelr2,'avgmotparam':modelavgmot,'comp avgmotparam':modelcavgmot,'sum of params':summodelmot,'no motion':cmmnomot,'median motion':cmmmedmot,'3rd quart motion':cmm3rdmot})
            #del testdf['sum of params']
            #testdf = testdf[testdf['comparison'] == 'compminusmean']
    
            testdf_sort = testdf.sort_values(by=['comparison','test','pipe'])

            print(round(testdf_sort,3).to_string())

            #print(round(testdf,3).to_string())
            print("")
            
            




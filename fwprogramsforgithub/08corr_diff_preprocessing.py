"""
This program finds the correlation between a participant's FC data when preprocessed in different ways


Inputs into this program are list of FC values for a scan
You need at least 2 per scan from 2 (or more) different preprocessing pipelines
Inputs into this program are generated from 06fittoparcellation

Made by Kirk Graff
kirk.graff@ucalgary.ca

Please email me if you have any questions :)
I'm not the best programmer so apologies if something is coded oddly!


Make sure your scans are in BIDS format before running
Edit the things near the top, and the program should run fine!

"""




"""***********************"""
"""GENERAL PROGRAM OPTIONS"""
"""***********************"""
#what directory are your images saved in?
dir_start = '/Users/example/example/directory_with_all_MRI_scans_in_BIDS_format/'

hierarchyfile = '/Users/example/example/Release/Hierarchy/MIST_PARCEL_ORDER.csv'
avgmotionname = 'task-movie_boldMcf.nii.gz_rel_mean.rms'
#df showing how old were participants at time of scan
agedf = '/Users/example/example/agedf.csv'


participants = [1,2,3,4,5]
imagesession = ["ses-0","ses-12"]


numparcels = 325



#what pipelines are you comparing?
imagetypes = [      
            ['BandpassCensorGSR/','YCDetFltRgwchvRemArBetPar325'],
            ['BandpassNoCensorGSR/','NCDetFltRgwchRemArBetPar325']]





#what files do you want to run this with?
#the first is the name of the file. The second is the folder it is in. Use 'main' if it's the main folder
#put !!! in the name instead of the number of parcels
fingerprintfiles = [['CorrForPar!!!_alltime_allnetworks.csv','main']]







#motion quartiles to include. If you want to include all scans, use 1,2,3,4
motquarts = [1,2,3,4]






"""*****************************************"""
"""ANYTHING BELOW HERE DOESN'T NEED CHANGING"""
"""**********(OR SO KIRK HOPES)*************"""
"""*****************************************"""
import pandas as pd
import numpy as np
import os

participant_folders = os.listdir(dir_start)


hdf = pd.read_csv(hierarchyfile)
filetypes = []
filefolders = []
fileparcels = []
for types in fingerprintfiles:
    filetypes.append(types[0])
    filefolders.append(types[1])
    fileparcels.append(np.nan)
    




#matchlist = []
ages = pd.read_csv(agedf,index_col=0)



avgmotion = []
avgmotquart = []

idlist = []

#avgmotquart = [np.nan]
for i in participants:
    person = participant_folders[i]
    for j in imagesession:              
        idlist.append([person,j])
        age = float(ages.loc[ages['scan'] == person + "_" + j]['age'])
        avgmotionfile = dir_start + person + "/" + j + "/func/" + person + "_" + j + "_" + avgmotionname
        with open(avgmotionfile) as file:
            for line in file:
                avgmotion.append(float(line))  
mot25 = np.percentile(avgmotion,25)
mot50 = np.percentile(avgmotion,50)
mot75 = np.percentile(avgmotion,75)
for num in range(len(avgmotion)):
    item = avgmotion[num]
    idlist[num].append(avgmotion[num])
    if item > mot75:
        avgmotquart.append(4)
        idlist[num].append(4)
    elif item > mot50:
        avgmotquart.append(3)
        idlist[num].append(3)
    elif item > mot25:
        avgmotquart.append(2)
        idlist[num].append(2)
    else:
        avgmotquart.append(1)
        idlist[num].append(1)






#list of connections to be removed cause they're duplicates
droplistdup = []

edge1list = []
edge2list = []
for num in range(len(imagetypes)):
    edge1column = [num+1]*len(imagetypes)
    edge1list.extend(edge1column)
    edge2list.append(num+1)
edge2list = edge2list*len(imagetypes)

fulllist = list(range(0,len(imagetypes)*len(imagetypes)))                           
for num in fulllist:
    if edge1list[num] >= edge2list[num]:
        #this removes all the duplicates (i.e. 1 to 2 is the same as 2 to 1)
        droplistdup.append(num)




        
        
numscans = len(participants)*2
matchrate = []
matchpercent = []
compcorr = []
cmb = []
acmb = []
cmm = []
numconnections = []
for filenum in range(len(filetypes)):
    filetype = filetypes[filenum]
    filetype = filetype.replace('!!!',str(numparcels))
    print("Now running intrasubject comparison for " + filetype)
    filetypes[filenum] = filetype
    scanlist = []
    seslist = []
    matchsuccess = []
    matchbin = []

    #create a df of within brain edge strengths for different pipelines
    i = participants[0]
    person = participant_folders[i]
    j = imagesession[0]
    pipeline = imagetypes[0]
    if filefolders[filenum] == 'main':
        datalink = dir_start + person + "/" + j + "/func/" + pipeline[0] + pipeline[1] + "/" + person + "_" + j + "_" + filetype
    else:
        datalink = dir_start + person + "/" + j + "/func/" + pipeline[0] + pipeline[1] + "/" + filefolders[filenum] + "/" + person + "_" + j + "_" + filetype
    data = list(pd.read_csv(datalink)['distance'])
    datadforig = pd.DataFrame({'distance':data})
    datadf = datadforig.copy()
                    
    for pipeline in imagetypes:
        if filefolders[filenum] == 'main':
            datalink = dir_start + person + "/" + j + "/func/" + pipeline[0] + pipeline[1] + "/" + person + "_" + j + "_" + filetype
        else:
            datalink = dir_start + person + "/" + j + "/func/" + pipeline[0] + pipeline[1] + "/" + filefolders[filenum] + "/" + person + "_" + j + "_" + filetype
        data = list(pd.read_csv(datalink)['weight'])
        tempdf = pd.DataFrame({pipeline[0]:data})
        tempdf = np.arctanh(tempdf[pipeline[0]])
        datadf = datadf.join(tempdf)

    del datadf['distance']        

    #create a list of all the different pipeline comparisons
    comparisondftemp = datadf.corr()
    comparisondftemp[comparisondftemp > 0] = 0
    
    #remove duplicate comparisons
    links = comparisondftemp.stack().reset_index()
    links.columns = ['pipe1', 'pipe2','corr']
    linksall = links.drop(droplistdup) 

    #create a list of all the different comparisons between piplines. 1v2, 1v3, etc etc
    comparisons = []

    for ro in range(len(linksall)):
        header = linksall.iloc[ro].pipe1[0:3] + "_" + linksall.iloc[ro].pipe2[0:3]
        comparisons.append(header)
        

        
    allcorrz = []     
    persons = []
    sessions = []
    avgmotion = []
    agelist = []
    meancorr = []


    
    #for each person and session, create a dataframe of all their edge correlations for different pipelines
    #there's some redundancy in those code because I'm too lazy to fix it
    for scanofint in idlist:
        person = scanofint[0]
        j = scanofint[1]
        
        if scanofint[3] in motquarts:
        
            print("Running for " + person + " " + j)
            age = float(ages.loc[ages['scan'] == person + "_" + j]['age'])
            agelist.append(age)
            avgmotionfile = dir_start + person + "/" + j + "/func/" + person + "_" + j + "_" + avgmotionname
            with open(avgmotionfile) as file:
                for line in file:
                    avgmotion.append(float(line))   

            datadf2 = datadforig.copy()
            
            for pipeline in imagetypes:
                if filefolders[filenum] == 'main':
                    datalink = dir_start + person + "/" + j + "/func/" + pipeline[0] + pipeline[1] + "/" + person + "_" + j + "_" + filetype
                else:
                    datalink = dir_start + person + "/" + j + "/func/" + pipeline[0] + pipeline[1] + "/" + filefolders[filenum] + "/" + person + "_" + j + "_" + filetype
                data = list(pd.read_csv(datalink)['weight'])
                tempdf = pd.DataFrame({pipeline[0]:data})
                tempdf = np.arctanh(tempdf[pipeline[0]])
                datadf2 = datadf2.join(tempdf)
    
            del datadf2['distance']        

            #correlate the different edge correlations, to see how similar different pipelines are for 1 scan
            comparisondf = datadf2.corr()
            comparisondf[comparisondf == 1] = 0
            comparisondf = np.arctanh(comparisondf)

            #add comparisondf to master comparison df, to find mean
            comparisondftemp = comparisondftemp + comparisondf
            
            #remove duplicates
            links = comparisondf.stack().reset_index()
            links.columns = ['pipe1', 'pipe2','corr']
            linksall = links.drop(droplistdup)
            
            #add the list of correlations to a list of lists, to eventually become a df
            corrz = list(linksall['corr'])
            allcorrz.append(corrz)
            
            #calculate mean correlation
            meancorr.append(sum(corrz)/len(corrz))
            
            persons.append(person)
            sessions.append(j)
            

    #turn list of pipeline correlations for each person into a list of scan scores for each pipeline comparison
    transposedcorrelations = list(map(list, zip(*allcorrz)))
    #create df of these correlations
    #zacdf has z scores instead of raw correlations
    acdf = pd.DataFrame({'person':persons,'ses':sessions,'age':agelist,'avgmotion':avgmotion,'meancorr':meancorr})
    zacdf = acdf.copy()
    meancomp = sum(zacdf['meancorr'])/len(zacdf['meancorr'])
    meancomp = np.tanh(meancomp)
    acdf['meancorr'] = np.tanh(acdf['meancorr'])
    acdfmini = acdf.copy()
    for xx in range(len(transposedcorrelations)):
        header = comparisons[xx]
        data = transposedcorrelations[xx]
        tempdf = pd.DataFrame({header:data})
        zacdf = zacdf.join(tempdf)
        tempdf = np.tanh(tempdf)
        acdf = acdf.join(tempdf)
    
    print("")
    print(acdf.to_string()) 
    #print(acdfmini.to_string())
    print("")

    print("Overall, the mean intrasubject mean is " + str(meancomp))
    print("")
    
    comparisondftemp = comparisondftemp/len(acdf)
    comparisondftemp = np.tanh(comparisondftemp)
    
    comparisondftemp[comparisondftemp == 0] = 1
    
    #this copies the dataframe for the plotting program
    compdfforgraphs = comparisondftemp.copy()
    #compdfforgraphslow = comparisondftemp.copy()
    #compdfforgraphshigh  = comparisondftemp.copy()
    
    print(compdfforgraphs)


       
    





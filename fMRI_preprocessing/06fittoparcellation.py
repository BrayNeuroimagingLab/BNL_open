"""
This program takes a denoised 4D volume, warps it into MNI space (based on a previously completed transformation with the registration program)
then fits all the time series data into parcellations. Then generations correlations based on the time series in those parcels

Currently this is designed for the MIST parcellation
It will generate correlations for whole brain, each network, time subs, randomly, and for each parcel

Run this program after 05makesstandregtosst and after 04advfuncpreprocessing


This program also does QC-FC stuff for each pipeline


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

#summary for QC-FC stuff
summaryfolder = '/Users/example/example/pipelinesummary/'

dir_parcellation_masks = '/Users/example/example/mist_parcellation_masks/'

#regression sub folder. Where the input is saved    
regfolder = 'BandpassCensorGSR/'

#what network does each parcel belong to?
hierarchyfile = '/Users/example/example/Release/Hierarchy/MIST_PARCEL_ORDER.csv'

#parcel location file. Will add "xx.csv" to the end, where xx is the number of parcels
locationfile = '/Users/example/example/Release/Parcel_Information/MIST_'

#your template and its mask, and the parcellation mask
templateimage = '/Users/example/example/SST.nii.gz'
templatemask = '/Users/example/example/SST_mask.nii.gz'


#what participants do you want this to run on? e.g. [1,2,3] or list(range(1,4))
#this is based on the files in the directory. 0 = first file in directory
participants = [0,1,2,3,4,5,6,7,9,10,11,20,21,22,23,24,25]


#do you want to run on ses-0, ses-12, or both? If both, type ["ses-0","ses-12"]
imagesession = ["ses-0","ses-12"]

#if replacer is false, the program won't run if output image already exists
#if replacer is true, the program will write over outputs that already exist
replacer = False

steps = ['warpimage','parcellation','deleter','basiccorrelation','qcfc']

#name of log book that output is saved to
logname = 'xparcellator.txt'



#how many minutes of data should all scans have at a minimum?
sharedmaxage = 11 

"""*************"""
"""OTHER OPTIONS"""
"""*************"""
#from func folder
warpmatrix = 'transformBOLDtoSST.h5'
applybetmask = 'task-movie_boldStcRefArBet_mask'


#from regression folder
inputimage = "YCDetFltRgwchvRem"
warpedimage = "YCDetFltRgwchvRemAr"
warpedimagebet = "YCDetFltRgwchvRemArBet"

tmaskname = "MASK_TEMPORAL"

#what is the name of the file that contains the average amount of head motion? Used for QC-FC
avgmotionname = 'task-movie_boldMcf.nii.gz_rel_mean.rms'


#mask file, output name, number of parcels. For as many parcellations as you want
#e.g. monpar = [['mist444_SSTJune26.nii.gz','StcMcfDetIntFltRegRemPar444.csv',444]]
#if using MISTATOM, mistatom_SST.nii.gz, 'YCDetFltRgwchvRemArBetPar1095',1095


monpar = [['mist325.nii.gz','YCDetFltRgwchvRemArBetPar325',325]]


#note: for parcellations, program assumes 0 = region of no interest (e.g. out of brain, or csf) then numofparcels = number of regions of interest
#so in a sense there are numofparcels+1 different parcels. For monpar, only go with the number of regions of interest


#which of the above parcellations files do you want to use?
#0 = the first parcellation listed, 1 = the second, etc. If only using one parcellation, use corrparcellation = [0]
corrparcellations = [0]

#which parcellation do you want to use to calculate qcfc values?
qcfcparcellations = [0]


qcfcplotfolder = '/Users/example/example/pipelinesummary/qcfcplots/'
saveqcfcplots = False
saveqcfcdata = False




"""*****************************************"""
"""ANYTHING BELOW HERE DOESN'T NEED CHANGING"""
"""**********(OR SO KIRK HOPES)*************"""
"""*****************************************"""

import nipype.interfaces.fsl as fsl
import nipype.interfaces.ants as ants
import os
import numpy as np
import pandas as pd
import nibabel as nib
import matplotlib.pyplot as plt
import time
#from shutil import copyfile
from scipy.stats.stats import pearsonr  
from scipy.stats import linregress





if os.path.isdir(qcfcplotfolder) == False:
    os.makedirs(qcfcplotfolder)






#get the current time
totaltimer = time.time()

#get a list of everything in the starting directory
participant_folders = os.listdir(dir_start)

#everything in log gets saved to the logbook. Text often gets appended to log
log = ["*************************************************"]
log.append('Starting log for ' + time.ctime())


for i in participants:
    person = participant_folders[i]
    for j in imagesession:
        dir_in = dir_start + person + "/" + j + "/func/"
        imagefile = dir_in + regfolder + person + "_" + j + "_" + inputimage + ".nii.gz"
        image_mask = dir_in + person + "_" + j + "_" + applybetmask + ".nii.gz"
        warpedimagefile = dir_in + regfolder + person + "_" + j + "_" + warpedimage + ".nii.gz"
        warpedimagefilebet = dir_in + regfolder + person + "_" + j + "_" + warpedimagebet + ".nii.gz"
        parcellationfile1 = dir_in + regfolder + str(monpar[0][1]) + "/" + person + "_" + j + "_" + str(monpar[0][1]) + ".csv"
        tmaskfile = dir_in + regfolder + person + "_" + j + "_" + tmaskname
        
        #determine the timepoints marked for censoring
        index = []
        currentline = 0
        with open(tmaskfile) as file:
            for line in file:
                if int(line) == 0:
                    index.append(currentline)
                currentline = currentline + 1        
                               
        #make folders for the different parcellations        
        for par in monpar:
            newfolder = dir_in + regfolder + str(par[1]) + "/"
            if not os.path.exists(newfolder):
                os.makedirs(newfolder)            
    
    
        for k in steps:
            if k == 'warpimage': 
                steptimer = time.time()               
                if os.path.isfile(imagefile) == False:
                    x = "This file doesn't exist: " + imagefile
                    print(x)
                    log.append(x)
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(warpedimagefile) == True:
                            x = "Apply Transforms did not run; file already exists for " + warpedimagefile
                            print(x)
                            log.append(x)
                            doit = False
                        if doit == True:
                            if os.path.isfile(parcellationfile1) == True: 
                                x = "Apply Transforms did not run; file already exists for " + parcellationfile1
                                print(x)
                                log.append(x)
                                doit = False
                    if doit == True:    
                        os.chdir(dir_in)
                    
                        x = "Applying Transform for " + imagefile
                        print(x)
                        log.append(x)                            
                    
                        myaat = ants.ApplyTransforms()
                        myaat.inputs.reference_image = templateimage
                        myaat.inputs.transforms = warpmatrix
                        #for some reason image type 3 means it's 4D
                        myaat.inputs.input_image_type = 3
                    
                        myaat.inputs.input_image = imagefile                        
                        myaat.inputs.output_image = warpedimagefile
                        myaat.run()
                        
                        mymath = fsl.ImageMaths()
                        mymath.inputs.in_file = warpedimagefile
                        mymath.inputs.out_file = warpedimagefilebet
                        mymath.inputs.args = "-mul " + image_mask
                        mymath.run()      
                        
                        steptimer = round(time.time()-steptimer,3)
                        x = "Individual step took " + str(steptimer) + " s to run."
                        print(x)
                        log.append(x)
                        steptimermin = round(steptimer/60,3)
                        x = "(which is " + str(steptimermin) + " minutes)"
                        print(x)
                        log.append(x)


            if k == 'parcellation': 
                steptimer = time.time()               
                if os.path.isfile(warpedimagefilebet) == False:
                    x = "This file doesn't exist: " + warpedimagefilebet
                    print(x)
                    log.append(x)
                else:
                    doit = True
                    if replacer == False:
                        if os.path.isfile(parcellationfile1) == True:
                            x = "Turn to parcellation did not run; file already exists for " + parcellationfile1
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:    
                        os.chdir(dir_in)
                    
                        x = "Creating parcellation files for " + warpedimagefilebet
                        print(x)
                        log.append(x)                                
    
                        #load the image using some package I found called NiBabel
                        img = nib.load(warpedimagefilebet)
                        image_data = img.get_fdata()
                              
                        #load the mask
                        img2 = nib.load(image_mask)
                        mask_data = img2.get_fdata()
                        
                        #get shape of image data
                        shape = image_data.shape
                        dim_x = shape[0]
                        dim_y = shape[1]
                        dim_z = shape[2]
                        dim_t = shape[3]               
    
                        timelist = list(range(0,dim_t))
                        #a list as long as the timelist, but of only zeros
                        fakeseries = [0] * len(timelist)

                        #create the list of times that do not need censoring
                        timesteps_subset = np.delete(timelist, index)

                        for pn in range(len(monpar)):
                            
                            #output
                            parcellationfile = dir_in + regfolder + monpar[pn][1] + "/" + person + "_" + j + "_" + monpar[pn][1] + ".csv"

                            x = "Creating parcellation file " + parcellationfile
                            print(x)
                            log.append(x) 

                            #load the parcellation
                            img3 = nib.load(dir_parcellation_masks + monpar[pn][0])
                            parcellation = img3.get_fdata()                                          
        
                            #list of possible parcels. Including 0, the "non-parcel" (the space between parcels)
                            parcellist = list(range(0,monpar[pn][2]+1))
                            #this is the number of voxels in each parcel
                            voxelcountlist = [0]*len(parcellist)
        
                            #sumserieslist is a timeseries for each parcel. So a list of lists
                            sumserieslist = [fakeseries]*len(parcellist)
                                                                                        
                            #loop over every possible voxel in 3D space, add time series to the relevant parcel series
                            for dimi in range(dim_x):
                                print("Running for x dimension slice " + str(dimi + 1) + " of " + str(dim_x) + " for " + person + " " + j + " for parcellation " + monpar[pn][0])
                                for dimj in range(dim_y):
                                    for dimk in range(dim_z):                              
                                        if mask_data[dimi][dimj][dimk] == 1:
                                            #what parcel does this voxel belong to?
                                            whatparcel = int(parcellation[dimi][dimj][dimk])
                                            #say that there's another voxel within the parcel of interest
                                            voxelcountlist[whatparcel] = voxelcountlist[whatparcel] + 1
                                            #what is the series of the voxel in question?
                                            currentseries = image_data[dimi][dimj][dimk]
                                            #load the sumseries for the parcel in question
                                            currentsum = sumserieslist[whatparcel]
                                            #for every point in the current series, add it to the sum series
                                            newcurrentsum = [currentseries[i]+currentsum[i] for i in range(len(currentseries))]
                                            #put this new sumseries into the sumserieslist
                                            sumserieslist[whatparcel] = newcurrentsum
                                
                            #this is the average time series for each parcel
                            parcelserieslist = []
                            for i in range(len(sumserieslist)):
                                #divide the sumseries by the number of voxels, i.e. create an average
                                parcelseries = [elem/voxelcountlist[i] for elem in sumserieslist[i]]                               
                                parcelserieslist.append(parcelseries)
                            
                            #create a dataframe of parcel ID# and its time series
                            parceldf = pd.DataFrame({'parcelnum':parcellist,'meanseries':parcelserieslist})
        
                            #remove parcel 0, as it isn't a parcel, but rather the space between parcels
                            newdf = parceldf.copy()
                            newdf = newdf.drop([0]) 
                            newdf = newdf.reset_index(drop=True)
                            
                            #create a dataframe of the timepoints
                            datadf = pd.DataFrame({'time':timelist})
                            
                            #for each parcel, add it to the timepoints dataframe
                            for i in range(len(newdf.meanseries)):
                                header = 'parcel' + str(i+1)
                                tempdf = pd.DataFrame({header :newdf.meanseries[i]})
                                datadf = datadf.join(tempdf)
                                
                            datadfpartial = datadf.copy()
                            
                            #remove the censored timepoints
                            for i in range(len(datadfpartial['time'])):
                                if datadfpartial['time'][i] not in timesteps_subset:
                                    datadfpartial = datadfpartial.drop([i])
                            
                            #remove the timepoints from the dataframe, since they're not actually importants   
                            del datadf['time']
                            del datadfpartial['time']
    
                            datadfpartial = datadfpartial.reset_index(drop=True)
          
                            #save the parcellation file
                            datadfpartial.to_csv(parcellationfile)
                        
                        steptimer = round(time.time()-steptimer,3)
                        x = "Individual step took " + str(steptimer) + " s to run."
                        print(x)
                        log.append(x)
                        steptimermin = round(steptimer/60,3)
                        x = "(which is " + str(steptimermin) + " minutes)"
                        print(x)
                        log.append(x)


            if k == 'deleter': 
                if os.path.isfile(warpedimagefile) == True:
                    os.remove(warpedimagefile)
                    x = "You have deleted " + warpedimagefile
                    print(x)
                    log.append(x)
                else:
                    x = "This file doesn't exist so it can't be deleted " + warpedimagefile
                    print(x)
                    log.append(x)                    
                    
                if os.path.isfile(warpedimagefilebet) == True:
                    os.remove(warpedimagefilebet)
                    x = "You have deleted " + warpedimagefilebet
                    print(x)
                    log.append(x)
                else:
                    x = "This file doesn't exist so it can't be deleted " + warpedimagefilebet
                    print(x)
                    log.append(x)                        
                    
                                       
            if k == 'basiccorrelation':
                steptimer = time.time()  
                for parcellation in corrparcellations:
                    par = monpar[parcellation]
                    
                    parfolder = dir_in + regfolder + str(par[1]) + "/"
                    #file of parcellation data
                    parcellationfile = parfolder + person + "_" + j + "_" + str(par[1]) + ".csv"
                    #starting point that every correlation file name will contain
                    corrfileroot = person + "_" + j + "_" + "CorrForPar" + str(par[2])
                    #main correlation file for all time, all networks
                    correlationfile = corrfileroot + "_" + "alltime" + "_" + "allnetworks" + ".csv"
                    locationcsv = locationfile + str(par[2]) + '.csv'
                                        
                    #create folder that contains each individual parcel's correlations
                    parcorrfolder = dir_in + regfolder + str(par[1]) + "/" + "parcorr/"
                    if not os.path.exists(parcorrfolder):
                        os.makedirs(parcorrfolder)                     
                    
             
                    if os.path.isfile(parcellationfile) == False:
                        x = "This file doesn't exist: " + parcellationfile
                        print(x)
                        log.append(x)
                    else:
                        doit = True
                        if replacer == False:
                            if os.path.isfile(parfolder + correlationfile) == True:
                                x = "Turn to correlation did not run; file already exists for " + correlationfile
                                print(x)
                                log.append(x)
                                doit = False
                        if doit == True:    
                            os.chdir(dir_in)
                        
                            x = "Creating basic correlation files for " + parcellationfile
                            print(x)
                            log.append(x)                                
        
                            #read in the parcellation data
                            parceldata = pd.read_csv(parcellationfile, index_col=0)   
                            numparcels = len(parceldata.columns)
    
                            #read in hierarchy data, to know which network each parcel belongs to
                            hdf = pd.read_csv(hierarchyfile)
                            hdf = hdf.rename(columns={'sATOM': 's1095'})
                            
                            #read in location file, generate lists of x,y,z coordinates
                            ldf = pd.read_csv(locationcsv,sep=';')
                            x_locations = list(ldf['x'])
                            y_locations = list(ldf['y'])
                            z_locations = list(ldf['z'])
                            
                            
                            parcels = list(range(1,numparcels+1))
                            networks = []
                            
                            #for each parcel, search it in hierarchy data and find its network
                            for parce in parcels:
                                x = hdf.loc[hdf['s'+str(numparcels)] == parce]['s7'].iloc[0]
                                networks.append(x)
                            #create dataframe of parcels and their networks
                            ndf = pd.DataFrame({'parcel':parcels,'network':networks})
                            
                            #create lists as they appear in the correlation dataframe
                            edge2netlist = list(ndf['network'])*numparcels
                            edge1netlist = []
                            for net in networks:
                                edge1netlist.extend(num for num in [net]*numparcels)
                                
                            #list of all parcel to parcel connections, including duplicates (eg 1to2 and 2to1)
                            fulllist = list(range(0,numparcels*numparcels))
                            
                            #edge lists, as they're arranged in the links dataframe generated below
                            edge1list = []
                            edge2list = []
                            for num in range(numparcels):
                                edge1column = [num+1]*numparcels
                                edge1list.extend(edge1column)
                                edge2list.append(num+1)
                            edge2list = edge2list*numparcels
                            
                            #figure out the distance between parcels
                            distance = []
                            for row in range(len(edge1list)):
                                a = edge1list[row]-1
                                b = edge2list[row]-1
                                
                                ax = x_locations[a]
                                ay = y_locations[a]
                                az = z_locations[a]
                                
                                bx = x_locations[b]
                                by = y_locations[b]
                                bz = z_locations[b]                             
                                
                                dist = ((ax-bx)**2+(ay-by)**2+(az-bz)**2)**0.5
                                
                                distance.append(dist)
                                
                            #list of connections to be removed cause they're duplicates
                            droplistdup = []
                                                        
                            for num in fulllist:
                                if edge1list[num] >= edge2list[num]:
                                    #this removes all the duplicates (i.e. 1 to 2 is the same as 2 to 1)
                                    droplistdup.append(num)
                                            

                            #create correlation data frame
                            corrdf = parceldata.corr()
                            #Transform it to a links data frame (3 columns only)
                            links = corrdf.stack().reset_index()
                            links.columns = ['edge1', 'edge2','weight']
                            
                            #create dataframe of the networks for each parcel to parcel connection. Join it to the links df    
                            tempdf = pd.DataFrame({'edge1network' :edge1netlist,'edge2network':edge2netlist,'distance':distance})
                            links = links.join(tempdf)
                            
                            #create correlation files for each time length, up to the rounded down length of scan
                            scanlength = int(len(parceldata)/24)

                            for minu in range(scanlength):
                                parceldatatime = parceldata.iloc[0:minu*24+24]    
                                corrdftime = parceldatatime.corr()
                                linkstime = corrdftime.stack().reset_index()
                                linkstime.columns = ['edge1', 'edge2','weight']
                                linkstime = linkstime.join(tempdf)
                                linkstime = linkstime.drop(droplistdup)
                                linkstime.to_csv(parfolder + corrfileroot + "_" + "min" + str(minu+1) + "_" + "allnetworks" + ".csv",index=False)
                            
                            tl = len(parceldata)
                            
                            #create correlation files for first and second half of the whole scan, and for 11 minutes of data (0 to 5.5 and 5.5 to 11)
                            parceldatafirsthalf = parceldata.iloc[0:int(tl/2)]
                            corrdffh = parceldatafirsthalf.corr()
                            linksfh = corrdffh.stack().reset_index()
                            linksfh.columns = ['edge1', 'edge2','weight']
                            linksfh = linksfh.join(tempdf)
                            linksfh = linksfh.drop(droplistdup)
                            linksfh.to_csv(parfolder + corrfileroot + "_" + "halffirst" + "_" + "allnetworks" + ".csv",index=False)                            
                            
                            parceldatasecondhalf = parceldata.iloc[int(tl/2):]
                            corrdfsh = parceldatasecondhalf.corr()
                            linkssh = corrdfsh.stack().reset_index()
                            linkssh.columns = ['edge1', 'edge2','weight']
                            linkssh = linkssh.join(tempdf)
                            linkssh = linkssh.drop(droplistdup)
                            linkssh.to_csv(parfolder + corrfileroot + "_" + "halfsecond" + "_" + "allnetworks" + ".csv",index=False)                             

                                
                            parceldatafirsthalf11 = parceldata.iloc[0:int(sharedmaxage*24/2)]
                            corrdffh11 = parceldatafirsthalf11.corr()
                            linksfh11 = corrdffh11.stack().reset_index()
                            linksfh11.columns = ['edge1', 'edge2','weight']
                            linksfh11 = linksfh11.join(tempdf)
                            linksfh11 = linksfh11.drop(droplistdup)
                            linksfh11.to_csv(parfolder + corrfileroot + "_" + "halffirstof" + str(int(sharedmaxage)) + "_" + "allnetworks" + ".csv",index=False)                            
                            

                            parceldatasecondhalf11 = parceldata.iloc[int(sharedmaxage*24/2):int(sharedmaxage*24)]
                            corrdfsh11 = parceldatasecondhalf11.corr()
                            linkssh11 = corrdfsh11.stack().reset_index()
                            linkssh11.columns = ['edge1', 'edge2','weight']
                            linkssh11 = linkssh11.join(tempdf)
                            linkssh11 = linkssh11.drop(droplistdup)
                            linkssh11.to_csv(parfolder + corrfileroot + "_" + "halfsecondof" + str(int(sharedmaxage)) + "_" + "allnetworks" + ".csv",index=False)
                                
                            
                            #linksall = all connections (without duplicates)
                            linksall = links.drop(droplistdup)

                            #save the all connections dataframe
                            linksall.to_csv(parfolder + correlationfile,index=False)
                            #why greater than 100? Smaller than that and the within a network connections are just so small

                            #create a droplist for each individual parcel, and then create a list of connections just with that parcel
                            pardict = {}
                            for parc in range(numparcels):
                                pardict[parc+1] = []
                            keeplistpar1 = []
                            for num in fulllist:
                                if edge1list[num] != edge2list[num]:
                                    pardict[edge1list[num]].append(num)
                            for parc in range(numparcels):
                                droplistpar = list(set(fulllist) - set(pardict[parc+1]))
                                linkspar = links.drop(droplistpar)
                                linkspar.to_csv(parcorrfolder + corrfileroot + "_" + "alltime" + "_" + "parcel" + str(parc+1) + ".csv",index=False)
                                

    

                            
                #find the final time, save info to log
                steptimer = round(time.time()-steptimer,3)
                x = "Individual step took " + str(steptimer) + " s to run."
                print(x)
                log.append(x)
                steptimermin = round(steptimer/60,3)
                x = "(which is " + str(steptimermin) + " minutes)"
                print(x)
                log.append(x)                        



for k in steps:

            
    
    if k == 'qcfc':         
        useses0 = True
        useses12 = True 
        
        motthres = [
                [0,100],
                #[0,50],
                #[50,100]
                ]
        
        #qcfc summary stuff
        pipelines = []
        slopes = []
        noiseedges = []
        hmcorr = []
        abshmcorr = []
        stdabshmcorr = []
    
        pipelines2 = []
        slopes2 = []
        noiseedges2 = []
        hmcorr2 = []
        abshmcorr2 = []    
        stdabshmcorr2 = []
        
        
        for motth in motthres:
            
            #which subjects do you want to use for the QCFC plots? The first two numbers are the percentile range for avg motion. Use 0-100 for all subjects
            #use 0-50 to use only the 50% of scans with least motion
            lowthres = motth[0]
            highthres = motth[1]
   
    
            steptimer = time.time() 
    
            x = "Now generating QC-FC values for " + regfolder + " " + str(lowthres) + "-" + str(highthres) + " motion"
            print(x)
            log.append(x) 
            
            for parcellation in qcfcparcellations:
                par = monpar[parcellation]
                #determine the file name of the file that contains the location (x,y,z) of each parcel
                locationcsv = locationfile + str(par[2]) + '.csv'
                numparcels = par[2]
                
                #create list of connections, as they would appear in a every-parcel-linked-to-every-other-parcel list
                edge1list = []
                edge2list = []
                for num in range(numparcels):
                    edge1column = [num+1]*numparcels
                    edge1list.extend(edge1column)
                    edge2list.append(num+1)
                edge2list = edge2list*numparcels
                
                fulllist = list(range(0,numparcels*numparcels))
                
                #create list of duplicates
                droplistdup = []
                for num in fulllist:
                    if edge1list[num] >= edge2list[num]:
                        #this removes all the duplicates (i.e. 1 to 2 is the same as 2 to 1)
                        droplistdup.append(num)
                
                #load location (x,y,z) data
                ldf = pd.read_csv(locationcsv,sep=';')
                x_locations = list(ldf['x'])
                y_locations = list(ldf['y'])
                z_locations = list(ldf['z'])
                
                
                #convert the drop list to a keep list
                #keeplist = [item for item in fulllist if item not in droplistdup]
                
                keeplist = list(set(fulllist)-set(droplistdup))
                keeplist.sort()
                
                #create a list of all the unique connections, and the distance between those connections
                connections = []
                distance = []
                for item in keeplist:
                    edge1 = edge1list[item]
                    edge2 = edge2list[item]
                    connection = str(edge1) + "-" + str(edge2)
                    connections.append(connection)
    
                    a = edge1-1
                    b = edge2-1
                    
                    ax = x_locations[a]
                    ay = y_locations[a]
                    az = z_locations[a]
                    
                    bx = x_locations[b]
                    by = y_locations[b]
                    bz = z_locations[b] 
                    
                    dist = ((ax-bx)**2+(ay-by)**2+(az-bz)**2)**0.5
                    
                    distance.append(dist)
    
                #create a list of the average motion for each person
                avgmotion = []
    
                #create a list of all the unique image scans (i.e. person-session combinations)
                allimages = []
                for i in participants:
                    person = participant_folders[i]
                    for j in imagesession:
                        image = person + '_' + j
                        allimages.append(image)  
                        
                        dir_in = dir_start + person + "/" + j + "/func/"
                        avgmotionfile = dir_in + person + "_" + j + "_" + avgmotionname
                        #load the average motion file, add it to the list of average motion
                        with open(avgmotionfile) as file:
                            for line in file:
                                avgmotion.append(float(line)) 
                                
                #create a dataframe of the images and their average motion
                sdf = pd.DataFrame({'images':allimages,'avgmotion':avgmotion}) 
    
    
    
                
                if useses0 == True:
                    if useses12 == True:
                        sestext = 'ses0+12'
                    else:
                        sestext = 'ses0'
                elif useses12 == True:
                    sestext = 'ses12'
                else:
                    sestext = 'noses'
    
                #if lowthres = 50, it'll give you the median. The 50th percentile
                lowmot = np.percentile(sdf['avgmotion'], lowthres)
                highmot = np.percentile(sdf['avgmotion'], highthres)
                droplistlowmo = []
                
                #create a list of each person's correlations for all the connections. This creates a list of lists
                allcorrelations = []
    
               # onlyuselowmo = False
    
               # if onlyuselowmo == True:     
                for d in range(len(sdf['avgmotion'])):
                    if sdf.loc[d]['avgmotion'] < lowmot:
                        droplistlowmo.append(d)
                    if sdf.loc[d]['avgmotion'] > highmot:
                        droplistlowmo.append(d)
                
                for d in range(len(sdf['images'])):
                    if 'ses-0' in sdf.loc[d]['images']:
                        if useses0 == False:
                            droplistlowmo.append(d)
                    if 'ses-12' in sdf.loc[d]['images']:
                        if useses12 == False:
                            droplistlowmo.append(d)
                
                sdflow = sdf.drop(droplistlowmo)
                
                lowscans = list(sdflow['images'])   
                avgmotionlow = list(sdflow['avgmotion'])
            
                for i in participants:
                    person = participant_folders[i]
                    for j in imagesession:
                        curscan = person + '_' + j
                        if curscan in lowscans:
                            dir_in = dir_start + person + "/" + j + "/func/"
                            
                            parfolder = dir_in + regfolder + str(par[1]) + "/"
                            #file of parcellation data
                            corrfileroot = person + "_" + j + "_" + "CorrForPar" + str(par[2])
                            #main correlation file for all time, all networks
                            correlationfile = parfolder + corrfileroot + "_" + "alltime" + "_" + "allnetworks" + ".csv"  
                            
                            #load the file of one scan's correlations between parcels
                            cdf = pd.read_csv(correlationfile)
                            #turn it into a list, add it to the list of lists
                            scancorrelations = list(cdf.weight)
                            allcorrelations.append(scancorrelations)         
                              
                #transpose the list of lists, so now instead of each list containing one person's correlations, it's one connection's correlations
                #so each item in the list is all the diff people's correlations for connection 1-2, then 1-3, then 1-4, and all the parcel combos                  
                transposedcorrelations = list(map(list, zip(*allcorrelations)))
                
                #add each of these connection correlation lists to the people dataframe
                #this creates a dataframe where the first 2 columns are scans and the motion, then each column after is a different connection
                    
                #calculate the correlation between each connection's correlations with the motion. Put that in a list
        
                m2cc = []
                m2ccsig = []
                for conn in range(len(transposedcorrelations)):
                    somecorrelation = transposedcorrelations[conn]                
                    pc = pearsonr(somecorrelation,avgmotionlow)
                    m2cc.append(pc[0])
                    m2ccsig.append(pc[1])
                    
                    #tempdf = pd.DataFrame({header:transposedcorrelations[conn]})
                    #sdf = sdf.join(tempdf)
    
                    
                #create a dataframe of the different connections, the distance between connections, and their qc-fc values (the correlation of those correlations with motion)
                distdf = pd.DataFrame({'connection':connections,'distance':distance,'qcfc':m2cc,'absqcfc':[abs(number) for number in m2cc],'p-value':m2ccsig})
                
                #do a Fisher transformation of correlations
                distdf['qcfc'] = np.arctanh(distdf['qcfc'])
                distdf['absqcfc'] = np.arctanh(distdf['absqcfc'])
                
                
                
                #calculate plot stuff
                linregresscalc = linregress(distdf['distance'],distdf['qcfc'])
                slope = linregresscalc.slope
                meanqcfc = sum(distdf['qcfc'])/len(distdf['qcfc'])
                meanabsqcfc = sum(distdf['absqcfc'])/len(distdf['absqcfc'])
                stdabsqcfc = np.nanstd(distdf['absqcfc'])
                intercept = linregresscalc.intercept
                minx = min(distdf['distance'])
                maxx = max(distdf['distance'])
                xrange = [minx,maxx]
                yfit = [intercept + slope * minx,intercept + slope * maxx]
                sigedges = sum(i < 0.05 for i in m2ccsig)
                sigedgepercent = sigedges/len(m2ccsig)*100
                
                #plot it, cause why not
                plt.scatter(distdf['distance'],distdf['qcfc'],marker='.',s=0.07)
                plt.plot(xrange,yfit,'r')
                plt.xlabel('distance (mm)')
                plt.ylabel('Z score')
                props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                textstr1 = 'mean = ' + str(round(meanqcfc,5)) + ', SD = ' + str(round(np.std(distdf['qcfc']),3)) + ', slope = ' + str(round(slope,5))
                textstr2 = '\nabsmean = ' + str(round(meanabsqcfc,5))
                textstr3 = '\nsignificant edges: ' + str(round(sigedgepercent,2)) + '% (p<0.05)'
                textstr4 = '# scans: ' + str(len(lowscans)) + ', avg avg rel fd = ' + str(round(sum(avgmotionlow)/len(avgmotionlow),3)) + ' (' + str(lowthres) + '-' + str(highthres) + '%ile, ' + sestext + ')'
                textstr = textstr1 + textstr2 + textstr3
    
                plt.annotate(textstr, xy=(0.01, 0.01), xycoords='axes fraction')
                plt.annotate(textstr4, xy=(0.01, 0.95), xycoords='axes fraction')
    
                plt.title('QC-FC plot for ' + regfolder[:-1])
                if saveqcfcplots == True:
                    plt.savefig(qcfcplotfolder + regfolder[:-1] + "_" + str(round(sigedgepercent,2)) + "qcfcplt.png", dpi = 400)   
                plt.show()
        
                if (lowthres == 0) & (highthres == 100):
                    curpipe = regfolder
                    if curpipe not in pipelines:
                        pipelines.append(regfolder)
                        slopes.append(slope)
                        noiseedges.append(sigedgepercent)
                        hmcorr.append(meanqcfc)
                        abshmcorr.append(meanabsqcfc)
                        stdabshmcorr.append(stdabsqcfc)
                        
                    if curpipe not in pipelines2:    
                        pipelines2.append(regfolder)
                        slopes2.append(slope)
                        noiseedges2.append(sigedgepercent)
                        hmcorr2.append(meanqcfc)
                        abshmcorr2.append(meanabsqcfc)
                        stdabshmcorr2.append(stdabsqcfc)
                    
                elif (lowthres == 0) & (highthres == 50):
                    curpipe = regfolder + 'low'
                    if curpipe not in pipelines2:    
                        pipelines2.append(curpipe)  
                        slopes2.append(slope)
                        noiseedges2.append(sigedgepercent)
                        hmcorr2.append(meanqcfc)
                        abshmcorr2.append(meanabsqcfc)   
                        stdabshmcorr2.append(stdabsqcfc)
                        
                elif (lowthres == 50) & (highthres == 100):
                   curpipe = regfolder + 'high'
                   if curpipe not in pipelines2:    
                        pipelines2.append(curpipe)  
                        slopes2.append(slope)
                        noiseedges2.append(sigedgepercent)
                        hmcorr2.append(meanqcfc)
                        abshmcorr2.append(meanabsqcfc)    
                        stdabshmcorr2.append(stdabsqcfc)
                            
        qcfcdf1 = pd.DataFrame({'pipeline':pipelines,'noise edges':noiseedges,'HM Corr':hmcorr,'Abs HM Corr':abshmcorr,'Abs HM Corr STD':stdabshmcorr,'Slope':slopes})
        qcfcdf2 = pd.DataFrame({'pipeline':pipelines2,'noise edges':noiseedges2,'HM Corr':hmcorr2,'Abs HM Corr':abshmcorr2,'Abs HM Corr STD':stdabshmcorr2,'Slope':slopes2})
        
        summaryfile1 = summaryfolder + 'qcfcsummary1-' + str(int(time.time())) + '.csv'
        qcfcdf1 = qcfcdf1.sort_values(by='pipeline')
        qcfcdf1 = qcfcdf1.reset_index(drop=True)
        if saveqcfcdata == True:
            qcfcdf1.to_csv(summaryfile1)        
                
        summaryfile2 = summaryfolder + 'qcfcsummary2-' + str(int(time.time())) + '.csv'
        qcfcdf2 = qcfcdf2.sort_values(by='pipeline')
        qcfcdf2 = qcfcdf2.reset_index(drop=True)
        if saveqcfcdata == True:
            qcfcdf2.to_csv(summaryfile2) 
        
        print(qcfcdf1.to_string())
        print(qcfcdf2.to_string())        
        
        qcfcdf2low = qcfcdf2[qcfcdf2['pipeline'].str.contains("low")==True]
        qcfcdf2high = qcfcdf2[qcfcdf2['pipeline'].str.contains("high")==True]
            
        #find the final time, save info to log
        steptimer = round(time.time()-steptimer,3)
        x = "Individual step took " + str(steptimer) + " s to run."
        print(x)
        log.append(x)
        steptimermin = round(steptimer/60,3)
        x = "(which is " + str(steptimermin) + " minutes)"
        print(x)
        log.append(x)                  
    
                         
#Wrap up the program

#subtract the new current time from the old current time. Also convert to minutes. Add to log
totaltimer = round(time.time()-totaltimer,3)
totaltimermin = round(totaltimer/60,3)
totaltimerhour = round(totaltimermin/60,3)
x = "All steps took " + str(totaltimer) + " s to run."
print(x)
log.append(x)
x = "(which is " + str(totaltimermin) + " minutes)"
print(x)
log.append(x)
x = "(which is " + str(totaltimerhour) + " hours)"
print(x)
log.append(x)

x = 'The end date/time is ' + time.ctime()
print(x)
log.append(x)

os.chdir(dir_start)
#add a couple blank lines to the log list, to make it look nicer
log.append('')
log.append('')

#open the log file, add the log list to the file
#'a' means append. You could also write a new file every time, if you wanted
with open(logname, 'a') as f:
    for item in log:
        f.write("%s\n" % item)
f.close()                    


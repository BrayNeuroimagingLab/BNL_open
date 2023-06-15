"""
Tintagel v1.0
Determine Reference Volumes & Count Number of Volumes

This program does 3 things
1) It does a rigid body realignment of a 4D image to the first volume, creating
motion estimates - via mcflirt
2) It looks at the FD (framewise displacement) for volumes 380-410 for MSC data (ie roughly in the middle of the scan)
and determines the one with the least amount of motion. This becomes the reference volume.
A table of 4D images and their reference volume is saved
3) Checks how many volumes are in a 4D image. This can be used to debug. For example,
if a 4D image only has 50 volumes, step 2 will fail

You generally only need to run step 1 and 2. Step 3 is just for debugging, basically


Update log:
v1.1 - June 26, 2019
Updated replacer
Minor fixes
Note: version 1.1 has not been extensively bug tested. See Kirk if problems arise!



"""

"""***********************"""
"""GENERAL PROGRAM OPTIONS"""
"""***********************"""
#what directory are your images saved in?
dir_start = "/Users/shefalirai/Desktop/sub-1973001C2/"

#where the reference volumes file is saved
Location = "/Users/shefalirai/Desktop/sub-1973001C2/xrefvolumes.csv"

#what participants do you want this to run on? e.g. [1,2,3] or list(range(1,4))
# participants = list(range(1, 59))
participants = [1]


#do you want to run on ses-0, ses-12, or both? If both, type ["ses-0","ses-12"]
imagesession = ["ses-func06"]

#if replacer is false, temprealign won't run if file already in reference volume list or if output file already exists
#if replacer is true, temprealign will run even if file already in reference volume list
replacer = False

#name of log book that output is saved to
logname = 'xtintagel.txt'



#what steps do you want to run? Possible steps are temprealign, refvol, volcount
steps = ['temprealign','refvol','volcount']
#temprealign = Use MCFLIRT to warp to first volume. Generate FD based on this
#refvol = Look through FD to determine reference volumes
#volcount = read through FD list. Count how many volumes there are in 4D data

"""******************"""
"""SEND EMAIL OPTIONS"""
"""******************"""
#if sendemail is True, the program will email you the log book when it finishes doing what it's doing
sendemail = False

receiver_email = "shefali.s.rai@gmail.com"
subject = "Python Program Update"
body = "Python program finished running. See attached log."


"""***************"""
"""PROGRAM OPTIONS"""
"""***************"""
inputepi = "task-Dora5_bold" #changed this from task-rest_bold to the task_motor file
outputepi = "task-Dora5_boldMcFto0"
outputfd = "task-Dora5_boldMcFto0.nii.gz_rel.rms"



"""*****************************************"""
"""ANYTHING BELOW HERE DOESN'T NEED CHANGING"""
"""**********(OR SO KIRK HOPES)*************"""
"""*****************************************"""

import nipype.interfaces.fsl as fsl
import os
import pandas as pd
import time
# import smtplib, ssl
# from email import encoders
# from email.mime.base import MIMEBase
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

#sending email options. Best practice says to not save a password in plain text,
#but I don't care about the email address kirkpython
# sender_email = "kirkpython@gmail.com"
# password = "TheScream"
# message = MIMEMultipart()
# message["From"] = sender_email
# message["To"] = receiver_email
# message["Subject"] = subject
# message.attach(MIMEText(body, "plain"))
# filename = rest


#get the current time
totaltimer = time.time()

#get a list of everything in the starting directory
participant_folders = sorted(os.listdir(dir_start))

#Start what will be added to the log book for this session
log = ["*************************************************"]
log.append('Starting log for ' + time.ctime())


#if your specified reference volume file doesn't exist, this creates it
if os.path.isfile(Location) == False:
    refdata = [('test',255)]
    df = pd.DataFrame(data = refdata, columns=['File', 'Ref_Volume'])
    
    os.chdir(dir_start)
    #save the data frame as a csv file
    df.to_csv(Location,index=False,header=True)


#Code here is based off of code in the Lancelot program. See there for more info

for k in steps:
    
    if k == 'temprealign':
        df = pd.read_csv(Location)
        files = list(df['File'])
        refframes = list(df['Ref_Volume'])
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/" + j + "/func/"
                input_file = dir_in + person + "_" + j + "_" + inputepi + ".nii.gz"
                output_file = dir_in + person + "_" + j + "_" + outputepi + ".nii.gz"
                ref_name = person + "_" + j + "_" + outputfd
                if os.path.isfile(input_file) == False:
                    input_file = dir_in + person + "_" + j + "_" + inputepi + ".nii"
                if os.path.isfile(input_file) == False:
                    x = "This file doesn't exist: " + input_file
                    print(x)
                    log.append(x)
                else:
                    doit = True
                    if replacer == False:
                        if ref_name in files:
                            x = "Mcflirt did not run, " + person + " " + j + " is already in the reference list."
                            print(x)
                            log.append(x)
                            doit = False
                    if doit == True:
                        if replacer == False:
                            if os.path.isfile(dir_in + ref_name) == True:
                                x = "McFlirt did not run; this file already exists " + ref_name
                                print(x)
                                log.append(x)
                                doit = False                            
                    if doit == True:
                        steptimer = time.time()

                        x = "McFlirt is beginning to run."
                        print(x)
                        log.append(x)
                        try:
                            os.chdir(dir_in)
                            mymcf = fsl.MCFLIRT()
                            mymcf.inputs.in_file = input_file
                            mymcf.inputs.out_file = output_file
                            mymcf.inputs.save_mats = True
                            mymcf.inputs.save_plots = True
                            mymcf.inputs.save_rms = True
                            mymcf.inputs.ref_vol = 0
                            mymcf.run()                        
                            
                            x = "McFlirt probably created " + output_file
                            print(x)
                            log.append(x)      
                        except:
                            x = "McFlirt failed."
                            print(x)
                            log.append(x)
                        steptimer = round(time.time()-steptimer,3)
                        x = "Individual step took " + str(steptimer) + " s to run."
                        print(x)
                        log.append(x)
                        steptimermin = round(steptimer/60,3)
                        x = "(which is " + str(steptimermin) + " minutes)"
                        print(x)
                        log.append(x)
                        

    if k == 'refvol':
        df = pd.read_csv(Location)
        files = list(df['File'])
        refframes = list(df['Ref_Volume'])
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/" + j + "/func/"
                x = []
                input_file = dir_in + person + "_" + j + "_" + outputfd
                if os.path.isfile(input_file) == False:
                    if input_file in files:
                        x = "Refvol did not run. This file already in reference list (and also no longer exists): " + input_file
                        print(x)
                        log.append(x)
                    else:                        
                        x = "Refvol did not run. This file doesn't exist: " + input_file
                        print(x)
                        log.append(x)
                else:                  
                    os.chdir(dir_in)
                    if not input_file in files:
                        f = open(input_file, "r")
                        for num in f:
                            x.append(float(num))
                        #define the reference volume as the one with the smallest FD between
                        #volumes 210 and 230
                        try:
                            y = min(x[85:105]) #Shefali: in the middle of 180 and 210 for Kate & Shefali Dev Scan 
                            refframes.append(x.index(y))
                            files.append(input_file)
                            x = person + " " + j + " added to reference list. The reference volume is " + str(x.index(y))
                            print(x)
                            log.append(x)
                        except:
                            x = "Refvol failed for " + person + " " + j + ". Perhaps the image was too short."
                            print(x)
                            log.append(x)                            
                    else:
                        x = "Refvol did not run, " + person + " " + j + " is already in the reference list."
                        print(x)
                        log.append(x)                        

        #create a data frame with the file name and its reference volume
        refdata = list(zip(files,refframes))
        df = pd.DataFrame(data = refdata, columns=['File', 'Ref_Volume'])

        os.chdir(dir_start)
        #print(df)
        #save the data frame as a csv file
        df.to_csv(Location,index=False,header=True)


    if k == 'volcount':
        for i in participants:
            person = participant_folders[i]
            for j in imagesession:
                dir_in = dir_start + person + "/" + j + "/func/"
                fdlist = []
                input_file = person + "_" + j + "_" + outputfd
                if os.path.isfile(dir_in + input_file) == True:
                    os.chdir(dir_in)
                    f = open(input_file, "r")
                    for num in f:
                        fdlist.append(float(num))
                    x = input_file + " has this many volumes: " + str(len(fdlist))
                    print(x)
                    log.append(x)
                else:
                    x = "this file does not exist: " + input_file
                    print(x)
                    log.append(x)                    




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

#I really don't know what this email code does. Taken from some website    
# if sendemail == True:
#     # Open PDF file in binary mode
#     with open(filename, "rb") as attachment:
#         # Add file as application/octet-stream
#         # Email client can usually download this automatically as attachment
#         part = MIMEBase("application", "octet-stream")
#         part.set_payload(attachment.read())

#     # Encode file in ASCII characters to send by email    
#     encoders.encode_base64(part)

#     # Add header as key/value pair to attachment part
#     part.add_header(
#         "Content-Disposition",
#         f"attachment; filename= {filename}",
#     )

#     # Add attachment to message and convert message to string
#     message.attach(part)
#     text = message.as_string()

#     # Log in to server using secure context and send email
#     context = ssl.create_default_context()
#     with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, text)

#     print("Email was sent to " + receiver_email + " containing " + logname)    
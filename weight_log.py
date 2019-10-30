#! /usr/bin/python
#-*-coding: utf-8 -*-

"""
Simple test script for TagReader
Reads a few tags and prints them
Last Modified:
2018/03/07 by Jamie Boyd - added some comments, cleaned up a bit
"""

from RFIDTagReader import TagReader
from datetime import datetime
import pymysql
import os
import csv

"""
Change serialPort to wherever your tagreader is
and kind to 'ID' for ID-L3,12,20 etc. or RDM for RDM630 etc.
"""
RFID_serialPort = '/dev/ttyUSB0'
#RFID_serialPort = '/dev/serial0'
#RFID_serialPort='/dev/cu.usbserial-AL00ES9A'
RFID_kind = 'ID'
"""
Setting to timeout to None means we don't return till we have a tag.
If a timeout is set and no tag is found, 0 is returned.
"""
RFID_timeout = None
RFID_doCheckSum = True
read = True
db1 = pymysql.connect(host='142.103.107.236', user='slavePi', db='AHF_laser_cage', password='iamapoorslave',autocommit=True)
cur1 = db1.cursor()
insert_statment='INSERT INTO Weight_ManualLog (Tag,Timestamp,Weight, Change_To_Baseline, Water_Needed,Cage) VALUES (%s,%s,%s,%s,%s,%s)'
try:
    tagReader = TagReader (RFID_serialPort, RFID_doCheckSum, timeOutSecs = RFID_timeout, kind=RFID_kind)
except Exception as e:
    raise e
while read:
    try:
        print ('Waiting for tags...')
        tag = tagReader.readTag ()
        print (tag)
        weight_float = input("Please enter the mouse's weight (g): ")
        Cage=input('Please enter the cage of the mouse:')
        record_filename = "/home/pi/Documents/RFIDTagReader/Mice/"+str(tag)+".csv"
        tm = datetime.now()
        timestamp = str(tm.year) + format(tm.month, '02d') + format(tm.day, '02d') + \
                           format(tm.hour, '02d') + format(tm.minute, '02d') + format(tm.second, '02d')
        if not os.path.exists("Mice/"):
                print("Creating data directory: %s","Mice/")
                os.makedirs("Mice/")
        if os.path.exists(record_filename)==False:
            print('BW Baseline Measurement')
            with open(record_filename, "a") as file:
                file.write("Timestamp, Tag, Weight, %Change_To_Baseline,15%_Cutoff(Y/N),Cage\n")
                file.write(timestamp+","+str(tag)+","+str(weight_float)+','+'0%'+','+'N'+"\n")
            values1=[tag,timestamp, weight_float,0,'N',Cage]
            cur1.execute(insert_statment,values)
        else:
            with open(record_filename,'r') as csv1:
                reader= csv.reader(csv1)
                reader1=list(reader)
                Baseline_Weight=float(reader1[1][2])
                not_valu=round((float(weight_float)-Baseline_Weight)/Baseline_Weight*100,1)
                print(str(not_valu))
                if (float(weight_float)-Baseline_Weight)/Baseline_Weight*100<-15.0:
                    CO='Y'
                    print('Mouse Underweight, Need supplment water')
                else:
                    CO='N'
            values=[tag,timestamp, weight_float,round((float(weight_float)-Baseline_Weight)/Baseline_Weight*100,1),CO,Cage]
            with open(record_filename, "a") as file:
                file.write(timestamp+","+str(tag)+","+str(weight_float)+','+str(not_valu)+'%'+
                ','+CO+','+Cage+"\n")
            cur1.execute(insert_statment,values)
    except ValueError as e:
        print (str (e))
        tagReader.clearBuffer()
print ('Read ' + ' tags')

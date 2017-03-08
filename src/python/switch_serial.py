import os
import csv
import serial
import time

CSVfile = 'NN2016_Prt_full.csv'

CSVfile = os.path.abspath(CSVfile)

ser = serial.Serial('COM6', 115200,timeout =1)

print ser.readall()

# read the specific line from the csv file
Prt = [0,0,0,0]
count = 0
with open(CSVfile) as f:
    r = csv.reader(f)
    for row in r:
        print "Current row " + str(count) + " : " + str(row)
        #print "I am now doing switch stuff"
        sw_str = row[0] + ',' + row[1] + ',' + row[2] + ',' + row[3] + '\n'
        #print sw_str
        ser.write(sw_str)
        str_in = ser.readline()
        print str_in.rstrip()
        #raw_input("Press Enter to continue...")
        count += 1

time.sleep(2)

ser.close()


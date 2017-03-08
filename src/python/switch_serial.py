import os
import csv
import serial
import time

CSVfile = 'NN2016_Prt_full.csv'

CSVfile = os.path.abspath(CSVfile)

ser = serial.Serial('COM6', 115200,timeout =1)


# read the specific line from the csv file
Prt = [0,0,0,0]
count = 0
with open(CSVfile) as f:
    r = csv.reader(f)
    for row in r:
        print "Current row :" + str(row)
        print "I am now doing switch stuff"
        count += 1

time.sleep(2)

print ser.readall()
ser.write('3,4,35,36\n')
print ser.readall()
ser.write('13,14,13,3\n')
print ser.readall()
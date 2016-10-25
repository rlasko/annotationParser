import xlrd
from datetime import time
import csv
import os

def convert(origin,dest):
    exFile = xlrd.open_workbook(origin)
    sheet = exFile.sheet_by_index(0)
    base = os.path.splitext(os.path.basename(origin))[0]
    filename = dest + "/" + base + ".csv"
    with open(filename, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        for i in range(sheet.nrows):
            row = sheet.row_values(i)
            if i != 0: # don't convert header
                try: # convert beginTime
                    beginTime = float(row[0])
                    beginTimeCorrected = xlrd.xldate.xldate_as_datetime(beginTime, exFile.datemode)
                    row[0] = str(beginTimeCorrected.strftime("%M:%S.%f"))
                except: # some files are formatted weirdly
                    print("Could not convert expected begin date field in file: " + base + " : ", row)
                try: # convert endTime
                    endTime = float(row[1])
                    endTimeCorrected = xlrd.xldate.xldate_as_datetime(endTime, exFile.datemode)
                    row[1] = str(endTimeCorrected.strftime("%M:%S.%f"))
                except: # some files are formatted weirdly
                    print("Could not convert expected begin date field in file: " + base + " : ", row)
            writer.writerow(row)

# convert all files starting at a top level directory
def run_from_root(origin):
    if (os.path.isdir(origin) == False):
        if (origin.endswith(".xlsx")):
            name = os.path.dirname(origin) + "/converted"
            if (not os.path.exists(name)): os.makedirs(name)
            convert(origin,name)
    else:
        for filename in os.listdir(origin):
            run_from_root(origin + "/" + filename);

# For testing single conversion
def run(origin):
    name = os.path.dirname(origin) + "/converted"
    if (not os.path.exists(name)): os.mkdir(name)
    convert(origin,name)

# run("/Users/RaeLasko/Documents/CMU/ArticuLab/D1S1_codes.xlsx")
run_from_root("/Users/RaeLasko/Documents/CMU/ArticuLab/TAR source files")

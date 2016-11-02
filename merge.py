import os
import csv
import copy

def merge(a, b):
    dest = os.path.dirname(a) + "/merged"
    if (not os.path.exists(dest)): os.mkdir(dest)
    fileA = csv.reader(open(a))
    fileB = csv.reader(open(b))
    newPath = dest + "/" + os.path.splitext(os.path.basename(a))[0] + ".csv"

    with open(newPath,"w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        for arow in fileA:
            try:
                brow = next(fileB)
            except:
                print("error")
            newRow = copy.copy(arow) + copy.copy(brow)[-4:]
            writer.writerow(newRow)

base = "/Users/RaeLasko/Documents/Converted/"

merge(base + "D7S1_Lauren_28Jan2016_Merged.csv", base + "D7S1_Sarah_17Mar2016.csv")
merge(base + "D7S2_Mikaila_26Jan2016.csv", base + "D7S2_Robbie_11Mar2016_Merged.csv")
merge(base + "D7S3_Lauren_26Jan2016.csv", base + "D7S3_Vanessa_22March2016.csv")
merge(base + "D7S4_Lauren_29March2016 1.csv", base + "D7S4_Robbie_25Jan2016_Merged.csv")
merge(base + "D7S5_Rae_19Mar2016.csv", base + "D7S5_Vanessa_24Jan2016.csv")

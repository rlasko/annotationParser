import os
import csv
import copy

def merge(a, b):
    dest = os.path.dirname(a) + "/merged"
    if (not os.path.exists(dest)): os.mkdir(dest)
    fileA = csv.reader(open(a))
    fileB = csv.reader(open(b))
    newPath = dest + "/" + os.path.splitext(os.path.basename(a))[0] + ".csv"
    i = 0
    with open(newPath,"w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        for arow in fileA:
            print(i)
            try:
                brow = next(fileB)
            except:
                print("error")
            newRow = copy.copy(arow) + copy.copy(brow)[-4:]
            writer.writerow(newRow)
            i += 1

base = "/Users/RaeLasko/Documents/CMU/ArticuLab/File cleaning/TA- need to merge/"

merge(base + "D4S5_1.csv", base + "D4S5_2.csv")
merge(base + "D8S5_1.csv", base + "D8S5_2.csv")
merge(base + "D9S5_1.csv", base + "D9S5_2.csv")
merge(base + "D10S5_1.csv", base + "D10S5_2.csv")
merge(base + "D13S5_1.csv", base + "D13S5_2.csv")

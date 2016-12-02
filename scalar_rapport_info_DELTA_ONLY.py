import os
import csv
import pprint

def get_rapport_dict(path):
    reader = csv.reader(open(path))
    header = next(reader)
    rapport_dict = dict()
    for val in header:
        rapport_dict[val] = []
    rapport_time = 0
    last_row = []
    for row in reader:
        for i in range(len(row)):
            if (row[i].strip() != ""):
                last = last_row[i].strip() if last_row != [] else "0"
                curr = row[i].strip()
                if int(last) == 0 or int(curr) == 0: continue
                val = int(curr) - int(last)
                val = str(val) if val >= 0 else "n" + str(abs(val))
                string = str(rapport_time) + " " + "scalar.Rapport" + val
                rapport_dict[header[i]].append(string)
        last_row = row
        rapport_time += 30
    return rapport_dict

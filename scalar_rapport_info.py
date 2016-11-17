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
    for row in reader:
        for i in range(len(row)):
            if (row[i].strip() != ""):
                string = str(rapport_time) + " " + "scalar.Rapport" + row[i].strip()
                rapport_dict[header[i]].append(string)
        rapport_time += 30
    return rapport_dict

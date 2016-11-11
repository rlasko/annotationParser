# For Tutoring_and_delivery_style_annotations, head-nods, backchannel, violate social norm, and rpc files
# Also for Mix-SE and Mix-SD and Praise after processing to fix columns
# remove annotator name from channel headings, duplicate channels and add tutee and tutor labels

import os
import csv
import copy
import pprint
from generate_dictionary import dictionary

def run(origin):
    num = 1
    if (not os.path.isdir(origin)):
        print("Please input folder name")
        return
    print("Finding files...")
    dest = origin + "/corrected_channels"
    if (not os.path.exists(dest)): os.mkdir(dest)
    for filename in os.listdir(origin):
        if (os.path.isdir(origin + "/" + filename)): continue
        print("Processing file " + str(num))
        get_channels(origin + "/" + filename, dest)
        num += 1
    print("Done!")

def find_time_index(header):
    for i in range(len(header)):
        if (("Time" in header[i] or "time" in header[i]) and
           ("Begin" not in header[i] and "End" not in header[i])):
            # print("Time index:", i)
            return i
    print("TIME COLUMN COULD NOT BE FOUND", header)

def find_channel_start(header):
    for i in range(len(header)):
        if (header[i].count("_") == 2 or
        (("P1" in header[i].upper() or "P2" in header[i].upper())
        and not ("1_" in header[i] or "2_" in header[i]))):
            # print("channel start:", i)
            return i
    print("Error finding channel start!!", header)
    return -1

def remove_annotator(header,start,end):
    for i in range(start,end):
        if (header[i].count("_") < 2): continue
        remove = header[i][::-1].find("_")
        if (remove == -1): continue # some channels are just for notes
        remove = len(header[i]) - remove - 1
        if (header[i][:remove] != "P1" and header[i][:remove] != "P2"):
            header[i] = header[i][:remove]
        else:
            person = header[i][remove-1:] # save person for later
            header[i] = header[i][:remove-1]
            remove = header[i][::-1].find("_")
            remove = len(header[i]) - remove - 1
            header[i] = header[i][:remove] # remove annotator
            header[i] += person
    return header

def standarize_header(header):
    for i in range(len(header)):
        if (header[i][-2:] == "p1" or header[i][:-2] == "p2"):
            header[i][-2:] = "P"
    return header

def get_channels(origin,dest):
    if (os.path.isdir(origin) or not origin.endswith(".csv")): return
    base = os.path.splitext(os.path.basename(origin))[0]
    print(base)
    filenameP = dest + "/" + base + "_channelsP"+ ".csv"
    filenameT1 = dest + "/" + base + "_channelsT1"+ ".csv"
    filenameT2 = dest + "/" + base + "_channelsT2"+ ".csv"

    reader = csv.reader(open(origin))
    header = next(reader)
    channel_start = find_channel_start(header)
    channel_end = len(header)

    header = remove_annotator(header,channel_start,channel_end)
    header = standarize_header(header)

    with open(filenameP, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        writer.writerow(header)
        for row in reader:
            writer.writerow(row)

    # Modify header for T1 and T2
    headerT1 = copy.deepcopy(header)
    headerT2 = copy.deepcopy(header)

    base = base[:base.find("_")] if base.find("_") != -1 else base
    sessionDictionary = dictionary()[base]
    for i in range(channel_start,channel_end):
        if (headerT1[i][-2:].lower() == "p1"):
            headerT1[i] = headerT1[i][:-2] + sessionDictionary["P1"]["T1"]
            headerT2[i] = headerT2[i][:-2] + sessionDictionary["P1"]["T2"]
        elif (headerT1[i][-2:].lower() == "p2"):
            headerT1[i] = headerT1[i][:-2] + sessionDictionary["P2"]["T1"]
            headerT2[i] = headerT2[i][:-2] + sessionDictionary["P2"]["T2"]
        elif (header[i].count("_") < 1): continue
        else:
            print("error!", header[i], "!!!!!!!!!!!!!!!!!!!!!!")

    timeIndex = find_time_index(header) # index location of time column
    reader = csv.reader(open(origin))
    next(reader)
    # write T1 file
    with open(filenameT1, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        writer.writerow(headerT1)
        start = False
        for row in reader:
            if "T1" in row[timeIndex]:
                start = True
            elif row[timeIndex] != "" and "T1" not in row[timeIndex]: start = False

            if start: writer.writerow(row)

    reader = csv.reader(open(origin))
    next(reader)

    #write T2 file
    with open(filenameT2, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        writer.writerow(headerT2)
        for row in reader:
            if "T2" in row[timeIndex]:
                start = True
            elif row[timeIndex] != "" and "T2" not in row[timeIndex]: start = False

            if start: writer.writerow(row)
    print()

# run("/Users/RaeLasko/Documents/CMU/ArticuLab/TAR source files/eye-gaze/converted")

# run("/Users/RaeLasko/Documents/CMU/ArticuLab/test")
run("/Users/RaeLasko/Documents/CMU/ArticuLab/Head Nods")

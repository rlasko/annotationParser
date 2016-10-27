# For eye-gaze files, head-nods, backchannel, violate social norm, and rpc
# remove annotator name from channel headings, duplicate channels and add tutee and tutor labels

import os
import csv
import copy

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

def get_channels(origin,dest):
    # variable index locations
    timeIndex = 2 # index location of time column
    channel_start = 5 # index location of first annotation column

    if (os.path.isdir(origin) or not origin.endswith(".csv")): return
    base = os.path.splitext(os.path.basename(origin))[0]
    filenameP = dest + "/" + base + "_channelsP"+ ".csv"
    filenameT1 = dest + "/" + base + "_channelsT1"+ ".csv"
    filenameT2 = dest + "/" + base + "_channelsT2"+ ".csv"

    reader = csv.reader(open(origin))
    header = next(reader)
    channel_end = len(header)

    # remove annotator name from channel heading
    for i in range(channel_start, channel_end):
        remove = header[i][::-1].find("_")
        remove = len(header[i]) - remove - 1
        header[i] = header[i][:remove]

    with open(filenameP, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        writer.writerow(header)
        for row in reader:
            writer.writerow(row)

    # Modify header for T1 and T2
    headerT1 = copy.deepcopy(header)
    headerT2 = copy.deepcopy(header)
    for i in range(channel_start,channel_end):
        if (headerT1[i][-2:len(headerT1[i])] == "P1"):
            headerT1[i] = headerT1[i][:-2] + "TUTOR"
            headerT2[i] = headerT2[i][:-2] + "TUTEE"
        else:
            headerT1[i] = headerT1[i][:-2] + "TUTEE"
            headerT2[i] = headerT2[i][:-2] + "TUTOR"

    reader = csv.reader(open(origin))
    next(reader)
    # write T1 file
    with open(filenameT1, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        writer.writerow(headerT2)
        start = False
        for row in reader:
            if row[timeIndex] == "T1 ":
                start = True
            elif row[timeIndex] != "": start = False

            if start: writer.writerow(row)

    reader = csv.reader(open(origin))
    next(reader)

    #write T2 file
    with open(filenameT2, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        writer.writerow(headerT2)
        for row in reader:
            if row[timeIndex] == "T2 ":
                start = True
            elif row[timeIndex] != "": start = False

            if start: writer.writerow(row)



run("/Users/RaeLasko/Documents/CMU/ArticuLab/TAR source files/backchannel/converted")

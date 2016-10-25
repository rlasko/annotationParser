# For Tutoring_and_delivery_style_annotations files
# remove annotator name from channel headings, duplicate channels and add tutee and tutor labels

import os
import csv

def run(origin):
    if (not os.path.isdir(origin)):
        print("Please input folder name")
        return

    dest = origin + "/corrected_channels"
    if (not os.path.exists(dest)): os.mkdir(dest)
    for filename in os.listdir(origin):
        get_channels(origin + "/" + filename, dest)

def get_channels(origin,dest):
    if (os.path.isdir(origin)): return
    base = os.path.splitext(os.path.basename(origin))[0]
    filenameP = dest + "/" + base + "_channelsP"+ ".csv"
    filenameT1 = dest + "/" + base + "_channelsT1"+ ".csv"
    filenameT2 = dest + "/" + base + "_channelsT2"+ ".csv"

    reader = csv.reader(open(origin))
    header = next(reader)
    print(header)
    channel_start = 6
    channel_end = len(header)
    # remove annotator name from channel heading
    for i in range(channel_start, channel_end):
        remove = header[i][::-1].find("_")
        remove = len(header[i]) - remove + 1
        header[i] = header[i][:remove]

    with open(filenameP, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        writer.writerow(header)
        for row in reader:
            writer.writerow(row)

    # Modify header for T1

    with open(filenameT1, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        writer.writerow(header)
        for row in reader:
            writer.writerow(row)

    # Modify header for T2

    with open(filenameT2, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        writer.writerow(header)
        for row in reader:
            writer.writerow(row)



run("/Users/RaeLasko/Documents/CMU/ArticuLab/test")

# For files that don't separate column by p1/p2
# Create separate columns

import os
import csv
import copy

def run(origin):
    num = 1
    if (not os.path.isdir(origin)):
        print("Please input folder name")
        return
    print("Finding files...")
    dest = origin + "/column_fix"
    if (not os.path.exists(dest)): os.mkdir(dest)
    for filename in os.listdir(origin):
        if (os.path.isdir(origin + "/" + filename)): continue
        print("Processing file " + str(num))
        print(filename)
        get_channels(origin + "/" + filename, dest)
        num += 1
    print("Done!")

def get_channels(origin,dest):
    # variable index locations
    timeIndex = 2 # index location of time column
    channel_start = 5 # index location of first annotation column
    p2_transcript_index = 4

    if (os.path.isdir(origin) or not origin.endswith(".csv")): return
    base = os.path.splitext(os.path.basename(origin))[0]
    filenameP = dest + "/" + base + "_columnfix"+ ".csv"

    reader = csv.reader(open(origin))
    header = next(reader)
    channel_end = len(header)
    end_of_unique = channel_end
    num_of_unique_channels = channel_end - channel_start

    # remove annotator name
    for i in range(channel_start, channel_end):
        remove = header[i][::-1].find("_")
        remove = len(header[i]) - remove - 1
        header[i] = header[i][:remove]

    # create p1/p2 header
    header = header + copy.deepcopy(header[channel_start:]) # add missing columns
    channel_end = len(header) # update end location
    for i in range(channel_start,channel_end):
        header[i] += "_P1" if i < end_of_unique else "_P2"

    with open(filenameP, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        writer.writerow(header)
        for row in reader:
            newRow = row + [""] * num_of_unique_channels
            if (newRow[p2_transcript_index]): # P2 said something, need to switch annotation location
                newRow[end_of_unique:] = copy.deepcopy(newRow[channel_start:end_of_unique]) # copy into new location
                newRow[channel_start:end_of_unique] = [""] * num_of_unique_channels # delete from old location
            writer.writerow(newRow)

run("/Users/RaeLasko/Documents/CMU/ArticuLab/File cleaning/Irrelevant/New SE Files/_Mix Cols Work")

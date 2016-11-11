# removes all channels that are not time or annotation
import os
import csv

# convert all files starting at a top level directory
def run_from_root(origin):
    print(origin)
    if (os.path.isdir(origin) == False):
        if (origin.endswith(".csv")): # make sure it's a csv
            name = os.path.dirname(origin) + "/_filtered" # create new dir
            if (not os.path.exists(name)): os.makedirs(name)
            filter_channels(origin,name)
    else:
        for filename in os.listdir(origin):
            if filename == "_filtered": continue # prevent filtering already filtered files
            run_from_root(origin + "/" + filename)

# determines whether or not a specific channel should be kept in the output file
def keep_channel(channel):
    if (channel == "" or channel == " "): return False
    if ("Begin" in channel):
        return True # keep begin time end time
    if (channel.count("_") < 1):
        return False
    if ("11" in channel): return False
    if (channel.count("_") > 1):
        print("Weird channel found:", channel)
        return False
    sp = channel.split("_")
    if (sp[0] == "1" or sp[0] == "2"): return False
    if (sp[1].lower() in ["tutor", "tutee", "p1", "p2"] and sp[0].isalpha()):
        return True
    if ("SV1" in channel or "SV2" in channel or
        "SD/QE_P1" in channel or "SD/QE_P2" in channel): return True
    if (sp[1].lower() in ["tutor", "tutee"]):
        return True
    if ("3_E1" in channel): return False
    else:
        print("Weird channel found2:", channel)
        return False

# return list of header indexes to keep
def get_keep_list(header):
    keep = []
    for i in range(len(header)):
        if (keep_channel(header[i])): keep += [i]
    return keep

# find the channel with start time
def get_start(row):
    for i in range(len(row)):
        if ("Begin" in row[i]): return i
    return -1

# creates new file and writes the wanted columns to it
def filter_channels(src, dst):
    # get file name
    base = os.path.splitext(os.path.basename(src))[0]
    filename = dst + "/" + base + "_filtered.csv"
    with open(filename, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        reader = csv.reader(open(src))
        header = next(reader)

        # get start index
        start_time_i = get_start(header)

        # error check
        if (start_time_i == -1):
            print("Time Stamps could not be found" + base, header)
            return
        keep = get_keep_list(header)
        header[start_time_i] = "Time"
        newHeader = [header[i] for i in keep]
        writer.writerow(newHeader)
        for row in reader:
            newRow = []
            newRow = [(row[i] if (i < len(row)) else "") for i in keep]
            writer.writerow(newRow)
    return

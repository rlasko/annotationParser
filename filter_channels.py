# removes all channels that are not time or annotation
import os
import csv


# convert all files starting at a top level directory
def run_from_root(origin):
    if (os.path.isdir(origin) == False):
        if (origin.endswith(".csv")):
            name = os.path.dirname(origin) + "/_filtered"
            if (not os.path.exists(name)): os.makedirs(name)
            print(origin)
            filter_channels(origin,name)
    else:
        for filename in os.listdir(origin):
            if filename == "_filtered": continue
            run_from_root(origin + "/" + filename)

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

def get_keep_list(header):
    keep = []
    for i in range(len(header)):
        if (keep_channel(header[i])): keep += [i]
    return keep

def get_sec(time_str):
    if len(time_str) < 2: return 0 # get rid of empty
    split = time_str.split(":")
    split_sec = split[-1].split(".")
    if (len(split) == 3 and len(split_sec) == 2): # with hour and mm
        h, m, s = split
        s, mm = split_sec
        return int(h) * 3600 + int(m) * 60 + int(s) + int(mm) * .1 * 10**len(mm)
    elif (len(split) == 3 and len(split_sec) == 1): # with hour no mm
        h, m, s = split
        return int(h) * 3600 + int(m) * 60 + int(s)
    elif (len(split) == 2 and len(split_sec) == 2):
        m, s = time_str.split(':')
        s, mm = s.split(".")
        return int(m) * 60 + int(s) + int(mm) * .1 * 10**len(mm)
    else:
        print (time_str)

def get_start(row):
    for i in range(len(row)):
        if ("Begin" in row[i]): return i
    return -1

def filter_channels(src, dst):
    base = os.path.splitext(os.path.basename(src))[0]
    # print("Filtering", base, "...", end=" ")
    filename = dst + "/" + base + "_filtered.csv"
    with open(filename, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        reader = csv.reader(open(src))
        header = next(reader)
        # get start and end index
        start_time_i = get_start(header)
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

run_from_root("/Users/RaeLasko/Documents/CMU/ArticuLab/Second Test")

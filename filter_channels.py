# removes all channels that are not time or annotation
import os
import csv

# convert all files starting at a top level directory
def run_from_root(origin):
    if (os.path.isdir(origin) == False):
        if (origin.endswith(".csv")):
            name = os.path.dirname(origin) + "/filtered"
            if (not os.path.exists(name)): os.makedirs(name)
            filter_channels(origin,name)
    else:
        for filename in os.listdir(origin):
            run_from_root(origin + "/" + filename)
    # print("Done!")

def keep_channel(channel):
    if (" Time " in channel): return True # keep begin time end time
    if (channel.count("_") < 1): return False
    if ("11" in channel): return False
    if (channel.count("_") > 1):
        print("Weird channel found:", channel)
        return False
    sp = channel.split("_")
    if (sp[0] == "1" or sp[0] == "2"): return False
    if (sp[1].lower() in ["tutor", "tutee", "p1", "p2"] and sp[0].isalpha()):
        return True
    else:
        print("Weird channel found:", channel)
        return False

def get_keep_list(header):
    keep = []
    for i in range(len(header)):
        if (keep_channel(header[i])): keep += [i]
    return keep


def filter_channels(src, dst):
    base = os.path.splitext(os.path.basename(src))[0]
    # print("Filtering", base, "...", end=" ")
    filename = dst + "/" + base + "_filtered.csv"
    with open(filename, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        reader = csv.reader(open(src))
        header = next(reader);
        print(base)
        keep = get_keep_list(header)
        newHeader = [header[i] for i in keep]
        writer.writerow(newHeader)
        # print("Writing body...", end=" ")
        for row in reader:
            newRow = []
            newRow = [(row[i] if (i < len(row)) else "") for i in keep]
            writer.writerow(newRow)
    # print("file complete")
    return

run_from_root("/Users/RaeLasko/Documents/CMU/ArticuLab/TAR Formatted Test")

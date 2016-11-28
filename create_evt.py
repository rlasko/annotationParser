import os
import csv
import bisect
import copy
from header import get_channels
from scalar_rapport_info_DELTA_ONLY import get_rapport_dict

start_path = "/Users/RaeLasko/Documents/CMU/ArticuLab/File cleaning/EVT_Delta_Only"
rapport_data = get_rapport_dict("/Users/RaeLasko/Documents/CMU/ArticuLab/File cleaning/2013_thin-slice_rapport_ratings.csv")

def get_ref_dict():
    dictionary = dict()
    count = 0
    for channel in get_channels():
        dictionary[count] = channel
        count += 1
    return dictionary

channel_reference_dict = get_ref_dict()
channels = get_channels()

# write each evt file
def create_evt(path, info_list):
    with open(path, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = "\t")
        # write events to file
        for e in info_list:
            writer.writerow([e])
        DS = os.path.splitext(os.path.basename(path))[0]
        rapport_list = rapport_data[DS]
        # write rapport scalar to file
        for e in rapport_list:
            writer.writerow([e])

# read each file and generate a list of events
def read_file(path):
    reader = csv.reader(open(path))
    header = next(reader)
    info_list = []
    for row in reader:
        if (len(row) < 3): continue
        time = row[0]
        for i in range(1, len(row[1:])):
            col = row[i]
            if col == "1":
                string = time + " " + "event." + header[i]
                info_list.append(string)
    return info_list

# Iterate across all files and start process
def start():
    assert(os.path.isdir(start_path))
    for filename in os.listdir(start_path):
        if ("evt" in filename or ".DS" in filename): continue
        print(filename)
        info_list = read_file(start_path + "/" + filename)
        if (not os.path.exists(start_path + "/evt")): os.makedirs(start_path + "/evt")
        create_evt(start_path + "/evt/" + filename[:-5] + ".evt", info_list)

start()

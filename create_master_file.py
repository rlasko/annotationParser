import os
import csv
import bisect
import copy
from header import get_channels

start_path = "/Users/RaeLasko/Documents/CMU/ArticuLab/File cleaning/Standarized work"

def get_ref_dict():
    dictionary = dict()
    count = 0
    for channel in get_channels():
        dictionary[channel] = count
        count += 1
    return dictionary

channel_reference_dict = get_ref_dict()
channels = get_channels()

def remove_row(row):
    for e in row:
        if e == "1":
            return False
    return True

# actually creates the master file using all the info
def create_master_file(path, dictionary, time_list):
    with open(path, "w") as csvfile:
        headerRow = ["Time"] + copy.deepcopy(channels)
        # headerRow = headerRow[:-8] # remove eyegaze
        writer = csv.writer(csvfile, delimiter = ",")
        writer.writerow(headerRow)
        for time in time_list:
            val = []
            for e in dictionary[time]:
                value = "1" if e == "x" else "0" # make zero or one
                val.append(value)
            # val = val[:-8] # remove eyegaze
            if (remove_row(val)): continue
            row = [time] + val
            writer.writerow(row)

# start parsing files
def start():
    assert(os.path.isdir(start_path))
    for folder in os.listdir(start_path):
        if (".DS" in folder or ".csv" in folder or "output" in folder): continue
        print (folder)
        folder_path = start_path + "/" + folder
        time_dict = dict()
        time_list = []
        for filename in os.listdir(folder_path):
            if (".DS" in filename): continue
            print(filename)
            file_path = folder_path + "/" + filename
            read_file_to_dict(file_path, time_dict, time_list)
        outputPath = start_path + "/output_annotations_only/" + folder + ".csv"
        if (not os.path.exists(start_path + "/output_annotations_only")): os.makedirs(start_path + "/output_annotations_only")
        create_master_file(outputPath , time_dict, time_list)

# prompt for user help
# . skips
def get_input():
    user_input = ""
    while "." not in user_input:
        user_input = input("Help! Input here:")
        if user_input == ".":
            return "."
        elif user_input in channel_reference_dict:
            return user_input

# actual work
# adds information to dictionary and list for later use
def read_file_to_dict(path, dictionary, time_list):
    reader = csv.reader(open(path))
    header = next(reader)
    for row in reader:
        if len(row) < 2: continue # Valid row has at least time field and one channel field
        time = row[0]
        # have not seen this time yet
        if (time not in dictionary):
            dictionary[time] = [""] * len(channels)
            bisect.insort(time_list, time)
        # parse channels
        for index in range(1, len(row)):
            channel = row[index].strip()
            if channel in ["", " ", "0.0"] or len(channel) < 2: continue
            # some entries have more than one annotation
            channel_name = channel.split(",")
            for i in range(len(channel_name)):
                if ("intimacy" in header[index].lower()):
                    if ("IL" in channel_name[i]):
                        channel_name[i] = channel_name[i].replace("IL", "LLI")
                if (" " in channel_name[i]):
                    channel_name.extend(channel_name[i].split(" "))
                    channel_name.pop(i)

            # most times, len will be 1
            for i in range(len(channel_name)):
                if ("QUALS" in channel_name[i] or "00" in channel_name[i] or "F-" in channel_name[i]): continue
                channel_name[i] = channel_name[i].strip()
                if (channel_name[i] in ["", " "]): continue
                # print("channel_name[i]", channel_name[i])
                channel_name[i] = channel_name[i].upper() if "g" not in channel_name[i] else channel_name[i]
                if "tutor" in header[index].lower():
                    channel_name[i] += "_Tutor"
                elif "tutee" in header[index].lower():
                    channel_name[i] += "_Tutee"
                else:
                    print("Corresponding Header:", header[i], ", Target:", channel_name[i])
                    get_input()
                    continue

                if (channel_name[i] not in channel_reference_dict): # need user help to match channel
                    print("Could not match channel:", channel_name[i])
                    user_input = get_input()
                    if user_input == ".":
                        continue
                    elif (user_input in channel_reference_dict):
                        channel_name[i] = user_input
                    else:
                        print("!!!!")
            # add to dictionary
            for channel in channel_name:
                # if ("g" in channel): continue # skip eye gaze
                if (channel in channel_reference_dict):
                    index = channel_reference_dict[channel]
                    dictionary[time][index] = "x"

start()

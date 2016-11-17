import os
import csv
import bisect
from header import get_channels

start_path = ""

def get_ref_dict():
    dictionary = dict()
    count = 0
    for channel in get_channels():
        dictionary[channel] = count
    return dictionary

channel_reference_dict = get_ref_dict()

def create_master_file(path,dictionary):
    with open(path, "w") as csvfile:
        pass

def start():
    assert(os.path.isdir(start_path))
    for folder in os.listdir(start_path):
        folder_path = start_path + "/" + folder
        time_dict = dict()
        time_list = []
        for filename in os.listdir(folder_path):
            file_path = folder_path + "/" + filename
            read_file_to_dict(file_path, time_dict, time_list)
        create_master_file()

def read_file_to_dict(path, dictionary, time_list):
    reader = csv.reader(open(path))
    header = next(reader)
    for row in reader:
        if len(row) < 2: continue # Valid row has at least time field and one channel field
        time = row[0]
        if (time not in dictionary):
            dictionary[time] = []
            bisect.insort(time_list, time)
        for i in range(1, len(row)):
            channel = row[i]
            if channel not in ["" or " "]:
                channel_name = channel.upper() if "g" not in channel else channel
                if "tutor" in header[i].lower():
                    channel_name += "_Tutor"
                elif "tutee" in header[i].lower():
                    channel_name += "_Tutee"
                else:
                    print("Corresponding Header:", header[i], "Target:", channel)
                    user_input = ""
                    while "continue" not in user_input:
                        user_input = input("Help!!")
                    continue

                if (channel_name not in channel_reference_dict):
                    user_input = ""
                    skip = False
                    while "continue" not in user_input and channel_name not in channel_reference_dict:
                        user_input = input("Help!!")
                        if user_input == "skip":
                            skip = True
                            break
                        elif user_input in channel_reference_dict:
                            channel_name = user_input
                    if skip: continue
                assert(channel_name not channel_reference_dict)
                dictionary[time].append(channel_name)
                

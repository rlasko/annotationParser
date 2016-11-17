import os
import csv
import bisect
from header import get_channels

start_path = "/Users/RaeLasko/Documents/CMU/ArticuLab/File cleaning/Standarized copy"

def get_ref_dict():
    dictionary = dict()
    count = 0
    for channel in get_channels():
        dictionary[channel] = count
    return dictionary

channel_reference_dict = get_ref_dict()

def create_master_file(path,dictionary):
    pass
    with open(path, "w") as csvfile:
        pass

def start():
    assert(os.path.isdir(start_path))
    for folder in os.listdir(start_path):
        if (".DS" in folder): continue
        print (folder)
        folder_path = start_path + "/" + folder
        time_dict = dict()
        time_list = []
        for filename in os.listdir(folder_path):
            if (".DS" in filename): continue
            print(filename)
            file_path = folder_path + "/" + filename
            read_file_to_dict(file_path, time_dict, time_list)
        # create_master_file()

def get_input():
    user_input = ""
    while "." not in user_input:
        user_input = input("Help! Input here:")
        if user_input == ".":
            return "."
        elif user_input in channel_reference_dict:
            return user_input

def read_file_to_dict(path, dictionary, time_list):
    reader = csv.reader(open(path))
    header = next(reader)
    for row in reader:
        if len(row) < 2: continue # Valid row has at least time field and one channel field
        time = row[0]
        if (time not in dictionary):
            dictionary[time] = []
            bisect.insort(time_list, time)
        for index in range(1, len(row)):
            channel = row[index].strip()
            if channel in ["", " ", "0.0"] or len(channel) < 2: continue
            channel_name = channel.split(",")
            for i in range(len(channel_name)):
                if (" " in channel_name[i]):
                    channel_name.extend(channel_name[i].split(" "))
                    channel_name.pop(i)
            for i in range(len(channel_name)):
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

                if (channel_name[i] not in channel_reference_dict):
                    print("Could not match channel:", channel_name[i])
                    user_input = get_input()
                    if user_input == ".":
                        continue
                    elif (user_input in channel_reference_dict):
                        channel_name[i] = user_input
                    else:
                        print("!!!!")
            dictionary[time].extend(channel_name)

start()

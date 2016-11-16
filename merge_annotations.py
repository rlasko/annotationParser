import csv
import os
from shutil import copyfile

# convert all files starting at a top level directory
def merge(origin):
    assert(os.path.isdir(origin))
    folders = os.listdir(origin)
    if ".DS" in folders[0]: folders.pop(0)
    loc = origin + "/" + folders[0]
    for filename in os.listdir(loc):
        if ".DS" in filename: continue
        new_name = filename.split("_")[0] + "_"
        session_folder = origin + "/" + new_name
        i = 0
        if (not os.path.exists(session_folder)): os.makedirs(session_folder)
        copyfile(loc + "/" + filename, session_folder + "/" + str(i) + filename )
        i += 1
        for other_folder in folders[1:]:
            if ".DS" in other_folder: continue
            this_loc = origin + "/" + other_folder
            other_files = os.listdir(this_loc)
            if  other_folder == new_name or "Tutoring" in other_folder: continue
            if filename not in other_files:
                print ("Error!! Could not find file", filename, "in", other_folder)
                continue
            copyfile(this_loc + "/" + filename, session_folder + "/" + str(i) + filename)
            i += 1

merge("/Users/RaeLasko/Documents/CMU/ArticuLab/File cleaning/Formatted work Merge")

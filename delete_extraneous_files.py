import os

def delete_extraneous_files(origin):
    if (os.path.isdir(origin) == False):
        if (origin.endswith(".csv")): # make sure it's a csv
            # delete
            filename = os.path.splitext(os.path.basename(origin))[0]
            if "channelsP" in filename:
                os.remove(origin)
    else:
        for filename in os.listdir(origin):
            delete_extraneous_files(origin + "/" + filename)

delete_extraneous_files("/Users/RaeLasko/Documents/CMU/ArticuLab/File cleaning/TA- need to merge/merged/corrected_channels")

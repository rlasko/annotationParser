import os

def standarize_paths(origin):
    if (os.path.isdir(origin) == False):
        if (origin.endswith(".csv")): # make sure it's a csv
            # rename
            filename = os.path.splitext(os.path.basename(origin))[0]
            i = filename.find("_") + 1
            sub = "T1" if "T1" in filename else "T2"
            new = os.path.dirname(origin) + "/" + filename[:i] + "_" + sub + ".csv"
            os.rename(origin, new)
    else:
        for filename in os.listdir(origin):
            standarize_paths(origin + "/" + filename)

standarize_paths("/Users/RaeLasko/Documents/CMU/ArticuLab/File cleaning/Formatted work final/_Head Nods")

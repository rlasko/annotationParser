import os

def run_time_fix(origin):
    if (os.path.isdir(origin) == False):
        if (origin.endswith(".csv")): # make sure it's a csv
            # delete
            filename = os.path.splitext(os.path.basename(origin))[0]
            print("Changing", filename + "...")

    else:
        for filename in os.listdir(origin):
            run_time_fix(origin + "/" + filename)


def change_time(src,dst):
    

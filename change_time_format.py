import os
import csv

# traverse folder system
def run_time_fix(origin):
    if (os.path.isdir(origin) == False):
        if (origin.endswith(".csv")): # make sure it's a csv
            # delete
            name = os.path.dirname(origin) + "/_timeFix" # create new dir
            if (not os.path.exists(name)): os.makedirs(name)

            filename = os.path.splitext(os.path.basename(origin))[0]
            print(os.path.dirname(origin))
            print("Changing", filename + "...")
            change_time(origin,name)
    else:
        for filename in os.listdir(origin):
            if filename == "_timeFix": continue # don't modify output folder
            run_time_fix(origin + "/" + filename)

# convert time to seconds
def get_second(time):
    assert(isinstance(time, str))
    assert(time.count(".") == 1 or time.count(".") == 0)
    if time.count(".") != 1:
        t = time
        mm = "00"
    else:
        t, mm = time.split(".")
        mm = mm[0:2] # some mms are too long
    tArr = t.split(":")
    assert(len(tArr) in [2,3])
    if len(tArr) == 3 and tArr[0] not in ["0", "00"]:
        print (tArr, "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    if len(tArr) == 2:
        tArr = [0] + tArr
    seconds = int(tArr[0]) * 3600 + int(tArr[1]) * 60 + int(tArr[2]) + int(mm) / 10**len(mm)
    seconds = float(format(seconds, ".2f")) # truncate to two decimals
    return seconds


def change_time(src,dst):
    base = os.path.splitext(os.path.basename(src))[0]
    filename = dst + "/" + base + "_time.csv"
    # write new file
    with open(filename, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        reader = csv.reader(open(src))
        header = next(reader)
        writer.writerow(header)
        # add_hour = False
        last = -1
        for row in reader:
            if not (row[0].count(".") == 1 and row[0].count(":") == 0):
                seconds = get_second(row[0])
                if seconds >= last:
                    last = seconds
                else: # account for inconsistencies - some files didn't include hour field
                    seconds = 3600 + seconds
                    seconds = float(format(seconds, ".2f"))
                    last = seconds

                row[0] = seconds
            writer.writerow(row)
    return

run_time_fix("/Users/RaeLasko/Documents/CMU/ArticuLab/File cleaning/_Tutoring Strategies")

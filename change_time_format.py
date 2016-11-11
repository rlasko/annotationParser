import os

def run_time_fix(origin):
    if (os.path.isdir(origin) == False):
        if (origin.endswith(".csv")): # make sure it's a csv
            # delete
            name = os.path.dirname(origin) + "/_timeFix" # create new dir
            if (not os.path.exists(name)): os.makedirs(name)
            change_time(origin,name)
            filename = os.path.splitext(os.path.basename(origin))[0]
            print("Changing", filename + "...")

    else:
        for filename in os.listdir(origin):
            run_time_fix(origin + "/" + filename)

def get_second(time):
    assert(isinstance(time, str))
    assert(time.count(".") == 1)
    t, mm = time.split(".")
    tArr = t.split(":")
    assert(len(tArr) in [2,3])
    if len(tArr) == 2:
        tArr = [0] + tArr
    seconds = int(tArr[0]) * 3600 + int(tArr[1]) * 60 + int(tArr[2]) + mm
    return seconds


def change_time(src,dst):
    base = os.path.splitext(os.path.basename(src))[0]
    filename = dst + "/" + base + "_time.csv"
    with open(filename, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        reader = csv.reader(open(src))
        header = next(reader)
        writer.writerow(header)
        for row in reader:
            row[0] = get_second(row[0])
            writer.writerow(row)
    return

run_time_fix("/Users/RaeLasko/Documents/CMU/ArticuLab/File cleaning/Seconds test")

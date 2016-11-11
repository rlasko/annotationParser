from datetime import datetime, timedelta
import csv
import os

def run_from_root(origin):
    print(origin)
    if (os.path.isdir(origin) == False):
        print("Need a folder")
        return
    for folder in os.listdir(origin):
        print(folder)
        if "Tutoring" in folder:
            continue
        if ".DS" in folder:
            continue
        for filename in os.listdir(origin + "/" + folder):
            if ".DS" in filename or os.path.isdir(origin + "/" + filename):
                continue
            name = origin + "/" + folder + "/time_fix"
            if (not os.path.exists(name)): os.makedirs(name)
            fix(origin + "/" + folder + "/" + filename, name)

def get_date(row):
    for i in range(len(row)):
        if "Begin" in row[i]:
            return i
    print("error")
    return 1

def fix(src, dst):
    base = os.path.splitext(os.path.basename(src))[0]
    add_hour = False
    newFile = dst + "/" + base + ".csv"
    reader = csv.reader(open(src))
    header = next(reader)
    date_index = get_date(header)
    with open(newFile, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        writer.writerow(header)
        last = 0
        for row in reader:
            date_string = row[date_index]
            if (len(date_string) > 2):
                try:
                    date = datetime.strptime(date_string, "%M:%S.%f")
                    if (date.minute < last): print (base)
                    if (date.minute < last or add_hour):
                        add_hour = True
                        date += timedelta(hours=1)
                    last = date.minute
                    row[date_index] = str(date.strftime("%H:%M:%S.%f"))
                except:
                    print("There was an error with:", row)

            writer.writerow(row)

run_from_root("/Users/RaeLasko/Documents/CMU/ArticuLab/TAR Formatted Files copy")

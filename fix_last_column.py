import os
import csv

def run(origin, matchFolder):
    if (os.path.isdir(origin) == False):
        if (origin.endswith(".csv")): # make sure it's a csv
            name = os.path.dirname(origin) + "/_fix" # create new dir
            if (not os.path.exists(name)): os.makedirs(name)
            print(os.path.dirname(origin))
            match_and_fix(origin,name, matchFolder)
    else:
        for filename in os.listdir(origin):
            if filename == "_fix": continue # prevent filtering already filtered files
            run(origin + "/" + filename, matchFolder)

def match_and_fix(src, dst, match):
    base = (os.path.splitext(os.path.basename(src))[0]).split("_")[0] + "_"
    for f in os.listdir(match):
        if base in f:
            fix(src,dst,match + "/" + f)

def find(L, target):
    for i in range(len(L)):
        if target in L[i]:
            return i
    return -1

def time_match(a,b):
    assert(a.count(".") == 1 or a.count(".") == 0)
    if a.count(".") != 1:
        t = a
    else:
        t = a.split(".")[0]
    tArr = t.split(":")
    if (len(tArr) not in [2,3]):
        print("!!!!", a)
        print(tArr)
    assert(len(tArr) in [2,3])
    if len(tArr) == 2:
        tArr = [0] + tArr
    min_a = tArr[1]
    sec_a = tArr[2]

    assert(b.count(".") == 1 or b.count(".") == 0)
    if b.count(".") != 1:
        t2 = b
    else:
        t2 = b.split(".")[0]
    tArr2 = t2.split(":")
    if (len(tArr2) not in [2,3]):
        print("!!!!", b)
        print(tArr2)
    assert(len(tArr2) in [2,3])
    if len(tArr2) == 2:
        tArr2 = [0] + tArr2
    min_b = tArr2[1]
    sec_b = tArr2[2]
    return min_a == min_b and sec_a == sec_b


def fix(src, dst, match_file):
    matchReader = csv.reader(open(match_file))
    srcReader = csv.reader(open(src))
    base = (os.path.splitext(os.path.basename(src))[0])
    print(base)
    filename = dst + "/" + base + "_column_fix.csv"
    with open(filename, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        match_header = next(matchReader)
        match_begin_time_i = find(match_header,"Begin Time")
        src_header = next(srcReader)
        first_src_row = next(srcReader)
        start_time = first_src_row[0]
        needed_data = (src_header[-1].split("_"))[0]
        if (find(match_header[::-1],needed_data)) == -1:
            print (needed_data)
            print(match_header)
            print("Unable to find wanted column")
            return
        match_i = len(match_header)-(find(match_header[::-1],needed_data)) - 1
        if match_begin_time_i == -1:
            print("Could not find time field!!")
            return
        start_matching = False
        writer.writerow(src_header)
        for row in matchReader:
            if (row[match_begin_time_i] == "" or row[match_begin_time_i] == " "):
                continue
            if time_match(row[match_begin_time_i], start_time) and not start_matching:
                new_start_row = first_src_row
                new_start_row[-1] = row[match_i]
                start_matching = True
                writer.writerow(new_start_row)
                continue
            if (start_matching):
                try:
                    new_start_row = next(srcReader)
                except:
                    return
                if not time_match(row[match_begin_time_i], new_start_row[0]):
                    print("Times do not match", new_start_row[0], row[match_begin_time_i])
                    return
                new_start_row[-1] = row[match_i]
                writer.writerow(new_start_row)
        if not start_matching:
            print("ERROR: FILE COULD NOT BE MATCHED!!!!!!!!!!!!!!!!!!!!!!" )

run("/Users/RaeLasko/Documents/CMU/ArticuLab/MERGE/_Eye Gaze","/Users/RaeLasko/Documents/CMU/ArticuLab/MERGE/EG_converted")
run("/Users/RaeLasko/Documents/CMU/ArticuLab/MERGE/_Mix-SD","/Users/RaeLasko/Documents/CMU/ArticuLab/MERGE/SD_converted")
run("/Users/RaeLasko/Documents/CMU/ArticuLab/MERGE/_Mix-SE","/Users/RaeLasko/Documents/CMU/ArticuLab/MERGE/SE_converted")
run("/Users/RaeLasko/Documents/CMU/ArticuLab/MERGE/_Praise","/Users/RaeLasko/Documents/CMU/ArticuLab/MERGE/PR_converted")
run("/Users/RaeLasko/Documents/CMU/ArticuLab/MERGE/_Reciprocation","/Users/RaeLasko/Documents/CMU/ArticuLab/MERGE/RCP_converted")
run("/Users/RaeLasko/Documents/CMU/ArticuLab/MERGE/_Social Norm Violation","/Users/RaeLasko/Documents/CMU/ArticuLab/MERGE/VSN_converted")
run("/Users/RaeLasko/Documents/CMU/ArticuLab/MERGE/_Tutoring Strategies","/Users/RaeLasko/Documents/CMU/ArticuLab/MERGE/TA_converted")

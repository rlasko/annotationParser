import os
import csv
import pprint

def header_values(origin):
    headers = set()
    run(origin, headers)
    return headers

def run(origin, headers):
    if (os.path.isdir(origin) == False):
        # print(os.path.dirname(origin))
        if (origin.endswith(".csv")): # make sure it's a csv
            headers.update(get_headers(origin))
    else:
        for filename in os.listdir(origin):
            run(origin + "/" + filename, headers)

def get_headers(src):
    annotation = set()
    reader = csv.reader(open(src))
    base = os.path.splitext(os.path.basename(src))[0]
    # print(base)
    next(reader)
    for row in reader:
        for c in row[1:]:
            if "," in c:
                for i in c.split(","):
                    i = i.strip()
                    if (i.lower() == "ih"):
                        print("found",src)
                    annotation.add(i)
            elif (" " in c):
                for i in c.split(" "):
                    i = i.strip()
                    if (i.lower() == "ih"):
                        print("found",src)
                    annotation.add(i)
            else:
                c = c.strip()
                if (c.lower() == "ih"):
                    print("found",src)
                annotation.add(c)
    return annotation

b = header_values("/Users/RaeLasko/Documents/CMU/ArticuLab/File cleaning/Formatted work")
print(b)

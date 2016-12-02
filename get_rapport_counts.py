import os
import csv

def get_rapport_dict(path):
    reader = csv.reader(open(path))
    header = next(reader)
    rapport_dict_values_only = dict()
    rapport_dict_delta_only = dict()
    rapport_dict_delta_values = dict()

    last_row = []
    for row in reader:
        for i in range(len(row)):
            if (row[i].strip() != ""):
                last = last_row[i].strip() if last_row != [] else "0"
                curr = row[i].strip()

                if (int(curr) == 0):
                    continue
                val = int(curr) - int(last)
                val = "+" + str(val) if val > 0 else str(val)

                if ("Rapport" + curr not in rapport_dict_values_only.keys()):
                    rapport_dict_values_only["Rapport" + curr] = 0
                rapport_dict_values_only["Rapport" + curr] += 1

                if (int(last) == 0):
                    continue
                if ("Rapport" + last + "to" + curr not in rapport_dict_delta_values.keys()):
                    rapport_dict_delta_values["Rapport" + last + "to" + curr] = 0
                rapport_dict_delta_values["Rapport" + last + "to" + curr] += 1

                if ("Rapport" + val not in rapport_dict_delta_only.keys()):
                    rapport_dict_delta_only["Rapport" + val] = 0
                rapport_dict_delta_only["Rapport" + val] += 1
        last_row = row

    with open(os.path.dirname(path) + "/histogram_data.csv", "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        for i in range(max(len(rapport_dict_delta_only), len(rapport_dict_values_only), len(rapport_dict_delta_values))):
            row = [""] * 8
            if len(rapport_dict_delta_only) > 0:
                (key1,val1) = rapport_dict_delta_only.popitem()
                row[0] = key1
                row[1] = val1

            if len(rapport_dict_values_only) > 0:
                (key2,val2) = rapport_dict_values_only.popitem()
                row[3] = key2
                row[4] = val2

            if len(rapport_dict_delta_values) > 0:
                (key3,val3) = rapport_dict_delta_values.popitem()
                row[6] = key3
                row[7] = val3
            writer.writerow(row)


get_rapport_dict("/Users/RaeLasko/Documents/CMU/ArticuLab/File cleaning/2013_thin-slice_rapport_ratings.csv")

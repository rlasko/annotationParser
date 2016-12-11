import os
import csv

def add_missing_vals(d):
    for session in d.keys():
        for i in range(1,8):
             if "Rapport" + str(i) not in d[session]["rapport_dict_values_only"]:
                 d[session]["rapport_dict_values_only"]["Rapport" + str(i)] = 0
        for i in range(-5,6):
             if "Rapport" + str(i) not in d[session]["rapport_dict_delta_only"]:
                 d[session]["rapport_dict_delta_only"]["Rapport" + str(i)] = 0
        for i in range(1,8):
            for j in range(1,8):
                v = "Rapport" + str(i) + "to" + str(j)
                if v not in d[session]["rapport_dict_delta_values"]:
                    d[session]["rapport_dict_delta_values"][v] = 0

def get_rapport_dict(path):
    reader = csv.reader(open(path))
    header = next(reader)

    all_dict = dict()

    last_row = []
    for i in range(len(header)):
        all_dict[header[i]] = dict()
        all_dict[header[i]]["rapport_dict_values_only"] = dict()
        all_dict[header[i]]["rapport_dict_delta_only"] = dict()
        all_dict[header[i]]["rapport_dict_delta_values"] = dict()

    for row in reader:
        for i in range(len(row)):
            if (row[i].strip() != ""):
                last = last_row[i].strip() if last_row != [] else "0"
                curr = row[i].strip()

                if (int(curr) == 0):
                    continue
                val = int(curr) - int(last)
                val = "+" + str(val) if val > 0 else str(val)

                if ("Rapport" + curr not in all_dict[header[i]]["rapport_dict_values_only"].keys()):
                    all_dict[header[i]]["rapport_dict_values_only"]["Rapport" + curr] = 0
                all_dict[header[i]]["rapport_dict_values_only"]["Rapport" + curr] += 1

                if (int(last) == 0):
                    continue
                if ("Rapport" + last + "to" + curr not in all_dict[header[i]]["rapport_dict_delta_values"].keys()):
                    all_dict[header[i]]["rapport_dict_delta_values"]["Rapport" + last + "to" + curr] = 0
                all_dict[header[i]]["rapport_dict_delta_values"]["Rapport" + last + "to" + curr] += 1

                if ("Rapport" + val not in all_dict[header[i]]["rapport_dict_delta_only"].keys()):
                    all_dict[header[i]]["rapport_dict_delta_only"]["Rapport" + val] = 0
                all_dict[header[i]]["rapport_dict_delta_only"]["Rapport" + val] += 1
        last_row = row
        add_missing_vals(all_dict)

    for key in sorted(all_dict):
        write_file(path, key, all_dict[key]["rapport_dict_values_only"],all_dict[key]["rapport_dict_delta_only"],all_dict[key]["rapport_dict_delta_values"])


def write_file(path, session, rapport_dict_values_only,rapport_dict_delta_only,rapport_dict_delta_values):
    with open(os.path.dirname(path) + "/histogram_data" + session + ".csv", "w") as csvfile:
        writer = csv.writer(csvfile, delimiter = ",")
        writer.writerow([session])

        rapport_dict_delta_only_list = ["Rapport-5","Rapport-4","Rapport-3","Rapport-2","Rapport-1","Rapport0","Rapport1","Rapport2","Rapport3","Rapport4","Rapport5"]
        rapport_dict_values_only_list = sorted(rapport_dict_values_only)
        rapport_dict_delta_values_list = sorted(rapport_dict_delta_values)

        for i in range(max(len(rapport_dict_delta_only), len(rapport_dict_values_only), len(rapport_dict_delta_values))):
            row = [""] * 8

            if i < len(rapport_dict_values_only_list):
                (key2,val2) = rapport_dict_values_only_list[i], rapport_dict_values_only[rapport_dict_values_only_list[i]]
                row[0] = key2
                row[1] = val2

            if i < len(rapport_dict_delta_only_list):
                (key1,val1) = rapport_dict_delta_only_list[i],rapport_dict_delta_only[rapport_dict_delta_only_list[i]]
                row[3] = key1
                row[4] = val1

            if i < len(rapport_dict_delta_values_list):
                (key3,val3) = rapport_dict_delta_values_list[i], rapport_dict_delta_values[rapport_dict_delta_values_list[i]]
                row[6] = key3
                row[7] = val3
            writer.writerow(row)
        writer.writerow([" "] * 3)
        writer.writerow([" "] * 3)

get_rapport_dict("/Users/RaeLasko/Documents/CMU/ArticuLab/File cleaning/2013_thin-slice_rapport_ratings.csv")

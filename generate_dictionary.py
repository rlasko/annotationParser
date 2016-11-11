import csv
import pprint

csvPath = "/Users/RaeLasko/Documents/CMU/ArticuLab/File cleaning/TAR source files/Delivery_styles_data.csv"

def dictionary():
    reader = csv.reader(open(csvPath))
    sessionMap = {}
    next(reader) # skip header
    roleIndex = 7
    participantIndex = 6
    sessionIndex = 5
    for row in reader:
        dyadSession = row[0][:-1] if row[0][-1] == "_" else row[0]
        if dyadSession not in sessionMap.keys():
            sessionMap[dyadSession] = dict()
        if row[participantIndex] not in sessionMap[dyadSession].keys():
            sessionMap[dyadSession][row[participantIndex]] = dict()
        sessionMap[dyadSession][row[participantIndex]][row[sessionIndex]] = row[roleIndex]
    return sessionMap

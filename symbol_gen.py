import csv
import requests
from contextlib import closing
def symbolgen():
    BSESym = dict()
    NSESym = dict()
    BSECodes = dict()
    Sectors = dict()
    f = open("BSEList.csv")
    for line in f:
        line = line.strip('\n')
        (key, val) = line.split(",")
        BSESym[key] = val

    f = open("NSEList.csv")
    for line in f:
        line = line.strip('\n')
        (key, val) = line.split(",")
        NSESym[key] = val

    f = open("BSECodes.csv")
    for line in f:
        line = line.strip('\n')
        (key, val) = line.split(",")
        BSECodes[key] = val

    with open("SectorNames.csv", 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            Sectors[row[0]] = row[1]

    BSESym.update(NSESym)
    return(BSESym,BSECodes,NSESym,Sectors)





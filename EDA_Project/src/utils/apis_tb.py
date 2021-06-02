import pandas as pd
import json
import csv

def cvs_to_json(fullpath, extension):
    csvFilePath = fullpath + extension + '.csv'
    jsonFilePath = fullpath + extension + '.json'
    data = {}
    with open(csvFilePath) as csvFile:
        csvReader = csv.DictReader(csvFile)
        for csvRow in csvReader:
            year = csvRow['YEAR']
            data[year] = csvRow
    with open(jsonFilePath, 'w') as jsonFile:
        jsonFile.write(json.dumps(data, indent= 4))
    test = pd.read_json(jsonFilePath)
    return test.to_json()


def read_json(fullpath):
    with open(fullpath, "r") as json_file_readed:
        json_readed = json.load(json_file_readed)
    return json_readed
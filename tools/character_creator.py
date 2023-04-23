import os
import json

jsonData = {"tables":{},"classes":{},"spells":{},"skills":{}}

for jsonDataset in list(jsonData.keys()):
    with open("..\\data\\{}\\data.json".format(jsonDataset)) as json_file:
        jsonData[jsonDataset] = json.load(json_file)
        
print(jsonData)
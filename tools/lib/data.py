import json
import os

cwd = os.getcwd()
dataRoot = ""
delverData = {}

def findDataRoot():
    global dataRoot
    if "tools" in cwd:
        if "lib" in cwd:
            dataRoot = "../../data/"
        else:        
            dataRoot = "../data/"
       
def mkDataImport():
    global delverData
    findDataRoot()
    for dataSet in os.listdir(dataRoot):
        with open('{}{}/data.json'.format(dataRoot,dataSet)) as json_file:
            delverData[dataSet] = json.load(json_file)       
    return delverData

def findDataStructure(dataType,dataName):
    mkDataImport()
    
    dataStruct = delverData[dataType]
    datum = dataStruct[dataName]
    
    return datum
    

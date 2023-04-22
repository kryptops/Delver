import json
from datetime import datetime

###
# There are multiple elements used in standard delver documentation that need to be parsed into json objects. This script parses entity profiles into json.
# Put any tables you want to parse into .\\input\\entities.txt, separated by a line matching the format DelverTableEntity.<entity type>_<name of entity>
# Run the script. 
###

jDict = {"undead":{},"faerie":{},"interloper":{},"monster":{},"automaton":{},"being":{},"daemon":{},"creature":{},"angel":{}}
fileData = open(".\\input\\entities.txt",'r',encoding='utf-8').read()
dataByLine = fileData.splitlines()


def primaryConfirmLoop():
    while True:
        confirmByInputB = input("[!] Is this correct? (Y/N): ")
        if confirmByInputB.lower() in ["y","ye","yes"]:
            break
        elif confirmByInputB.lower() in ["n","no"]:
            print("[+] Aborting due to user input")
            break
        else:
            print("[!] Invalid input, please specify Y/N)...")
            
def writeToErrLog():
    dataFile = ".\\error\\raw_error_data_{}.log".format(datetime.now().strftime("%Y%m%d"))
    errorFileH = open(dataFile,'w')
    errorFileH.write(str(jDict))
    errorFileH.close()
    print("[+] Wrote raw entity data to {}. Exiting...".format(dataFile))          

def writeToJson():
    dataFile = ".\\output\\entity_data_{}.json".format(datetime.now().strftime("%Y%m%d"))
    with open(dataFile,'w') as jsonDataFileHandle:
        json.dump(jDict, jsonDataFileHandle, indent=4, sort_keys=True)
    print("[+] Wrote jsonified entity data to {}! Enjoy!".format(dataFile))

def mkJsonDefault(entityData):
    finalOut = {}
    for lineData in entityData:
        if "description" not in lineData.lower():
            cleanFmt = lineData.replace(" ","")
            keyValData = cleanFmt.split(":")
            finalOut[keyValData[0].lower().strip()] = keyValData[1]
        else:
            keyValData = lineData.split(":")
            finalOut["Description"] = keyValData[1].strip()
    return finalOut

def mkJsonSummary(entityData):
    return mkJsonDefault(entityData)

def mkJsonAttributes(entityData):
    return mkJsonDefault(entityData)

def mkJsonStats(entityData):
    return mkJsonDefault(entityData)

def mkJsonAdjustments(entityData):
    finalOut = {}
    for lineData in entityData:
        cleanFmt = lineData.replace(" ","")
        keyValData = cleanFmt.split(":")
        finalOut[keyValData[0].lower().strip()] = keyValData[1].split(",")      
    return finalOut        

def mkJsonProficiencies(entityData):
    finalOut = {}
    for lineData in entityData:
        keyValData = lineData.split("(")
        finalOut[keyValData[0].lower().strip()] = keyValData[1][:-1]      
    return finalOut     

def mkJsonActions(entityData):
    finalOut = {}
    if len(entityData) > 1:
        if entityData[0].strip()[-2:] != "//":
            print("[!] ERROR! Incorrect Formatting for actions!")
    fmtEntityData = "".join(entityData)
    sepActions = fmtEntityData.split("//")
    for discreteAction in sepActions:
        if "(" in discreteAction:
            keyValData = discreteAction.strip().split("(")
            finalOut["_".join(keyValData[0].lower().strip().split(" "))] = keyValData[1][:-1].split(" | ")
        else:
            finalOut["_".join(discreteAction.lower().strip().split(" "))] = "NULL"
    return finalOut
    

def mkJsonFeatures(entityData):
    finalOut = {}
    for lineData in entityData:
        print(lineData)
        keyValData = lineData.split("(")
        finalOut["_".join(keyValData[0].lower().strip().split(" "))] = keyValData[1][:-1]      
    return finalOut  

def mkJsonEntityFacsimile(entityNameProp,entityData,entityTypeName):    
    jRawData = {}
    
    jRawData["summary"] = mkJsonSummary(entityData[1:6])
    jRawData["attributes"] = mkJsonAttributes(entityData[7:11])
    jRawData["stats"] = mkJsonStats(entityData[12:17])
    jRawData["adjustments"] = mkJsonAdjustments(entityData[18:21])
    
    entityDataNew = []
    
    for lineFeed in entityData[22:]:
        if "- actions -" in lineFeed.lower():
            jRawData["proficiencies"] = mkJsonProficiencies(entityDataNew)
            entityDataNew=[]
        elif "- features -" in lineFeed.lower():
            jRawData["actions"] = mkJsonActions(entityDataNew)
            entityDataNew=[]
        else:
            entityDataNew.append(lineFeed)  
        
    #if jRawData["features"] == {}
    jRawData["features"] = mkJsonFeatures(entityDataNew)
     
    jDict[entityTypeName.lower()][entityNameProp.lower()] = jRawData


entityNameProp = ""
entityData = []
entityTypeName = ""

entityNames = []
for textLinePre in dataByLine:
    if "DelverEntityData." in textLinePre:
        splitTextPre = textLinePre.split(".")
        if " " in splitTextPre[1].split("_")[1]:
            entityNames.append(splitTextPre[1].split("_")[1].replace(" ","_"))
        else:
            entityNames.append("_".join(splitTextPre[1].split("_")[1:]))        
        
print("[!] Detected {} entities for parsing:".format(len(entityNames)))
for eName in entityNames:
    print("[.]  Discovered entity '{}'".format(eName))

primaryConfirmLoop()
    
for textLine in dataByLine:
    if "DelverEntityData." in textLine:
        if len(entityData) > 0:
            mkJsonEntityFacsimile(entityNameProp,entityData,entityTypeName)
            entityData = []
        splitText = textLine.split(".")
        if " " in splitText[1].split("_")[1]:
            entityNameProp = splitText[1].split("_")[1].replace(" ","_")
        else:    
            entityNameProp = "_".join(splitText[1].split("_")[1:])
        entityTypeName = splitText[1].split("_")[0]
        print("[+] Attempting to parse {}...".format(entityNameProp))
    elif textLine == "DelverEntityEnd":
        mkJsonEntityFacsimile(entityNameProp,entityData,entityTypeName)
        break
    else:
        entityData.append(textLine)
writeToJson()

#print(jDict)			
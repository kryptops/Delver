import json
from datetime import datetime

###
# There are multiple elements used in standard delver documentation that need to be parsed into json objects. This script parses entity profiles into json.
# Put any tables you want to parse into .\\input\\classes.txt, separated by a line matching the format DelverTableEntity.<entity type>_<name of entity>
# Run the script. 
###

jDict = {"athletics":[],"martial":[],"arcana":[],"social":[],"awareness":[],"tradecraft":[],"wisdom":[]}
fileData = open(".\\input\\skills.txt",'r',encoding='utf-8').read()
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
    dataFile = ".\\output\\skill_data_{}.json".format(datetime.now().strftime("%Y%m%d"))
    with open(dataFile,'w') as jsonDataFileHandle:
        json.dump(jDict, jsonDataFileHandle, indent=4, sort_keys=True)
    print("[+] Wrote jsonified class feature data to {}! Enjoy!".format(dataFile))


for splitText in dataByLine:
    jRawData = {}
    fieldSplit = splitText.split(".")
    baseSplit = fieldSplit[1].replace(")","").split("(")
    jRawData["base_atter"] = baseSplit[1]
    jRawData["name"] = baseSplit[0]
    jDict[fieldSplit[0].lower()].append(jRawData)

writeToJson()

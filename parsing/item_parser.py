import json
from datetime import datetime

###
# There are multiple elements used in standard delver documentation that need to be parsed into json objects. This script parses entity profiles into json.
# Put any tables you want to parse into .\\input\\items.txt, separated by a line matching the format DelverTableEntity.<entity type>_<name of entity>
# Run the script. 
###

jDict = {}
fileData = open(".\\input\\items.txt",'r',encoding='utf-8').read()
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
    dataFile = ".\\output\\item_data_{}.json".format(datetime.now().strftime("%Y%m%d"))
    with open(dataFile,'w') as jsonDataFileHandle:
        json.dump(jDict, jsonDataFileHandle, indent=4, sort_keys=True)
    print("[+] Wrote jsonified entity data to {}! Enjoy!".format(dataFile))


def mkJsonitemFacsimile(itemNameProp,itemData): 
    jRawData = {}
    
    for lineFeed in itemData:
        if ":" not in lineFeed:
            jRawData[list(jRawData.keys())[-1]] += lineFeed
        else:
            fmtLine = lineFeed.split(":")
            jRawData[fmtLine[0].strip().lower()] = fmtLine[1].strip()
    
    jDict[itemNameProp] = jRawData
    
        

ItemNameProp = ""
itemData = []

itemNames = []
for textLinePre in dataByLine:
    if "delveritemname." in textLinePre.lower():
        splitTextPre = textLinePre.split(".")
        if " " in splitTextPre[1]:
            itemNames.append(splitTextPre[1].strip().replace(" ","_").replace("’","'").replace("'",""))
        else:
            itemNames.append("_".join(splitTextPre[1:]))        
        
print("[!] Detected {} items for parsing:".format(len(itemNames)))
for eName in itemNames:
    print("[.]  Discovered item '{}'".format(eName))

primaryConfirmLoop()
    
for textLine in dataByLine:
    if "delveritemname." in textLine.lower():
        if len(itemData) > 0:
            mkJsonitemFacsimile(ItemNameProp,itemData)
            itemData = []
        splitText = textLine.split(".")
        if " " in splitText[1]:
            ItemNameProp = splitText[1].strip().replace(" ","_").replace("’","'").replace("'","")
        else:    
            ItemNameProp = "_".join(splitText[1:])
        print("[+] Attempting to parse {}...".format(ItemNameProp))
    elif textLine == "DelveritemEnd":
        mkJsonitemFacsimile(ItemNameProp,itemData)
        break
    else:
        itemData.append(textLine)
writeToJson()

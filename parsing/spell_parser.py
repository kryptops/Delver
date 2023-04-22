import json
from datetime import datetime

###
# There are multiple elements used in standard delver documentation that need to be parsed into json objects. This script parses entity profiles into json.
# Put any tables you want to parse into .\\input\\spells.txt, separated by a line matching the format DelverTableEntity.<entity type>_<name of entity>
# Run the script. 
###

jDict = {"alchemy":[],"apotropaism":[],"conjuration":[],"divination":[],"enchantment":[],"illusion":[],"necromancy":[],"olethromancy":[]}
fileData = open(".\\input\\spells.txt",'r',encoding='utf-8').read()
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
    dataFile = ".\\output\\spell_data_{}.json".format(datetime.now().strftime("%Y%m%d"))
    with open(dataFile,'w') as jsonDataFileHandle:
        json.dump(jDict, jsonDataFileHandle, indent=4, sort_keys=True)
    print("[+] Wrote jsonified entity data to {}! Enjoy!".format(dataFile))


def mkJsonSpellFacsimile(spellNameProp,spellData,spellTypeName): 
    jRawData = {}
    
    jRawData["name"] = spellNameProp
    
    for dataField in spellData[0:6]:
        rawFieldSplit = dataField.split(":")
        jRawData[rawFieldSplit[0].strip().lower()] = rawFieldSplit[1].strip().lower()
    
    if len(spellData) > 7:
        descriptionData = ", ".join(spellData[7:]).replace(".,",",")
        jRawData["description"] = ("{}{}".format("".join(spellData[6].split(":")[1:]).strip(),descriptionData)).replace("…",": ").replace("...",":")
    else:
        jRawData["description"] = "".join(spellData[6].split(":")[1:]).strip()
    
    jDict[spellTypeName.lower()].append(jRawData)
    
        

spellNameProp = ""
spellData = []
spellTypeName = ""

spellNames = []
for textLinePre in dataByLine:
    if "DelverSpellName." in textLinePre:
        splitTextPre = textLinePre.split(".")
        if " " in splitTextPre[1].split("_")[1]:
            spellNames.append(splitTextPre[1].split("_")[1].replace(" ","_"))
        else:
            spellNames.append("_".join(splitTextPre[1].split("_")[1:]))        
        
print("[!] Detected {} spells for parsing:".format(len(spellNames)))
for eName in spellNames:
    print("[.]  Discovered entity '{}'".format(eName))

primaryConfirmLoop()
    
for textLine in dataByLine:
    if "DelverSpellName." in textLine:
        if len(spellData) > 0:
            mkJsonSpellFacsimile(spellNameProp,spellData,spellTypeName)
            spellData = []
        splitText = textLine.split(".")
        if " " in splitText[1].split("_")[1]:
            spellNameProp = splitText[1].split("_")[1].strip().replace(" ","_").replace("’","'").replace("'","")
        else:    
            spellNameProp = "_".join(splitText[1].split("_")[1:])
        spellTypeName = splitText[1].split("_")[0]
        print("[+] Attempting to parse {}...".format(spellNameProp))
    elif textLine == "DelverSpellEnd":
        mkJsonSpellFacsimile(spellNameProp,spellData,spellTypeName)
        break
    else:
        spellData.append(textLine)
writeToJson()
		
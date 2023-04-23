import json
from datetime import datetime

###
# There are multiple elements used in standard delver documentation that need to be parsed into json objects. This script parses entity profiles into json.
# Put any tables you want to parse into .\\input\\classes.txt, separated by a line matching the format DelverTableEntity.<entity type>_<name of entity>
# Run the script. 
###

jDict = {"warrior":[],"mage":[],"rogue":[],"scholar":[]}
fileData = open(".\\input\\classes.txt",'r',encoding='utf-8').read()
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
    dataFile = ".\\output\\class_data_{}.json".format(datetime.now().strftime("%Y%m%d"))
    with open(dataFile,'w') as jsonDataFileHandle:
        json.dump(jDict, jsonDataFileHandle, indent=4, sort_keys=True)
    print("[+] Wrote jsonified class feature data to {}! Enjoy!".format(dataFile))


def mkJsonClassFacsimile(ClassNameProp,classData,FeatLvlProp,FeatNameProp): 
    jRawData = {}
    
    jRawData["name"] = FeatNameProp
    jRawData["level"] = FeatLvlProp
    jRawData["options"] = []
    jRawData["caveats"] = []
    
    rawDescriptor = ""
    
    if len(classData) == 1:
        rawDescriptor = classData[0]
        jRawData["description"] = rawDescriptor.split("-")[1].strip()

    elif len(classData) > 1:
        for cField in classData:
            if "delverclassname" in cField.lower():
                rawDescriptor = cField
                jRawData["description"] = rawDescriptor.split("-")[1].strip()
            else:
                jRawData["options"].append(cField)
                

    if "(" in rawDescriptor.split("-")[0]:
        caveatData = rawDescriptor.split("-")[0].split("(")[1].replace(")","").split("|")
        for caveatField in caveatData:
            jRawData["caveats"].append(caveatField.strip())

    
    jDict[ClassNameProp.lower()].append(jRawData)
    
        

ClassNameProp = ""
ClassFeatLvlProp = ""
FeatNameProp = ""
classData = []

classNames = []
for textLinePre in dataByLine:
    if "delverclassname." in textLinePre.lower():
        splitTextPre = textLinePre.split(".")
        metaFieldSplit = splitTextPre[1].split("_")
        classNames.append(metaFieldSplit[2].split("-")[0].strip().split("(")[0].replace(" ","_").replace("'",""))

        
print("[!] Detected {} class features for parsing:".format(len(classNames)))
for eName in classNames:
    print("[.]  Discovered class feature '{}'".format(eName))

primaryConfirmLoop()
    
for textLine in dataByLine:
    if "delverclassname." in textLine.lower():
        splitText = textLine.split(".")
        metaFieldSplit = splitText[1].split("_")
        #check if there are additional lines to the feature below it

        #because these appear inline instead of one line before
        if len(classData) > 0:
            mkJsonClassFacsimile(ClassNameProp,classData,ClassFeatLvlProp,FeatNameProp)
            classData = []
        classData.append(textLine)
        ClassNameProp = metaFieldSplit[0]
        ClassFeatLvlProp = metaFieldSplit[1]
        FeatNameProp = metaFieldSplit[2].split("-")[0].strip().split("(")[0].replace(" ","_").replace("'","")  
        if "delverclassname" in dataByLine[dataByLine.index(textLine)+1].lower():            
            mkJsonClassFacsimile(ClassNameProp,classData,ClassFeatLvlProp,FeatNameProp)
            classData = []
            
        #check if this was performed in the mkJsonClassFacsimile step

        print("[+] Attempting to parse {}...".format(FeatNameProp))
    elif textLine == "DelverClassEnd":
        mkJsonClassFacsimile(ClassNameProp,classData,ClassFeatLvlProp,FeatNameProp)
        break
    else:
        classData.append(textLine)
writeToJson()

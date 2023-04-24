import os
import json

jsonData = {"tables":{},"classes":{},"spells":{},"skills":{}}

# select class
# select race
# select occupation
# generate bonuses
# generate attributes and assign bonuses
# select gear
# generate stats
# assign skill proficiencies
# assign bonuses
# select features

charSheetObj = {}
#stores protodata about selections, if needed
charSheetConfigObj = {}

for jsonDataset in list(jsonData.keys()):
    with open("..\\data\\{}\\data.json".format(jsonDataset)) as json_file:
        jsonData[jsonDataset] = json.load(json_file)

def normalizeDataToLower(dataNorms):
    if type(dataNorms) != list:
        print("[!] incorrect data format!")
        exit()
    newData = []
    for idx in dataNorms:
        newData.append(idx)
    return newData
    
        

def inputLoop(prompt,objIndex,validInputs):

    while True:
        confirmByInputB = input(prompt)
        if confirmByInputB.lower() in normalizeDataToLower(validInputs):
            charSheetConfigObj[objIndex] = confirmByInputB
            return confirmByInputB
        elif confirmByInputB.lower() in ["help","list"]:
            for datum in validInputs:
                print(" >>> {}".format(datum))
        else:
            print("[!] Invalid input, please try again...")
        
def mkFmtSkills():
    parsedSkills = []
    for skillDatum in jsonData["skills"]:
        parsedSkills.append("{}({}".format(skillDatum["name"],skillDatum["base_attr"]))
    return parsedSkills
        
def getCharClass():
    charClassSelection = inputLoop("[+] Please select your class: ","class",list(jsonData["classes"].keys()))
    print("[+] Selected {}...".format(charClassSelection))

def getCharRace():
    raceFeats = {}
    validRaces = []
    for raceObj in jsonData["tables"]["race_detail"]:
        validRaces.append(raceObj["Race"])
        raceFeats[raceObj["Race"]] = raceObj["Feature"]
    charRaceSelection = inputLoop("[+] Please select your race: ","race",validRaces)
    
    charSheetConfigObj["race_feat"] = "NULL"
    featSelect = raceFeats[charRaceSelection].lower()
    if "proficiency" in featSelect:
        inputLoop("[+] Please select {}: ".format(featSelect),"race_feat",mkFmtSkills())
        if "half" in featSelect:
            charSheetConfigObj["race_feet_halfprof"] = 1
        else:
            charSheetConfigObj["race_feet_halfprof"] = 0
    print("[+] Selected {}...".format(charRaceSelection))
    
def getCharOccupation():


def getCharBonuses():


def getCharAttr():


def getCharGear():


def getCharStats():


def getCharProficiencies():


def populateCharBonuses():


def getCharFeatures():


def populateCharSheetObj():



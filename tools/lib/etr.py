import json
import lib.data

etrlib = None

"""
    Description                      	 Modifier
	----------------------------------------------------------------------
	10 points of health                  +1
	10 points of mana                    +1
	1 point of armor                     +1
	1 resistance                         +1
	1 point of potential damage          +1
	1 feature                            +1
	1 Eldritch word                      +1
	1 proficiency (half or full)         +1
	1 condition (feature)                +2
	1 decreased action pt cost (feature) +2
	1 additional action pt               +5
	1 additional action pt (feature)     +5
	1 increased crit range (feature)     +5
	1 additional health die (feature)    +5
	1 additional damage die (feature)    +5
	1 immunity                           +5
	1 vulnerability                      -5
"""

class etrLib():
    def __init__(self):
        self.etrTarget = None
        self.etrTablePrimary = lib.data.findDataStructure("tables","etr_calculation")
        self.etrTableSimple = lib.data.findDataStructure("tables","etr_calculation_simplified")

    def findCalcMatch(self,tableToUse,query):
        for i in tableToUse:
            if query in i["Description"]:
                return int(i["Modifier"].replace("+",""))
        return 0

    def calcHealth(self,tableToUse):
        modifier = self.findCalcMatch(tableToUse,"points of health")

        healthPts = int(int(self.etrTarget["stats"]["health"])/10)
        return healthPts*modifier
        
    
    def calcMana(self,tableToUse):
        modifier = self.findCalcMatch(tableToUse,"points of mana")

        manaPts = int(int(self.etrTarget["stats"]["mana"])/10)
        return manaPts*modifier

    def calcArmor(self,tableToUse):
        modifier = self.findCalcMatch(tableToUse,"point of armor")
 
        armorPts = int(self.etrTarget["stats"]["armor"])
        return armorPts*modifier
 
    def calcResistance(self,tableToUse):
        modifier = self.findCalcMatch(tableToUse,"resistance")

        resistancePts = len(self.etrTarget["adjustments"]["resistances"])
        return resistancePts*modifier

    def calcDamage(self,tableToUse):
        modifier = self.findCalcMatch(tableToUse,"potential damage")

        damagePts = 0

        damageOpts = self.etrTarget["actions"]
        for actionOpt in damageOpts:
            for field in damageOpts[actionOpt]:
                if "d" in field:
                    dice = field.split(" ")[0].split("d")
                    if dice[0] == '':
                        dice[0] = 1
                    diceNum = int(dice[0])
                    damagePrimary = dice[1].split("+")
                    if len(damagePrimary) > 1:
                        if damagePrimary[1] == '':
                            damagePrimary[1] = '0'
                    diceSize = int(damagePrimary[0])
                    damagePts+=((diceNum*diceSize)+int(damagePrimary[1]))
        return damagePts*modifier
            
    def calcFeatures(self,tableToUse):
        modifier = self.findCalcMatch(tableToUse,"1 feature")

        featurePts = int(len(self.etrTarget["features"].keys()))
        return featurePts*modifier
            
    def calcEldritchWords(self,tableToUse):
        modifier = self.findCalcMatch(tableToUse,"Eldritch")

        spellTable = lib.data.mkDataImport()["spellcraft"]
        featureSet = self.etrTarget["features"]
        eldritchWords = []
        
        wordCount = 0
        
        for wordCategory in spellTable.keys():
            for wordSet in spellTable[wordCategory]:
                if "Verb" not in wordSet.keys():
                    if "Eldritch Pronoun" in wordSet.keys() or "Cost" in wordSet.keys():
                        continue
                    else:
                        eldritchWords.append(wordSet["Eldritch Modifier"])
                else:
                    eldritchWords.append(wordSet["Verb"])
        
        for eWord in eldritchWords:
            for feature in featureSet:
                if eWord in featureSet[feature]:
                    wordCount +=1
        
        return wordCount*modifier
                    
            
    def calcProficiencies(self,tableToUse):
        modifier = self.findCalcMatch(tableToUse,"proficiency")

        proficiencyPts = len(self.etrTarget["proficiencies"].keys())
        return proficiencyPts*modifier
            
    def calcConditions(self,tableToUse):
        modifier = self.findCalcMatch(tableToUse,"condition")

        conditionPts = 0
        conditions = ["charmed","bleeding","prone","restrained","grappled","blind","incapacitated","surprised","poisoned","diseased"]

        featureKeys = self.etrTarget["features"].keys()

        for con in conditions:
            for keyItem in featureKeys:
                if con in self.etrTarget["features"][keyItem]:
                    conditionPts+=1
        return conditionPts*modifier
            
    def calcAPDecrease(self,tableToUse):
        modifier = self.findCalcMatch(tableToUse,"decreased action")

        apPts = 0
        featureKeys = self.etrTarget["features"].keys()

        for keyItem in featureKeys:
            if "1 action point" in self.etrTarget["features"][keyItem]:
                apPts += 1
        return apPts*modifier
            
    def calcAPSurplus(self,tableToUse):
        modifier = self.findCalcMatch(tableToUse,"additional action point")

        apPts = 0
        apData = self.etrTarget["stats"]["action"]
        if int(apData) > 3:
            apPts = apData-3
        return apPts*modifier
            
    def calcAPIncrease(self,tableToUse):
        modifier = self.findCalcMatch(tableToUse,"action point (")

        apPts = 0
        featureKeys = self.etrTarget["features"].keys()

        for keyItem in featureKeys:
            if "increase" in self.etrTarget["features"][keyItem] and "action point pool" in self.etrTarget["features"][keyItem]:
                apPts += 1
        return apPts*modifier
        
    def calcCrit(self,tableToUse):
        modifier = self.findCalcMatch(tableToUse,"increased crit")
        
        critPts = 0
        featureKeys = self.etrTarget["features"].keys()

        for keyItem in featureKeys:
            if "crit" in self.etrTarget["features"][keyItem] and "1-10" in self.etrTarget["features"][keyItem]:
                critPts+=1
        return critPts*modifier
            
    def calcHealingBuff(self,tableToUse):
        modifier = self.findCalcMatch(tableToUse,"additional health")

        healthPts = 0
        featureKeys = self.etrTarget["features"].keys()
        for keyItem in featureKeys:
            if "regain health" in self.etrTarget["features"][keyItem]:
                healthPts +=1
        return healthPts*modifier
                            
    def calcDamageBuff(self,tableToUse):
        modifier = self.findCalcMatch(tableToUse,"additional damage")

        damagePts = 0
        featureKeys = self.etrTarget["features"].keys()
        for keyItem in featureKeys:
            if "immediately make" in self.etrTarget["features"][keyItem] or "additional damage" in self.etrTarget["features"][keyItem] or "damage at" in self.etrTarget["features"][keyItem]:        
                damagePts+=1
        return damagePts*modifier
            
    def calcImmunity(self,tableToUse):
        modifier = self.findCalcMatch(tableToUse,"immunity")

        immunityPts = len(self.etrTarget["adjustments"]["immunities"])
        return immunityPts*modifier
            
    def calcVulnerability(self,tableToUse):
        modifier = self.findCalcMatch(tableToUse,"vulnerability")

        vulnerabilityPts = len(self.etrTarget["adjustments"]["vulnerabilities"])
        return vulnerabilityPts
            
def calcSimple():
    etrS = 0
    for libFunc in dir(etrlib):
        if 'calc' in libFunc:
            etrS += getattr(etrlib,libFunc)(etrlib.etrTableSimple)
    return etrS

def calcPrimary():
    etrP = 0
    for libFunc in dir(etrlib):
        if 'calc' in libFunc:
            etrP += getattr(etrlib,libFunc)(etrlib.etrTablePrimary)
    return etrP

def etrCalc(entity):
    global etrlib
    etrlib = etrLib()
    
    etrlib.etrTarget = entity
    resSet = {}
    resSet = {"primary":calcPrimary(),"simple":calcSimple()}
    return resSet
    

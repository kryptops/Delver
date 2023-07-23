import lib.data
import lib.etr
import sqlite3

class combatCore():
    def __init__(self):
        self.allData = lib.data.mkDataImport()

class threat():
    def __init__(self):
        self.core = combatCore()
        self.bulkCalculationAll = ["all","*"]
        self.bulkCalculationByType = ["none","null",""]
        self.entities = self.core.allData["bestiary"]
        self.etrData = []
        
    def getEtr(self,entityType,entityName):
        if entityName in self.bulkCalculationAll:
            if entityType in self.bulkCalculationByType:
                for entityCategory in self.entities:
                    for entity in self.entities[entityCategory]:
                        self.etrData.append({entity:lib.etr.etrCalc(self.entities[entityCategory][entity])})
            else:
                for entity in self.entities[entityType]:
                    self.etrData.append({entity:lib.etr.etrCalc(self.entities[entityType][entity])})
        else:
            self.etrData.append({entityName:lib.etr.etrCalc(self.entities[entityType][entityName])})
                    
        return self.etrData
        
class data():
    def __init__(self):
        pass 
             
class activity():
    def __init__(self):
        self.combatOrder = {}
        self.party = {}
        self.entities = {}
    
    def start(self):
        pass
    
    def end(self):
        pass
    
    def get(self):
        pass
    
    def put(self):
        pass
    
    def create(self):
        pass
    
    def configure(self):
        pass
    
    def damage(self):
        pass
        
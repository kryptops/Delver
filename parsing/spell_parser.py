import json
from datetime import datetime

###
# There are multiple elements used in standard delver documentation that need to be parsed into json objects. This script parses standard tables into json.
# Put any tables you want to parse into .\\input\\table.txt, separated by a line matching the format DelverTableName.<name of table, underline separated>
# Run the script. 
###

jDict = {}
fileData = open(".\\input\\spells.txt",'r').read()
dataByLine = fileData.splitlines()
printRowData = False

def rowDataConfirmLoop():
    global printRowData
    while True:
        confirmByInputA = input("[+] Ready to Parse! Do you want to print row data as parsing occurs (column headers only otherwise)? (Y/N): ")
        if confirmByInputA.lower() in ["y","ye","yes"]:
            printRowData = True
            print("[+] Parsing with row data...")
            break
        elif confirmByInputA.lower() in ["n","no"]:
            print("[+] Parsing without row data...")
            break
        else:
            print("[!] Invalid input, please specify Y/N)...")
            break
            
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
    rowDataConfirmLoop()

def finalConfirmLoop():
    while True:
        confirmByInput = input("[!] Please review data results above, confirm if it appears correct (Y/N): ")
        if confirmByInput.lower() in ["y","ye","yes"]:
            print("[+] Parsing complete! Writing data to output directory...")
            writeToJson()
            break
        elif confirmByInput.lower() in ["n","no"]:
            print("[+] Parsing failed! Writing data to error directory...")
            writeToErrLog()
            break
        else:
            print("[!] Invalid input, please specify Y/N)...")
            
def writeToErrLog():
    dataFile = ".\\error\\raw_error_data_{}.log".format(datetime.now().strftime("%Y%m%d"))
    errorFileH = open(dataFile,'w')
    errorFileH.write(str(jDict))
    errorFileH.close()
    print("[+] Wrote raw table data to {}. Exiting...".format(dataFile))          

def writeToJson():
    dataFile = ".\\output\\table_data_{}.json".format(datetime.now().strftime("%Y%m%d"))
    with open(dataFile,'w') as jsonDataFileHandle:
        json.dump(jDict, jsonDataFileHandle, indent=4, sort_keys=True)
    print("[+] Wrote jsonified table data to {}! Enjoy!".format(dataFile))

def mkJsonTableFacsimile(tableNameProp,tableData):
    
    jDict[tableNameProp] = []
    tableHeader = tableData[0].split("  ")

    tableHeaderParsedFields = []

    #parse the column heads
    for headerCandidateField in tableHeader:
        if headerCandidateField != '':
            print("[.]  Detected column header: '{}'...".format(headerCandidateField.strip()))
            tableHeaderParsedFields.append(headerCandidateField.strip())
           

    tableLineParsedFields = []

    #parse each row
    for tableLine in tableData[2:]:
    
        if printRowData == True:
            print("[.]  Detected row data: '{}'...".format(tableLine.strip()))
        tableCandidateFields = tableLine.split("  ")
        tableFields = []
        tDict = {}

        for lineCandidateField in tableCandidateFields:
            if lineCandidateField != '':
                tableFields.append(lineCandidateField)
        
        for lCFIndex in range(len(tableHeaderParsedFields)):
            try:

                tDict[tableHeaderParsedFields[lCFIndex]] = tableFields[lCFIndex].replace("\t","").strip()
            except:
                print("[!] ERROR! Unparsable line!")
                print("Error Detail...")
                print("    Error occurred on line {}: [{}]".format(tableData.index(tableLine),tableFields))
                exit
        jDict[tableNameProp].append(tDict)


tableNameProp = ""
tableData = []

print("[+] Opening table.txt for parsing...")

tableNames = []
for textLinePre in dataByLine:
    if "DelverTableName" in textLinePre:
        tableNames.append(textLinePre.split(".")[1])
        
print("[!] Detected {} tables for parsing:".format(len(tableNames)))

for tName in tableNames:
    print("[.]  Discovered table '{}'".format(tName))
    
primaryConfirmLoop()
    
for textLine in dataByLine:
    if "DelverTableName." in textLine:
        
        if len(tableData) > 0:
            mkJsonTableFacsimile(tableNameProp,tableData)
            tableData = []
        tableNameProp = textLine.split(".")[1]
        print("[+] Attempting to parse {}...".format(tableNameProp))
    elif textLine == "DelverTableEnd":
        mkJsonTableFacsimile(tableNameProp,tableData)
        break
    else:
        tableData.append(textLine)

finalConfirmLoop()

#print(jDict)			
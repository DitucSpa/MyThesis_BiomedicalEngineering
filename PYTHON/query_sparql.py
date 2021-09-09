from sepy.SAPObject import *
from sepy import *
import json
from sepy.SEPA import *
import os

global stringa
stringa = "DTCGLC99"
mySAP = open(r"C:\Users\gianl\Documents\GitHub\MyThesis_BiomedicalEngineering\JSAP\TesiProva.jsap","r")
sap = SAPObject(json.load(mySAP))
sc = SEPA(sapObject=sap)

def inserisci_fiscale():
    result = sc.update(
        "INSERT_FISCAL_CODE",
        forcedBindings={"fiscalCode": stringa})

def inserisci_nome():
    nome = "Gianluca"
    result = sc.update(
        "INSERT_PATIENT_NAME",
        forcedBindings={"fiscalCode":stringa, "givenName": nome})

#inserisci_fiscale()
#inserisci_nome()
result = sc.query("QUERY_FISCAL_CODE")
str1 = json.dumps(result)
str1 = str1.replace(" ","").replace('"value":"',"&&&").replace("{","").replace("}","").replace(",","\n")
#index = str1.find("&&&")
#print(index)
text_file = open("Output.txt","w")
text_file.write(str1)
text_file.close()
with open("Output.txt","r") as fin:
    with open("input.txt","w") as fout:
        for line in fin:
            if line.startswith('&&&'):
                fout.write(line)
            else:
                fout.write("")
with open("input.txt","r") as file:
    data = file.read().replace("&&&","").replace("[","").replace("]","").replace('"',"")
os.remove("input.txt")
os.remove("output.txt ")
print(data)

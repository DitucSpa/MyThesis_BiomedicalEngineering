from sepy.SAPObject import *
from sepy import *
import json
from sepy.SEPA import *

global stringa
stringa = "DTCGLC99"
mySAP = open("TesiProva.jsap","r")
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

inserisci_fiscale()
inserisci_nome()
result = sc.query("QUERY")
print(result)

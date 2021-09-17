import icd9_package
#https://github.com/fabiocaccamo/python-codicefiscale
from codicefiscale import codicefiscale

string = "statistiche text cercami icd9 003.1".lower().replace(".","")
string = string.split(" ")
print(string)


def check_cartella(text):
    for y in text:
        if y == "comune":
            for z in text:
                if z.isnumeric():
                    print("Cartella comune: " + z)
                    return
            print("Mi dispiace, non trovo la cartella comune con quell'ID")
            return
        elif y == "specifica":
            for z in text:
                if z.isnumeric():
                    print("Cartella specifica: " + z)
                    return
            print("Mi dispiace, non trovo la cartella specifica con quell'ID")
            return
    print("Mi dispiace, ma devi specificare se devo cercare una cartella comune o specifica")
    return


def check_icd9(text):
    if "statistiche" in text:
        for y in text:
            if y.isnumeric():
                if icd9_package.search_diagn(y) != None:
                    print("statistiche: " + y)
                    return
        return
    else:
        for y in text:
            if y.isnumeric():
                if icd9_package.search_diagn(y) != None:
                    print(icd9_package.return_diagn(y))
                    return
        print("Mi dispiace, ma il codice icd9-cm che mi hai detto non è valido")
        return
    print("Mi dispiace, ma non ho capito")
    return


def check_fiscalCode(text):
    pass



check_icd9(string)
print(codicefiscale.encode(surname='Caccamo', name='Fabio', sex='M', birthdate='03/04/1985', birthplace='Torino'))

# 'CCCFBA85D03L219P'

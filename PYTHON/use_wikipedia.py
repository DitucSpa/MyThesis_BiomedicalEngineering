# USE_WIKIPEDIA.PY
# Questo modulo permette l'utilizzo di wikipedia attraverso il linguaggio python


import wikipedia
import webbrowser
import os
import requests

# questo metodo è utilizzato per restituire un riassunto della pagina cercata
# e per aprirla tramite browser (in questo caso è impostato firefox come browser di default)
# riceve la parola da cercare (previa verifica dell'esistenza di quest'ultima tramite il medoto "exist")
def search(text):
    wikipedia.set_lang("it")
    webbrowser.open("https://it.wikipedia.org/wiki/"+text)
    return wikipedia.summary(text)


# permette di chiudere il browser; si potrebbe implementare una variabile per indicare il browser di default
def kill():
    os.system("taskkill /im firefox.exe /f")


# questo metodo serve per verificare se la pagine esiste 
def exist(text):
    response = requests.get("https://it.wikipedia.org/wiki/"+text)
    if response.status_code == 200:
        return True
    else:
        return False

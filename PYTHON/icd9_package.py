# ICD9_PACKAGE.PY
# questo pacchetto permette l'uso del codice icd9-cm


# https://pypi.org/project/icd9cms/
# https://pythonhosted.org/PyMedTermino/tuto_en.html
from icd9cms.icd9 import search


# restituisce la diagnosi relativa a quel codice (passato come stringa)
def search_diagn(text):
    return search(text)

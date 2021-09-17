# https://pypi.org/project/icd9cms/
#https://pythonhosted.org/PyMedTermino/tuto_en.html
from icd9cms.icd9 import search

def search_diagn(text):
    if search(text) != None:
        return search(text)
    else:
        return None

def return_diagn(text):
    return search(text)

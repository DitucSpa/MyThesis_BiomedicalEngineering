# https://pypi.org/project/icd9cms/
#https://pythonhosted.org/PyMedTermino/tuto_en.html
from icd9cms.icd9 import search

def search_diagn(text):
    return search(text)

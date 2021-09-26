# USE_WIKIPEDIA.PY
# This module is used for check if a wiki page exists or to return page and close it then


import wikipedia
import webbrowser
import os
# from googlesearch import search
import requests


def search(text):
    wikipedia.set_lang("it")
    webbrowser.open("https://it.wikipedia.org/wiki/"+text)
    return wikipedia.summary(text)

def kill():
    os.system("taskkill /im firefox.exe /f")

def exist(text):
    response = requests.get("https://it.wikipedia.org/wiki/"+text)
    if response.status_code == 200:
        return True
    else:
        return False

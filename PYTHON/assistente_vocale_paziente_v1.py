# Software helps patients to find email, phone number, time schedule of doctors
# https://www.codesofinterest.com/2017/04/energy-threshold-calibration-in-speech-recognition.html
# Remeber to active SEPA and to se the value of microphone (noise level)

# packages for tkinter
from tkinter import *

# packages for writing files
import os
import sys

# packages used for speech recognition
import playsound
import time
from gtts import gTTS
import speech_recognition

# package for usign Microphone
import use_microphone

# package for using SEPA
import query_sparql

# for creating a new document with sparql_query
import create_sparql


import use_wikipedia
from time import sleep


path = r"C:\Users\Ovettino\Downloads\GitHub\MyThesis_BiomedicalEngineering\JSAP\TesiProva.jsap" # path of JSAP file
path_new = r"C:\Users\Ovettino\Downloads\GitHub\MyThesis_BiomedicalEngineering\JSAP"
f = ('Times', 14) # font
ws = Tk()
ws.title('Tesi Di Tuccio -- Assistente Vocale Paziente')
ws.geometry('600x300')


nome_assistente = "mario"
nome_chiusura = "chiudi"
valore_microfono = 500


key_word = ['orari', 'orario', 'stanza', 'camera', 'studio', "numero di cellulare", "recapito telefonico", "telefono", "email", "reparto",
    'dove', "dov'è", 'giorni', 'oggi', 'domani', 'cerco', 'sto cercando', 'mail']


duck_sleep = r"""
           ,~~.
 ,       (  -     )>
 )`~~'       (
(    .__)        )
 `-.________,'
"""
duck_talk = r"""
           ,~~.
 ,       (  °     )<
 )`~~'       (
(    .__)        )
 `-.________,'
"""

# activate duck
def talking_duck():
    duck_label.configure(text=duck_talk)
    vocal_label.configure(text="Ti ascolto...")
    ws.update()

# disactivate duck
def sleeping_duck():
    duck_label.configure(text=duck_sleep)
    vocal_label.configure(text="")
    ws.update()


# il metodo riceve la frase che deve essere letta ad alta voce dall'assistente
def audio_bot(cosa_dire):
    tts = gTTS(text=cosa_dire, lang='it') # si potrebbe implementare una variabile language che può assumere "it", "en", ...
    nome_file_mp3 = "prova.mp3" # crea un file mp3 con la frase da dire, lo riproduce e poi lo cancella immediatamente
    tts.save(nome_file_mp3)
    playsound.playsound(nome_file_mp3)
    os.remove(nome_file_mp3)


# for calling voice assistant
def start():
    text = use_microphone.understand(valore_microfono, None, 1.5, "it-IT", 0.5)
    if text == "Errore":
        return
    else:
        if text.lower() == nome_assistente:
            talking_duck()
            response()
        elif text.lower() == nome_chiusura:
            vocal_label.configure(text="Chiusura in corso...")
            ws.update()
            audio_bot("chiusura in corso")
            sys.exit()


def wiki(text):
    vocal_label.configure(text="Cosa vuoi cercare?")
    ws.update()
    audio_bot("Cosa vuoi cercare?")
    new_text = use_microphone.understand(valore_microfono, None,2, "it-IT", 3)
    if use_wikipedia.exist(new_text) and new_text != "Error":
        result = use_wikipedia.search(new_text)
        audio_bot(result)
        use_wikipedia.kill()
    else:
        vocal_label.configure(text="Mi dispiace, non trovo la pagina")
        ws.update()
        audio_bot("Mi dispiace, non trovo la pagina")




# if you ask something
def response():
    audio_bot("Ti ascolto")
    text = use_microphone.understand(valore_microfono, None, None, "it-IT", 2.5)
    if text == "Error":
        return
    user_label.configure(text=text)
    ws.update()
    if text.lower() == "cosa sai fare":
        vocal_label.configure(text="Allora, posso aiutarti con:\norario di un Medico;\nstudio di un Medico;\nreparto di un Medico;\nrecapito di un Medico;\nin alternativa contatta il XXXXXX")
        ws.update()
        audio_bot("Allora, posso aiutarti con,orario di un Medico,studio di un Medico;\nreparto di un Medico,recapito di un Medico;\nin alternativa contatta il XXXXXX")
    elif "wikipedia" in text.lower():
        wiki(text.lower())
    else:
        risposta(text.lower())



def speak_label(received_text):
    vocal_label.configure(text=received_text)
    ws.update()
    audio_bot(received_text)



def setting():
    user_label.configure(text="")
    ws.update()
    start()
    sleeping_duck()
    setting()


def who(name, surname, answer):
    if key_word[0] in answer or key_word[1] in answer or key_word[12] in answer or key_word[13] in answer or key_word[14] in answer:
        orario(name, surname)
    if key_word[2] in answer or key_word[3] in answer or key_word[4] in answer or key_word[10] in answer or key_word[11] in answer or key_word[15] in answer or key_word[16] in answer:
        studio(name, surname)
    if key_word[5] in answer or key_word[6] in answer or key_word[7] in answer:
        telefono(name, surname)
    if key_word[8] in answer or key_word[17] in answer:
        email(name,surname)
    if key_word[9] in answer:
        reparto(name,surname)



def orario(name, surname):
    stringa = '"SELECT ?orario WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/Medical_Staff> {?h rdf:type sha:Medical_Staff ; sha:timeSchedule ?orario ; sha:givenName ?givenName ; sha:familyName ?familyName . '
    stringa = stringa + "FILTER (regex (?givenName, '" + name + "')) . FILTER (regex (?familyName, '" + surname + "')) }}" + '"'
    name_query = '"QUERY"'
    stringa = name_query + ': { "sparql": ' + stringa + '}'
    stringa = create_sparql.creating(path_new, stringa)
    stringa = stringa.replace("%%", "ì").replace("&&"," ").replace("&"," ")
    vocal_label.configure(text="Gli orari sono:  " + stringa)
    ws.update()
    audio_bot("Gli orari sono:  " + stringa)

def telefono(name, surname):
    stringa = '"SELECT ?telefono WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/Medical_Staff> {?h rdf:type sha:Medical_Staff ; sha:phoneNumberWork ?telefono ; sha:givenName ?givenName ; sha:familyName ?familyName . '
    stringa = stringa + "FILTER (regex (?givenName, '" + name + "')) . FILTER (regex (?familyName, '" + surname + "')) }}" + '"'
    name_query = '"QUERY"'
    stringa = name_query + ': { "sparql": ' + stringa + '}'
    stringa = create_sparql.creating(path_new, stringa)
    stringa = stringa.replace("%%", "ì").replace("&&"," ").replace("&"," ")
    vocal_label.configure(text="Il recapito telefonico è:  " + stringa)
    ws.update()
    audio_bot("Il recapito telefonico è:  " + stringa)

def studio(name, surname):
    stringa = '"SELECT ?studio WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/Medical_Staff> {?h rdf:type sha:Medical_Staff ; sha:studio ?studio ; sha:givenName ?givenName ; sha:familyName ?familyName . '
    stringa = stringa + "FILTER (regex (?givenName, '" + name + "')) . FILTER (regex (?familyName, '" + surname + "')) }}" + '"'
    name_query = '"QUERY"'
    stringa = name_query + ': { "sparql": ' + stringa + '}'
    stringa = create_sparql.creating(path_new, stringa)
    stringa = stringa.replace("%%", "ì").replace("&&"," ").replace("&"," ")
    vocal_label.configure(text="Lo trovi nello studio numero:  " + stringa)
    ws.update()
    audio_bot("Lo trovi nello studio numero:  " + stringa)
    reparto(name, surname)

def email(name, surname):
    stringa = '"SELECT ?email WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/Medical_Staff> {?h rdf:type sha:Medical_Staff ; sha:emailWork ?email ; sha:givenName ?givenName ; sha:familyName ?familyName . '
    stringa = stringa + "FILTER (regex (?givenName, '" + name + "')) . FILTER (regex (?familyName, '" + surname + "')) }}" + '"'
    name_query = '"QUERY"'
    stringa = name_query + ': { "sparql": ' + stringa + '}'
    stringa = create_sparql.creating(path_new, stringa)
    stringa = stringa.replace("%%", "ì").replace("&&"," ").replace("&"," ")
    vocal_label.configure(text="La mail è:  " + stringa)
    ws.update()
    audio_bot("La mail è:  " + stringa)

def reparto(name, surname):
    stringa = '"SELECT ?reparto WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/Medical_Staff> {?h rdf:type sha:Medical_Staff ; sha:wardName ?reparto ; sha:givenName ?givenName ; sha:familyName ?familyName . '
    stringa = stringa + "FILTER (regex (?givenName, '" + name + "')) . FILTER (regex (?familyName, '" + surname + "')) }}" + '"'
    name_query = '"QUERY"'
    stringa = name_query + ': { "sparql": ' + stringa + '}'
    stringa = create_sparql.creating(path_new, stringa)
    stringa = stringa.replace("%%", "ì").replace("&&"," ").replace("&"," ").replace("_"," ")
    vocal_label.configure(text="Il reparto è:  " + stringa)
    ws.update()
    audio_bot("Il reparto è:  " + stringa)


def check_answer(answer):
    last = answer
    check_name = query_sparql.connessione("QUERY_MEDICAL_STAFF_NAME", path).replace("_", " ")
    check_surname = query_sparql.connessione("QUERY_MEDICAL_STAFF_SURNAME", path).replace("_", " ")
    check_name = check_name.upper().split("\n")
    check_surname = check_surname.upper().split("\n")

    for x in check_name:
        if x in answer:
            stringa = '"SELECT ?familyName WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/Medical_Staff> {?h rdf:type sha:Medical_Staff ; sha:givenName ?givenName ; sha:familyName ?familyName . '
            stringa = stringa + "FILTER (regex (?givenName, '" + x + "')) }}" + '"'
            name_query = '"QUERY"'
            stringa = name_query + ': { "sparql": ' + stringa + '}'
            stringa = create_sparql.creating(path_new, stringa)
            stringa = list(stringa.replace("%%", "ì").replace("&&"," ").replace("&"," ").replace("_"," ").split("\n"))
            for y in stringa:
                if y in answer:
                    who(x.replace(" ","_"),y.replace(" ", "_"),last.lower())
                    return

    for x in check_surname:
        if x in answer:
            stringa = '"SELECT ?givenName WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/Medical_Staff> {?h rdf:type sha:Medical_Staff ; sha:givenName ?givenName ; sha:familyName ?familyName . '
            stringa = stringa + "FILTER (regex (?familyName, '" + x + "')) }}" + '"'
            name_query = '"QUERY"'
            stringa = name_query + ': { "sparql": ' + stringa + '}'
            stringa = create_sparql.creating(path_new, stringa)
            stringa = list(stringa.replace("%%", "ì").replace("&&"," ").replace("&"," ").replace("_"," ").split("\n"))
            for y in stringa:
                if y in answer:
                    who(x.replace(" ","_"),y.replace(" ", "_"),last)
                    return

    vocal_label.configure(text="Mi dispiace, non conosco questo medico o primario.")
    ws.update()
    audio_bot("Mi dispiace, non conosco questo medico o primario")


def risposta(input_user):
    for x in key_word:
        if x in input_user:
            check_answer(input_user.upper())
            break
    else:
        vocal_label.configure(text = "Mi dispiace, non posso aiutarti. \nPer sapere cosa posso fare per te, prova a chiedermi:\n''cosa sai fare?''")
        ws.update()
        audio_bot("mi dispiace, non posso aiutarti. Per sapere cosa posso fare per te, prova a chiedermi, cosa sai fare?")



duck_label = Label(ws, justify=LEFT, text=duck_sleep)
duck_label.place(relx = 0.1, rely = 0.1, anchor = 'nw')
vocal_label = Label(ws, justify=LEFT, text="", font = f)
vocal_label.place(relx = 0.6, rely = 0.3, anchor = 'center')
user_label = Label(ws, text="", font = f)
user_label.place(relx = 0.5, rely = 0.7, anchor = 'center')
ws.resizable(False, False)
ws.after(1000, setting)
ws.mainloop()

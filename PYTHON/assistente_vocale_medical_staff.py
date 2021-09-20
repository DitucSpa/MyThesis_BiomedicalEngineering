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


import icd9_package
#https://github.com/fabiocaccamo/python-codicefiscale
from codicefiscale import codicefiscale

from time import sleep


path = r"C:\Users\Ovettino\Downloads\GitHub\MyThesis_BiomedicalEngineering\JSAP\TesiProva.jsap" # path of JSAP file
path_new = r"C:\Users\Ovettino\Downloads\GitHub\MyThesis_BiomedicalEngineering\JSAP"
f = ('Times', 14) # font
ws = Tk()
ws.title('Tesi Di Tuccio -- Assistente Vocale Medico')
ws.geometry('1200x500')
CF = "DTCGLC99C29C573A"
background_frame = "#80b3ff" # background of the frame
background_window = "#b3ccff" # background of the window










nome_assistente = "mario"
nome_chiusura = "chiudi"
valore_microfono = 1000


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


def response():
    audio_bot("Ti ascolto")
    text = use_microphone.understand(valore_microfono-100, None, None, "it-IT", 2.5)
    if text == "Error":
        return
    user_label.configure(text = text)
    ws.update()
    check(text.lower())


def check(text):
    for x in text.split(" "):
        if x == "paziente":
            check_paziente()
            return
        if x == "mia" or x == "mie":
            check_dottore(text)
            return
        if x == "statistiche":
            check_statistiche(text)
            return
        if x == "ICD9":
            check_icd9(text)
            return


def check_paziente():
    frame = Frame(ws, bd = 2, relief = SOLID, padx = 5, pady = 5)
    frame.config(bg = background_frame)
    frame.place(x=700, y=50)
    Label(frame, text="Codice Fiscale", font=f, bg=background_frame).grid(row=0, column=0, sticky=W, pady=10)
    input_cod_fis = Entry(frame, font=f)
    input_cod_fis.grid(row=0, column=1, pady=10, padx=20)
    input_cod_fis.configure(state="disabled")
    input_cod_fis.configure(state="normal")
    var = IntVar()
    btn_invia = Button(ws, width = 15, text = 'Invia', command=lambda: var.set(1), font=f, bg=background_window,
        activebackground="#3399ff")
    btn_invia.place(height=60, width=360, x = 700, y = 150)
    vocal_label.configure(text="Inserisci il codice fiscale qui accanto")
    ws.update()
    audio_bot("Inserisci il codice fiscale qui accanto")
    btn_invia.wait_variable(var)
    btn_invia.destroy()
    input_cod_fis.configure(state="disabled")
    stringa = '"SELECT ?familyName ?givenName ?birthDate ?birthPlace WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/Patient> {?p rdf:type schema:Patient ; sha:fiscalCode ?cf ; sha:familyName ?familyName ; sha:givenName ?givenName  ; sha:birthDate ?birthDate ; sha:birthPlace ?birthPlace . '
    stringa = stringa + "FILTER (regex (?cf, '" + input_cod_fis.get().upper() + "')) }}" + '"'
    name_query = '"QUERY"'
    stringa = name_query + ': { "sparql": ' + stringa + '}'
    stringa = create_sparql.creating(path_new, stringa)
    if stringa == "":
        vocal_label.configure(text="Mi dispiace, non ho trovato questo paziente")
        ws.update()
        audio_bot("Mi dispiace, non ho trovato questo paziente")
        return
    stringa = stringa.replace("%%", "ì").replace("&&"," ").replace("&"," ").replace("T00:00:00","").replace("\n",";\n")
    vocal_label.configure(text="Ho trovato i seguenti dati:\n"+stringa)
    ws.update()
    audio_bot("Ho trovato i seguenti dati;\n"+stringa)
    input_cod_fis.delete(0, "end")
    frame2 = Frame(ws, bd = 2, relief = SOLID, padx = 5, pady = 5)
    frame2.config(bg = background_frame)
    frame2.place(x=900, y=210)
    scroll = Scrollbar(frame2)
    scroll.pack(side="right", fill="y")

    listbox = Listbox(frame2, yscrollcommand=scroll.set)
    listbox.pack(side="right", fill="both")

    stringa = '"SELECT * WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/General_Section> {?p rdf:type sha:General_Section ; sha:fiscalCode ?cf . '
    stringa = stringa + "FILTER (regex (?cf, '" + input_cod_fis.get().upper() + "')) }}" + '"'
    name_query = '"QUERY"'
    stringa = name_query + ': { "sparql": ' + stringa + '}'
    stringa = create_sparql.creating(path_new, stringa)
    stringa = stringa.split("\n")

    for i in range(len(stringa)):
        listbox.insert("end", stringa[i])

    var = IntVar()
    btn_invia = Button(ws, width = 15, text = 'Va bene', command=lambda: var.set(1), font=f, bg=background_window,
        activebackground="#3399ff")
    btn_invia.place(height=60, width=360, x = 700, y = 150)
    btn_invia.wait_variable(var)
    btn_invia.destroy()
    listbox.destroy()
    input_cod_fis.destroy()
    scroll.destroy()
    frame.destroy()
    frame2.destroy()




def check_dottore():
    pass


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


def check_statistiche(text):
    pass


#check_icd9(string)
#print(codicefiscale.encode(surname='Caccamo', name='Fabio', sex='M', birthdate='03/04/1985', birthplace='Torino'))


duck_label = Label(ws, justify=LEFT, text=duck_sleep)
duck_label.place(relx = 0.1, rely = 0.1, anchor = 'nw')
vocal_label = Label(ws, justify=LEFT, text="", font = f)
vocal_label.place(relx = 0.4, rely = 0.3, anchor = 'center')
user_label = Label(ws, text="", font = f)
user_label.place(relx = 0.4, rely = 0.6, anchor = 'center')
ws.resizable(False, False)
ws.after(1000, setting)





ws.mainloop()

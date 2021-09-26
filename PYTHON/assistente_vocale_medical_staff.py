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

from time import sleep
import tkinter.font as tkFont
from tkinter import ttk




path = r"C:\Users\Ovettino\Downloads\GitHub\MyThesis_BiomedicalEngineering\JSAP\TesiProva.jsap" # path of JSAP file
path_new = r"C:\Users\Ovettino\Downloads\GitHub\MyThesis_BiomedicalEngineering\JSAP"
f = ('Times', 14) # font
ws = Tk()
ws.title('Tesi Di Tuccio -- Assistente Vocale Medico')
ws.geometry('1460x900')
CF = "DTCGLC99C29C573A"
background_frame = "#80b3ff" # background of the frame
background_window = "#b3ccff" # background of the window


string_to_number = ["zero","uno","due","tre","quattro","cinque","sei","sette","otto","nove"]
string_to_month = ["GENNAIO","FEBBRAIO","MARZO","APRILE","MAGGIO","GIUGNO","LUGLIO","AGOSTO","SETTEMBRE","OTTOBRE","NOVEMBRE","DICEMBRE"]
string_to_year = ["2018","2019","2020","2021"]




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
    #user_label.configure(text = text)
    #ws.update()
    check(text.lower())


def check(text):
    for x in text.split(" "):
        if x == "paziente":
            check_paziente()
            return
    for x in text.split(" "):
        if x == "mia" or x == "mie":
            check_dottore()
            return
        elif x == "statistiche":
            check_statistiche(text)
            return
        elif "icd9" in x:
            check_icd9(text.lower())
            return
        elif x == "reparto":
            check_reparto(text.upper())
            return
    if "cartella" in text.split(" ") or "cartelle" in text.split(" "):
        check_cartella(text.lower())
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
    btn_invia.place(height=60, width=355, x = 700, y = 150)
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
    stringa = stringa.replace("%%", "ì").replace("&&"," ").replace("&"," ").replace("T00:00:00","").replace("\n",";\n")
    if stringa == "":
        vocal_label.configure(text="Mi dispiace, non ho trovato questo paziente")
        ws.update()
        audio_bot("Mi dispiace, non ho trovato questo paziente")
        return
    vocal_label.configure(text="Ho trovato i seguenti dati:\n"+stringa.replace(";",""))
    ws.update()
    audio_bot("Ho trovato i seguenti dati;\n"+stringa)


    # frame 3 for General Ward patient info
    frame3 = Frame(ws, bd = 2, relief = SOLID, padx = 5, pady = 5)
    frame3.config(bg = background_frame)
    frame3.place(x=600, y=250)
    general_string = '"SELECT ?id ?blood ?long ?terapia ?allergie ?resume ?create ?medicalCreate ?mod ?medicalMod WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/General_Section> {?p rdf:type sha:General_Section ; sha:id ?id ; sha:bloodgroup ?blood ; sha:fiscalCode ?cf ; sha:longDiseas ?long ; sha:terapia ?terapia ; sha:allergie ?allergie ; sha:resume ?resume ; sha:creationComune ?create ; sha:createFiscalCodeMedical ?medicalCreate ; sha:modifyComune ?mod  ; sha:modifyFiscalCodeMedical ?medicalMod . '
    general_string = general_string + "FILTER (regex (?cf, '" + input_cod_fis.get().upper() + "')) }}" + '"'
    name_query = '"QUERY"'
    general_string = name_query + ': { "sparql": ' + general_string + '}'
    general_string = create_sparql.creating(path_new, general_string)
    general_string = general_string.split("\n")
    Label(frame3, text="Sezione Socio Sanitaria Comune:", font=f, bg=background_frame).grid(row=0, column=0, sticky=W, pady=10)
    Label(frame3, text="ID\t\t\t\t"+general_string[0], font=f, bg=background_frame).grid(row=1, column=0, sticky=W, pady=10)
    Label(frame3, text="Gruppo Sanguigno\t\t\t"+general_string[1], font=f, bg=background_frame).grid(row=2, column=0, sticky=W, pady=10)
    Label(frame3, text="Patologie in atto\t\t\t"+general_string[2], font=f, bg=background_frame).grid(row=3, column=0, sticky=W, pady=10)
    Label(frame3, text="Terapia Continuativa\t\t"+general_string[3], font=f, bg=background_frame).grid(row=4, column=0, sticky=W, pady=10)
    Label(frame3, text="Allergie Note\t\t\t"+general_string[4], font=f, bg=background_frame).grid(row=5, column=0, sticky=W, pady=10)
    Label(frame3, text="Riassunto Paziente\t\t\t"+general_string[5], font=f, bg=background_frame).grid(row=6, column=0, sticky=W, pady=10)


    # frame 4 for General Ward patient info
    frame4 = Frame(ws, bd = 2, relief = SOLID, padx = 5, pady = 5)
    frame4.config(bg = background_frame)
    frame4.place(x=20, y=250)
    Label(frame4, text="Sezione Socio Sanitaria Comune:", font=f, bg=background_frame).grid(row=0, column=0, sticky=W, pady=10)
    Label(frame4, text="Data Creazione\t\t\t"+general_string[6].replace("T","    ").replace("Z",""), font=f, bg=background_frame).grid(row=1, column=0, sticky=W, pady=10)
    Label(frame4, text="Creata da\t\t\t\t"+general_string[7], font=f, bg=background_frame).grid(row=2, column=0, sticky=W, pady=10)
    if general_string[6] == general_string[8]:
        Label(frame4, text="Data Modifica\t\t\tMAI", font=f, bg=background_frame).grid(row=3, column=0, sticky=W, pady=10)
        Label(frame4, text="Modificata da\t\t\tMAI", font=f, bg=background_frame).grid(row=4, column=0, sticky=W, pady=10)
    else:
        Label(frame4, text="Data Modifica\t\t\t"+general_string[8].replace("T","    ").replace("Z",""), font=f, bg=background_frame).grid(row=3, column=0, sticky=W, pady=10)
        Label(frame4, text="Modificata da\t\t\t"+general_string[9], font=f, bg=background_frame).grid(row=4, column=0, sticky=W, pady=10)


    # creation frame for tree view for Ward Section
    frame2 = Frame(ws, bd = 2, relief = SOLID, padx = 5, pady = 5)
    frame2.config(bg = background_frame)
    frame2.place(x=20, y=600)
    Label(frame2, text="Sezioni Socio Sanitaria Specifica", font=f, bg=background_frame).grid(row=0, column=0, sticky=W, pady=10)
    columns = ('#1', '#2','#3', '#4','#5', '#6')
    # tree view for Ward Section
    tree = ttk.Treeview(ws, columns=columns, show='headings')
    vsb = ttk.Scrollbar(orient="vertical",
                command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    # define headings
    tree.heading('#1', text='ID Specifico')
    tree.heading('#2', text='Reparto')
    tree.heading('#3', text='Data Creazione')
    tree.heading('#4', text='Creata da')
    tree.heading('#5', text='Data Modifica')
    tree.heading('#6', text='Modificata da')
    tree.grid(column=0, row=1, sticky='nsew', in_=frame2)

    # search results
    ward_string = '"SELECT ?id ?reparto ?create ?medicalCreate ?mod ?medicalMod WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/Ward_Section> {?p rdf:type sha:Ward_Section ; sha:idSpec ?id ; sha:wardName ?reparto ; sha:fiscalCode ?cf ; sha:creationSpecifica ?create ; sha:createFiscalCodeMedical ?medicalCreate ; sha:modifySpecifica ?mod  ; sha:modifyFiscalCodeMedical ?medicalMod . '
    ward_string = ward_string + "FILTER (regex (?cf, '" + input_cod_fis.get().upper() + "')) }}" + '"'
    name_query = '"QUERY"'
    ward_string = name_query + ': { "sparql": ' + ward_string + '}'
    ward_string = create_sparql.creating(path_new, ward_string)
    ward_string = ward_string.split("\n")
    ward_result = []
    for i in range(0, len(ward_string), 6):
        string = (ward_string[i],ward_string[i+1],ward_string[i+2].replace("T","    ").replace("Z",""),ward_string[i+3],ward_string[i+4].replace("T","    ").replace("Z",""),ward_string[i+5])
        ward_result.append(string)


    for ward_result in ward_result:
        tree.insert('', END, values=ward_result)

    # bind the select event
    def item_selected(event):
        for selected_item in tree.selection():
            # dictionary
            item = tree.item(selected_item)
            # list
            record = item['values']
            #
    tree.bind('<<TreeviewSelect>>', item_selected)
    var = IntVar()
    btn_invia = Button(ws, width = 15, text = 'Va bene', command=lambda: var.set(1), font=f, bg=background_window,
        activebackground="#3399ff")
    btn_invia.place(height=60, width=355, x = 700, y = 150)
    btn_invia.wait_variable(var)
    btn_invia.destroy()
    frame.destroy()
    frame2.destroy()
    frame3.destroy()
    frame4.destroy()
    sleeping_duck()


def check_dottore():
    # program searches all your General Sections
    general_string = '"SELECT ?id ?cf ?create ?medicalCreate ?mod ?medicalMod WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/General_Section> {?p rdf:type sha:General_Section ; sha:id ?id ; sha:fiscalCode ?cf ; sha:creationComune ?create ; sha:createFiscalCodeMedical ?medicalCreate ; sha:modifyComune ?mod ; sha:modifyFiscalCodeMedical ?medicalMod . '
    general_string = general_string + "FILTER (regex (?medicalCreate, '" + CF + "')) }}" + '"'
    name_query = '"QUERY"'
    general_string = name_query + ': { "sparql": ' + general_string + '}'
    general_string = create_sparql.creating(path_new, general_string)
    general_string = general_string.replace("%%", "ì").replace("&&"," ").replace("&"," ").split("\n")


    # program searches all your Ward Sections
    ward_string = '"SELECT ?id ?cf ?reparto ?create ?medicalCreate ?mod ?medicalMod WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/Ward_Section> {?p rdf:type sha:Ward_Section ; sha:idSpec ?id ; sha:fiscalCode ?cf ; sha:wardName ?reparto ; sha:creationSpecifica ?create ; sha:createFiscalCodeMedical ?medicalCreate ; sha:modifySpecifica ?mod ; sha:modifyFiscalCodeMedical ?medicalMod . '
    ward_string = ward_string + "FILTER (regex (?medicalCreate, '" + CF + "')) }}" + '"'
    name_query = '"QUERY"'
    ward_string = name_query + ': { "sparql": ' + ward_string + '}'
    ward_string = create_sparql.creating(path_new, ward_string)
    ward_string = ward_string.replace("%%", "ì").replace("&&"," ").replace("&"," ").split("\n")


    # checking if there aren't your Sections
    if general_string == "" and ward_string == "":
        vocal_label.configure(text="Mi dispiace, non ho trovato alcuna tua cartella clinica")
        ws.update()
        audio_bot("Mi dispiace, non ho trovato alcuna tua cartella clinica")
        return


    # creation frame and treeview for general section
    frame = Frame(ws, bd = 2, relief = SOLID, padx = 5, pady = 5)
    frame.config(bg = background_frame)
    frame.place(x=20, y=300)
    Label(frame, text="Sezioni Socio Sanitaria Comune", font=f, bg=background_frame).grid(row=0, column=0, sticky=W, pady=10)
    columns = ('#1', '#2','#3', '#4','#5', '#6')
    tree = ttk.Treeview(ws, columns=columns, show='headings')
    vsb = ttk.Scrollbar(orient="vertical",
                    command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree.heading('#1', text='ID Comune')
    tree.heading('#2', text='Codice Fiscale')
    tree.heading('#3', text='Data Creazione')
    tree.heading('#4', text='Creata da')
    tree.heading('#5', text='Data Modifica')
    tree.heading('#6', text='Modificata da')
    tree.grid(column=0, row=1, sticky='nsew', in_=frame)
    general_result =[]
    for i in range(0, len(general_string), 6):
        string = (general_string[i],general_string[i+1],general_string[i+2].replace("T","    ").replace("Z",""),general_string[i+3],general_string[i+4].replace("T","    ").replace("Z",""),general_string[i+5])
        general_result.append(string)
    for general_result in general_result:
        tree.insert('', END, values=general_result)
    def item_selected(event):
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']
    tree.bind('<<TreeviewSelect>>', item_selected)


    # creation frame and treeview for ward section
    frame2 = Frame(ws, bd = 2, relief = SOLID, padx = 5, pady = 5)
    frame2.config(bg = background_frame)
    frame2.place(x=20, y=600)
    Label(frame2, text="Sezioni Socio Sanitaria Specifica", font=f, bg=background_frame).grid(row=0, column=0, sticky=W, pady=10)
    columns = ('#1', '#2','#3', '#4','#5', '#6','#7')
    tree2 = ttk.Treeview(ws, columns=columns, show='headings')
    vsb2 = ttk.Scrollbar(orient="vertical",
                    command=tree.yview)
    tree2.configure(yscrollcommand=vsb2.set)
    tree2.heading('#1', text='ID Specifica')
    tree2.heading('#2', text='Codice Fiscale')
    tree2.heading('#3', text='Reparto')
    tree2.heading('#4', text='Data Creazione')
    tree2.heading('#5', text='Creata da')
    tree2.heading('#6', text='Data Modifica')
    tree2.heading('#7', text='Modificata da')
    tree2.grid(column=0, row=1, sticky='nsew', in_=frame2)
    ward_result =[]
    for i in range(0, len(ward_string), 7):
        string2 = (ward_string[i],ward_string[i+1],ward_string[i+2],ward_string[i+3].replace("T","    ").replace("Z",""),ward_string[i+4],ward_string[i+5].replace("T","    ").replace("Z",""),ward_string[i+6])
        ward_result.append(string2)
    for ward_result in ward_result:
        tree2.insert('', END, values=ward_result)
    def item_selected(event):
        for selected_item in tree2.selection():
            item = tree2.item(selected_item)
            record = item['values']
    tree2.bind('<<TreeviewSelect>>', item_selected)


    # wait button for delating all components of frames
    var = IntVar()
    btn_invia = Button(ws, width = 15, text = 'Va bene', command=lambda: var.set(1), font=f, bg=background_window,
        activebackground="#3399ff")
    btn_invia.place(height=60, width=355, x = 700, y = 150)
    btn_invia.wait_variable(var)
    btn_invia.destroy()
    frame.destroy()
    frame2.destroy()




def check_reparto(text):
    vocal_label.configure(text="")
    ws.update()
    text5 = text
    ward = query_sparql.connessione("QUERY_WARD", path)
    ward = ward.split("\n")
    text = text.split(" ")
    for x in ward:
        for y in text:
            if x == y or x.replace("_"," ") in text5:
                text1 = []
                for z in text:
                    if z in string_to_month:
                        text1.append("%%" + str(string_to_month.index(z)+1) + " ")
                    elif z in string_to_number:
                        text1.append(str(string_to_month.index(z)) + " ")
                    elif z in string_to_year:
                        text1.append("&&" + z)
                    else:
                        text1.append(z + " ")
                text2 = ""
                for ele in text1:
                    text2 += ele + " "
                if not "&&" in text2 or not "%%" in text2:
                    vocal_label.configure(text="Mi dispiace, la data non è corretta")
                    ws.update()
                    audio_bot("Mi dispiace, la data non è corretta")
                    return
                month = text2[text2.index("%%")+2] + text2[text2.index("%%")+3]
                if month[1] == " ":
                    month = "0" + text2[text2.index("%%")+2]
                month = month.replace("%%","")

                year = text2[text2.index("&&")+2] + text2[text2.index("&&")+3] + text2[text2.index("&&")+4] + text2[text2.index("&&")+5]
                year = year.replace("&&","")
                day = 0
                text2 = text2.replace(month, "").replace(year, "")
                text2 = text2.split(" ")
                for k in text2:
                    if k.isnumeric():
                        day = k
                        date = year + "-" + month + "-" + day


                        # program searches all your General Sections
                        general_string = '"SELECT * WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/General_Section> {?p rdf:type sha:General_Section ; sha:id ?id ; sha:fiscalCode ?cf ; sha:creationComune ?create ; sha:createFiscalCodeMedical ?medicalCreate . '
                        general_string = general_string + "FILTER (regex (?create, '^" + date + "')) }}" + '"'
                        name_query = '"QUERY"'
                        general_string = name_query + ': { "sparql": ' + general_string + '}'
                        general_string = create_sparql.creating(path_new, general_string)
                        general_string = general_string.replace("%%", "ì").replace("&&"," ").replace("&"," ").split("\n")


                        # creation frame and treeview for general section
                        frame = Frame(ws, bd = 2, relief = SOLID, padx = 5, pady = 5)
                        frame.config(bg = background_frame)
                        frame.place(x=20, y=300)
                        Label(frame, text="Sezioni Socio Sanitaria Comune", font=f, bg=background_frame).grid(row=0, column=0, sticky=W, pady=10)
                        columns = ('#1', '#2','#3')
                        tree = ttk.Treeview(ws, columns=columns, show='headings')
                        vsb = ttk.Scrollbar(orient="vertical",
                                        command=tree.yview)
                        tree.configure(yscrollcommand=vsb.set)
                        tree.heading('#1', text='ID Comune')
                        tree.heading('#2', text='Codice Fiscale')
                        tree.heading('#3', text='Creata da')
                        tree.grid(column=0, row=1, sticky='nsew', in_=frame)
                        general_result =[]


                        if general_string != ['']:
                            for i in range(0, len(general_string), 5):
                                string = (general_string[i+1],general_string[i+2],general_string[i+4])
                                general_result.append(string)
                            for general_result in general_result:
                                tree.insert('', END, values=general_result)
                            def item_selected(event):
                                for selected_item in tree.selection():
                                    item = tree.item(selected_item)
                                    record = item['values']
                            tree.bind('<<TreeviewSelect>>', item_selected)


                        # program searches all your General Sections
                        ward_string = '"SELECT * WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/Ward_Section> {?p rdf:type sha:Ward_Section ; sha:idSpec ?id ; sha:fiscalCode ?cf ; sha:creationSpecifica ?create ; sha:createFiscalCodeMedical ?medicalCreate . '
                        ward_string = ward_string + "FILTER (regex (?create, '^" + date + "')) }}" + '"'
                        name_query = '"QUERY"'
                        ward_string = name_query + ': { "sparql": ' + ward_string + '}'
                        ward_string = create_sparql.creating(path_new, ward_string)
                        ward_string = ward_string.replace("%%", "ì").replace("&&"," ").replace("&"," ").split("\n")


                        # creation frame and treeview for ward section
                        frame2 = Frame(ws, bd = 2, relief = SOLID, padx = 5, pady = 5)
                        frame2.config(bg = background_frame)
                        frame2.place(x=20, y=600)
                        Label(frame2, text="Sezioni Socio Sanitaria Specifica", font=f, bg=background_frame).grid(row=0, column=0, sticky=W, pady=10)
                        columns = ('#1', '#2','#3')
                        tree2 = ttk.Treeview(ws, columns=columns, show='headings')
                        vsb2 = ttk.Scrollbar(orient="vertical",
                                        command=tree.yview)
                        tree2.configure(yscrollcommand=vsb2.set)
                        tree2.heading('#1', text='ID Specifica')
                        tree2.heading('#2', text='Codice Fiscale')
                        tree2.heading('#3', text='Creata da')
                        tree2.grid(column=0, row=1, sticky='nsew', in_=frame2)
                        ward_result =[]

                        if ward_string != ['']:
                            for i in range(0, len(ward_string), 5):
                                string2 = (ward_string[i+1],ward_string[i+2],ward_string[i+4])
                                ward_result.append(string2)
                            for ward_result in ward_result:
                                tree2.insert('', END, values=ward_result)
                            def item_selected(event):
                                for selected_item in tree2.selection():
                                    item = tree2.item(selected_item)
                                    record = item['values']
                            tree2.bind('<<TreeviewSelect>>', item_selected)

                        vocal_label.configure(text=date)
                        ws.update()
                        # wait button for delating all components of frames
                        var = IntVar()
                        btn_invia = Button(ws, width = 15, text = 'Va bene', command=lambda: var.set(1), font=f, bg=background_window,
                            activebackground="#3399ff")
                        btn_invia.place(height=60, width=355, x = 700, y = 150)
                        btn_invia.wait_variable(var)
                        btn_invia.destroy()
                        frame.destroy()
                        frame2.destroy()
                        return

                vocal_label.configure(text="Mi dispiace, la data non è corretta")
                ws.update()
                audio_bot("Mi dispiace, la data non è corretta")
                return

    vocal_label.configure(text="Mi dispiace, non trovo il reparto")
    ws.update()
    audio_bot("Mi dispiace, non trovo il reparto")
    return





def check_cartella(text):
    text = text.split(" ")
    text1 = []
    for y in text:
        if y in string_to_number:
            text1.append(str(string_to_number.index(y)))
        else:
            text1.append(y)
    text = text1
    for y in text:
        if y == "comune":
            for z in text:
                if z.isnumeric():
                    general_string = '"SELECT * WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/General_Section> {?p rdf:type sha:General_Section ; sha:id ?id ; sha:fiscalCode ?cf ; sha:bloodgroup ?blood ; sha:longDiseas ?long ; sha:terapia ?terapia ; sha:allergie ?allergie ; sha:resume ?resume ; sha:creationComune ?create ; sha:createFiscalCodeMedical ?medicalCreate ; sha:modifyComune ?mod ; sha:modifyFiscalCodeMedical ?medicalMod . '
                    general_string = general_string + "FILTER (regex (?id, '" + z + "')) }}" + '"'
                    name_query = '"QUERY"'
                    general_string = name_query + ': { "sparql": ' + general_string + '}'
                    general_string = create_sparql.creating(path_new, general_string)

                    # check if that medical records exists
                    if general_string == "":
                        vocal_label.configure(text="Mi dispiace, non trovo la cartella comune con quell'ID")
                        ws.update()
                        audio_bot("Mi dispiace, non trovo la cartella comune con quell'ID")
                        return


                    general_string = general_string.replace("%%", "ì").replace("&&"," ").replace("&"," ").split("\n")


                    # frame 4 for General Ward patient info
                    frame3 = Frame(ws, bd = 2, relief = SOLID, padx = 5, pady = 5)
                    frame3.config(bg = background_frame)
                    frame3.place(x=600, y=250)
                    Label(frame3, text="Sezione Socio Sanitaria Comune:", font=f, bg=background_frame).grid(row=0, column=0, sticky=W, pady=10)
                    Label(frame3, text="ID\t\t\t\t"+general_string[1], font=f, bg=background_frame).grid(row=1, column=0, sticky=W, pady=10)
                    Label(frame3, text="Codice Fiscale\t\t\t"+general_string[2], font=f, bg=background_frame).grid(row=2, column=0, sticky=W, pady=10)
                    Label(frame3, text="Gruppo Sanguigno\t\t\t"+general_string[3], font=f, bg=background_frame).grid(row=3, column=0, sticky=W, pady=10)
                    Label(frame3, text="Patologie in atto\t\t\t"+general_string[4], font=f, bg=background_frame).grid(row=4, column=0, sticky=W, pady=10)
                    Label(frame3, text="Terapia Continuativa\t\t"+general_string[5], font=f, bg=background_frame).grid(row=5, column=0, sticky=W, pady=10)
                    Label(frame3, text="Allergie Note\t\t\t"+general_string[6], font=f, bg=background_frame).grid(row=6, column=0, sticky=W, pady=10)
                    Label(frame3, text="Riassunto Paziente\t\t\t"+general_string[7], font=f, bg=background_frame).grid(row=7, column=0, sticky=W, pady=10)


                    # frame 4 for General Ward patient info
                    frame4 = Frame(ws, bd = 2, relief = SOLID, padx = 5, pady = 5)
                    frame4.config(bg = background_frame)
                    frame4.place(x=20, y=250)
                    Label(frame4, text="Sezione Socio Sanitaria Comune:", font=f, bg=background_frame).grid(row=0, column=0, sticky=W, pady=10)
                    Label(frame4, text="Data Creazione\t\t\t"+general_string[8].replace("T","    ").replace("Z",""), font=f, bg=background_frame).grid(row=1, column=0, sticky=W, pady=10)
                    Label(frame4, text="Creata da\t\t\t\t"+general_string[9], font=f, bg=background_frame).grid(row=2, column=0, sticky=W, pady=10)
                    if general_string[8] == general_string[10]:
                        Label(frame4, text="Data Modifica\t\t\tMAI", font=f, bg=background_frame).grid(row=3, column=0, sticky=W, pady=10)
                        Label(frame4, text="Modificata da\t\t\tMAI", font=f, bg=background_frame).grid(row=4, column=0, sticky=W, pady=10)
                    else:
                        Label(frame4, text="Data Modifica\t\t\t"+general_string[10].replace("T","    ").replace("Z",""), font=f, bg=background_frame).grid(row=3, column=0, sticky=W, pady=10)
                        Label(frame4, text="Modificata da\t\t\t"+general_string[11], font=f, bg=background_frame).grid(row=4, column=0, sticky=W, pady=10)


                    audio_bot("Cartella comune: " + z)


                    # wait button for delating all components of frames
                    var = IntVar()
                    btn_invia = Button(ws, width = 15, text = 'Va bene', command=lambda: var.set(1), font=f, bg=background_window,
                        activebackground="#3399ff")
                    btn_invia.place(height=60, width=355, x = 700, y = 150)
                    btn_invia.wait_variable(var)
                    btn_invia.destroy()
                    frame3.destroy()
                    frame4.destroy()
                    return


        elif y == "specifica":
            for z in text:
                if z.isnumeric():
                    ward_string = '"SELECT * WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/Ward_Section> {?p rdf:type sha:Ward_Section ; sha:idSpec ?id ; sha:fiscalCode ?cf ; sha:wardName ?reparto ; sha:dimission ?dimission ; sha:exam ?exam ; sha:plan ?plan ; sha:creationSpecifica ?create ; sha:createFiscalCodeMedical ?medicalCreate ; sha:modifySpecifica ?mod ; sha:modifyFiscalCodeMedical ?medicalMod ; sha:diagn ?diagn. '
                    ward_string = ward_string + "FILTER (regex (?id, '" + z + "')) }}" + '"'
                    name_query = '"QUERY"'
                    ward_string = name_query + ': { "sparql": ' + ward_string + '}'
                    ward_string = create_sparql.creating(path_new, ward_string)

                    # check if that medical records exists
                    if ward_string == "":
                        vocal_label.configure(text="Mi dispiace, non trovo la cartella specifica con quell'ID")
                        ws.update()
                        audio_bot("Mi dispiace, non trovo la specifica comune con quell'ID")
                        return

                    ward_string = ward_string.replace("%%", "ì").replace("&&"," ").replace("&"," ").split("\n")


                    # frame 4 for General Ward patient info
                    frame3 = Frame(ws, bd = 2, relief = SOLID, padx = 5, pady = 5)
                    frame3.config(bg = background_frame)
                    frame3.place(x=600, y=250)
                    Label(frame3, text="Sezione Socio Sanitaria Specifica:", font=f, bg=background_frame).grid(row=0, column=0, sticky=W, pady=10)
                    Label(frame3, text="ID\t\t\t\t"+ward_string[1], font=f, bg=background_frame).grid(row=1, column=0, sticky=W, pady=10)
                    Label(frame3, text="Codice Fiscale\t\t\t"+ward_string[2], font=f, bg=background_frame).grid(row=2, column=0, sticky=W, pady=10)
                    Label(frame3, text="Reparto\t\t\t\t"+ward_string[3], font=f, bg=background_frame).grid(row=3, column=0, sticky=W, pady=10)
                    Label(frame3, text="Lettera di Dimissione\t\t"+ward_string[4], font=f, bg=background_frame).grid(row=4, column=0, sticky=W, pady=10)
                    Label(frame3, text="Esami effettuati\t\t\t"+ward_string[5], font=f, bg=background_frame).grid(row=5, column=0, sticky=W, pady=10)
                    Label(frame3, text="Piano di cura\t\t\t"+ward_string[6], font=f, bg=background_frame).grid(row=6, column=0, sticky=W, pady=10)
                    diagn = ""
                    for i in range(0,len(ward_string),12):
                        diagn = diagn + str(ward_string[i+11]) + "; "
                    Label(frame3, text="Diagnosi [ICD9-CM]\t\t"+diagn, font=f, bg=background_frame).grid(row=6, column=0, sticky=W, pady=10)


                    # frame 4 for General Ward patient info
                    frame4 = Frame(ws, bd = 2, relief = SOLID, padx = 5, pady = 5)
                    frame4.config(bg = background_frame)
                    frame4.place(x=20, y=250)
                    Label(frame4, text="Sezione Socio Sanitaria Specifica:", font=f, bg=background_frame).grid(row=0, column=0, sticky=W, pady=10)
                    Label(frame4, text="Data Creazione\t\t\t"+ward_string[7].replace("T","    ").replace("Z",""), font=f, bg=background_frame).grid(row=1, column=0, sticky=W, pady=10)
                    Label(frame4, text="Creata da\t\t\t\t"+ward_string[8], font=f, bg=background_frame).grid(row=2, column=0, sticky=W, pady=10)
                    if ward_string[7] == ward_string[9]:
                        Label(frame4, text="Data Modifica\t\t\tMAI", font=f, bg=background_frame).grid(row=3, column=0, sticky=W, pady=10)
                        Label(frame4, text="Modificata da\t\t\tMAI", font=f, bg=background_frame).grid(row=4, column=0, sticky=W, pady=10)
                    else:
                        Label(frame4, text="Data Modifica\t\t\t"+ward_string[9].replace("T","    ").replace("Z",""), font=f, bg=background_frame).grid(row=3, column=0, sticky=W, pady=10)
                        Label(frame4, text="Modificata da\t\t\t"+ward_string[10], font=f, bg=background_frame).grid(row=4, column=0, sticky=W, pady=10)


                    vocal_label.configure(text="Cartella specifica: " + z)
                    ws.update()
                    audio_bot("Cartella specifica: " + z)


                    # wait button for delating all components of frames
                    var = IntVar()
                    btn_invia = Button(ws, width = 15, text = 'Va bene', command=lambda: var.set(1), font=f, bg=background_window,
                        activebackground="#3399ff")
                    btn_invia.place(height=60, width=355, x = 700, y = 150)
                    btn_invia.wait_variable(var)
                    btn_invia.destroy()
                    frame3.destroy()
                    frame4.destroy()
                    return


    vocal_label.configure(text="Mi dispiace, ma devi specificare se devo cercare una cartella comune o specifica")
    ws.update()
    audio_bot("Mi dispiace, ma devi specificare se devo cercare una cartella comune o specifica")



def check_icd9(text):
    text = text.replace("00 ","00").split(" ")
    for y in text:
        if y.isnumeric():
            if icd9_package.search_diagn(y) != None:
                vocal_label.configure(text=icd9_package.search_diagn(y))
                ws.update()
                code_icd9 = str(icd9_package.search_diagn(y))
                audio_bot(code_icd9.replace(":",";"))
                return
    vocal_label.configure(text="Mi dispiace, ma il codice icd9-cm che mi hai detto non è valido")
    ws.update()
    audio_bot("Mi dispiace, ma il codice icd9-cm che mi hai detto non è valido")



def check_statistiche(text):
    for y in text:
        if y.isnumeric():
            if icd9_package.search_diagn(y) != None:
                print("statistiche: " + y)
                return
        print("Mi dispiace, ma il codice icd9-cm che mi hai detto non è valido")
        return
    print("Mi dispiace, ma non ho capito il codice ICD9")
    return


duck_label = Label(ws, justify=LEFT, text=duck_sleep)
duck_label.place(x=150, y=80)
vocal_label = Label(ws, justify=LEFT, text="", font = f)
vocal_label.place(x=350, y=80)
user_label = Label(ws, text="", font = f)
user_label.place(x=700, y=250)
ws.after(1000, setting)


ws.mainloop()

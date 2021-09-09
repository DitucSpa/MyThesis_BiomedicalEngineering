# TECHNICIAN.PY
# This is a form - tkinter program for technicians who insert new health workers on OWL (Protegé file).
# Technicians must insert: name, fiscal code, birth date and others.
# When technicians click on the button, the program check all the inputs.
# It uses SEPA (https://github.com/arces-wot/SEPABins).
# Note: some information are in italian.

# Packages for form - tkinter
from tkinter import *
from tkinter import messagebox
import ctypes
import re
import datetime
from datetime import date
import os

# Packages for SEPA
from sepy.SAPObject import *
from sepy import *
import json
from sepy.SEPA import *


# Open the jsap and connection
mySAP = open(r"C:\Users\gianl\Documents\GitHub\MyThesis_BiomedicalEngineering\JSAP\TesiProva.jsap","r") # CHANGE DIRECTORY
sap = SAPObject(json.load(mySAP))
sc = SEPA(sapObject=sap)

result = sc.query("QUERY_WARD")
str1 = json.dumps(result)
# the follow lines are used for extrapolating only the values
str1 = str1.replace(" ","").replace('"value":"',"&&&").replace("{","").replace("}","").replace(",","\n")
text_file = open("Output.txt", "w")
text_file.write(str1)
text_file.close()
with open("Output.txt","r") as fin:
    with open("input.txt","w") as fout:
        for line in fin:
            if line.startswith('&&&'):
                fout.write(line)
            else:
                fout.write("")
with open("input.txt","r") as file:
    ward = file.read().replace("&&&","").replace("[","").replace("]","").replace('"',"")
os.remove("input.txt")
os.remove("output.txt ")

# other declarations
f = ('Times', 14) # the font of the program
background_frame = "#80b3ff" # background of the frame
background_window = "#b3ccff" # background of the window
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' # it's used for checking email

# declaration of message box; there are three parametres --> title, text of the message and style (0 for OK, 1 for OK - CANCEl, ...)
def Mbox(title, text):
    return messagebox.showerror(title=title, message=text, icon = 'error')
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


# declaration of the window
ws = Tk()
ws.title('Tesi Di Tuccio -- Technician')
ws.geometry('1100x600')
ws.config(bg = background_window)


# There are two frames. They are used for general information (left frame) and others (right frame)
frame = Frame(ws, bd = 2, relief = SOLID, padx = 5, pady = 5)
frame.config(bg = background_frame)
frame2 = Frame(ws, bd = 2, relief = SOLID, padx = 20, pady = 15)
frame2.config(bg = background_frame)


# list of gender option menu
var_sesso = StringVar()
sesso = ('Maschio', 'Femmina', 'Altro')
var_sesso.set(sesso[0]) # default --> first value

# list of ward option menu
var_ward = StringVar()
h_ward = ward.replace("\n","|").split("|")
var_ward.set(h_ward[0]) # default --> first value

# list of role option menu
var_ruolo = StringVar()
ruolo = ('Doctor', 'Head Nurse', 'Head Physician', 'Nurse')
var_ruolo.set(ruolo[0]) # default --> first value

# declaration of the gender option menu
input_sesso = OptionMenu(frame, var_sesso, *sesso)
input_sesso["menu"].config(bg=background_frame) # change color
input_sesso.config(width=15, font=f, bg=background_frame, activebackground=background_frame)
input_sesso["highlightthickness"]= 0 # disable the color of the background

# declaration of the role option menu
input_ward = OptionMenu(frame, var_ward, *h_ward)
input_ward["menu"].config(bg=background_frame) # change color
input_ward.config(width=15, font=f, bg=background_frame, activebackground=background_frame)
input_ward["highlightthickness"]= 0 # disable the color of the background

# declaration of the role option menu
input_ruolo = OptionMenu(frame, var_ruolo, *ruolo)
input_ruolo["menu"].config(bg=background_frame) # change color
input_ruolo.config(width=15, font=f, bg=background_frame, activebackground=background_frame)
input_ruolo["highlightthickness"]= 0 # disable the color of the background


# declaration of label and text box for further information
Label(frame2, text = 'Ulteriori informazioni:', font=f, bg = background_frame).pack(pady=5)
text_area = Text(frame2, height = 13, width = 40,font = f)
text_area.pack()

# declaration of label for health workers' dates
Label(frame, text="Cognome Nome", font=f, bg=background_frame).grid(row=0, column=0, sticky=W, pady=10)
Label(frame, text="Data di Nascita", font=f, bg=background_frame).grid(row=1, column=0, sticky=W, pady=10)
Label(frame, text="(YYYY/MM/DD)", font=f, bg=background_frame).grid(row=1, column=3, sticky=W, pady=10)
Label(frame, text="Sesso", font=f, bg=background_frame).grid(row=2, column=0, sticky=W, pady=10)
Label(frame, text="Codice Fiscale", font=f, bg=background_frame).grid(row=3, column=0, sticky=W, pady=10)
Label(frame, text="Email", font=f, bg=background_frame).grid(row=4, column=0, sticky=W, pady=10)
Label(frame, text="Recapito Telefonico", font=f, bg=background_frame).grid(row=5, column=0, sticky=W, pady=10)
Label(frame, text="Reparto", font=f, bg=background_frame).grid(row=6, column=0, sticky=W, pady=10)
Label(frame, text="Ruolo", font=f, bg=background_frame).grid(row=7, column=0, sticky=W, pady=10)

# declaration of text box for health workers' dates
input_nome_cognome = Entry(frame, font=f)
input_eta = Entry(frame, font=f)
input_cod_fis = Entry(frame, font=f)
input_email = Entry(frame, font=f)
input_recapito = Entry(frame, font=f)
#input_reparto = Entry(frame, font=f)


# position of the text box in the left frame
input_nome_cognome.grid(row=0, column=1, pady=10, padx=20)
input_eta.grid(row=1, column=1, pady=10, padx=20)
input_sesso.grid(row=2, column=1, pady=10, padx=20)
input_cod_fis.grid(row=3, column=1, pady=10, padx=20)
input_email.grid(row=4, column=1, pady=10, padx=20)
input_recapito.grid(row=5, column=1, pady=10, padx=20)
input_ward.grid(row=6, column=1, pady=10, padx=20)
input_ruolo.grid(row=7, column=1, pady=10, padx=20)

# position of the frames
frame.place(x=50, y=50)
frame2.place(x=650, y=50)


# Does fiscal code already exist in the OWL? And then program uploads dates on OWL
def check_cod_fis():
    result = sc.query("QUERY_HEALTH_WORKER_FISCAL_CODE")
    str1 = json.dumps(result)
    # the follow lines are used for extrapolating only the values
    str1 = str1.replace(" ","").replace('"value":"',"&&&").replace("{","").replace("}","").replace(",","\n")
    text_file = open("Output.txt","w")
    text_file.write(str1)
    text_file.close()
    with open("Output.txt","r") as fin:
        with open("input.txt","w") as fout:
            for line in fin:
                if line.startswith('&&&'):
                    fout.write(line)
                else:
                    fout.write("")
    with open("input.txt","r") as file:
        data = file.read().replace("&&&","").replace("[","").replace("]","").replace('"',"")
    os.remove("input.txt")
    os.remove("output.txt ")
    # check if fiscal code already exists
    if input_cod_fis.get().upper() in data:
        Mbox('Attenzione!', "L'utente già esiste")
    else:
        # SPARQL insert
        sc.update("INSERT_HEALTH_WORKER_FISCAL_CODE",
            forcedBindings={"fiscalCode": input_cod_fis.get().upper()})


# check all inputs when technician click on the button
def controllo():
    # check name
    if (len(input_nome_cognome.get()) == 0):
        Mbox('Attenzione!', 'Cognome e Nome non validi.')
        return
    # check birth date
    isValidDate = True
    try:
        year,month,day = input_eta.get().split('/') # it gets the current day
        if len(year) != 4:
            isValidDate = False
        a = datetime.datetime(int(year),int(month),int(day))
        b = datetime.date.today()
        if (b - a.date()).days == 0 or (b - a.date()).days < 0 or (b - a.date()).days < 365 * 18: # health worker must be over 18yo (365 days * 18)
            isValidDate = False
    except ValueError:
        isValidDate = False
    if not (isValidDate):
        Mbox('Attenzione!', 'La data di nascita non è valida.')
        return
    # check fiscal code
    if len(input_cod_fis.get()) != 16:
        Mbox('Attenzione!', 'Il codice fiscale inserito non è corretto.')
        return
    # check email
    if not (re.fullmatch(regex, input_email.get())):
        Mbox('Attenzione!', 'La mail inserita non è valida.')
        return
    # check phone number
    if not (input_recapito.get().isnumeric()):
        Mbox('Attenzione!', 'Numero di telefono non valido.')
        return
    # message box with all parametres
    stringa = 'I seguenti dati sono corretti?\n'
    stringa = stringa + '\n' + input_nome_cognome.get().upper() + '\n' + input_eta.get() + '\n' + var_sesso.get()
    stringa = stringa + '\n' + input_cod_fis.get().upper() + '\n' + input_email.get().lower() + '\n' + input_recapito.get()
    stringa = stringa + '\n' + var_ward.get() + '\n' + var_ruolo.get() + '\n' + '\n' + text_area.get("1.0", "end-1c")
    result = messagebox.askquestion("Attenzione...", stringa, icon = 'question')
    if result == 'yes':
            check_cod_fis() # Does fiscal code already exist in the OWL? And then program uploads dates on OWL
    else:
        pass


# declaration of the button
btn_crea = Button(ws, width = 15, text = 'Crea', font=f, command = controllo, bg='#4d94ff',
    activebackground="#3399ff")
btn_crea.pack()
btn_crea.place(height=50, width=300, x = 700, y = 450)



ws.mainloop()

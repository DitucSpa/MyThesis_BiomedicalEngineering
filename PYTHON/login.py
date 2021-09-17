# LOGIN.PY
from tkinter import *
import ctypes
import re
import getpass

# package used for matching the log-in inputs
import create_sparql



path_new = r"C:\Users\Ovettino\Downloads\GitHub\MyThesis_BiomedicalEngineering\JSAP" # path used for temp file
background_window = "#b3ccff"
background_frame = "#80b3ff"
f = ('Times', 14) # font
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' # check email


ws = Tk()
ws.title('Tesi Di Tuccio -- Login')
ws.geometry('450x300')
ws.config(bg=background_window)
frame = Frame(ws, bd=2, relief=SOLID, padx=20, pady=20)
frame.config(bg=background_frame)
Label(frame, text="Email", bg=background_frame,font=f).grid(row=0, column=0, sticky=W, pady=10)
Label(frame, text="Password", bg=background_frame,font=f).grid(row=1, column=0, pady=10)
txt_email = Entry(frame, font=f)
txt_password = Entry(frame, font=f,show="*")
txt_email.grid(row=0, column=1, pady=10, padx=20)
txt_password.grid(row=1, column=1, pady=10, padx=20)
frame.place(x=50, y=50)


# message box
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)



def login_button():
    if not (re.fullmatch(regex, txt_email.get())):
        Mbox('Attenzione!', 'La mail inserita non è valida.', 1)
        return
    # controllo Reparto e Stanza
    if (len(txt_password.get()) == 0):
        Mbox('Attenzione!', 'Password non valida.', 1)
        return

    # check if username and password exist
    stringa = '"SELECT ?cf WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/Medical_Staff> {?h rdf:type sha:Medical_Staff ; sha:fiscalCode ?cf ; sha:password ?p ; sha:username ?u . '
    stringa = stringa + "FILTER (regex (?u, '" + txt_email.get() + "')) . FILTER (regex (?p, '" + txt_password.get() + "')) }}" + '"'
    name_query = '"QUERY"'
    stringa = name_query + ': { "sparql": ' + stringa + '}'
    stringa = create_sparql.creating(path_new, stringa)
    if stringa != "":



btn_login = Button(frame, width=15, text='Login', bg='#4d94ff', activebackground="#3399ff",font=f, command=login_button)
btn_login.grid(row=2, column=1, pady=10, padx=20)
ws.mainloop()

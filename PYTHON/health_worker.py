# HEALTH_WORKER.PY
# Questo software permette l'inserimento dei dati diagnostici riferiti a:
# pazienti, cartelle cliniche e modifiche dei dati personali.
# Inserimento dei pazienti avviene tramite l'utilizzo del file JSAP, come per le cartelle cliniche.
# Una volta controllato che il dato non esista, lo inscerisce.
# Cartella clinica comune --> Sezione Socio Sanitaria Comune.
# Cartella clinica specifica --> Sezione Socio Sanitaria Specifica
# Per inserire una cartella clinica specifica è necessario prima di tutto inserire
# i dati di una cartella clinica comune, dopo aver inserito i dati del paziente.
# Molte parti possono essere ottimizzate e scritte con una miglior sintassi


# packages for tkinter
import tkinter
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import re
import datetime
from datetime import date
import os
import query_sparql
import create_sparql
import getpass
import icd9_package
from codicefiscale import codicefiscale


# other declarations
f = ('Times', 14) # the font of the program
background_frame = "#80b3ff" # background of the frame
background_window = "#b3ccff" # background of the window
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' # it's used for checking email
path = r"C:\Users\raffa\Downloads\GitHub\MyThesis_BiomedicalEngineering\JSAP\TesiProva.jsap" # path of JSAP file
path_new = r"C:\Users\raffa\Downloads\GitHub\MyThesis_BiomedicalEngineering\JSAP" # path used for temp file
CF = "DTCGLC99C29C573A" # fake login (only this fiscal code can log into this program)


class tkinterApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = Frame(self)
        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # initializing frames to an empty array
        self.frames = {}
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Login, MainPage, Add_Patient, Add_CCE_Comune, Add_CCE_Specifica, Mod_Medical):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
            self.currentFrame = None
        self.show_frame(Login)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()





class Login(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)


        frame = Frame(self, bd=2, relief=SOLID, padx=20, pady=20)
        frame.config(bg=background_frame)
        Label(frame, text="Email", bg=background_frame,font=f).grid(row=0, column=0, sticky=W, pady=10)
        Label(frame, text="Password", bg=background_frame,font=f).grid(row=1, column=0, pady=10)
        txt_email = Entry(frame, font=f)
        txt_password = Entry(frame, font=f,show="*")
        txt_email.grid(row=0, column=1, pady=10, padx=20)
        txt_password.grid(row=1, column=1, pady=10, padx=20)
        frame.place(x=480, y=270)


        def Mbox(title, text):
            return messagebox.showerror(title=title, message=text, icon = 'error')


        def login_button():
            if not (re.fullmatch(regex, txt_email.get())):
                Mbox('Attenzione!', 'La mail inserita non è valida.')
                return
            # controllo Reparto e Stanza
            if (len(txt_password.get()) == 0):
                Mbox('Attenzione!', 'Password non valida.')
                return
            # check if username and password exist
            stringa = '"SELECT ?cf WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/Medical_Staff> {?h rdf:type sha:Medical_Staff ; sha:fiscalCode ?cf ; sha:password ?p ; sha:username ?u . '
            stringa = stringa + "FILTER (regex (?u, '" + txt_email.get() + "')) . FILTER (regex (?p, '" + txt_password.get() + "')) }}" + '"'
            name_query = '"QUERY"'
            stringa = name_query + ': { "sparql": ' + stringa + '}'
            stringa = create_sparql.creating(path_new, stringa)
            if stringa == CF:
                controller.show_frame(MainPage)
            else:
                Mbox("Attenzione!","Credenziali non valide.")


        btn_login = Button(frame, width=15, text='Login', bg='#4d94ff', activebackground="#3399ff",font=f, command=login_button)
        btn_login.grid(row=2, column=1, pady=10, padx=20)


# fake LOGIN
class MainPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        stringa = '"SELECT ?cf ?email ?wMail ?phone ?wPhone ?ward ?studio ?orari ?other WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/Medical_Staff> {?h rdf:type sha:Medical_Staff ; sha:fiscalCode ?cf ; sha:wardName ?ward ; sha:email ?email ; sha:emailWork ?wMail ; sha:phoneNumber ?phone ; sha:phoneNumberWork ?wPhone ; sha:studio ?studio ; sha:timeSchedule ?orari ; sha:otherWorker ?other . '
        stringa = stringa + "FILTER (regex (?cf, '" + CF + "'))}}" + '"'
        name_query = '"QUERY"'
        stringa = name_query + ': { "sparql": ' + stringa + '}'
        stringa = create_sparql.creating(path_new, stringa)
        stringa = stringa.replace("%%", "ì").replace("&"," ").replace("&&"," ").split("\n")

        frame = Frame(self, bd = 2, relief = SOLID, padx = 5, pady = 5)
        frame.config(bg = background_frame)
        frame.place(x=50, y=70)
        orario = "Orario:\t\t"
        string_orario = stringa[7].replace(";","\n").split("\n")
        for i in range(len(string_orario)):
            orario = orario + string_orario[i] + "\n\t\t"
        Label(frame, text="Codisce fiscale:\t\t "+stringa[0], font=f, bg=background_frame).grid(row=0, column=0, sticky=W, pady=10)
        Label(frame, text="Email (personale):\t\t "+stringa[2], font=f, bg=background_frame).grid(row=1, column=0, sticky=W, pady=10)
        Label(frame, text="Email (lavorativa):\t\t "+stringa[3], font=f, bg=background_frame).grid(row=2, column=0, sticky=W, pady=10)
        Label(frame, text="Recapito (personale):\t "+stringa[4], font=f, bg=background_frame).grid(row=3, column=0, sticky=W, pady=10)
        Label(frame, text="Recapito (lavorativo):\t "+stringa[5].replace(" ",""), font=f, bg=background_frame).grid(row=4, column=0, sticky=W, pady=10)
        Label(frame, text="Reparto:\t\t\t " + stringa[1], font=f, bg=background_frame).grid(row=5, column=0, sticky=W, pady=10)
        Label(frame, text="Studio:\t\t\t "+stringa[6], font=f, bg=background_frame).grid(row=6, column=0, sticky=W, pady=10)
        Label(frame, text=orario, font=f, bg=background_frame).grid(row=7, column=0, sticky=W, pady=10)
        Label(frame, text="Altre informazioni:\t\t"+stringa[8], font=f, bg=background_frame).grid(row=8, column=0, sticky=W, pady=10)


        frame2 = Frame(self, bd = 1, relief = SOLID, padx = 20, pady = 0.2)
        frame2.place(x=50, y=20)
        Label(frame2, text="STATUS:\t ONLINE", font=('Times', 10)).grid(row=0, column=0, sticky=W, pady=10)


        # using for changing health worker style
        btn_modify = Button(self, width = 15, text = 'Modifica Dati Personali', font=f, bg=background_window, command = lambda : controller.show_frame(Mod_Medical),
            activebackground="#3399ff")
        btn_modify.pack()
        btn_modify.place(height=60, width=420, x = 50, y = 750)

        # using for changing health worker style
        btn_add_patient = Button(self, width = 15, text = 'Aggiungi Nuovo Paziente', command = lambda : controller.show_frame(Add_Patient), font=f, bg=background_window,
            activebackground="#3399ff")
        btn_add_patient.pack()
        btn_add_patient.place(height=60, width=408, x = 700, y = 50)

        # using for changing health worker style
        btn_add_cce_comune = Button(self, width = 15, text = 'Aggiungi Nuova Sezione Comune',  command = lambda : controller.show_frame(Add_CCE_Comune), font=f, bg=background_window,
            activebackground="#3399ff")
        btn_add_cce_comune.pack()
        btn_add_cce_comune.place(height=60, width=408, x = 700, y = 250)

        # using for changing health worker style
        btn_mod_patient = Button(self, width = 15, text = 'Modifica Dati Paziente', font=f, bg=background_window,
            activebackground="#3399ff")
        btn_mod_patient.pack()
        btn_mod_patient.place(height=60, width=408, x = 700, y = 150)

        # using for changing health worker style
        btn_mod_cce_comune = Button(self, width = 15, text = 'Modifica Dati Sezione Comune', font=f, bg=background_window,
            activebackground="#3399ff")
        btn_mod_cce_comune.pack()
        btn_mod_cce_comune.place(height=60, width=408, x = 700, y = 350)

        # using for changing health worker style
        btn_add_cce_specifica = Button(self, width = 15, text = 'Aggiungi Nuova Sezione Specifica', font=f, bg=background_window, command = lambda : controller.show_frame(Add_CCE_Specifica),
            activebackground="#3399ff")
        btn_add_cce_specifica.pack()
        btn_add_cce_specifica.place(height=60, width=408, x = 700, y = 450)

        # using for changing health worker style
        btn_mod_cce_specifica = Button(self, width = 15, text = 'Modifica Dati Sezione Specifica', font=f, bg=background_window,
            activebackground="#3399ff")
        btn_mod_cce_specifica.pack()
        btn_mod_cce_specifica.place(height=60, width=408, x = 700, y = 550)

        # using for changing health worker style
        btn_open = Button(self, width = 15, text = 'Apri Assistente Vocale', font=f, bg=background_window,
            activebackground="#3399ff")
        btn_open.pack()
        btn_open.place(height=60, width=408, x = 700, y = 750)


class Add_Patient(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # There are three frames. They are used for general information (left frame), other information (center) and time schedule (right frame)
        frame = Frame(self, bd = 2, relief = SOLID, padx = 5, pady = 5)
        frame.config(bg = background_frame)

        # position of the frames in the window
        frame.place(x=50, y=50)


        # list of gender option menu
        var_sesso = StringVar()
        sesso = ('Maschio', 'Femmina', 'Altro')
        var_sesso.set(sesso[0]) # default --> first value

        ward = query_sparql.connessione("QUERY_ALL_MEDICAL_STAFF", path)
        global var_ward
        var_ward = StringVar()
        h_ward = ward.replace("_", " ").split("\n")
        i = 0
        while i < len(h_ward):
            h_ward[i] = h_ward[i] + " " + h_ward[i+1]
            i += 2
        i = 0
        del h_ward[1::2]
        h_ward.insert(0, "------")
        var_ward.set(h_ward[0]) # default --> first value

        # declaration of the ward option menu
        global input_ward
        input_ward = OptionMenu(frame, var_ward, *h_ward)
        input_ward["menu"].config(bg=background_frame) # change color
        input_ward.config(width=15, font=f, bg=background_frame, activebackground=background_frame)
        input_ward["highlightthickness"]= 0 # disable the color of the background

        # declaration of the gender option menu
        input_sesso = OptionMenu(frame, var_sesso, *sesso)
        input_sesso["menu"].config(bg=background_frame) # change color
        input_sesso.config(width=15, font=f, bg=background_frame, activebackground=background_frame)
        input_sesso["highlightthickness"]= 0 # disable the color of the background


        # declaration of label for health workers' dates
        Label(frame, text="Nome", font=f, bg=background_frame).grid(row=0, column=0, sticky=W, pady=10)
        Label(frame, text="Cognome", font=f, bg=background_frame).grid(row=1, column=0, sticky=W, pady=10)
        Label(frame, text="Data di Nascita", font=f, bg=background_frame).grid(row=2, column=0, sticky=W, pady=10)
        Label(frame, text="(YYYY/MM/DD)", font=f, bg=background_frame).grid(row=2, column=3, sticky=W, pady=10)
        Label(frame, text="Luogo di Nascita", font=f, bg=background_frame).grid(row=3, column=0, sticky=W, pady=10)
        Label(frame, text="Indirizzo", font=f, bg=background_frame).grid(row=4, column=0, sticky=W, pady=10)
        Label(frame, text="(Via/Piaz./Viale)", font=f, bg=background_frame).grid(row=4, column=3, sticky=W, pady=10)
        Label(frame, text="Residenza", font=f, bg=background_frame).grid(row=5, column=0, sticky=W, pady=10)
        Label(frame, text="Nazionalità", font=f, bg=background_frame).grid(row=6, column=0, sticky=W, pady=10)
        Label(frame, text="Sesso", font=f, bg=background_frame).grid(row=7, column=0, sticky=W, pady=10)
        Label(frame, text="Codice Fiscale", font=f, bg=background_frame).grid(row=8, column=0, sticky=W, pady=10)
        Label(frame, text="Email", font=f, bg=background_frame).grid(row=9, column=0, sticky=W, pady=10)
        Label(frame, text="Recapito Telefonico", font=f, bg=background_frame).grid(row=10, column=0, sticky=W, pady=10)
        Label(frame, text="Medico", font=f, bg=background_frame).grid(row=11, column=0, sticky=W, pady=10)

        # declaration of text box for health workers' dates
        input_nome = Entry(frame, font=f)
        input_cognome = Entry(frame, font=f)
        input_eta = Entry(frame, font=f)
        input_luogo_nascita = Entry(frame, font=f)
        input_address = Entry(frame, font=f)
        input_residenza = Entry(frame, font=f)
        input_nazionalita = Entry(frame, font=f)
        input_cod_fis = Entry(frame, font=f)
        input_email = Entry(frame, font=f)
        input_recapito = Entry(frame, font=f)

        # position of the text box in the left frame
        input_nome.grid(row=0, column=1, pady=10, padx=20)
        input_cognome.grid(row=1, column=1, pady=10, padx=20)
        input_eta.grid(row=2, column=1, pady=10, padx=20)
        input_luogo_nascita.grid(row=3, column=1, pady=10, padx=20)
        input_address.grid(row=4, column=1, pady=10, padx=20)
        input_residenza.grid(row=5, column=1, pady=10, padx=20)
        input_nazionalita.grid(row=6, column=1, pady=10, padx=20)
        input_sesso.grid(row=7, column=1, pady=10, padx=20)
        input_cod_fis.grid(row=8, column=1, pady=10, padx=20)
        input_email.grid(row=9, column=1, pady=10, padx=20)
        input_recapito.grid(row=10, column=1, pady=10, padx=20)
        input_ward.grid(row=11, column=1, pady=10, padx=20)




        # declaration of message box; there are three parametres --> title, text of the message and style (0 for OK, 1 for OK - CANCEl, ...)
        def Mbox(title, text):
            return messagebox.showerror(title=title, message=text, icon = 'error')


        # Does fiscal code already exist in the OWL? And then program uploads dates on OWL
        def check_cod_fis():
            check_result = query_sparql.connessione("QUERY_PATIENT_FISCAL_CODE", path)
            # check if fiscal code already exists
            if input_cod_fis.get().upper() in check_result:
                Mbox('Attenzione!', "L'utente già esiste")
            else:
                force = { "fiscalCode": input_cod_fis.get().upper().replace(" ","_")}
                # SPARQL insert fiscal codice
                query_sparql.insert_one("INSERT_PATIENT_FISCAL_CODE", path, force)
                # SPARQL insert other datas
                force = {"fiscalCode": input_cod_fis.get().upper().replace(" ",""),
                    "givenName": input_nome.get().upper().replace(" ","_"),
                    "familyName": input_cognome.get().upper().replace(" ","_"),
                    "birthDate": input_eta.get() + "T00:00:00",
                    "gender": var_sesso.get(),
                    "email": input_email.get().lower(),
                    "nation": input_nazionalita.get().upper(),
                    "phoneNumber": input_recapito.get(),
                    "address": input_address.get().replace("'"," "),
                    "birthPlace": input_luogo_nascita.get().upper(),
                    "residence": input_residenza.get().upper()}
                query_sparql.insert_one("INSERT_PATIENT", path, force)


        # check all inputs when technician click on the button
        def controllo():
            # check name and surname
            if (len(input_nome.get()) == 0):
                Mbox('Attenzione!', 'Nome non valido.')
                return
            if (len(input_cognome.get()) == 0):
                Mbox('Attenzione!', 'Cognome non valido.')
                return
            # check birth date
            isValidDate = True
            try:
                year,month,day = input_eta.get().split('/') # it gets the current day
                if len(year) != 4:
                    isValidDate = False
                a = datetime.datetime(int(year),int(month),int(day))
                b = datetime.date.today()
                if (b - a.date()).days == 0 or (b - a.date()).days < 0: # health worker must be over 18yo (365 days * 18)
                    isValidDate = False
            except ValueError:
                isValidDate = False
            if not (isValidDate):
                Mbox('Attenzione!', 'La data di nascita non è valida.')
                return
            # check birth place
            if input_luogo_nascita.get() == "":
                Mbox('Attenzione!', 'Il luogo di nascita inserito non è corretto.')
                return
            # check address
            if input_address.get() == "":
                Mbox('Attenzione!', "L'indirizzo inserito non è corretto.")
                return
            # check residence
            if input_residenza.get() == "":
                Mbox('Attenzione!', "La residenza inserita non è corretta.")
                return
            # check nationality
            if input_nazionalita.get() == "":
                Mbox('Attenzione!', "La nazionalità inserita non è corretta.")
                return
            # check fiscal code
            if not codicefiscale.is_valid(input_cod_fis.get().replace(" ", "")):
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
            stringa = stringa + '\n' + input_nome.get().upper() + '\n'+ input_cognome.get().upper() + "\n" + input_eta.get() + '\n' + input_luogo_nascita.get().upper() + "\n" + input_address.get() + "\n" + input_residenza.get() + "\n" + var_sesso.get()
            stringa = stringa + '\n' + input_nazionalita.get() + "\n" + input_cod_fis.get().upper() + '\n' + input_email.get().lower() + "\n" + input_recapito.get() + "\n"

            result = messagebox.askquestion("Attenzione...", stringa, icon = 'question')
            if result == 'yes':
                    check_cod_fis() # Does fiscal code already exist in the OWL? And then program uploads dates on OWL
            else:
                pass


        # declaration of the button "create patient"
        btn_crea = Button(self, width = 15, text = 'Crea', font=f, bg=background_window, command = controllo,
            activebackground="#3399ff")
        btn_crea.pack()
        btn_crea.place(height=60, width=400, x = 750, y = 300)

        # declaration of the button "indietro"
        btn_indietro = Button(self, width = 15, text = 'Indietro', font=f, command = lambda : controller.show_frame(MainPage),
            bg=background_window, activebackground="#3399ff")
        btn_indietro.pack()
        btn_indietro.place(height=60, width=400, x = 750, y = 580)





class Add_CCE_Comune(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)


        # There are three frames. They are used for general information (left frame), other information (center) and time schedule (right frame)
        frame = Frame(self, bd = 2, relief = SOLID, padx = 5, pady = 5)
        frame.config(bg = background_frame)
        frame2 = Frame(self, bd = 2, relief = SOLID, padx = 20, pady = 15)
        frame2.config(bg = background_frame)
        frame3 = Frame(self, bd = 2, relief = SOLID, padx = 20, pady = 15)
        frame3.config(bg = background_frame)
        frame4 = Frame(self, bd = 2, relief = SOLID, padx = 20, pady = 15)
        frame4.config(bg = background_frame)
        frame5 = Frame(self, bd = 2, relief = SOLID, padx = 20, pady = 15)
        frame5.config(bg = background_frame)

        # position of the frames in the window
        frame.place(x=50, y=50)
        frame2.place(x=450, y=50)
        frame3.place(x=880, y=50)
        frame4.place(x=450, y=450)
        frame5.place(x=880, y=450)


        # list of role option menu
        var_blood = StringVar()
        blood = ('O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+')
        var_blood.set(blood[0]) # default --> first value

        # declaration of the role option menu
        input_blood = OptionMenu(frame, var_blood, *blood)
        input_blood["menu"].config(bg=background_frame) # change color
        input_blood.config(width=15, font=f, bg=background_frame, activebackground=background_frame)
        input_blood["highlightthickness"]= 0 # disable the color of the background


        # declaration of label and text box for further information
        Label(frame2, text = 'Patologie in atto:', font=f, bg = background_frame).pack(pady=5)
        txt_malattie = Text(frame2, height = 14, width = 40,font = f)
        txt_malattie.pack()

        # declaration of label and text box for time schedule
        Label(frame3, text = 'Terapia Continuativa:', font=f, bg = background_frame).pack(pady=5)
        txt_terapia = Text(frame3, height = 14, width = 40,font = f)
        txt_terapia.pack()


        Label(frame4, text = 'Allergie Note:', font=f, bg = background_frame).pack(pady=5)
        txt_allergie = Text(frame4, height = 14, width = 40,font = f)
        txt_allergie.pack()

        # declaration of label and text box for time schedule
        Label(frame5, text = 'Riassunto Paziente:', font=f, bg = background_frame).pack(pady=5)
        txt_resume = Text(frame5, height = 14, width = 40,font = f)
        txt_resume.pack()

        # declaration of label for health workers' dates
        Label(frame, text="Codice Fiscale", font=f, bg=background_frame).grid(row=0, column=0, sticky=W, pady=10)
        Label(frame, text="gruppo Sanguigno", font=f, bg=background_frame).grid(row=1, column=0, sticky=W, pady=10)

        # declaration of text box for health workers' dates
        input_cod_fis = Entry(frame, font=f)

        # position of the text box in the left frame
        input_cod_fis.grid(row=0, column=1, pady=10, padx=20)
        input_blood.grid(row=1, column=1, pady=10, padx=20)

        txt_allergie.insert(END,"Nothing")
        txt_resume.insert(END,"Nothing")
        txt_terapia.insert(END,"Nothing")
        txt_malattie.insert(END,"Nothing")

        # declaration of message box; there are three parametres --> title, text of the message and style (0 for OK, 1 for OK - CANCEl, ...)
        def Mbox(title, text):
            return messagebox.showerror(title=title, message=text, icon = 'error')


        def controllo():
            resultID = query_sparql.connessione("QUERY_ID_CCE_COMUNE", path)
            result_fiscal = query_sparql.connessione("QUERY_PATIENT_FISCAL_CODE", path)
            result_fiscal_cce = query_sparql.connessione("QUERY_CCE_COMUNE_FISCAL_CODE", path)
            if not input_cod_fis.get().upper().replace(" ","") in result_fiscal or input_cod_fis.get() == "":
                Mbox("Attenzione!", "Il codice fiscale non risulta presente nell'ontologia.")
                return
            elif input_cod_fis.get().upper().replace(" ","") in result_fiscal_cce:
                Mbox("Attenzione!", "La sezione comune di questo paziente già esiste.")
                return
            stringa = var_blood.get() + "\n" + txt_malattie.get("1.0", "end-1c") + "\n" + txt_resume.get("1.0", "end-1c") + "\n" + txt_terapia.get("1.0", "end-1c") + "\n" + txt_allergie.get("1.0", "end-1c")
            result = messagebox.askquestion("Attenzione...", "Saranno inviati i seguenti dati:\n" + stringa, icon = 'question')
            if not result == 'yes':
                    return
            ora = query_sparql.connessione("ORA", path)

            force = {"cf": input_cod_fis.get().upper().replace(" ","_"),
                "id": str(int(resultID) + 1),
                "diseas": txt_malattie.get("1.0", "end-1c").replace("ì", "%%").replace("\n", "; ").replace(".", ":").replace(" ","&&"),
                "resume": txt_resume.get("1.0", "end-1c").replace("ì", "%%").replace("\n", "; ").replace(".", ":").replace(" ","&&"),
                "blood": var_blood.get(),
                "terapia": txt_terapia.get("1.0", "end-1c").replace("ì", "%%").replace("\n", "; ").replace(".", ":").replace(" ","&&"),
                "allergie": txt_allergie.get("1.0", "end-1c").replace("ì", "%%").replace("\n", "; ").replace(".", ":").replace(" ","&&"),
                "createFiscalMedical": CF,
                "modFiscalMedical": CF,
                "wardName": var_ward.get(),
                "creation": ora,
                "modify": ora}
            query_sparql.insert_one("INSERT_CCE_COMUNE", path, force)


        # declaration of the button "create patient"
        btn_crea = Button(self, width = 15, text = 'Crea', font=f, bg=background_window, command = controllo,
            activebackground="#3399ff")
        btn_crea.pack()
        btn_crea.place(height=60, width=380, x = 50, y = 300)

        # declaration of the button "indietro"
        btn_indietro = Button(self, width = 15, text = 'Indietro', font=f, command = lambda : controller.show_frame(MainPage),
            bg=background_window, activebackground="#3399ff")
        btn_indietro.pack()
        btn_indietro.place(height=60, width=380, x = 50, y = 400)


class Add_CCE_Specifica(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # There are three frames. They are used for general information (left frame), other information (center) and time schedule (right frame)
        frame = Frame(self, bd = 2, relief = SOLID, padx = 20, pady = 15)
        frame.config(bg = background_frame)
        frame2 = Frame(self, bd = 2, relief = SOLID, padx = 20, pady = 15)
        frame2.config(bg = background_frame)
        frame3 = Frame(self, bd = 2, relief = SOLID, padx = 20, pady = 15)
        frame3.config(bg = background_frame)
        frame4 = Frame(self, bd = 2, relief = SOLID, padx = 20, pady = 15)
        frame4.config(bg = background_frame)
        frame5 = Frame(self, bd = 2, relief = SOLID, padx = 5, pady = 15)
        frame5.config(bg = background_frame)

        # position of the frames in the window
        frame.place(x=20, y=50)
        frame2.place(x=450, y=50)
        frame3.place(x=20, y=450)
        frame4.place(x=450, y=450)
        frame5.place(x=900, y=250)

        ward = query_sparql.connessione("QUERY_WARD", path)
        var_ward = StringVar()
        h_ward = ward.replace("\n","|").split("|")
        var_ward.set(h_ward[0]) # default --> first value
        input_ward = OptionMenu(frame5, var_ward, *h_ward)
        input_ward["menu"].config(bg=background_frame) # change color
        input_ward.config(width=15, font=f, bg=background_frame, activebackground=background_frame)
        input_ward["highlightthickness"]= 0 # disable the color of the background
        Label(frame5, text = 'Reparto:', font=f, bg = background_frame).grid(row=3, column=0, pady=10, padx=20)
        input_ward.grid(row=3, column=1, pady=10, padx=20)


        # declaration of label and text box for further information
        Label(frame, text = 'Diagnosi (ICD9-CM):', font=f, bg = background_frame).pack(pady=5)
        txt_diagn = Text(frame, height = 14, width = 40,font = f)
        txt_diagn.pack()

        # declaration of label and text box for time schedule
        Label(frame2, text = 'Esami effettuati:', font=f, bg = background_frame).pack(pady=5)
        txt_esami = Text(frame2, height = 14, width = 40,font = f)
        txt_esami.pack()

        # declaration of label and text box for further information
        Label(frame3, text = 'Piano di cura:', font=f, bg = background_frame).pack(pady=5)
        txt_piano = Text(frame3, height = 14, width = 40,font = f)
        txt_piano.pack()

        # declaration of label and text box for time schedule
        Label(frame4, text = 'Lettera di Dimissione:', font=f, bg = background_frame).pack(pady=5)
        txt_dimissione = Text(frame4, height = 14, width = 40,font = f)
        txt_dimissione.pack()

        # declaration of label and text box for time schedule
        Label(frame5, text = 'Codice Fiscale:', font=f, bg = background_frame).grid(row=0, column=0, sticky=W, pady=10)
        input_cod_fis = Entry(frame5, font=f)
        input_cod_fis.grid(row=0, column=1, pady=10, padx=20)

        txt_diagn.insert(END,"Nothing")
        txt_esami.insert(END,"Nothing")
        txt_piano.insert(END,"Nothing")
        txt_dimissione.insert(END,"Nothing")


        # declaration of message box; there are three parametres --> title, text of the message and style (0 for OK, 1 for OK - CANCEl, ...)
        def Mbox(title, text):
            return messagebox.showerror(title=title, message=text, icon = 'error')

        def controllo():
            resultID = query_sparql.connessione("QUERY_ID_CCE_SPECIFICA", path)
            result_fiscal = query_sparql.connessione("QUERY_PATIENT_FISCAL_CODE", path)
            result_fiscal_cce_comune = query_sparql.connessione("QUERY_CCE_COMUNE_FISCAL_CODE", path)

            if not input_cod_fis.get().upper().replace(" ","") in result_fiscal or input_cod_fis.get() == "":
                Mbox("Attenzione!", "Il codice fiscale non risulta presente nell'ontologia.")
                return
            if not input_cod_fis.get().upper().replace(" ","") in result_fiscal_cce_comune:
                Mbox("Attenzione!", "Non risulta presente una sezione socio sanitaria comune di tale paziente.")
                return

            stringa = txt_diagn.get("1.0", "end-1c") + "\n" + txt_esami.get("1.0", "end-1c") + "\n" + txt_piano.get("1.0", "end-1c") + "\n" + txt_dimissione.get("1.0", "end-1c")
            result = messagebox.askquestion("Attenzione...", "Saranno inviati i seguenti dati: \n" + stringa, icon = 'question')
            if not result == 'yes':
                    return
            diagnosi = txt_diagn.get("1.0", "end-1c").replace(" ","").replace(";","").split("\n")
            for i in range(len(diagnosi)):
                check = icd9_package.search_diagn(diagnosi[i])
                if check == None:
                    Mbox("Attenzione!", "Il codice ICD9-CM inserito nella riga " + str(i+1) + " non risulta valido.")
                    return
            ora = query_sparql.connessione("ORA", path)
            force = {"cf": input_cod_fis.get().upper().replace(" ","_"),
                "idSpec": str(int(resultID) + 1),
                "plan": txt_piano.get("1.0", "end-1c").replace("ì", "%%").replace("\n", "; ").replace(".", ":").replace(" ","&&"),
                "exam": txt_esami.get("1.0", "end-1c").replace("ì", "%%").replace("\n", "; ").replace(".", ":").replace(" ","&&"),
                "dimission": txt_dimissione.get("1.0", "end-1c").replace("ì", "%%").replace("\n", "; ").replace(".", ":").replace(" ","&&"),
                "createFiscalMedical": CF,
                "modFiscalMedical": CF,
                "wardName": var_ward.get(),
                "creation": ora,
                "modify": ora}
            query_sparql.insert_one("INSERT_CCE_SPECIFICA", path, force)
            for i in range(len(diagnosi)):
                force = {"fiscalCode": input_cod_fis.get().upper().replace(" ","_"),
                "diagn": str(diagnosi[i]),
                "idSpec": str(int(resultID) + 1)}
                query_sparql.insert_one("INSERT_DIAGNOSI", path, force)
            # "diagn": txt_diagn.get("1.0", "end-1c").replace(" ","").replace("\n", ";"),


        # declaration of the button "create patient"
        btn_crea = Button(self, width = 15, text = 'Crea', font=f, bg=background_window, command = controllo,
            activebackground="#3399ff")
        btn_crea.pack()
        btn_crea.place(height=60, width=370, x = 900, y = 600)

        # declaration of the button "indietro"
        btn_indietro = Button(self, width = 15, text = 'Indietro', font=f, command = lambda : controller.show_frame(MainPage),
            bg=background_window, activebackground="#3399ff")
        btn_indietro.pack()
        btn_indietro.place(height=60, width=370, x = 900, y = 760)



class Mod_Medical(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)


        # There are three frames. They are used for general information (left frame), other information (center) and time schedule (right frame)
        frame = Frame(self, bd = 2, relief = SOLID, padx = 5, pady = 5)
        frame.config(bg = background_frame)
        frame2 = Frame(self, bd = 2, relief = SOLID, padx = 20, pady = 15)
        frame2.config(bg = background_frame)
        frame3 = Frame(self, bd = 2, relief = SOLID, padx = 20, pady = 15)
        frame3.config(bg = background_frame)
        frame4 = Frame(self, bd = 2, relief = SOLID, padx = 20, pady = 15)
        frame4.config(bg = background_frame)


        # position of the frames in the window
        frame.place(x=50, y=150)
        frame2.place(x=650, y=50)
        frame3.place(x=1130, y=50)
        frame4.place(x=50, y=50)


        # connecting to OWL with SEPA module
        ward = query_sparql.connessione("QUERY_WARD", path)


        # list of gender option menu
        var_sesso = StringVar()
        sesso = ('Maschio', 'Femmina', 'Altro')
        var_sesso.set(sesso[0]) # default --> first value

        # list of ward option menu
        global var_ward
        var_ward = StringVar()
        h_ward = ward.replace("\n","|").split("|")
        var_ward.set(h_ward[0]) # default --> first value

        # list of role option menu
        var_ruolo = StringVar()
        ruolo = ('Doctor', 'Head Physician')
        var_ruolo.set(ruolo[0]) # default --> first value

        # declaration of the gender option menu
        input_sesso = OptionMenu(frame, var_sesso, *sesso)
        input_sesso["menu"].config(bg=background_frame) # change color
        input_sesso.config(width=15, font=f, bg=background_frame, activebackground=background_frame)
        input_sesso["highlightthickness"]= 0 # disable the color of the background

        # declaration of the ward option menu
        global input_ward
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
        text_area = Text(frame2, height = 14, width = 40,font = f)
        text_area.pack()

        # declaration of label and text box for time schedule
        Label(frame3, text = 'Orario:', font=f, bg = background_frame).pack(pady=5)
        time_schedule = Text(frame3, height = 14, width = 40,font = f)
        time_schedule.pack()

        Label(frame4, text="Codice Fiscale", font=f, bg=background_frame).grid(row=1, column=0, sticky=W, pady=10)
        input_cod_fis = Entry(frame4, font=f)
        input_cod_fis.grid(row=1, column=1, pady=10, padx=20)

        # declaration of label for health workers' dates
        Label(frame, text="Nome", font=f, bg=background_frame).grid(row=0, column=0, sticky=W, pady=10)
        Label(frame, text="Cognome", font=f, bg=background_frame).grid(row=1, column=0, sticky=W, pady=10)
        Label(frame, text="Data di Nascita", font=f, bg=background_frame).grid(row=2, column=0, sticky=W, pady=10)
        Label(frame, text="(YYYY/MM/DD)", font=f, bg=background_frame).grid(row=2, column=3, sticky=W, pady=10)
        Label(frame, text="Luogo di Nascita", font=f, bg=background_frame).grid(row=3, column=0, sticky=W, pady=10)
        Label(frame, text="Indirizzo", font=f, bg=background_frame).grid(row=4, column=0, sticky=W, pady=10)
        Label(frame, text="(Via/Piaz./Viale)", font=f, bg=background_frame).grid(row=4, column=3, sticky=W, pady=10)
        Label(frame, text="Sesso", font=f, bg=background_frame).grid(row=5, column=0, sticky=W, pady=10)

        Label(frame, text="Email", font=f, bg=background_frame).grid(row=7, column=0, sticky=W, pady=10)
        Label(frame, text="(personale)", font=f, bg=background_frame).grid(row=7, column=3, sticky=W, pady=10)
        Label(frame, text="Email", font=f, bg=background_frame).grid(row=8, column=0, sticky=W, pady=10)
        Label(frame, text="(lavorativa)", font=f, bg=background_frame).grid(row=8, column=3, sticky=W, pady=10)
        Label(frame, text="Recapito Telefonico", font=f, bg=background_frame).grid(row=9, column=0, sticky=W, pady=10)
        Label(frame, text="(personale)", font=f, bg=background_frame).grid(row=9, column=3, sticky=W, pady=10)
        Label(frame, text="Recapito Telefonico", font=f, bg=background_frame).grid(row=10, column=0, sticky=W, pady=10)
        Label(frame, text="(lavorativo)", font=f, bg=background_frame).grid(row=10, column=3, sticky=W, pady=10)
        Label(frame, text="Numero Studio", font=f, bg=background_frame).grid(row=11, column=0, sticky=W, pady=10)
        Label(frame, text="Reparto", font=f, bg=background_frame).grid(row=12, column=0, sticky=W, pady=10)
        Label(frame, text="Ruolo", font=f, bg=background_frame).grid(row=13, column=0, sticky=W, pady=10)

        # declaration of text box for health workers' dates
        input_nome = Entry(frame, font=f)
        input_cognome = Entry(frame, font=f)
        input_eta = Entry(frame, font=f)
        input_luogo_nascita = Entry(frame, font=f)
        input_address = Entry(frame, font=f)

        input_email = Entry(frame, font=f)
        input_email_lavorativa = Entry(frame, font=f)
        input_recapito = Entry(frame, font=f)
        input_recapito_lavorativo = Entry(frame, font=f)
        input_studio = Entry(frame, font=f)

        # position of the text box in the left frame
        input_nome.grid(row=0, column=1, pady=10, padx=20)
        input_cognome.grid(row=1, column=1, pady=10, padx=20)
        input_eta.grid(row=2, column=1, pady=10, padx=20)
        input_luogo_nascita.grid(row=3, column=1, pady=10, padx=20)
        input_address.grid(row=4, column=1, pady=10, padx=20) # -->
        input_sesso.grid(row=5, column=1, pady=10, padx=20)

        input_email.grid(row=7, column=1, pady=10, padx=20) # -->
        input_email_lavorativa.grid(row=8, column=1, pady=10, padx=20) # -->
        input_recapito.grid(row=9, column=1, pady=10, padx=20) # -->
        input_recapito_lavorativo.grid(row=10, column=1, pady=10, padx=20) # -->
        input_studio.grid(row=11, column=1, pady=10, padx=20) # -->
        input_ward.grid(row=12, column=1, pady=10, padx=20) # -->
        input_ruolo.grid(row=13, column=1, pady=10, padx=20) # -->

        # declaration of message box; there are three parametres --> title, text of the message and style (0 for OK, 1 for OK - CANCEl, ...)
        def Mbox(title, text):
            return messagebox.showerror(title=title, message=text, icon = 'error')

        def start():
            input_nome.configure(state="normal")
            input_cognome.configure(state="normal")
            input_eta.configure(state="normal")
            input_luogo_nascita.configure(state="normal")
            input_address.configure(state="normal")
            input_sesso.configure(state="normal")
            input_email.configure(state="normal")
            input_email_lavorativa.configure(state="normal")
            input_recapito.configure(state="normal")
            input_recapito_lavorativo.configure(state="normal")
            input_studio.configure(state="normal")
            input_ward.configure(state="normal")
            input_ruolo.configure(state="normal")
            text_area.configure(state="normal")
            time_schedule.configure(state="normal")

            input_nome.delete(0, "end")
            input_cognome.delete(0, "end")
            input_eta.delete(0, "end")
            input_luogo_nascita.delete(0, "end")
            input_address.delete(0, "end")
            input_email.delete(0, "end")
            input_email_lavorativa.delete(0, "end")
            input_recapito.delete(0, "end")
            input_recapito_lavorativo.delete(0, "end")
            input_studio.delete(0, "end")
            text_area.delete("1.0","end")
            time_schedule.delete("1.0","end")

            input_nome.configure(state="disabled")
            input_cognome.configure(state="disabled")
            input_eta.configure(state="disabled")
            input_luogo_nascita.configure(state="disabled")
            input_address.configure(state="disabled")
            input_sesso.configure(state="disabled")
            input_email.configure(state="disabled")
            input_email_lavorativa.configure(state="disabled")
            input_recapito.configure(state="disabled")
            input_recapito_lavorativo.configure(state="disabled")
            input_studio.configure(state="disabled")
            input_ward.configure(state="disabled")
            input_ruolo.configure(state="disabled")
            text_area.configure(state="disabled")
            time_schedule.configure(state="disabled")




        def popola(text):
            input_cod_fis.configure(state="disabled")

            input_nome.configure(state="normal")
            input_nome.insert(END, text[2])
            input_nome.configure(state="disabled")

            input_cognome.configure(state="normal")
            input_cognome.insert(END, text[3])
            input_cognome.configure(state="disabled")

            input_eta.configure(state="normal")
            input_eta.insert(END, text[5].replace("T00:00:00",""))
            input_eta.configure(state="disabled")

            input_luogo_nascita.configure(state="normal")
            input_luogo_nascita.insert(END, text[6])
            input_luogo_nascita.configure(state="disabled")

            input_address.configure(state="normal")
            input_address.insert(END, text[8])

            input_sesso.configure(state="normal")
            var_sesso.set(text[4])

            input_email.configure(state="normal")
            input_email.insert(END, text[9])

            input_email_lavorativa.configure(state="normal")
            input_email_lavorativa.insert(END, text[10])

            input_recapito.configure(state="normal")
            input_recapito.insert(END, text[11])

            input_recapito_lavorativo.configure(state="normal")
            input_recapito_lavorativo.insert(END, text[12].replace(" ",""))

            input_studio.configure(state="normal")
            input_studio.insert(END, text[13])

            input_ward.configure(state="normal")
            var_ward.set(text[15])

            input_ruolo.configure(state="normal")
            var_ruolo.set(text[14])

            text_area.configure(state="normal")
            text_area.insert(END, text[16])

            time_schedule.configure(state="normal")
            time_schedule.insert(END, text[7].replace("; ","\n"))


        def modifica():
            if input_cod_fis.cget("state") == "disabled":
                result = messagebox.askquestion("Attenzione...", "Confermi?", icon = 'question')
                if result != 'yes':
                    return
                force = { "fiscalCode": input_cod_fis.get().upper().replace(" ","_")}
                # SPARQL insert fiscal codice
                query_sparql.insert_one("INSERT_MEDICAL_STAFF_FISCAL_CODE", path, force)
                phone = input_recapito_lavorativo.get()
                phone = '&'.join(phone[i:i + 1] for i in range(0, len(phone)))
                # SPARQL insert other datas
                force = {"fiscalCode": input_cod_fis.get().upper().replace(" ","_"),
                    "givenName": input_nome.get().upper().replace(" ","_"),
                    "familyName": input_cognome.get().upper().replace(" ","_"),
                    "birthDate": input_eta.get() + "T00:00:00",
                    "gender": var_sesso.get(),
                    "email": input_email.get().lower(),
                    "workMail": input_email_lavorativa.get().lower(),
                    "phoneNumber": input_recapito.get(),
                    "workPhone": phone,
                    "wardName": var_ward.get(),
                    "role": var_ruolo.get(),
                    "address": input_address.get().replace("'"," ").replace(" ","&&"),
                    "birthPlace": input_luogo_nascita.get().upper(),
                    "otherWorker": text_area.get("1.0", "end-1c"),
                    "studio": input_studio.get().replace(" ", "&&"),
                    "timeSchedule": time_schedule.get("1.0", "end-1c").replace("ì", "%%").replace("\n", "; ").replace(".", ":").replace(" ","&&")}
                query_sparql.insert_one("INSERT_MEDICAL_STAFF", path, force)
                start()
                input_cod_fis.configure(state="normal")
                input_cod_fis.delete(0, "end")
                return

            check_result = query_sparql.connessione("QUERY_MEDICAL_STAFF_FISCAL_CODE", path)
            # check if fiscal code already exists
            if not input_cod_fis.get().upper() in check_result or input_cod_fis.get().upper() == "":
                Mbox('Attenzione!', "Codice fiscale non valido")
            else:
                stringa = '"SELECT * WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/Medical_Staff> {?h rdf:type sha:Medical_Staff ; sha:fiscalCode ?cf ; sha:givenName ?name ; sha:familyName ?surname ; sha:gender ?gender ; sha:birthDate ?d ; sha:birthPlace ?p ; sha:timeSchedule ?time ; sha:address ?address ; sha:email ?email ; sha:emailWork ?wMail ; sha:phoneNumber ?phone ; sha:phoneNumberWork ?wPhone ; sha:studio ?studio ; sha:role ?role ; sha:wardName ?wardName ; sha:otherWorker ?other . '
                stringa = stringa + "FILTER (regex (?cf, '" + input_cod_fis.get().upper() + "'))}}" + '"'
                name_query = '"QUERY"'
                stringa = name_query + ': { "sparql": ' + stringa + '}'
                stringa = create_sparql.creating(path_new, stringa)
                stringa = stringa.replace("%%", "ì").replace("&&"," ").replace("&"," ").split("\n")
                popola(stringa)

        # declaration of the button "create patient"
        btn_modifica = Button(self, width = 15, text = 'Modifica', font=f, bg=background_window, command = modifica,
            activebackground="#3399ff")
        btn_modifica.pack()
        btn_modifica.place(height=60, width=370, x = 1100, y = 600)

        # declaration of the button "indietro"
        btn_indietro = Button(self, width = 15, text = 'Indietro', font=f, command = lambda : controller.show_frame(MainPage),
            bg=background_window, activebackground="#3399ff")
        btn_indietro.pack()
        btn_indietro.place(height=60, width=370, x = 1100, y = 760)


        start()

# Main code
app = tkinterApp()
app.title('Tesi Di Tuccio -- Medical Staff')
app.geometry('1600x900')
app.resizable(width=False, height=False)
app.mainloop()

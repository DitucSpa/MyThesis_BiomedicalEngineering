# TECHNICIAN.PY
# This is a form - tkinter program for technicians who insert new medical staff on OWL (Protegé file).
# Technicians must insert: name, fiscal code, birth date and others.
# When technicians click on the button, the program check all the inputs.
# It uses SEPA (https://github.com/arces-wot/SEPABins).
# Note: some information are in italian.
# Technician can also add a new hospital ward or starting the vocal assistance
# Internet page of "how to switch page" --> https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/


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


# other declarations
f = ('Times', 14) # the font of the program
background_frame = "#80b3ff" # background of the frame
background_window = "#b3ccff" # background of the window
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' # it's used for checking email
path = r"C:\Users\Ovettino\Downloads\GitHub\MyThesis_BiomedicalEngineering\JSAP\TesiProva.jsap" # path of JSAP file


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
        for F in (StartPage, Add_Ward):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
            self.currentFrame = None
        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()




# this is the start page of the technician --> he can add new doctor, test vocal assistance or add a new ward
class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # There are three frames. They are used for general information (left frame), other information (center) and time schedule (right frame)
        frame = Frame(self, bd = 2, relief = SOLID, padx = 5, pady = 5)
        frame.config(bg = background_frame)
        frame2 = Frame(self, bd = 2, relief = SOLID, padx = 20, pady = 15)
        frame2.config(bg = background_frame)
        frame3 = Frame(self, bd = 2, relief = SOLID, padx = 20, pady = 15)
        frame3.config(bg = background_frame)

        # position of the frames in the window
        frame.place(x=50, y=50)
        frame2.place(x=650, y=50)
        frame3.place(x=1130, y=50)


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


        # declaration of label for health workers' dates
        Label(frame, text="Nome", font=f, bg=background_frame).grid(row=0, column=0, sticky=W, pady=10)
        Label(frame, text="Cognome", font=f, bg=background_frame).grid(row=1, column=0, sticky=W, pady=10)
        Label(frame, text="Data di Nascita", font=f, bg=background_frame).grid(row=2, column=0, sticky=W, pady=10)
        Label(frame, text="(YYYY/MM/DD)", font=f, bg=background_frame).grid(row=2, column=3, sticky=W, pady=10)
        Label(frame, text="Luogo di Nascita", font=f, bg=background_frame).grid(row=3, column=0, sticky=W, pady=10)
        Label(frame, text="Indirizzo", font=f, bg=background_frame).grid(row=4, column=0, sticky=W, pady=10)
        Label(frame, text="(Via/Piaz./Viale)", font=f, bg=background_frame).grid(row=4, column=3, sticky=W, pady=10)
        Label(frame, text="Sesso", font=f, bg=background_frame).grid(row=5, column=0, sticky=W, pady=10)
        Label(frame, text="Codice Fiscale", font=f, bg=background_frame).grid(row=6, column=0, sticky=W, pady=10)
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
        input_cod_fis = Entry(frame, font=f)
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
        input_address.grid(row=4, column=1, pady=10, padx=20)
        input_sesso.grid(row=5, column=1, pady=10, padx=20)
        input_cod_fis.grid(row=6, column=1, pady=10, padx=20)
        input_email.grid(row=7, column=1, pady=10, padx=20)
        input_email_lavorativa.grid(row=8, column=1, pady=10, padx=20)
        input_recapito.grid(row=9, column=1, pady=10, padx=20)
        input_recapito_lavorativo.grid(row=10, column=1, pady=10, padx=20)
        input_studio.grid(row=11, column=1, pady=10, padx=20)
        input_ward.grid(row=12, column=1, pady=10, padx=20)
        input_ruolo.grid(row=13, column=1, pady=10, padx=20)


        # declaration of message box; there are three parametres --> title, text of the message and style (0 for OK, 1 for OK - CANCEl, ...)
        def Mbox(title, text):
            return messagebox.showerror(title=title, message=text, icon = 'error')


        # Does fiscal code already exist in the OWL? And then program uploads dates on OWL
        def check_cod_fis():
            check_result = query_sparql.connessione("QUERY_MEDICAL_STAFF_FISCAL_CODE", path)
            # check if fiscal code already exists
            if input_cod_fis.get().upper() in check_result:
                Mbox('Attenzione!', "L'utente già esiste")
            else:
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
                if (b - a.date()).days == 0 or (b - a.date()).days < 0 or (b - a.date()).days < 365 * 18: # health worker must be over 18yo (365 days * 18)
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
            # check fiscal code
            if len(input_cod_fis.get().replace(" ", "")) != 16:
                Mbox('Attenzione!', 'Il codice fiscale inserito non è corretto.')
                return
            # check email
            if not (re.fullmatch(regex, input_email.get())) or not (re.fullmatch(regex, input_email_lavorativa.get())):
                Mbox('Attenzione!', 'La mail inserita non è valida.')
                return
            # check phone number
            if not (input_recapito.get().isnumeric()) or not (input_recapito_lavorativo.get().isnumeric()):
                Mbox('Attenzione!', 'Numero di telefono non valido.')
                return

            # message box with all parametres
            stringa = 'I seguenti dati sono corretti?\n'
            stringa = stringa + '\n' + input_nome.get().upper() + '\n'+ input_cognome.get().upper() + "\n" + input_eta.get() + '\n' + input_luogo_nascita.get().upper() + "\n" + input_address.get() + "\n" + var_sesso.get()
            stringa = stringa + '\n' + input_cod_fis.get().upper() + '\n' + input_email.get().lower() + '\n'+ input_email_lavorativa.get().lower() + "\n" + input_recapito.get() + "\n" + input_recapito_lavorativo.get()
            stringa = stringa + '\n' + input_studio.get() + "\n" + var_ward.get() + '\n' + var_ruolo.get() + '\n' + '\n' + text_area.get("1.0", "end-1c") + "\n" + time_schedule.get("1.0", "end-1c")

            result = messagebox.askquestion("Attenzione...", stringa, icon = 'question')
            if result == 'yes':
                    check_cod_fis() # Does fiscal code already exist in the OWL? And then program uploads dates on OWL
            else:
                pass


        # technician can open the patient vocal assistance for testing it
        def open_assistance():
            import assistente_vocale_paziente_v1 # import the assistance, but this line won't close this page


        def reload():
            global input_ward
            input_ward['menu'].delete(0, 'end')
            global var_ward
            reparto = query_sparql.connessione("QUERY_WARD", path)
            var_ward = StringVar()
            h_ward = reparto.replace("\n","|").split("|")
            var_ward.set(h_ward[0]) # default --> first value
            input_ward = OptionMenu(frame, var_ward, *h_ward)
            input_ward["menu"].config(bg=background_frame) # change color
            input_ward.config(width=15, font=f, bg=background_frame, activebackground=background_frame)
            input_ward["highlightthickness"]= 0 # disable the color of the background
            input_ward.grid(row=12, column=1, pady=10, padx=20)


        # declaration of the button "create health worker"
        btn_crea = Button(self, width = 15, text = 'Crea', font=f, bg=background_window, command = controllo,
            activebackground="#3399ff")
        btn_crea.pack()
        btn_crea.place(height=80, width=408, x = 885, y = 450)

        # declaration of the button "start vocal assistance"
        btn_vocal_patient = Button(self, width = 15, text = 'Assistente Vocale -- Paziente', command = open_assistance, font=f, bg=background_window,
            activebackground="#3399ff")
        btn_vocal_patient.pack()
        btn_vocal_patient.place(height=60, width=408, x = 650, y = 680)

        # declaration of the button "start vocal assistance"
        btn_vocal_staff = Button(self, width = 15, text = 'Assistente Vocale -- Health Worker', command = open_assistance, font=f, bg=background_window,
            activebackground="#3399ff")
        btn_vocal_staff.pack()
        btn_vocal_staff.place(height=60, width=408, x = 1130, y = 680)

        # declaration of the button "add ward"
        btn_add_ward = Button(self, width = 15, text = 'Aggiungi Reparto', command = lambda : controller.show_frame(Add_Ward), font=f, bg=background_window,
            activebackground="#3399ff")
        btn_add_ward.pack()
        btn_add_ward.place(height=60, width=408, x = 1130, y = 600)

        # using for reloading wards
        btn_reloading = Button(self, width = 15, text = 'Ricarica Pagina', command = reload, font=f, bg=background_window,
            activebackground="#3399ff")
        btn_reloading.pack()
        btn_reloading.place(height=60, width=408, x = 650, y = 600)


# this is a page used for adding new hospital wards
class Add_Ward(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # There are two frames. They are used for general information (left frame) and others (right frame)
        frame1 = Frame(self, bd = 2, relief = SOLID, padx = 5, pady = 5)
        frame1.config(bg = background_frame)
        frame2 = Frame(self, bd = 2, relief = SOLID, padx = 20, pady = 15)
        frame2.config(bg = background_frame)

        # position of the frames
        frame1.place(x=50, y=50)
        frame2.place(x=650, y=50)

        global query

        # declaration of label for all wards in frame 2
        label_query = Label(frame2, text = "", font=f, bg = background_frame) # at fisrt it's empty
        label_query.pack(pady=5)


        # declaration of label for health workers' dates in frame 1
        Label(frame1, text="Aggiungi Reparto", font=f, bg=background_frame).grid(row=0, column=0, sticky=W, pady=10)

        # declaration of text box for health workers' dates
        input_reparto = Entry(frame1, font=f)

        # position of the text box in the left frame
        input_reparto.grid(row=0, column=1, pady=10, padx=20)


        # declaration of message box; there are three parametres --> title, text of the message and style (0 for OK, 1 for OK - CANCEl, ...)
        def Mbox(title, text):
            return messagebox.showerror(title=title, message=text, icon = 'error')


        # Does ward already exist in the OWL? And then program uploads dates on OWL
        def add_reparto():
            if input_reparto.get().upper() == "":
                Mbox('Attenzione!', "Nome non valido")
            elif input_reparto.get().upper().replace(" ", "_") in query:
                Mbox('Attenzione!', "Il nome del reparto risulta già essere presente.")
            else:
                question = messagebox.askquestion("Attenzione...", "Confermi: " + input_reparto.get().upper() + " ?", icon = 'question')
                if question == 'yes':
                    force = {"wardName": input_reparto.get().upper().replace(" ", "_")}
                    query_sparql.insert_one("INSERT_WARD", path, force)
                    update_label()
                    self.update()
                else:
                    pass


        # update of the query label with new results
        def update_label():
            global query
            query = query_sparql.connessione("QUERY_WARD", path)
            query = "Reparti:\n\n" + query
            label_query.configure(text=query)

        # declaration of the button "indietro"
        btn_indietro = Button(self, width = 15, text = 'Indietro', font=f, command = lambda : controller.show_frame(StartPage),
            bg=background_window, activebackground="#3399ff")
        btn_indietro.pack()
        btn_indietro.place(height=60, width=400, x = 50, y = 500)

        # declaration of the button "add ward"
        btn_add_ward = Button(self, width = 15, text = 'Aggiungi Nuovo Reparto', command=add_reparto, font=f, bg=background_window,
            activebackground="#3399ff")
        btn_add_ward.pack()
        btn_add_ward.place(height=60, width=400, x = 600, y = 500)
        update_label()




# Main code
app = tkinterApp()
app.title('Tesi Di Tuccio -- Technician')
app.geometry('1600x850')
app.config(bg = background_window) # --> not working
app.resizable(width=False, height=False)
force = {"fiscalCode": "xxx"}
app.mainloop()
#SELECT ?cf WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/Health_Worker> {?h rdf:type sha:Health_Worker ; sha:fiscalCode ?cf  . FILTER regex (?cf, "^r", "i" )}}
#SELECT ?cf  WHERE {GRAPH <http://unibo.it/ontology/SmartHospitalAssistant/Health_Worker> {?h rdf:type sha:Health_Worker ; sha:fiscalCode ?cf ; sha:givenName ?givenName ; sha:familyName ?familyName . FILTER regex (?givenName, "GIANLUCA", "i" ) . FILTER regex (?familyName, "Di_TUCCIO", "i" ) }}

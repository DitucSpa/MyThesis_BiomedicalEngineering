from tkinter import *
import ctypes
import re
import datetime
from datetime import date

f = ('Times', 14) # font
background_frame = "#80b3ff"
background_window = "#b3ccff"
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' # controllo email, caratteri non validi

# dichiarazione della message box
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


# dichiarazione della window
ws = Tk()
ws.title('Tesi Di Tuccio -- Technician')
ws.geometry('1100x600')
ws.config(bg = background_window)




# dichiarazione delle scelte dell'option menu per sesso
var_sesso = StringVar()
sesso = ('Maschio', 'Femmina', 'Altro')
var_sesso.set(sesso[0])

# dichiarazione delle scelte dell'option menu per ruolo
var_ruolo = StringVar()
ruolo = ('Doctor', 'Head Nurse', 'Head Physician')
var_ruolo.set(ruolo[0])

# realizzazione di due frame: quello a sinistra per le informazioni anagrafiche,
# quello a destra per le informazioni generali (tipo data del certificato, data inizio lavoro)
frame = Frame(ws, bd = 2, relief = SOLID, padx = 5, pady = 5)
frame.config(bg = background_frame)
frame2 = Frame(ws, bd = 2, relief = SOLID, padx = 20, pady = 15)
frame2.config(bg = background_frame)

# dichiarazione della lbl e txt per le informazioni aggiuntive
Label(frame2, text = 'Ulteriori informazioni:', font=f, bg = background_frame).pack(pady=5)
text_area = Text(frame2, height = 13, width = 40,font = f)
text_area.pack()

# dichiarazione delle lbl e txt per le informazioni dell'operatore sanitario
Label(frame, text="Cognome Nome", font=f, bg=background_frame).grid(row=0, column=0, sticky=W, pady=10)
Label(frame, text="Data di Nascita", font=f, bg=background_frame).grid(row=1, column=0, sticky=W, pady=10)
Label(frame, text="(YYYY/MM/DD)", font=f, bg=background_frame).grid(row=1, column=3, sticky=W, pady=10)
Label(frame, text="Sesso", font=f, bg=background_frame).grid(row=2, column=0, sticky=W, pady=10)
Label(frame, text="Codice Fiscale", font=f, bg=background_frame).grid(row=3, column=0, sticky=W, pady=10)
Label(frame, text="Email", font=f, bg=background_frame).grid(row=4, column=0, sticky=W, pady=10)
Label(frame, text="Recapito Telefonico", font=f, bg=background_frame).grid(row=5, column=0, sticky=W, pady=10)
Label(frame, text="Reparto", font=f, bg=background_frame).grid(row=6, column=0, sticky=W, pady=10)
Label(frame, text="Ruolo", font=f, bg=background_frame).grid(row=7, column=0, sticky=W, pady=10)
Label(frame, text="Stanza", font=f, bg=background_frame).grid(row=8, column=0, sticky=W, pady=10)


# dichiarazione delle text box
input_nome_cognome = Entry(frame, font=f)
input_email = Entry(frame, font=f)
input_recapito = Entry(frame, font=f)
input_eta = Entry(frame, font=f)
input_reparto = Entry(frame, font=f)
input_stanza = Entry(frame, font=f)
input_cod_fis = Entry(frame, font=f)

# dichiarazione dell'option meù del sesso
input_sesso = OptionMenu(frame, var_sesso, *sesso)
input_sesso["menu"].config(bg=background_frame) # configura il colore delle scelte
input_sesso.config(width=15, font=f, bg=background_frame, activebackground=background_frame)
input_sesso["highlightthickness"]= 0 # disattiva il bordo attorno all'option menù

# dichiarazione dell'option meù del ruolo
input_ruolo = OptionMenu(frame, var_ruolo, *ruolo)
input_ruolo["menu"].config(bg=background_frame) # configura il colore delle scelte
input_ruolo.config(width=15, font=f, bg=background_frame, activebackground=background_frame)
input_ruolo["highlightthickness"]= 0 # disattiva il bordo attorno all'option menù


# posizione delle text box nel frame di sinistra
input_nome_cognome.grid(row=0, column=1, pady=10, padx=20)
input_eta.grid(row=1, column=1, pady=10, padx=20)
input_sesso.grid(row=2, column=1, pady=10, padx=20)
input_cod_fis.grid(row=3, column=1, pady=10, padx=20)
input_email.grid(row=4, column=1, pady=10, padx=20)
input_recapito.grid(row=5, column=1, pady=10, padx=20)
input_reparto.grid(row=6, column=1, pady=10, padx=20)
input_ruolo.grid(row=7, column=1, pady=10, padx=20)
input_stanza.grid(row=8, column=1, pady=10, padx=20)


frame.place(x=50, y=50)
frame2.place(x=650, y=50)


# quando il tecnico clicca sul btn, si avvia un controllo dei dati
def crea():
    controllo()


# metodo per il controllo dei dati
def controllo():
    # controllo Cognome e Nome
    if (len(input_nome_cognome.get()) == 0):
        Mbox('Attenzione!', 'Cognome e Nome non validi.', 1)
        return
    # controllo della data di nascita
    isValidDate = True
    try:
        year,month,day = input_eta.get().split('/')
        if len(year) != 4:
            isValidDate = False
        a = datetime.datetime(int(year),int(month),int(day))
        b = datetime.date.today()
        if (b - a.date()).days == 0 or (b - a.date()).days < 0 or (b - a.date()).days < 360 * 18:
            isValidDate = False
    except ValueError:
        isValidDate = False
    if not (isValidDate):
        Mbox('Attenzione!', 'La data di nascita non è valida.', 1)
        return
    # controllo codice fiscale
    if len(input_cod_fis.get()) != 16:
        Mbox('Attenzione!', 'Il codice fiscale inserito non è corretto.', 1)
        return
    #controllo email
    if not (re.fullmatch(regex, input_email.get())):
        Mbox('Attenzione!', 'La mail inserita non è valida.', 1)
        return
    # controllo del numero di telefono
    if not (input_recapito.get().isnumeric()):
        Mbox('Attenzione!', 'Numero di telefono non valido.', 1)
        return
    # controllo Reparto e Stanza
    if (len(input_reparto.get()) == 0) or (len(input_stanza.get()) == 0):
        Mbox('Attenzione!', 'Reparto o Stanza non validi.', 1)
        return
    # se tutto va a buon fine, invia i dati
    inviadati()

# i dati che poi devono essere inviati con SPAEQL
def inviadati():
    stringa = 'I dati inviati saranno:\n'
    stringa = stringa + '\n' + input_nome_cognome.get().upper() + '\n' + input_eta.get() + '\n' + var_sesso.get()
    stringa = stringa + '\n' + input_cod_fis.get().upper() + '\n' + input_email.get().lower() + '\n' + input_recapito.get()
    stringa = stringa + '\n' + input_reparto.get() + '\n' + var_ruolo.get() + '\n' + input_stanza.get() + '\n' + text_area.get("1.0", "end-1c")
    Mbox('Allora...', stringa, 1)


# dichiarazione del tasto crea per inserire un nuovo operatore sanitario nell'ontologia
btn_crea = Button(ws, width = 15, text = 'Crea', font=f, command = crea, bg='#4d94ff',
    activebackground="#3399ff")
btn_crea.pack()
btn_crea.place(height=50, width=300, x = 700, y = 450)


ws.mainloop()

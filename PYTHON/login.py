from tkinter import *
import ctypes
import re
import getpass

# dichiarazione della message box
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


background_window = "#b3ccff" # colore dello sfondo della finestra
background_frame = "#80b3ff"
f = ('Times', 14) # font
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' # controllo email, caratteri non validi


ws = Tk()
ws.title('Tesi Di Tuccio -- Login')
ws.geometry('450x300')
ws.config(bg=background_window)


# da completare con SPARQL per il LOGIN
def login_button():
    if not (re.fullmatch(regex, txt_email.get())):
        Mbox('Attenzione!', 'La mail inserita non è valida.', 1)
        return
    # controllo Reparto e Stanza
    if (len(txt_password.get()) == 0):
        Mbox('Attenzione!', 'Password non valida.', 1)
        return
    Mbox('Da completare!', 'Da completare.', 1)


frame = Frame(ws, bd=2, relief=SOLID, padx=20, pady=20)
frame.config(bg=background_frame)
Label(frame, text="Email", bg=background_frame,font=f).grid(row=0, column=0, sticky=W, pady=10)
Label(frame, text="Password", bg=background_frame,font=f).grid(row=1, column=0, pady=10)
txt_email = Entry(frame, font=f)
txt_password = Entry(frame, font=f,show="*")
btn_login = Button(frame, width=15, text='Login', bg='#4d94ff', activebackground="#3399ff",font=f, command=login_button)
txt_email.grid(row=0, column=1, pady=10, padx=20)
txt_password.grid(row=1, column=1, pady=10, padx=20)
btn_login.grid(row=2, column=1, pady=10, padx=20)
frame.place(x=50, y=50)


ws.mainloop()

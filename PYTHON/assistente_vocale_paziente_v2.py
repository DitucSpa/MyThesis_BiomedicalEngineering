# questo assistente vocale verrà in aiuto a tutte quelle persone che non riescono a trovare un dottore, non conoscono il suo contatto,
# non sanno dove si trovi, ecc

#librerie ed import
from tkinter import *
import os
import playsound
import time
from gtts import gTTS
import speech_recognition
import sys
from time import sleep

# variabili globali
f = ('Times', 14) # impostazione del font
ws = Tk() # creazione dell'oggetto tkinter
ws.title('Tesi Di Tuccio -- Assistente Vocale Paziente') # titolo della finestra
ws.geometry('600x300') # dimensione della finestra

nome_assistente = "mario" # nome dell'assistente vocale
nome_chiusura = "chiudi" # parola d'ordine per terminare l'assistente vocale

key_word = ['orari', 'stanza', 'camera', 'orario', 'studio', 'dove', "dov'è", "contatti", "numero", "reparto", "contatto"] # parole chiave per invocare l'ontologia
key_word_lan = [] # implementazione della lingua straniera --> il vettore key_word verrà tradotto nella lingua desiderata
language_it = ["francese", "inglese", "tedesco", "italiano", "spagnolo"]
language_en = ["french", "english", "german", "italian", "spanish"]
language_fr = ["français", "anglais", "allemand", "italien", "espanol"]
language_ge = ["französisch", "englisch", "deutsch", "italienisch", "spanisch"]
language_es = ["francés", "inglés", "alemán", "italiano", "español"]
set_language_label = "français\nenglish\ndeutsch\nitaliano\nespañol"
global language_cont

global language_number
language_number = ['fr', 'en', 'de', 'it', 'es']

# immagine in ASCII
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



def talking_duck():
    duck_label.configure(text=duck_talk)
    vocal_label.configure(text="Ti ascolto...")
    ws.update()


def sleeping_duck():
    duck_label.configure(text=duck_sleep)
    vocal_label.configure(text="")
    ws.update()


# il metodo riceve la frase che deve essere letta ad alta voce dall'assistente
def audio_bot(cosa_dire):
    tts = gTTS(text=cosa_dire, lang=language_number[language_cont]) # si potrebbe implementare una variabile language che può assumere "it", "en", ...
    nome_file_mp3 = "prova.mp3" # crea un file mp3 con la frase da dire, lo riproduce e poi lo cancella immediatamente
    tts.save(nome_file_mp3)
    playsound.playsound(nome_file_mp3)
    os.remove(nome_file_mp3)


def inizio():
    riconoscitore = speech_recognition.Recognizer()
    riconoscitore.energy_threshold = 1100
    riconoscitore.dynamic_energy_threshold = False
    riconoscitore.pause_threshold = 0.5
    with speech_recognition.Microphone() as source:
        riconoscitore.adjust_for_ambient_noise(source, 0.5)
        # print("sono in ascolto")
        kkk = riconoscitore.listen(source, None, 1.5)
    try:
        text = riconoscitore.recognize_google(kkk, language=language_number[language_cont])
        if text.lower() == nome_assistente:
            talking_duck()
            microfono_se_risponde()
            pass
        elif text.lower() == nome_chiusura:
            chiusura = TRUE
            vocal_label.configure(text="Chiusura in corso...")
            ws.update()
            audio_bot("chiusura in corso")
            sys.exit()
            pass
        elif text.lower() != "":
            find_language(text.lower())
    except Exception:
        pass


def find_language(input_language):
    okay = 0
    global language_cont
    while okay == 0:
        cont = 0
        for x in language_it:
            if x in input_language:
                language_cont = cont
                check_language(cont)
                return
            cont = cont + 1
        cont = 0
        for x in language_en:
            if x in input_language:
                language_cont = cont
                check_language(cont)
                return
            cont = cont + 1
        cont = 0
        for x in language_fr:
            if x in input_language:
                language_cont = cont
                check_language(cont)
                return
            cont = cont + 1
        cont = 0
        for x in language_es:
            if x in input_language:
                language_cont = cont
                check_language(cont)
                return
            cont = cont + 1
        cont = 0
        for x in language_ge:
            if x in input_language:
                language_cont = contlanguage_cont = cont
                check_language(cont)
                return
            cont = cont + 1
        okay = 1

def check_language(cont):
    if cont == 0:
        audio_bot(language_fr[cont])
    elif cont == 1:
        audio_bot(language_en[cont])
    elif cont == 2:
        audio_bot(language_ge[cont])
    elif cont == 3:
        audio_bot(language_it[cont])
    elif cont == 4:
        audio_bot(language_es[cont])


def microfono_se_risponde():
    riconoscitore = speech_recognition.Recognizer()
    riconoscitore.energy_threshold = 1100
    riconoscitore.dynamic_energy_threshold = False
    riconoscitore.pause_threshold = 0.5
    with speech_recognition.Microphone() as source:
        riconoscitore.adjust_for_ambient_noise(source)
        audio_bot("Ti ascolto")
        audio = riconoscitore.listen(source)
    try:
        text1 = riconoscitore.recognize_google(audio, language="it-IT")
        user_label.configure(text=text1)
        ws.update()
        if text1.lower() == "cosa sai fare":
            vocal_label.configure(text="Allora, posso aiutarti con:\norario di un Medico;\nstanza, studio o camera di un Medico;\nreparto di un Medico.")
            ws.update()
            audio_bot("Allora, posso aiutarti con:\norario di un Medico;\nstanza, studio o camera di un Medico;\nreparto di un Medico")
        else:
            risposta(text1.lower())
        pass
    except Exception:
        pass


def setting():
    user_label.configure(text="")
    ws.update()
    inizio()
    sleeping_duck()
    setting()


def risposta(input_user):
    for x in key_word:
        if x in input_user:
            audio_bot("inserisci una ontologia")
            break
    else:
        vocal_label.configure(text = "Mi dispiace, non posso aiutarti. \nPer sapere cosa posso fare per te, prova a chiedermi:\n''cosa sai fare?''")
        ws.update()
        audio_bot("mi dispiace, non posso aiutarti. Per sapere cosa posso fare per te, prova a chiedermi, cosa sai fare?")



if __name__ == '__main__':
    language_cont = 3
    duck_label = Label(ws, justify=LEFT, text=duck_sleep)
    duck_label.place(relx = 0.1, rely = 0.1, anchor = 'nw')
    vocal_label = Label(ws, justify=LEFT, text="", font = f)
    vocal_label.place(relx = 0.6, rely = 0.3, anchor = 'center')
    user_label = Label(ws, text="", font = f)
    user_label.place(relx = 0.5, rely = 0.7, anchor = 'center')
    language_label = Label(ws, justify=LEFT, text=set_language_label, font = ('Times', 11))
    language_label.place(relx = 0.2, rely = 0.8, anchor = 'center')
    ws.resizable(False, False)
    ws.after(1000, setting)
    ws.mainloop()

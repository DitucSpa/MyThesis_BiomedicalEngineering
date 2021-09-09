# il software si occupa di aiutare i pazienti che richiedono informazioni

from tkinter import *
import os
import playsound
import time
from gtts import gTTS
import speech_recognition
import sys
from time import sleep


f = ('Times', 14) # font
ws = Tk()
ws.title('Tesi Di Tuccio -- Assistente Vocale Paziente')
ws.geometry('600x300')

nome_assistente = "mario"
nome_chiusura = "chiudi"

key_word = ['orari', 'orario', 'stanza', 'camera', 'studio', "numero di cellulare", "recapito telefonico", "numero di telefono", "email", "reparto", 'dove', "dov'è", 'giorni', 'oggi', 'domani']

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
    tts = gTTS(text=cosa_dire, lang='it') # si potrebbe implementare una variabile language che può assumere "it", "en", ...
    nome_file_mp3 = "prova.mp3" # crea un file mp3 con la frase da dire, lo riproduce e poi lo cancella immediatamente
    tts.save(nome_file_mp3)
    playsound.playsound(nome_file_mp3)
    os.remove(nome_file_mp3)


def inizio():
    riconoscitore = speech_recognition.Recognizer()
    riconoscitore.energy_threshold = 10
    riconoscitore.dynamic_energy_threshold = False
    riconoscitore.pause_threshold = 0.5
    with speech_recognition.Microphone() as source:
        riconoscitore.adjust_for_ambient_noise(source, 0.5)
        # print("sono in ascolto")
        kkk = riconoscitore.listen(source, None, 1.5)
    try:
        text = riconoscitore.recognize_google(kkk, language="it-IT")
        if text.lower() == nome_assistente:
            talking_duck()
            microfono_se_risponde()
        elif text.lower() == nome_chiusura:
            chiusura = TRUE
            vocal_label.configure(text="Chiusura in corso...")
            ws.update()
            audio_bot("chiusura in corso")
            sys.exit()
    except Exception:
        pass


def microfono_se_risponde():
    riconoscitore = speech_recognition.Recognizer()
    riconoscitore.pause_threshold = 0.7
    with speech_recognition.Microphone() as source:
        riconoscitore.adjust_for_ambient_noise(source, 0.5)
        audio_bot("Ti ascolto")
        audio = riconoscitore.listen(source)
    try:
        text1 = riconoscitore.recognize_google(audio, language="it-IT")
        user_label.configure(text=text1)
        ws.update()
        if text1.lower() == "cosa sai fare":
            vocal_label.configure(text="Allora, posso aiutarti con:\norario di un Medico;\nstudio di un Medico;\nreparto di un Medico;\nrecapito di un Medico;\nin alternativa contatta il XXXXXX")
            ws.update()
            audio_bot("Allora, posso aiutarti con,orario di un Medico,studio di un Medico;\nreparto di un Medico,recapito di un Medico;\nin alternativa contatta il XXXXXX")
        else:
            risposta(text1.lower())
        pass
    except Exception:
        pass


def speak_label(received_text):
    vocal_label.configure(text=received_text)
    ws.update()
    audio_bot(received_text)



def setting():
    user_label.configure(text="")
    ws.update()
    inizio()
    sleeping_duck()
    setting()


def check_answer(answer):
    if key_word[0] in answer or key_word[1] in answer:
        speak_label("Check orari")
    if key_word[2] in answer or key_word[3] in answer or key_word[4] in answer or key_word[10] in answer or key_word[11] in answer:
        speak_label("Check studio")
    if key_word[5] in answer or key_word[6] in answer or key_word[7] in answer:
        speak_label("Check recapito telefonico")
    if key_word[8] in answer:
        speak_label("Check email")
    if key_word[9] in answer:
        speak_label("Check reparto")



def risposta(input_user):
    for x in key_word:
        if x in input_user:
            check_answer(input_user.lower())
            break
    else:
        vocal_label.configure(text = "Mi dispiace, non posso aiutarti. \nPer sapere cosa posso fare per te, prova a chiedermi:\n''cosa sai fare?''")
        ws.update()
        audio_bot("mi dispiace, non posso aiutarti. Per sapere cosa posso fare per te, prova a chiedermi, cosa sai fare?")



if __name__ == '__main__':
    duck_label = Label(ws, justify=LEFT, text=duck_sleep)
    duck_label.place(relx = 0.1, rely = 0.1, anchor = 'nw')
    vocal_label = Label(ws, justify=LEFT, text="", font = f)
    vocal_label.place(relx = 0.6, rely = 0.3, anchor = 'center')
    user_label = Label(ws, text="", font = f)
    user_label.place(relx = 0.5, rely = 0.7, anchor = 'center')
    ws.resizable(False, False)
    ws.after(1000, setting)
    ws.mainloop()


# string.replace[" ", "_"]

# packages used for speech recognition
import playsound
import time
from gtts import gTTS
import speech_recognition

def understand(valore_microfono, parA, parB, lang, pause):
    riconoscitore = speech_recognition.Recognizer()
    riconoscitore.energy_threshold = valore_microfono
    riconoscitore.dynamic_energy_threshold = False
    riconoscitore.pause_threshold = pause
    with speech_recognition.Microphone() as source:
        riconoscitore.adjust_for_ambient_noise(source)
        kkk = riconoscitore.listen(source, parA, parB)
    try:
        text = riconoscitore.recognize_google(kkk, language=lang)
        return(text)
    except Exception:
        return("Error")

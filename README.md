# MyThesis_BiomedicalEngineering
This is my thesis. Luca Roffia (https://github.com/lroffia) and Elisa Riforgiato have collaborated with this thesis.
Here you can find my thesis' files. There are: an installation file (for installing Virtual Box on macOS), 
a folder with my python files, a folder with owl files and a folder with jsap files.



HOW TO USE THIS THESIS


First Step:
Download and install Git from this link: https://git-scm.com/downloads
Use GitBash (or cmd) for cloning and pushing files
Download and install SEPABins --> https://github.com/arces-wot/SEPABins


Second Step:
Download and install this repository --> https://github.com/DitucSpa/MyThesis_BiomedicalEngineering.git
Download and install Python (see pdf file named "HowToInstallPython.pdf" inside HowToInstall folder)


Third Step:
Download and instal these packages inside Python folder (ex. C:\Users\(your_user_name)\AppData\Local\Programs\Python\Python39)
- python -m pip install wikipedia
- python -m pip install gTTS
- python -m pip install SpeechRecognition
- python -m pip install tk
- python -m pip install playsound==1.2.2 (other versions have problem with microphone for virtual machine)
- for installing pyaudio go to https://www.lfd.uci.edu/~gohlke/pythonlibs/ --> PyAudio and install the whl files
(for example I've used PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl). Then digit  python -m pip install (paste here that file)
If you have problems with "C++ 14.0 is required", go to https://visualstudio.microsoft.com/it/visual-cpp-build-tools/


Fourth Step:
With any Python Editors change the paths (ex. you will find path = "something" and you need to change this
value with your folder's path) inside the scripts of:
- assistente_vocale_medical_staff.py
- assistente_vocale_paziente_v1.py
- health_worker.py
- technician.py
You must have a microphone and an internet connection for using this project.
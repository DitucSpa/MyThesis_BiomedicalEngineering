# packages for tkinter
from tkinter import *
from tkinter import ttk

# packages for writing files
import os
import sys

# packages used for speech recognition
import playsound
import time
from gtts import gTTS
import speech_recognition

# package for usign Microphone
import use_microphone

# package for using SEPA
import query_sparql

# for creating a new document with sparql_query
import create_sparql


import icd9_package
#https://github.com/fabiocaccamo/python-codicefiscale
from codicefiscale import codicefiscale

from time import sleep
import tkinter.font as tkFont

path = r"C:\Users\Ovettino\Downloads\GitHub\MyThesis_BiomedicalEngineering\JSAP\TesiProva.jsap" # path of JSAP file
path_new = r"C:\Users\Ovettino\Downloads\GitHub\MyThesis_BiomedicalEngineering\JSAP"
f = ('Times', 14) # font
CF = "DTCGLC99C29C573A"
background_frame = "#80b3ff" # background of the frame
background_window = "#b3ccff" # background of the window


duck_talk = r"""
           ,~~.
 ,       (  °     )<
 )`~~'       (
(    .__)        )
 `-.________,'
"""

car_header = ['ID comune', 'Codice Fiscale']
car_list = [
('5', 'DTCGLC99C29C573A') ,
('6', 'MRORSS99C29C573A') ,
('7', 'ELSRFF99C29C573A')
]

car_list2 = [
('2', 'DTCGLC99C29C573A') ,
('3', 'ELSRFF99C29C573A'),
('4', 'QPRTUV99B26V067Y')
]


import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.title('Treeview demo')
root.geometry('1200x500')

frame = Frame(root, bd = 2, relief = SOLID, padx = 5, pady = 5)
frame.config(bg = background_frame)
frame.place(x=750, y=35)
# columns
columns = ('#1', '#2')
Label(frame, text="Sezione:\t\tSpecifica", font=f, bg=background_frame).grid(row=2, column=0, sticky=W, pady=10)
Label(frame, text="Data:\t\t2021-09-10", font=f, bg=background_frame).grid(row=1, column=0, sticky=W, pady=10)
Label(frame, text="Reparto:\t\tCARDIOLOGIA", font=f, bg=background_frame).grid(row=3, column=0, sticky=W, pady=10)
tree = ttk.Treeview(root, columns=columns, show='headings')
vsb = ttk.Scrollbar(orient="vertical",
            command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
# define headings
tree.heading('#1', text='ID Comune')
tree.heading('#2', text='Codice Fiscale')
tree.grid(column=0, row=0, sticky='nsew', in_=frame)



frame2 = Frame(root, bd = 2, relief = SOLID, padx = 5, pady = 5)
frame2.config(bg = background_frame)
frame2.place(x=300, y=35)
Label(frame2, text="Sezione:\t\tComune", font=f, bg=background_frame).grid(row=2, column=0, sticky=W, pady=10)
Label(frame2, text="Data:\t\t2021-09-10", font=f, bg=background_frame).grid(row=1, column=0, sticky=W, pady=10)
Label(frame2, text="Reparto:\t\tCARDIOLOGIA", font=f, bg=background_frame).grid(row=3, column=0, sticky=W, pady=10)
# columns
columns = ('#1', '#2')

tree2 = ttk.Treeview(frame2, columns=columns, show='headings')
vsb2 = ttk.Scrollbar(orient="vertical",
            command=tree2.yview)
tree2.configure(yscrollcommand=vsb2.set)
# define headings
tree2.heading('#1', text='ID Comune')
tree2.heading('#2', text='Codice Fiscale')
tree2.grid(column=0, row=2, sticky='nsew', in_=frame2)

# generate sample data
contacts = []
for n in range(1, 100):
    contacts.append((f'first {n}', f'last {n}', f'email{n}@example.com'))

# adding data to the treeview
for car_list in car_list:
    tree.insert('', tk.END, values=car_list)

for car_list2 in car_list2:
    tree2.insert('', tk.END, values=car_list2)




# bind the select event
def item_selected(event):
    for selected_item in tree.selection():
        # dictionary
        item = tree.item(selected_item)
        # list
        record = item['values']
        #


def item_selected2(event):
    for selected_item in tree2.selection():
        # dictionary
        item = tree2.item(selected_item)
        # list
        record = item['values']
        #



tree.bind('<<TreeviewSelect>>', item_selected)
tree2.bind('<<TreeviewSelect>>', item_selected2)

tree.grid(row=0, column=0, sticky='nsew')
tree2.grid(row=0, column=0, sticky='nsew')

# add a scrollbar
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
tree2.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')

duck_label = Label(root, justify=LEFT, text=duck_talk)
duck_label.place(relx = 0.1, rely = 0.1, anchor = 'nw')

btn_reloading = Button(root, width = 15, text = 'Va bene', font=f, bg=background_window,
    activebackground="#3399ff")
btn_reloading.place(height=60, width=408, x = 530, y = 430)
# run the app
root.mainloop()

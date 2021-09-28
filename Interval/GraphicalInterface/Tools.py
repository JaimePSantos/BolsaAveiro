import tkinter as tk
from tkinter import ttk

def UnderConstruction(window):
    tk.Label(window, text='UNDER CONSTRUCTION', font=('Arial', 14, ('bold')),
             anchor='center').grid(row=0, column=0, sticky='EW')

def myLabelFrame(f, txt, row, col, stick='NEWS', py=5, span=1, pad=(5, 5, 5, 5)):
    l = ttk.LabelFrame(f, text=txt, padding=pad)
    l.grid(row=row, column=col, sticky=stick, columnspan=span, pady=py)
    return l

def myEntryFrame(f, width, row, col, stick='W', span=1, pad=(5, 5, 5, 5)):
    translationTxt = tk.Entry(f, width=width)
    translationTxt.grid(row=row, column=col, sticky=stick, columnspan=span)
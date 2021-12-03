import tkinter as tk
from tkinter import ttk

def UnderConstruction(window):
    tk.Label(window, text='UNDER CONSTRUCTION', font=('Arial', 14, ('bold')),
             anchor='center').grid(row=0, column=0, sticky='EW')

def myLabelFrame(f, row, col, text,colspan,rowspan,stick='NEWS',py=5, pad=(5, 5, 5, 5)):
    l = ttk.LabelFrame(f, text=text, padding=pad)
    #l.grid(row=row, column=col, sticky=stick, columnspan=colspan,rowspan=rowspan, pady=py)
    return l

def myEntryFrame(f, row, col, width, stick, colspan):
    entryTxt = tk.Entry(f, width=width)
    entryTxt.grid(row=row, column=col, sticky=stick, columnspan=colspan)
    return entryTxt

def myTextFrame(f,row,col,width,height,stick,colspan,bg=None,fg=None,bd=None,font=None,yscrollcommand=None,xscrollcommand=None):
    textTxt = tk.Text(f, width=width,height=height,bg=bg,fg=fg,bd=bd,font=font,yscrollcommand=yscrollcommand,xscrollcommand=xscrollcommand)
    textTxt.grid(row=row, column=col, sticky=stick, columnspan=colspan)
    return textTxt

def myListBoxFrame(f,row,col,width,height,stick,colspan,bg=None,fg=None,bd=None,font=None,yscrollcommand=None,xscrollcommand=None):
    textTxt = tk.Listbox(f, width=width,height=height,bg=bg,fg=fg,bd=bd,font=font,yscrollcommand=yscrollcommand,xscrollcommand=xscrollcommand)
    textTxt.grid(row=row, column=col, sticky=stick, columnspan=colspan)
    return textTxt

def myButton(f,row,col,command,rowspan,colspan,sticky,text,bg=None,fg=None,font=None,bd=None,relief=None):
    myButton = tk.Button(f,text=text,command=command,bg=bg,fg=fg,font=font,bd=bd,relief=relief)
    myButton.grid(row=row,column=col,rowspan=rowspan,columnspan=colspan,sticky=sticky)
    return myButton

def myScrollBar(f,row,col,stick):
    scrollbar = tk.Scrollbar(f)
    scrollbar.grid(row=row,column=col,sticky=stick)
    return scrollbar

def myFrame(f,side,fill,expand):
    myF = tk.Frame(f)
    myF.pack(side=side,fill=fill,expand=expand)
    return myF
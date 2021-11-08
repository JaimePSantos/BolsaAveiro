import tkinter as tk
from tkinter import ttk
# from Tools import
from NotePage import BasicNotepage
from BasicTranslationFrame import BasicTranslation
from FileFrame import FileTranslation
from HistoryFrame import HistoryTranslation
import os
import sys

sys.path.append('../')
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from Interval.RunProgram import runGUI
from PIL import Image
from PIL import ImageTk
import tkinter.messagebox as MessageBox

base_folder = os.path.dirname(__file__)
bgPath = base_folder + '/Resources/background2.png'


class IntervalInterface(tk.Frame):
    def __init__(self, root, title):
        tk.Frame.__init__(self, root)
        self.root = root
        self.title = title
        self.root.title(title)

        master = root
        master.rowconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.config(padx=5, pady=5)

        frame1 = ttk.Frame(master, padding=(5, 5, 5, 5))
        frame1.grid(row=0, column=0, sticky="NSEW")
        frame1.rowconfigure(2, weight=1)
        frame1.columnconfigure(0, weight=1)

        # ------------ Notebook with translation options. -----------
        frame1 = ttk.Frame(master, padding=(5, 5, 5, 5))
        frame1.grid(row=0, column=0, sticky="NSEW")
        frame1.rowconfigure(2, weight=1)
        frame1.columnconfigure(0, weight=1)
        self.AlwaysPreview = False

        n = ttk.Notebook(frame1, padding=(5, 5, 5, 5))
        n.grid(row=1, column=0, rowspan=1, columnspan=5, sticky=(tk.N, tk.E, tk.W, tk.S))
        n.columnconfigure(0, weight=1)
        n.enable_traversal()

        #self.basicTranslation = BasicTranslation(n)
        self.fileTranslation = FileTranslation(n)
        self.translationHistory = HistoryTranslation(n)
        #n.add(self.basicTranslation, text='Basic', underline=0)
        n.add(self.fileTranslation, text='File', underline=0)
        n.add(self.translationHistory,text='History', underline=0)

        # --------------------------- Menu ------------------------------

        menubar = tk.Menu(root,
                          foreground='black', background='#F0F0F0', activebackground='#86ABD9',
                          activeforeground='white')
        filemenu = tk.Menu(menubar, tearoff=0, foreground='black', background='#F0F0F0',
                           activebackground='#86ABD9', activeforeground='white')
        filemenu.add_command(label="Load", underline=0,
                             compound='left', accelerator='Ctrl+L',
                             command=self.fileTranslation.openFile)
        root.bind_all('<Control-l>',lambda e: self.fileTranslation.openFile())
        filemenu.add_command(label="Quit", underline=0,
                             compound='left', accelerator='Ctrl+Q',
                             command=lambda e=None: self.quitProgram(e))
        filemenu.add_separator()
        menubar.add("cascade", label='File', underline=0, menu=filemenu)
        root.config(menu=menubar)

    def quitProgram(self, event):
        if MessageBox.askyesno("Quit PiCamera", "Exit %s?" % self.title):
            self.master.destroy()

win = tk.Tk()
app = IntervalInterface(win, title="idDL2DL")
win.minsize(900, 768)
win.mainloop()

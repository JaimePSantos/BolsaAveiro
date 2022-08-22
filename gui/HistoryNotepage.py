import tkinter as tk
import tkinter.messagebox as MessageBox
from tkinter import ttk

from gui.Tools import UnderConstruction


class HistoryNotepage(tk.Frame):
    def __init__(self, parent, camera=None, cancel=None, ok=None,
                 rowconfig=False, colconfig=True, data=None, ):
        ttk.Frame.__init__(self, parent, padding=(10, 10, 10, 10))
        self.grid(sticky='NSEW')
        if colconfig is True:
            self.columnconfigure(0, weight=1)
        if rowconfig is True:
            self.rowconfigure(0, weight=1)
        self.parent = parent
        self.CancelButton = cancel
        self.OkButton = ok
        self.data = data
        self.init = True  # disable SomethingChanged
        self.BuildPage()
        self.init = False
        self.Changed = False

    def BuildPage(self, fileTranslation):  # MUST Overide this!
        UnderConstruction(self)

    def SomethingChanged(self, val):  # Can override but call super!
        if self.init:
            return
        self.Changed = True
        if self.CancelButton is not None:
            self.CancelButton.config(state='normal')  # '!disabled')
            if self.OkButton is not None:
                self.OkButton.config(text='Save')

    def SaveChanges(self):  # MUST override this!
        MessageBox.showwarning(
            "SaveChanges",
            "SaveChanges not implemented!")

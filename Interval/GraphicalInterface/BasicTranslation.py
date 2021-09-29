import tkinter as tk
from tkinter import ttk
from Tools import UnderConstruction, myLabelFrame, myEntryFrame, myButton,myTextFrame
from NotePage import BasicNotepage
import sys
sys.path.append('../')
from Interval.RunProgram import runGUI

class BasicTranslation(BasicNotepage):
    def BuildPage(self):
        # --- Translation frame ---
        f1 = myLabelFrame(self,0, 0,  colspan=2, text='Enter text for translation')
        self.translationButton = myButton(f1,row=2,col=0,command=self.translate,rowspan=2,colspan=1,sticky='W',text='Translate', bg='white',fg='black',font=('Arial',12),relief='raised')
        self.textEntry = myEntryFrame(f1,row=0, col=0, width=100 , stick='W',colspan=100)

        # --- Translated Frame ---
        f2 = myLabelFrame(self,row=1, col=0,colspan=2, text='Translated Text')
        self.translatedText = myTextFrame(f2,row=1, col=0,width=100,height=0,stick='W',colspan=100)
        self.clearButton = myButton(f2,row=2,col=0,command=self.clear,rowspan=1,colspan=1,sticky='W',text='Clear', bg='white',fg='black',font=('Arial',12),relief='raised')
        self.clipboardButton = myButton(f2,row=2,col=1,command=self.copyToClipboard,rowspan=1,colspan=1,sticky='W',text='Copy', bg='white',fg='black',font=('Arial',12),relief='raised')

    def translate(self):
        self.clear(self.translatedText)
        input = self.textEntry.get()
        if input == "":
            transl = "Please enter an expression to convert."
        else:
            transl,catcher = self.runTranslation(input)
        self.translatedText.insert(tk.END,transl)

    def clear(self,btn=None):
        if btn is not None:
            btn.delete('1.0',tk.END)
        else:
            self.textEntry.delete(0,tk.END)
            self.translatedText.delete('1.0',tk.END)

    def copyToClipboard(self):
        self.translatedText.clipboard_clear()
        self.translatedText.clipboard_append(self.translatedText.get('1.0','end-1c'))


    def runTranslation(self,input):
        return runGUI('<stdin>', input)


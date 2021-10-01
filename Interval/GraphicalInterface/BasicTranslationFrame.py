import tkinter as tk
from tkinter import ttk
from Tools import UnderConstruction, myLabelFrame, myEntryFrame, myButton,myTextFrame,myScrollBar,myFrame
from NotePage import BasicNotepage
import sys
sys.path.append('../')
from Interval.RunProgram import runGUI

class BasicTranslation(BasicNotepage):
    def BuildPage(self):
        # --- Translation frame ---
        f1 = myLabelFrame(self,0, 0,  colspan=2,rowspan=3, text='Enter text for translation')
        f1.pack(side='top',fill='both',expand=True)

        controls = myFrame(f1,side='bottom',fill='both',expand=True)
        txtFrame = myFrame(f1,side='top',fill='both',expand=True)

        self.translationText = myTextFrame(txtFrame,row=0, col=0, width=99,height=13 , stick='W',colspan=100)
        self.translationScrollBar = myScrollBar(txtFrame,0,101,'ns')
        self.translationText.config(yscrollcommand=self.translationScrollBar.set)
        self.translationScrollBar.config(command=self.translationText.yview)

        self.translationButton = myButton(controls,row=1,col=0,command=self.translate,rowspan=2,colspan=1,sticky='W',text='Translate', bg='white',fg='black',font=('Arial',12),relief='raised')

        # --- Translated Frame ---
        f2 = myLabelFrame(self,row=4, col=0,colspan=2,rowspan=3, text='Translated Text')
        f2.pack(side='top',fill='both',expand=True)

        controls2 = myFrame(f2,side='bottom',fill='both',expand=True)
        txtFrame2 = myFrame(f2,side='top',fill='both',expand=True)

        self.translatedText = myTextFrame(txtFrame2,row=4, col=0,width=99,height=13,stick='W',colspan=100)
        self.translatedText.config(state=tk.DISABLED)
        self.scrollBar2 = myScrollBar(txtFrame2,row=4,col=100,stick='ns')
        self.translatedText.config(yscrollcommand=self.scrollBar2.set)
        self.scrollBar2.config(command=self.translatedText.yview)

        self.clearButton = myButton(controls2,row=5,col=0,command=self.clear,rowspan=1,colspan=1,sticky='W',text='Clear', bg='white',fg='black',font=('Arial',12),relief='raised')
        self.clipboardButton = myButton(controls2,row=5,col=1,command=self.copyToClipboard,rowspan=1,colspan=1,sticky='W',text='Copy', bg='white',fg='black',font=('Arial',12),relief='raised')

    def translate(self):
        self.translatedText.config(state=tk.NORMAL)
        self.clear(self.translatedText)
        inputs = self.translationText.get('1.0',tk.END)
        self.runMultipleTranslations(inputs)
        transList = []
        if inputs == "":
            transList.append("Please enter an expression to convert.")
        else:
             transList = self.runMultipleTranslations(inputs)
        for transl in transList:
            self.translatedText.insert(tk.END,transl)
            self.translatedText.insert(tk.END,"\n")
        self.translatedText.config(state=tk.DISABLED)

    def clear(self,btn=None):
        if btn is not None:
            btn.delete('1.0',tk.END)
        else:
            self.translationText.delete(0,tk.END)
            self.translatedText.delete('1.0',tk.END)

    def copyToClipboard(self):
        self.translatedText.clipboard_clear()
        self.translatedText.clipboard_append(self.translatedText.get('1.0','end-1c'))

    def runTranslation(self,input):
        return runGUI('<stdin>', input)

    def breakInput(self,input):
        chars = ""
        inputList = []
        for char in input:
            if(char=='\n'):
                inputList.append(chars)
                chars = ""
                continue
            else:
                chars+= char
        inputList = [input for input in inputList if input.strip()]
        return inputList

    def runMultipleTranslations(self,inputs):
        inputList = self.breakInput(inputs)
        outputList = []
        for input in inputList:
            if('#' in input):
                continue
            else:
                outputList.append(runGUI('<stdin>',input))
        return outputList
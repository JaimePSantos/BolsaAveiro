import tkinter as tk
from tkinter import ttk
from Tools import UnderConstruction, myLabelFrame, myEntryFrame, myButton,myTextFrame,myScrollBar
from NotePage import BasicNotepage
import sys
sys.path.append('../')
import os
from Interval.RunProgram import runGUI
base_folder = os.path.join(os.path.dirname(__file__,),'..')
class FileTranslation(BasicNotepage):
    def BuildPage(self):
        # --- File loading frame ---
        f1 = myLabelFrame(self,0, 0,  colspan=2,rowspan=3, text='Text from file')
        self.loadButton = myButton(f1,row=2,col=0,command=self.openFile,rowspan=1,colspan=1,sticky='W',text='Load', bg='white',fg='black',font=('Arial',12),relief='raised')
        self.translationButton = myButton(f1,row=1,col=1,command=self.translate,rowspan=2,colspan=1,sticky='W',text='Translate', bg='white',fg='black',font=('Arial',12),relief='raised')
        self.path = myEntryFrame(f1,row=2,col=2,width=50,stick='W',colspan=1)
        self.loadedText = myTextFrame(f1,row=0, col=0, width=99,height = 13 , stick='W',colspan=100)
        self.scrollBar = myScrollBar(f1,0,101,'ns')
        self.loadedText.config(yscrollcommand=self.scrollBar.set)
        self.scrollBar.config(command=self.loadedText.yview)

        # --- Translated Frame ---
        f2 = myLabelFrame(f1, row=4, col=0, colspan=2, rowspan=3, text='Translated Text')
        self.translatedText = myTextFrame(f2, row=4, col=0, width=99, height=13, stick='W', colspan=100)
        self.translatedText.config(state=tk.DISABLED)
        self.clearButton = myButton(f2, row=5, col=0, command=self.clear, rowspan=1, colspan=1, sticky='W',
                                    text='Clear', bg='white', fg='black', font=('Arial', 12), relief='raised')
        self.clipboardButton = myButton(f2, row=5, col=1, command=self.copyToClipboard, rowspan=1, colspan=1,
                                        sticky='W', text='Copy', bg='white', fg='black', font=('Arial', 12),
                                        relief='raised')

    def openFile(self):
        self.clear(self.loadedText)
        tf = tk.filedialog.askopenfilename(
            initialdir=base_folder,
            title="Open Text file",
            filetypes=(("Text Files", "*.txt"),)
        )
        self.path.insert(tk.END, tf)
        with open(tf) as tf:
            data = tf.read()
            self.loadedText.insert(tk.END, data)
        self.clear(self.translatedText)

    def translate(self):
        self.translatedText.config(state=tk.NORMAL)
        self.clear(self.translatedText)
        inputs = self.loadedText.get('1.0',tk.END)
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
            self.loadedText.delete(0,tk.END)
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

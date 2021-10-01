import tkinter as tk
from tkinter import ttk
from Tools import UnderConstruction, myLabelFrame, myEntryFrame, myButton,myTextFrame,myScrollBar,myFrame
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
        f1.pack(side='top',fill='both',expand=True)

        controls = myFrame(f1,side='bottom',fill='both',expand=True)
        txtFrame = myFrame(f1,side='top',fill='both',expand=True)

        self.loadedText = myTextFrame(txtFrame,row=0, col=0, width=99,height = 13 , stick='W',colspan=100)
        self.scrollBar = myScrollBar(txtFrame,row=0,col=100,stick='ns')
        self.loadedText.config(yscrollcommand=self.scrollBar.set)
        self.scrollBar.config(command=self.loadedText.yview)

        self.loadButton = myButton(controls,row=1,col=0,command=self.openFile,rowspan=1,colspan=1,sticky='W',text='Load', bg='white',fg='black',font=('Arial',12),relief='raised')
        self.translationButton = myButton(controls,row=1,col=1,command=self.translate,rowspan=1,colspan=1,sticky='W',text='Translate', bg='white',fg='black',font=('Arial',12),relief='raised')
        self.path = myEntryFrame(controls,row=1,col=2,width=30,stick='W',colspan=1)


        # --- Translated Frame ---
        f2 = myLabelFrame(self, row=4, col=0, colspan=2, rowspan=3, text='Translated Text')
        f2.pack(side='top',fill='both',expand=True)

        controls2 = myFrame(f2,side='bottom',fill='both',expand=True)
        txtFrame2 = myFrame(f2,side='top',fill='both',expand=True)

        self.translatedText = myTextFrame(txtFrame2, row=4, col=0, width=99, height=13, stick='W', colspan=100)
        self.translatedText.config(state=tk.DISABLED)
        self.scrollBar2 = myScrollBar(txtFrame2,row=4,col=100,stick='ns')
        self.translatedText.config(yscrollcommand=self.scrollBar2.set)
        self.scrollBar2.config(command=self.translatedText.yview)

        self.clearButton = myButton(controls2, row=5, col=0, command=self.clear, rowspan=1, colspan=1, sticky='W',
                                    text='Clear', bg='white', fg='black', font=('Arial', 12), relief='raised')
        self.clipboardButton = myButton(controls2, row=5, col=1, command=self.copyToClipboard, rowspan=1, colspan=1,
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

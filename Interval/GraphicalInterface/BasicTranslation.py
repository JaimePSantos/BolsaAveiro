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
        f1 = myLabelFrame(self,0, 0, 'Enter text for translation',  span=2)
        self.translationButton = myButton(f1,1,0,self.translate,2,'W','Translate', bg='white',fg='black',font=('Arial',12),relief='flat')
        self.textEntry = myEntryFrame(f1, 100, 0, 0, 'W',span=1)

        # --- Translated Frame ---
        f = myLabelFrame(self,1, 0, 'Translated Text',  span=2)
        self.translatedText = myTextFrame(f,1,0,100,0,'W',span=1)

    def translate(self):
        self.translatedText.delete('1.0',tk.END)
        input = self.textEntry.get()
        if input == "":
            transl = "Please enter an expression to convert."
        else:
            transl,catcher = self.runTranslation(input)
        self.translatedText.insert(tk.END,transl)

    def runTranslation(self,input):
        return runGUI('<stdin>', input)


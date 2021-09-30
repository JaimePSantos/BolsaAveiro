import tkinter as tk
from tkinter import ttk
from Tools import UnderConstruction, myLabelFrame, myEntryFrame, myButton,myTextFrame,myScrollBar
from NotePage import BasicNotepage
import sys
sys.path.append('../')
from Interval.RunProgram import runGUI

class FileTranslation(BasicNotepage):
    def BuildPage(self):
        # --- Translation frame ---
        f1 = myLabelFrame(self,0, 0,  colspan=2,rowspan=3, text='Text from file')
        #self.translationButton = myButton(f1,row=2,col=0,command=self.translate,rowspan=2,colspan=1,sticky='W',text='Translate', bg='white',fg='black',font=('Arial',12),relief='raised')
        self.loadedText = myTextFrame(f1,row=0, col=0, width=99,height = 13 , stick='W',colspan=100)
        self.scrollBar = myScrollBar(f1,0,101,'ns')

        self.loadedText.config(yscrollcommand=self.scrollBar.set)
        self.scrollBar.config(command=self.loadedText.yview)

        # def open_text_file():
        #     # file type
        #     filetypes = (
        #         ('text files', '*.txt'),
        #         ('All files', '*.*')
        #     )
        #     # show the open file dialog
        #     f = fd.askopenfile(filetypes=filetypes)
        #     # read the text file and show its content on the Text
        #     #text.insert('1.0', f.readlines())
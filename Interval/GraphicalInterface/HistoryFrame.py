import tkinter as tk
from tkinter import ttk
from Tools import UnderConstruction, myLabelFrame, myEntryFrame, myButton, myTextFrame, myScrollBar, myFrame
from NotePage import BasicNotepage
from FileFrame import FileTranslation
from HistoryNotepage import HistoryNotepage
import sys

sys.path.append('../')
import os
from Interval.RunProgram import runGUI
from ast import literal_eval

base_folder = os.path.join(os.path.dirname(__file__, ), '..')

class HistoryTranslation(HistoryNotepage):
    def BuildPage(self,fileTranslation):
        # --- File loading frame ---
        f1 = myLabelFrame(self, 0, 0, colspan=2, rowspan=3, text='Text from file')
        f1.pack(side='top', fill='both', expand=True)
        controls = myFrame(f1, side='bottom', fill='both', expand=True)
        self.fileTranslation = fileTranslation
        self.translationHistoryCatcher = {}
        self.translationHistory = {}
        self.translationButton = myButton(controls, row=1, col=1, command=self.testPrint, rowspan=1, colspan=1,
                                          sticky='W', text='Translate', bg='white', fg='black', font=('Arial', 12),
                                          relief='raised')
        self.refreshButton = myButton(controls, row=1, col=2, command=self.refreshHistory, rowspan=1, colspan=1,
                                          sticky='W', text='Refresh', bg='white', fg='black', font=('Arial', 12),
                                          relief='raised')
        self.clearButton = myButton(controls, row=1, col=3, command=self.clearHistory, rowspan=1, colspan=1,
                                          sticky='W', text='Clear', bg='white', fg='black', font=('Arial', 12),
                                          relief='raised')

    def refreshHistory(self):
        self.translationHistoryCatcher = self.fileTranslation.getHistory()
        for k,v in self.translationHistoryCatcher.items():
            keyList = literal_eval(k)
            for key,value in zip(keyList, v):
                self.translationHistory[key] = value


    def testPrint(self):
        i=0
        for k,v in self.translationHistory.items():
            i+=1
            print("%s - %s \t -> \t %s"%(i,k,v))

    def clearHistory(self):
        self.translationHistory = {}
        self.fileTranslation.clearHistory()
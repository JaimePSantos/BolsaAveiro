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

base_folder = os.path.join(os.path.dirname(__file__, ), '..')

class HistoryTranslation(HistoryNotepage):
    def BuildPage(self,fileTranslation):
        # --- File loading frame ---
        f1 = myLabelFrame(self, 0, 0, colspan=2, rowspan=3, text='Text from file')
        f1.pack(side='top', fill='both', expand=True)
        controls = myFrame(f1, side='bottom', fill='both', expand=True)
        self.fileTranslation = fileTranslation
        self.translationButton = myButton(controls, row=1, col=1, command=self.testPrint, rowspan=1, colspan=1,
                                          sticky='W', text='Translate', bg='white', fg='black', font=('Arial', 12),
                                          relief='raised')

    def testPrint(self):
        pass
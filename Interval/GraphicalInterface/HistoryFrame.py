import tkinter as tk
from tkinter import ttk
from Tools import UnderConstruction, myLabelFrame, myEntryFrame, myButton, myTextFrame, myScrollBar, myFrame
from NotePage import BasicNotepage
import sys

sys.path.append('../')
import os
from Interval.RunProgram import runGUI

base_folder = os.path.join(os.path.dirname(__file__, ), '..')

class HistoryTranslation(BasicNotepage):
    def BuildPage(self):
        # --- File loading frame ---
        f1 = myLabelFrame(self, 0, 0, colspan=2, rowspan=3, text='Text from file')
        f1.pack(side='top', fill='both', expand=True)
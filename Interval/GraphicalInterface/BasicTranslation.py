import tkinter as tk
from tkinter import ttk
from Tools import UnderConstruction, myLabelFrame, myEntryFrame
from NotePage import BasicNotepage

class BasicTranslation(BasicNotepage):
    def BuildPage(self):
        f1 = myLabelFrame(self, 'Enter text for translation', 0, 0, span=2)
        self.textEntry = myEntryFrame(f1, 10, 0, 0, 'W')

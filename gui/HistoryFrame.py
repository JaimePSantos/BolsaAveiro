from ast import literal_eval
import os
import re
import sys
import tkinter as tk

from gui.HistoryNotepage import HistoryNotepage
from gui.Tools import myLabelFrame, myButton, \
    myTextFrame, myScrollBar, myFrame, myListBoxFrame

sys.path.append('../idDL2DL/')

base_folder = os.path.join(os.path.dirname(__file__, ), '../idDL2DL')


class HistoryTranslation(HistoryNotepage):
    def BuildPage(self):
        # --- File loading frame ---
        f1 = myLabelFrame(
            self,
            0,
            0,
            colspan=2,
            rowspan=3,
            text='History')
        f1.pack(side='top', fill='both', expand=True)

        padx = 5
        pady = 2

        controls = myFrame(f1, side='top', fill='both', expand=True)
        self.refreshButton = myButton(
            controls,
            row=1,
            col=1,
            command=self.refreshHistory,
            rowspan=1,
            colspan=1,
            sticky='W',
            text='Refresh',
            bg='white',
            fg='black',
            font=(
                'Arial',
                12),
            relief='raised',
            padx=padx,
            pady=pady)
        self.clearButton = myButton(
            controls,
            row=1,
            col=2,
            command=self.clearHistory,
            rowspan=1,
            colspan=1,
            sticky='W',
            text='Clear',
            bg='white',
            fg='black',
            font=(
                'Arial',
                12),
            relief='raised',
            padx=padx,
            pady=pady
        )

        txtFrame = myFrame(f1, side='top', fill='both', expand=True)
        self.translationListBox = myListBoxFrame(
            txtFrame, row=0, col=0, width=99, height=13, stick='W', colspan=100)
        self.scrollBar = myScrollBar(
            txtFrame,
            row=1,
            col=0,
            stick='ew',
            orient='horizontal',
            columnspan=100)
        self.translationListBox.config(
            xscrollcommand=self.scrollBar.set)
        self.translationListBox.bind(
            '<<ListboxSelect>>',
            lambda e: self.showTranslation())
        self.translationListBox.bind(
            '<Double-Button-1>',
            lambda e: self.listboxCopy())
        self.scrollBar.config(command=self.translationListBox.xview)

        f2 = myLabelFrame(
            f1,
            row=4,
            col=0,
            colspan=2,
            rowspan=3,
            text='Translation')
        f2.pack(side='bottom', fill='both', expand=True)
        txtFrame2 = myFrame(f2, side='top', fill='both', expand=True)
        self.translatedText = myTextFrame(
            txtFrame2,
            row=4,
            col=0,
            width=99,
            height=13,
            stick='W',
            colspan=100)
        self.translatedText.config(state=tk.DISABLED)

        self.translationHistoryCatcher = {}
        self.translationHistory = {}

    def refreshHistory(self):
        self.translationHistoryCatcher = self.fileTranslation.getHistory()
        for k, v in self.translationHistoryCatcher.items():
            keyList = literal_eval(k)
            for key, value in zip(keyList, v):
                self.translationHistory[key] = value
        self.translationListBox.delete(0, tk.END)
        index = 1
        for k, v in self.translationHistory.items():
            self.translationListBox.insert(
                tk.END, "%s. %s" % (index, k))
            index += 1

    def clearHistory(self):
        self.translationHistory = {}
        self.fileTranslation.clearHistory()
        self.refreshHistory()
        self.translatedText.config(state=tk.NORMAL)
        self.translatedText.delete("1.0", tk.END)
        self.translatedText.config(state=tk.DISABLED)

    def selectItem(self):
        # get selected indices
        selectedIndex = self.translationListBox.curselection()
        # get selected items
        selectedTranslation = ",".join(
            [self.translationListBox.get(i) for i in selectedIndex])
        # To remove the index inserted in the history box.
        selectedTranslation = re.sub(
            r'[0-9]*\. ', '', selectedTranslation)
        return selectedTranslation

    def showTranslation(self):
        if not self.translationHistory:
            return
        self.translatedText.config(state=tk.NORMAL)
        self.translatedText.delete("1.0", tk.END)
        selectedTranslation = self.selectItem()
        if (selectedTranslation != ''):
            self.translatedText.insert(
                tk.END, self.translationHistory[selectedTranslation] + '\n')
        else:
            pass
        self.translatedText.config(state=tk.DISABLED)

    def listboxCopy(self):
        self.translationListBox.clipboard_clear()
        selected = self.translationListBox.get(tk.ANCHOR)
        selected = re.sub(r'[0-9]*\. ', '', selected)
        tk.messagebox.showinfo("Copied!", "Selection copied.")
        self.translationListBox.clipboard_append(selected)

    def setFileTranslation(self, fileTranslation):
        self.fileTranslation = fileTranslation

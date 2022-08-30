import os
import sys
import tkinter as tk
import tkinter.filedialog

from core.RunProgram import runGUI, runInterpGUI
from gui.NotePage import BasicNotepage
from gui.Tools import myLabelFrame, myEntryFrame, myButton, myTextFrame, myScrollBar, myFrame, myCheckButton

sys.path.append('/')
base_folder = os.path.join(os.path.dirname("../" + __file__, ), '')


class FileTranslation(BasicNotepage):
    def BuildPage(self):
        self.history = {}
        # --- File loading frame ---
        f1 = myLabelFrame(
            self,
            0,
            0,
            colspan=2,
            rowspan=3,
            text='Begin Translating')
        f1.pack(side='top', fill='both', expand=True)

        controls = myFrame(f1, side='bottom', fill='both', expand=True)
        txtFrame = myFrame(f1, side='top', fill='both', expand=True)

        padx = 5
        pady = 2

        self.loadedText = myTextFrame(
            txtFrame,
            row=0,
            col=0,
            width=99,
            height=13,
            stick='W',
            colspan=100,
            font = ('Arial',16))
        self.scrollBar = myScrollBar(
            txtFrame, row=0, col=100, stick='ns')
        self.loadedText.config(yscrollcommand=self.scrollBar.set)
        self.scrollBar.config(command=self.loadedText.yview)

        self.loadButton = myButton(
            controls,
            row=1,
            col=2,
            command=self.openFile,
            rowspan=1,
            colspan=1,
            sticky='W',
            text='Load',
            bg='white',
            fg='black',
            font=(
                'Arial',
                12),
            relief='raised',
            padx=padx,
            pady=pady)
        self.translationButton = myButton(
            controls,
            row=1,
            col=0,
            command=self.translate,
            rowspan=1,
            colspan=1,
            sticky='W',
            text='Translate',
            bg='white',
            fg='black',
            font=(
                'Arial',
                12),
            relief='raised',
            padx=padx,
            pady=pady)
        self.path = myEntryFrame(
            controls,
            row=1,
            col=3,
            width=79,
            stick='W',
            colspan=1,
            padx=padx,
            pady=pady,
            highlightthickness=2,
            highlightbackground='black',
            highlightcolor='black')
        # self.interpretButton = myButton(controls, row=1, col=3, command=self.interpret, rowspan=1, colspan=1,
        #                                   sticky='W', text='Interpret', bg='white', fg='black', font=('Arial', 12),
        #                                   relief='raised')
        self.interpVar = tk.IntVar()
        self.interpretButton = myCheckButton(
            controls,
            row=1,
            col=1,
            command=self.interpOn,
            rowspan=1,
            colspan=1,
            sticky='W',
            text='Interp Off',
            variable=self.interpVar,
            onvalue=1,
            offvalue=0,
            bg='white',
            fg='black',
            font=(
                'Arial',
                12),
            relief='raised',
            padx=padx,
            pady=pady,
            height=1)

        # --- Translated Frame ---
        f2 = myLabelFrame(
            self,
            row=4,
            col=0,
            colspan=2,
            rowspan=3,
            text='Translated Text')
        f2.pack(side='top', fill='both', expand=True)

        controls2 = myFrame(f2, side='bottom', fill='both', expand=True)
        txtFrame2 = myFrame(f2, side='top', fill='both', expand=True)

        self.translatedText = myTextFrame(
            txtFrame2,
            row=4,
            col=0,
            width=99,
            height=13,
            stick='W',
            colspan=100,
            font=(
                'Arial',
                14),
        )
        self.translatedText.config(state=tk.DISABLED)
        self.scrollBar2 = myScrollBar(
            txtFrame2, row=4, col=100, stick='ns')
        self.translatedText.config(yscrollcommand=self.scrollBar2.set)
        self.scrollBar2.config(command=self.translatedText.yview)

        self.clearButton = myButton(
            controls2,
            row=5,
            col=0,
            command=self.clear,
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
            pady=pady)
        self.clipboardButton = myButton(
            controls2,
            row=5,
            col=1,
            command=self.copyToClipboard,
            rowspan=1,
            colspan=1,
            sticky='W',
            text='Copy',
            bg='white',
            fg='black',
            font=(
                'Arial',
                12),
            relief='raised')
        self.saveButton = myButton(
            controls2,
            row=5,
            col=2,
            command=self.saveAs,
            rowspan=1,
            colspan=1,
            sticky='W',
            text='Save',
            bg='white',
            fg='black',
            font=(
                'Arial',
                12),
            relief='raised',
            padx=padx,
            pady=pady
        )

    def saveAs(self):
        text = self.translatedText.get('1.0', 'end')
        nLines = text.count('\n') - 1
        multipleFiles = False
        if (nLines <= 0):
            tk.messagebox.showerror('Error', 'Nothing to translate!')
            return
        elif (nLines > 1):
            multipleFiles = tk.messagebox.askyesnocancel(
                "Warning!", "Create multiple files for KMX?")
            if (multipleFiles):
                self.saveMultipleFiles(text)
            if (not (multipleFiles)):
                tk.messagebox.showwarning(
                    "Warning!", "All translations will be written to a single file!")
        if (nLines == 1 or not (multipleFiles)):
            self.filename = tk.filedialog.asksaveasfilename(
                initialdir=base_folder, defaultextension='.kyx')
            if (isinstance(self.filename, str) and self.filename != ''):
                fileNameList = self.filename.split("/")
                fileName = fileNameList[len(fileNameList) - 1]
                f = open(self.filename, 'w')
                f.write("Theorem \" " + fileName + ' \"\n\nProblem\n\n')
                f.write(text)
                f.write("\nEnd.")
                f.write("\nEnd.")
                f.close()
                tk.messagebox.showinfo('FYI', 'File Saved!')
            else:
                pass

    def saveMultipleFiles(self, text):
        textList = text.split('\n')
        textList.pop()
        textList.pop()
        fileCount = 0
        self.filename = tk.filedialog.asksaveasfilename(
            initialdir=base_folder)
        fileNameList = self.filename.split("/")
        fileName = fileNameList[len(fileNameList) - 1]
        if (isinstance(self.filename, str) and self.filename != ''):
            for line in textList:
                f = open(
                    self.filename +
                    "_" +
                    str(fileCount) +
                    '.kyx',
                    'w')
                f.write(
                    "Theorem \" " +
                    fileName +
                    "_" +
                    str(fileCount) +
                    ' \"\n\nProblem\n\n')
                f.write(line)
                f.write("\n\nEnd.")
                f.write("\nEnd.")
                f.close()
                fileCount += 1
        else:
            pass
        tk.messagebox.showinfo(
            'Info',
            str(fileCount) +
            " translation files created.")

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
        inputs = self.loadedText.get('1.0', tk.END)
        transList = []
        if inputs == "":
            transList.append("Please enter an expression to convert.")
        else:
            if(self.interpVar.get() == 1):
                transList = self.runMultipleInterpretations(inputs)
            else:
                transList = self.runMultipleTranslations(inputs)
        for transl in transList:
            self.translatedText.insert(tk.END, transl)
            self.translatedText.insert(tk.END, "\n")
        self.translatedText.config(state=tk.DISABLED)
        self.translationHistory.refreshHistory()

    def interpOn(self):
        print(self.interpVar.get())
        if self.interpVar.get() == 1:
            self.interpretButton['text'] = 'Interp On'
        else:
            self.interpretButton['text'] = 'Interp Off'

    def interpret(self):
        self.translatedText.config(state=tk.NORMAL)
        self.clear(self.translatedText)
        inputs = self.loadedText.get('1.0', tk.END)
        transList = []
        if inputs == "":
            transList.append("Please enter an expression to convert.")
        else:
            transList = self.runMultipleInterpretations(inputs)
        for transl in transList:
            self.translatedText.insert(tk.END, transl)
            self.translatedText.insert(tk.END, "\n\n")
        self.translatedText.config(state=tk.DISABLED)
        self.translationHistory.refreshHistory()

    def clear(self, btn=None):
        if btn is not None:
            btn.delete('1.0', tk.END)
        else:
            self.loadedText.delete('1.0', tk.END)
            self.translatedText.delete('1.0', tk.END)

    def copyToClipboard(self):
        self.translatedText.clipboard_clear()
        self.translatedText.clipboard_append(
            self.translatedText.get('1.0', 'end-1c'))

    def runTranslation(self, input):
        return runGUI('<stdin>', input)

    def clearInput(self, inputList):
        for input in inputList:
            if ('#' in input):
                inputList.remove(input)
            elif (input == '\n' or input == ''):
                inputList.remove(input)
        return inputList

    def getHistory(self):
        return self.history

    def clearHistory(self):
        self.history = {}

    def runMultipleTranslations(self, inputs):
        inputList = inputs.split('\n')
        inputList.pop()
        outputList = []
        for input in inputList:
            if ('#' in input):
                continue
            elif (input == '\n' or input == ''):
                continue
            else:
                outputList.append(runGUI('<stdin>', input))

        self.history[repr(self.clearInput(inputList))] = outputList
        return outputList

    def runMultipleInterpretations(self, inputs):
        inputList = inputs.split('\n')
        inputList.pop()
        outputList = []
        for input in inputList:
            if ('#' in input):
                continue
            elif (input == '\n' or input == ''):
                continue
            else:
                outputList.append(runInterpGUI('<stdin>', input))

        self.history[repr(self.clearInput(inputList))] = outputList
        return outputList

    def setTranslationHistory(self, translationHistory):
        self.translationHistory = translationHistory

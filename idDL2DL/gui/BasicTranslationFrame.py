import os
import sys
import tkinter as tk

from NotePage import BasicNotepage
from idDL2DL.gui.Tools import myLabelFrame, myButton, myTextFrame, myScrollBar, myFrame

sys.path.append('../')
from Interval.Core.RunProgram import runGUI

base_folder = os.path.join(os.path.dirname(__file__, ), '..')


class BasicTranslation(BasicNotepage):
    def BuildPage(self):
        # --- Translation frame ---
        f1 = myLabelFrame(self, 0, 0, colspan=2, rowspan=3, text='Enter text for translation')
        f1.pack(side='top', fill='both', expand=True)

        controls = myFrame(f1, side='bottom', fill='both', expand=True)
        txtFrame = myFrame(f1, side='top', fill='both', expand=True)

        self.translationText = myTextFrame(txtFrame, row=0, col=0, width=99, height=13, stick='W', colspan=100)
        self.translationScrollBar = myScrollBar(txtFrame, 0, 101, 'ns')
        self.translationText.config(yscrollcommand=self.translationScrollBar.set)
        self.translationScrollBar.config(command=self.translationText.yview)

        self.translationButton = myButton(controls, row=1, col=0, command=self.translate, rowspan=2, colspan=1,
                                          sticky='W', text='Translate', bg='white', fg='black', font=('Arial', 12),
                                          relief='raised')

        # --- Translated Frame ---
        f2 = myLabelFrame(self, row=4, col=0, colspan=2, rowspan=3, text='Translated Text')
        f2.pack(side='top', fill='both', expand=True)

        controls2 = myFrame(f2, side='bottom', fill='both', expand=True)
        txtFrame2 = myFrame(f2, side='top', fill='both', expand=True)

        self.translatedText = myTextFrame(txtFrame2, row=4, col=0, width=99, height=13, stick='W', colspan=100)
        self.translatedText.config(state=tk.DISABLED)
        self.scrollBar2 = myScrollBar(txtFrame2, row=4, col=100, stick='ns')
        self.translatedText.config(yscrollcommand=self.scrollBar2.set)
        self.scrollBar2.config(command=self.translatedText.yview)

        self.clearButton = myButton(controls2, row=5, col=0, command=self.clear, rowspan=1, colspan=1, sticky='W',
                                    text='Clear', bg='white', fg='black', font=('Arial', 12), relief='raised')
        self.clipboardButton = myButton(controls2, row=5, col=1, command=self.copyToClipboard, rowspan=1, colspan=1,
                                        sticky='W', text='Copy', bg='white', fg='black', font=('Arial', 12),
                                        relief='raised')
        self.saveButton = myButton(controls2, row=5, col=2, command=self.saveAs, rowspan=1, colspan=1,
                                   sticky='W', text='Save', bg='white', fg='black', font=('Arial', 12),
                                   relief='raised')

    def saveAs(self):
        text = self.translatedText.get('1.0', 'end')
        nLines = text.count('\n') - 1
        multipleFiles = False
        if (nLines <= 0):
            tk.messagebox.showerror('Error', 'Nothing to translate!')
            return
        elif (nLines > 1):
            multipleFiles = tk.messagebox.askyesnocancel("Warning!", "Create multiple files for KMX?")
            if (multipleFiles):
                self.saveMultipleFiles(text)
            if (not (multipleFiles)):
                tk.messagebox.showwarning("Warning!", "All translations will be written to a single file!")
        if (nLines == 1 or not (multipleFiles)):
            self.filename = tk.filedialog.asksaveasfilename(initialdir=base_folder, defaultextension='.kyx')
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
        self.filename = tk.filedialog.asksaveasfilename(initialdir=base_folder)
        fileNameList = self.filename.split("/")
        fileName = fileNameList[len(fileNameList) - 1]
        if (isinstance(self.filename, str) and self.filename != ''):
            for line in textList:
                f = open(self.filename + "_" + str(fileCount) + '.kyx', 'w')
                f.write("Theorem \" " + fileName + "_" + str(fileCount) + ' \"\n\nProblem\n\n')
                f.write(line)
                f.write("\n\nEnd.")
                f.write("\nEnd.")
                f.close()
                fileCount += 1
        else:
            pass
        tk.messagebox.showinfo('Info', str(fileCount) + " translation files created.")

    def translate(self):
        self.translatedText.config(state=tk.NORMAL)
        self.clear(self.translatedText)
        inputs = self.translationText.get('1.0', tk.END)
        transList = []
        if inputs == "":
            transList.append("Please enter an expression to convert.")
        else:
            transList = self.runMultipleTranslations(inputs)
        for transl in transList:
            self.translatedText.insert(tk.END, transl)
            self.translatedText.insert(tk.END, "\n")
        self.translatedText.config(state=tk.DISABLED)

    def clear(self, btn=None):
        if btn is not None:
            btn.delete('1.0', tk.END)
        else:
            self.translationText.delete(0, tk.END)
            self.translatedText.delete('1.0', tk.END)

    def copyToClipboard(self):
        self.translatedText.clipboard_clear()
        self.translatedText.clipboard_append(self.translatedText.get('1.0', 'end-1c'))

    def runTranslation(self, input):
        return runGUI('<stdin>', input)

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
        return outputList

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from RunProgram import runGUI
import os
from PIL import Image
from PIL import ImageTk
import tkinter.messagebox as MessageBox

base_folder = os.path.dirname(__file__)
bgPath = base_folder + '/Resources/background2.png'


# bluebutton_path = base_folder + '/Resources/blueButton2.png'
#
# def openfile():
#     return fd.filedialog.askopenfilename()
#
# def select_file():
#     filetypes = (
#         ('text files', '*.txt'),
#         ('All files', '*.*')
#     )
#     filename = fd.askopenfilename(
#         title='Open a file',
#         initialdir='/home/jaime/Programming/ResearchKlee/Parser/Interval',
#         filetypes=filetypes)
#     showinfo(
#         title='Selected File',
#         message=filename
#     )
#
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
#
# root = tk.Tk()
# root.title("idDL2dDL")
# root.geometry('800x450')
#
# bg = tk.PhotoImage(file=bg_path)
# photoBlueButton = ImageTk.PhotoImage(file= bluebutton_path)
#
# # Create a canvas
# my_canvas = tk.Canvas(root, width=800, height=500)
# my_canvas.pack(fill="both", expand=True)
#
# # Set image in canvas
# my_canvas.create_image(0,0, image=bg, anchor="nw")
#
# def runTranslation(input):
#     return runGUI('<stdin>', input)
#
# def translate():
#     translatedTxt.delete('1.0',tk.END)
#     input = translationTxt.get()
#     if input == "":
#         transl = "Please enter an expression to convert."
#     else:
#         transl,catcher = runTranslation(input)
#     translatedTxt.insert(tk.END,transl)
#     translationTxt.delete(tk.END)
#
# my_canvas.create_text(65, 20, text="Interval dDL: ", font=("Helvetica", 15), fill="black")
#
# translationTxt = tk.Entry(root,width=80)
# translationTxt_window = my_canvas.create_window(130, 8, anchor="nw", window=translationTxt)
#
# st = ttk.Style()
# st.configure('W.TButton', background='white', foreground='black', font=('Arial', 14 ))
# #transButton = tk.Button(root, text="Translate",command=translate,image=photoBlueButton,width=60, height = 25,borderwidth=0,highlightthickness=0)
# transButton = ttk.Button(root, text="Translate",command=translate,width=10, style='W.TButton')
# transButton_window = my_canvas.create_window(370, 60, anchor="nw", window=transButton)
#
# my_canvas.create_text(65, 140, text="dDL: ", font=("Helvetica", 15), fill="black")
#
# translatedTxt = tk.Text(root,width = 80,height=2)
# translatedTxt_window = my_canvas.create_window(130, 120, anchor="nw", window=translatedTxt)


# root.mainloop()

class IntervalInterface(tk.Frame):
    def __init__(self, root, title):
        tk.Frame.__init__(self, root)
        self.root = root
        self.title = title
        self.root.title = title

        master = root
        master.rowconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.config(padx=5, pady=5)

        frame1 = ttk.Frame(master, padding=(5, 5, 5, 5))
        frame1.grid(row=0, column=0, sticky="NSEW")
        frame1.rowconfigure(2, weight=1)
        frame1.columnconfigure(0, weight=1)

        # ------------ Notebook with all camera control pages -----------
        frame1 = ttk.Frame(master, padding=(5, 5, 5, 5))
        frame1.grid(row=0, column=0, sticky="NSEW")
        frame1.rowconfigure(2, weight=1)
        frame1.columnconfigure(0, weight=1)
        self.AlwaysPreview = False

        n = ttk.Notebook(frame1, padding=(5, 5, 5, 5))
        n.grid(row=1, column=0, rowspan=2, sticky=(tk.N, tk.E, tk.W, tk.S))
        n.columnconfigure(0, weight=1)
        n.enable_traversal()

        self.basicTranslation = BasicTranslation(n)
        n.add(self.basicTranslation, text='Basic', underline=0)

class BasicNotepage(tk.Frame):
    def __init__(self, parent, camera=None, cancel=None, ok=None,
                 rowconfig=False, colconfig=True, data=None):
        ttk.Frame.__init__(self, parent, padding=(10, 10, 10, 10))
        self.grid(sticky='NSEW')
        if colconfig is True:
            self.columnconfigure(0, weight=1)
        if rowconfig is True:
            self.rowconfigure(0, weight=1)
        self.parent = parent
        self.CancelButton = cancel
        self.OkButton = ok
        self.data = data
        self.init = True  # disable SomethingChanged
        self.BuildPage()
        self.init = False
        self.Changed = False

    def BuildPage(self):  # MUST Overide this!
        UnderConstruction(self)

    def SomethingChanged(self, val):  # Can override but call super!
        if self.init: return
        self.Changed = True
        if self.CancelButton != None:
            self.CancelButton.config(state='normal')  # '!disabled')
            if self.OkButton != None:
                self.OkButton.config(text='Save')

    def SaveChanges(self):  # MUST override this!
        MessageBox.showwarning("SaveChanges", "SaveChanges not implemented!")

class BasicTranslation(BasicNotepage):
    def BuildPage(self):
        f1 = myLabelFrame(self, 'Enter text for translation', 0, 0, span=2)
        self.textEntry = myEntryFrame(f1, 10, 0, 0, 'W')





def UnderConstruction(window):
    tk.Label(window, text='UNDER CONSTRUCTION', font=('Arial', 14, ('bold')),
             anchor='center').grid(row=0, column=0, sticky='EW')


def myLabelFrame(f, txt, row, col, stick='NEWS', py=5, span=1, pad=(5, 5, 5, 5)):
    l = ttk.LabelFrame(f, text=txt, padding=pad)
    l.grid(row=row, column=col, sticky=stick, columnspan=span, pady=py)
    return l


def myEntryFrame(f, width, row, col, stick='W', span=1, pad=(5, 5, 5, 5)):
    translationTxt = tk.Entry(f, width=80)
    translationTxt.grid(row=row, column=col, sticky=stick, columnspan=span)

    #     ## Create Background Canvas ##
    #     self.background = tk.PhotoImage(file=bgPath)
    #     self.rootCanvas = tk.Canvas(self.root, width=1280, height=791)
    #     self.rootCanvas.pack(fill="both", expand=True)
    #     self.rootCanvas.create_image(0,0, image=self.background, anchor="nw")
    #
    #     ## labels ##
    #     self.createLabel(self.rootCanvas,80, 50,"Interval dDL: ", ("Helvetica", 17), fill = "white")
    #     self.createLabel(self.rootCanvas,65,250,"dDL: ",("Helvetica",17),"white")
    #
    #     ## Windows ##
    #     self.createEntry(self.root,self.rootCanvas,170,37,80,"nw")
    #     self.createText(self.root,self.rootCanvas,170,237,80,1,"nw")
    #
    # def createLabel(self,canvas,x,y,text,font,fill):
    #     canvas.create_text(x,y,text=text,font=font,fill=fill)
    #
    # def createEntry(self,frame,canvas,x,y,width,anchor):
    #     createdEntry = tk.Entry(frame,width=width)
    #     canvas.create_window(x,y,anchor=anchor,window=createdEntry)
    #
    # def createText(self,frame,canvas,x,y,width,height,anchor):
    #     createdText = tk.Text(frame,width = width,height=height)
    #     canvas.create_window(x, y, anchor=anchor, window=createdText)


win = tk.Tk()
app = IntervalInterface(win, title="idl")
win.minsize(1024, 768)
win.mainloop()

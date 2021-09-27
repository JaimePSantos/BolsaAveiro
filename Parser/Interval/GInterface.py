import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from RunProgram import runGUI
import os
from PIL import Image
from PIL import ImageTk

base_folder = os.path.dirname(__file__)
#print(base_folder)
bg_path = base_folder + '/Resources/background.png'
bluebutton_path = base_folder + '/Resources/blueButton2.png'

def openfile():
    return fd.filedialog.askopenfilename()

def select_file():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/home/jaime/Programming/ResearchKlee/Parser/Interval',
        filetypes=filetypes)
    showinfo(
        title='Selected File',
        message=filename
    )

def open_text_file():
    # file type
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    # show the open file dialog
    f = fd.askopenfile(filetypes=filetypes)
    # read the text file and show its content on the Text
    #text.insert('1.0', f.readlines())

root = tk.Tk()
root.title("idDL2dDL")
root.geometry('800x450')

bg = tk.PhotoImage(file=bg_path)
photoBlueButton = ImageTk.PhotoImage(file= bluebutton_path)

# Create a canvas
my_canvas = tk.Canvas(root, width=800, height=500)
my_canvas.pack(fill="both", expand=True)

# Set image in canvas
my_canvas.create_image(0,0, image=bg, anchor="nw")

def runTranslation(input):
    return runGUI('<stdin>', input)

def translate():
    translatedTxt.delete('1.0',tk.END)
    input = translationTxt.get()
    if input == "":
        transl = "Please enter an expression to convert."
    else:
        transl,catcher = runTranslation(input)
    translatedTxt.insert(tk.END,transl)
    translationTxt.delete(tk.END)

my_canvas.create_text(65, 20, text="Interval dDL: ", font=("Helvetica", 15), fill="black")

translationTxt = tk.Entry(root,width=80)
translationTxt_window = my_canvas.create_window(130, 8, anchor="nw", window=translationTxt)

st = ttk.Style()
st.configure('W.TButton', background='white', foreground='black', font=('Arial', 14 ))
#transButton = tk.Button(root, text="Translate",command=translate,image=photoBlueButton,width=60, height = 25,borderwidth=0,highlightthickness=0)
transButton = ttk.Button(root, text="Translate",command=translate,width=10, style='W.TButton')
transButton_window = my_canvas.create_window(370, 60, anchor="nw", window=transButton)

my_canvas.create_text(65, 140, text="dDL: ", font=("Helvetica", 15), fill="black")

translatedTxt = tk.Text(root,width = 80,height=2)
translatedTxt_window = my_canvas.create_window(130, 120, anchor="nw", window=translatedTxt)


root.mainloop()

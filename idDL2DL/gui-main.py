import tkinter as tk

from idDL2DL.gui.IntervalInterface import IntervalInterface

win = tk.Tk()
app = IntervalInterface(win, title="idDL2DL")
win.maxsize(900, 768)
win.mainloop()

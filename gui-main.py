import tkinter as tk

from gui.IntervalInterface import IntervalInterface

win = tk.Tk()
app = IntervalInterface(win, title="idDL2DL")
win.maxsize(1000, 968)
win.mainloop()

from tkinter import Tk
from tkinter import PhotoImage

tk = Tk()
tk.title('SORIDAMA')
tk.iconphoto(False, PhotoImage(file= './data/icon.png'))
tk.minsize(400, 300)

tk.mainloop()
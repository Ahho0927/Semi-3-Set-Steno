import tkinter

is_running = True

ui = tkinter.Tk()
ui.title("SORIDAMA")
ui.geometry("1200x700")

def _Enable():
    is_running = not is_running

submit_button = tkinter.Button(ui, text="Enable", command=_Enable)
tkinter.Button()
submit_button.pack()



ui.mainloop()

import ctypes

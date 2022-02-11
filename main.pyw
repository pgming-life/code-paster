from gui_application import *

window = gui.tk.Tk()
app = GuiApplication(master=window, paths=[], exts=[])
app.mainloop()
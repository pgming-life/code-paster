import gui_application as app_main

# jsonデータの要素取得
rate_path = [] if app_main.jd.load_error else app_main.jd.data_json['inputbox'][app_main.jd.tag_list['path']]
rate_ext = [] if app_main.jd.load_error else app_main.jd.data_json['inputbox'][app_main.jd.tag_list['ext']]

# Tkinter起動
window = app_main.gui.tk.Tk()
app = app_main.GuiApplication(master=window, paths=rate_path, exts=rate_ext)
app.mainloop()

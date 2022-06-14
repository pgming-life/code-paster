from tkinter import *

splash = Tk()
splash.overrideredirect(1)
ww=splash.winfo_screenwidth()
wh=splash.winfo_screenheight()
splash.geometry("500x300+"+str((ww-500)//2)+"+"+str((wh-300)//2))
label = Label(splash, text="起動中...", font=("メイリオ", "20", "bold"), fg="gray")
label.place(x=200, y=135)

def interval():
	splash.destroy()

# スプラッシュインターバル
splash.after(5000, interval)
mainloop()

import gui_application as app_main
import code_txt_data as ctd
import historical_data as hd

# txtファイルを確認・作成
ctd.code_txt_create()

# historyフォルダを確認・作成
hd.history_folder_create()

# jsonデータの要素取得
rate_path = [] if app_main.jd.load_error else app_main.jd.data_json['inputbox'][app_main.jd.tag_list['path']]
rate_ext = [] if app_main.jd.load_error else app_main.jd.data_json['inputbox'][app_main.jd.tag_list['ext']]

# Tkinter起動
window = app_main.mgt.tk.Tk()
app = app_main.GuiApplication(master=window, paths=rate_path, exts=rate_ext)
app.mainloop()
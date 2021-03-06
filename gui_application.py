from processing_target import *
import json_data as jd
import widget_placement as wp
import app_string as astr

class GuiApplication(mgt.tk.Frame):
    def __init__(self, master=None, paths=[], exts=[]):
        window_width = wp.window_width
        window_height = wp.window_height
        super().__init__(master, width=window_width, height=window_height)

        self.master = master
        self.master.title(astr.str_window_title)
        self.master.minsize(window_width, window_height)
        self.pack()

        self.input_path = []
        self.input_ext = []
        self.paths = paths
        self.exts = exts

        # 処理ターゲット
        self.target = ProcessingTarget(
            self,
            label_process_x=wp.label_process_x,
            label_process_y=wp.label_process_y,
            label_move_x=wp.label_move_x,
            label_move_y=wp.label_move_y,
            label_move_len=wp.label_move_len,
            bar_x=wp.bar_x,
            bar_y=wp.bar_y,
            bar_len=wp.bar_len,
        )

        # ウィジェット作成
        self.create_widgets()

    # ウィジェット作成
    def create_widgets(self) -> None:
        # パスウィジェットの位置、幅、数
        path_label_x = wp.path_label_x
        path_label_y = wp.path_label_y
        path_box_width = wp.path_box_width
        path_box_x = wp.path_box_x
        path_box_y = wp.path_box_y
        path_box_y_margin = wp.path_box_y_margin
        path_box_num = wp.path_box_num

        # 拡張子ウィジェットの位置、幅、数
        ext_label_x = wp.ext_label_x
        ext_label_y = wp.ext_label_y
        ext_box_width = wp.ext_box_width
        ext_box_x = wp.ext_box_x
        ext_box_y = wp.ext_box_y
        ext_box_y_margin = wp.ext_box_y_margin
        ext_box_num = wp.ext_box_num

        # ラベル作成
        self.label_note = mgt.tk.Label(text=astr.str_label_note)
        self.label_note.place(x=wp.label_note_x, y=wp.label_note_y)
        self.label_path = mgt.tk.Label(text=astr.str_label_path)
        self.label_path.place(x=path_label_x, y=path_label_y)
        self.label_ext = mgt.tk.Label(text=astr.str_label_ext)
        self.label_ext.place(x=ext_label_x, y=ext_label_y)

        # インプットボックス作成
        self.input_path.append(mgt.tk.Entry(width=path_box_width))
        self.input_path[0].place(x=path_box_x, y=path_box_y)
        if self.paths:
            self.input_path[0].insert(mgt.tk.END, self.paths[0])
        p = mgt.counter(path_box_y, path_box_y_margin)
        for i in range(1, path_box_num):
            p.count()
            self.input_path.append(mgt.tk.Entry(width=path_box_width))
            self.input_path[i].place(x=path_box_x, y=p.result())
            if i < len(self.paths):
                self.input_path[i].insert(mgt.tk.END, self.paths[i])
        for i in self.input_path:
            i.bind("<Key>", self.search_start_sck)
        self.input_ext.append(mgt.tk.Entry(width=ext_box_width))
        self.input_ext[0].place(x=ext_box_x, y=ext_box_y)
        if self.exts:
            self.input_ext[0].insert(mgt.tk.END, self.exts[0])
        p = mgt.counter(ext_box_y, ext_box_y_margin)
        for i in range(1, ext_box_num):
            p.count()
            self.input_ext.append(mgt.tk.Entry(width=ext_box_width))
            self.input_ext[i].place(x=ext_box_x, y=p.result())
            if i < len(self.exts):
                self.input_ext[i].insert(mgt.tk.END, self.exts[i])
        for i in self.input_ext:
            i.bind("<Key>", self.search_start_sck)

        # ボタン作成
        self.button_start = mgt.tk.ttk.Button(self, text=astr.str_button_start, padding=10, command=self.get_input)
        self.button_start.place(x=wp.button_start_x, y=wp.button_start_y)
    
    # 処理開始ショートカットキー
    def search_start_sck(self, event) -> None:
        # Enterキーが押された場合
        if event.keysym == 'Return':
            self.get_input()

    # 入力文字列取得
    def get_input(self) -> None:
        paths = []
        exts = []
        for i in self.input_path:
            if i.get() != "":
                paths.append(i.get())
        for i in self.input_ext:
            if i.get() != "":
                exts.append(i.get())

        # 入力データ保存
        jd.save_input_data(paths, exts)

        # ターゲット処理開始
        if paths and exts:
            self.target_start(paths, exts)
        else:
            self.target.label_progress.update(astr.str_input_none)

    # ターゲット処理開始
    def target_start(self, paths: list[str], exts: list[str]) -> None:
        # スレッド重複処理の防止
        if not self.target.is_running:
            self.target.label_progress_move.is_loop = True
            self.target.label_progress_move.start(astr.str_progress_move)
            self.target.progressbar.reset()
            self.target.start(paths, exts)
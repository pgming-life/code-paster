from practical_package import module_gui_text as gui

class ProcessingTarget:
    def __init__(self, self_root, label_process_x, label_process_y, label_move_x, label_move_y, label_move_len, bar_x, bar_y, bar_len):
        self.is_running = False
        self.label_progress = gui.ProgressLabel(label_process_x, label_process_y)
        self.label_progress_move = gui.MoveProgressLabel(label_move_x, label_move_y, label_move_len)
        self.progressbar = gui.Progressbar(self_root, bar_x, bar_y, bar_len)

    # 処理ターゲット
    def target(self, raw_paths, raw_exts):
        self.is_running = True

        # 処理内容
        # ▼▼▼▼▼▼
        # テスト
        len = 100
        self.progressbar.set.configure(maximum=len)
        for i in range(len):
            self.label_progress.update(i)
            self.progressbar.update(i)
            gui.time.sleep(0.01)
        # ▲▲▲▲▲▲

        # スレッド終了処理
        self.is_running = False
        self.label_progress_move.is_loop = False

        # ラベルリセット
        self.label_progress.end("", is_dt=True, is_timer=True)
        self.label_progress_move.end()

    # スレッドスタート
    def start(self, paths, exts):
        self.thread_target = gui.threading.Thread(target = self.target, args=(paths, exts,))
        self.thread_target.setDaemon(True)
        self.thread_target.start()

from practical_package import module_gui_text as gui
import test
import main_logic

class ProcessingTarget:
    def __init__(self, self_root, label_process_x, label_process_y, label_move_x, label_move_y, label_move_len, bar_x, bar_y, bar_len):
        self.is_running = False
        self.label_progress = gui.ProgressLabel(label_process_x, label_process_y)
        self.label_progress_move = gui.MoveProgressLabel(label_move_x, label_move_y, label_move_len)
        self.progressbar = gui.Progressbar(self_root, bar_x, bar_y, bar_len)    

    # スレッドスタート
    def start(self, paths, exts):
        # テスト
        #self.thread_target = gui.threading.Thread(target=test.start, args=(self, gui))
        
        # 本処理
        self.thread_target = gui.threading.Thread(target=main_logic.start, args=(self, gui, paths, exts,))
        
        self.thread_target.setDaemon(True)
        self.thread_target.start()

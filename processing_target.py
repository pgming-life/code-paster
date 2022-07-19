from practical_package import module_gui_text as mgt
import debug_test
import main_logic

class ProcessingTarget:
    def __init__(self, self_root, label_process_x: int, label_process_y: int, label_move_x: int, label_move_y: int, label_move_len: int, bar_x: int, bar_y: int, bar_len: int):
        self.is_running = False
        self.label_progress = mgt.ProgressLabel(label_process_x, label_process_y)
        self.label_progress_move = mgt.MoveProgressLabel(label_move_x, label_move_y, label_move_len)
        self.progressbar = mgt.Progressbar(self_root, bar_x, bar_y, bar_len)    

    # スレッドスタート
    def start(self, paths: list[str], exts: list[str]) -> None:
        # テスト
        #self.thread_target = mgt.threading.Thread(target=debug_test.start, args=(self, mgt))
        
        # 本処理
        self.thread_target = mgt.threading.Thread(target=main_logic.start, args=(self, mgt, paths, exts,))
        
        self.thread_target.setDaemon(True)
        self.thread_target.start()
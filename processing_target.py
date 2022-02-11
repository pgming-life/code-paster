from practical_package import module_gui_text as gui

class ProcessingTarget:
    def __init__(self, self_root, label_process_x, label_process_y, label_move_x, label_move_y, label_move_len, bar_x, bar_y, bar_len):
        self.label_progress = gui.ProgressLabel(label_process_x, label_process_y)
        self.label_progress_move = gui.MoveProgressLabel(label_move_x, label_move_y, label_move_len)
        self.progressbar = gui.Progressbar(self_root, bar_x, bar_y, bar_len)

    def target(self):
        pass

    def start(self):
        self.thread_target = gui.threading.Tread(target = self.target, args=())
        self.thread_target.setDaemon(True)
        self.thread_target.start()
# テスト
def start(self_root, mgt: "module_gui_text") -> None:
    # スレッド開始処理
    self_root.is_running = True

    #▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼ 処理内容 ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
    len = 100
    self_root.progressbar.set.configure(maximum=len)
    for i in range(len):
        self_root.label_progress.update(i)
        self_root.progressbar.update(i)
        mgt.time.sleep(0.01)
    #▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲ 処理内容 ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

    # スレッド終了処理
    self_root.is_running = False
    self_root.label_progress_move.is_loop = False

    # ラベルリセット
    self_root.label_progress.end("", is_dt=True, is_timer=True)
    self_root.label_progress_move.end()

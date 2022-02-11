import glob as g
from natsort import natsorted
import app_string as astr
import code_txt_data as ctd

def start(self_root, gui, raw_paths, raw_exts):
    # スレッド開始処理
    self_root.is_running = True

    #▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼ 処理内容 ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
    time_interval = 2
    is_ok, text, line = ctd.code_txt_read()
    if is_ok:
        is_ok = False
        if line != []:
            for i in [i for i in line if i != ""]:
                if i.replace(" ", "").replace("\t", "") != "":
                    is_ok = True
                    break
        if is_ok:
            is_error = False
            output_error = []

            # ";"で区切られる複数の検索対象の抽出
            paths = []
            exts = []
            for i in raw_paths:
                if ";" in i:
                    s = i.split(";")
                    for j in s:
                        if j != "":
                            paths.append(j)
                else:
                    paths.append(i)
            for i in raw_exts:
                if ";" in i:
                    s = i.split(";")
                    for j in s:
                        if j != "":
                            exts.append(j)
                else:
                    exts.append(i)

            # 動的３次元配列のヒープ領域確保(パス×拡張子)
            list_file = [[[] for _ in exts] for _ in paths]

            # ファイルリスト作成(パス以降の階層を再帰的に探索)
            self_root.label_progress.update(astr.str_create_file_list)
            for num_path, rate_path in enumerate(paths):
                for num_ext, rate_ext in enumerate(exts):
                    if rate_path[0:3] != "\\/*":    # このパターン以外を受け付ける(終了できないデッドロック状態に陥るため)
                        if rate_ext[0:2] == "*.":   # このパターンだけ受け付ける(「*」だけだとフォルダ名も検索してしまうので「*」と「.」でセットで受け付ける)
                            # 当該パス・相対パス・絶対パス対応
                            list_file[num_path][num_ext] = g.glob("{0}{1}".format("**/" if rate_path == "\\" else rate_path[1:] + "/**/" if rate_path[0] == "\\" else rate_path + "/**/", rate_ext), recursive=True)

            # int型正規表現ソート(自然順ソート)
            for num_path, rate_path in enumerate(list_file):
                for num_ext, rate_ext in enumerate(rate_path):
                    list_file[num_path][num_ext] = natsorted(rate_ext)

            # エラーログ出力
            if is_error:
                self_root.label_progress.update(astr.str_read_error)
                gui.time.sleep(time_interval)
                self_root.label_progress.update(astr.str_read_error_output)
                gui.time.sleep(time_interval)
                with open(astr.file_error, 'w') as f:
                    self_root.progressbar.set.configure(maximum=len(output_error))
                    for num_line, rate_line in enumerate(output_error):
                        self_root.progressbar.update(num_line)
                        f.writelines("{}\n".format(rate_line))
                self_root.label_progress.update(astr.str_open_error_log)
                try:
                    # cmdから非同期でエクスプローラー経由で開く
                    gui.subprocess.Popen(args=['explorer', astr.file_error], shell=True)
                except gui.subprocess.CalledProcessError:
                    self_root.label_progress.update(astr.str_open_log_error)
                    gui.time.sleep(time_interval)
                    self_root.label_progress.update(astr.str_end)
                    gui.time.sleep(time_interval)
        else:
            self_root.label_progress.update(astr.str_read_none_txt)
            gui.time.sleep(time_interval)
            self_root.label_progress.update(astr.str_end)
            gui.time.sleep(time_interval)
    else:
        self_root.label_progress.update(text)
        gui.time.sleep(time_interval)
        self_root.label_progress.update(astr.str_read_error_txt)
        gui.time.sleep(time_interval)
        self_root.label_progress.update(astr.str_end)
        gui.time.sleep(time_interval)
    #▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲ 処理内容 ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

    # スレッド終了処理
    self_root.is_running = False
    self_root.label_progress_move.is_loop = False

    # ラベルリセット
    self_root.label_progress.end("", is_dt=True, is_timer=True)
    self_root.label_progress_move.end()
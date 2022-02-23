import glob as g
from natsort import natsorted
import app_string as astr
import code_txt_data as ctd
import historical_data as hd

def start(self_root, mgt, raw_paths, raw_exts):
    # スレッド開始処理
    self_root.is_running = True

    #▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼ 処理内容 ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
    time_interval = 2
    is_ok, text, data = ctd.code_txt_read()
    if is_ok:
        if data != "":
            is_error = False
            output_error = []

            # 現在コードをヒストリカルデータに追加
            hd.write_history(data)

            # ヒストリカルデータの読み込み
            hist = hd.get_history()

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

            # 対象ファイルへペースト
            self_root.label_progress.update(astr.str_paste)
            for num_path, rate_path in enumerate(paths):
                for num_ext, rate_ext in enumerate(exts):
                    if list_file[num_path][num_ext]:
                        self_root.progressbar.set.configure(maximum=len(list_file[num_path][num_ext]))
                        for num_file, rate_file in enumerate(list_file[num_path][num_ext]):
                            self_root.progressbar.update(num_file)
                            reader = mgt.file_readlines(rate_file)
                            if reader.is_ok:
                                # ヒストリカルデータに一致するテキストを削除
                                output = []
                                is_second = False
                                for i in hist.line:
                                    num = 0
                                    cache = []
                                    lines = output if is_second else reader.line
                                    for j in lines:
                                        cache.append(j)
                                        if j.replace(" ", "").replace("\t", "") == i[num].format(mgt.os.path.basename(rate_file)).replace(" ", "").replace("\t", ""):
                                            num += 1
                                            if num == len(i):
                                                for k in range(len(cache) - num, len(cache))[::-1]:
                                                    del cache[k]
                                                num = 0
                                        else:
                                            num = 0
                                    output = cache

                                # BOM付きutf-8のプリフィックスを削除
                                output[0] = output[0].replace("\ufeff", "")

                                # コードテキストを新規書き込み
                                with open(rate_file, 'w', encoding=reader.encoding) as f:
                                    f.write(data.format(mgt.os.path.basename(rate_file)) + "\n")
                                    for i, j in enumerate(output):
                                        if i != len(output) - 1:
                                            f.writelines("{}\n".format(j))
                                        else:
                                            f.writelines("{}".format(j))
                            else:
                                is_error = True
                                output_error.append(reader.text)

            # ファイル読み込みエラーログ出力
            if is_error:
                self_root.label_progress.update(astr.str_read_error)
                mgt.time.sleep(time_interval)
                self_root.label_progress.update(astr.str_read_error_output)
                mgt.time.sleep(time_interval)
                with open(astr.file_error, 'w') as f:
                    self_root.progressbar.set.configure(maximum=len(output_error))
                    for num_line, rate_line in enumerate(output_error):
                        self_root.progressbar.update(num_line)
                        f.writelines("{}\n".format(rate_line))
                self_root.label_progress.update(astr.str_open_error_log)
                try:
                    # cmdから非同期でエクスプローラー経由で開く
                    mgt.subprocess.Popen(args=['explorer', astr.file_error], shell=True)
                except mgt.subprocess.CalledProcessError:
                    self_root.label_progress.update(astr.str_open_log_error)
                    mgt.time.sleep(time_interval)
                    self_root.label_progress.update(astr.str_end)
                    mgt.time.sleep(time_interval)
        else:
            self_root.label_progress.update(astr.str_read_none_txt)
            mgt.time.sleep(time_interval)
            self_root.label_progress.update(astr.str_end)
            mgt.time.sleep(time_interval)
    else:
        self_root.label_progress.update(text)
        mgt.time.sleep(time_interval)
        self_root.label_progress.update(astr.str_read_error_txt)
        mgt.time.sleep(time_interval)
        self_root.label_progress.update(astr.str_end)
        mgt.time.sleep(time_interval)
    #▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲ 処理内容 ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

    # スレッド終了処理
    self_root.is_running = False
    self_root.label_progress_move.is_loop = False

    # ラベルリセット
    self_root.label_progress.end("", is_dt=True, is_timer=True)
    self_root.label_progress_move.end()

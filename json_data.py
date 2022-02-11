import json
from practical_package import module_gui_text as gui

# タグ辞書
tag_list = {'path' : "path", 'ext' : "extension"}

# データ保存先
file_config = "paster_config.json"

# ファイル確認・作成
def file_write_create():
    lines = []
    lines.append("{")
    lines.append("    \"inputbox\": {")
    lines.append("        \"{}\": [],".format(tag_list['path']))
    lines.append("        \"{}\": []".format(tag_list['ext']))
    lines.append("    }")
    lines.append("}")
    gui.file_create(file_config, lines_string=lines)
file_write_create()

# 入力データ保存
def save_input_data(paths, exts):
    # ファイル確認・作成
    file_write_create()

    # データ加工
    data = gui.cl.OrderedDict()
    data[tag_list['path']] = [i for i in paths]
    data[tag_list['ext']] = [i for i in exts]
    ys = gui.cl.OrderedDict()
    ys["inputbox"] = data

    # JSONファイルへ出力
    with open(file_config, 'w') as fw:
        json.dump(ys, fw, indent=4)

load_error = False
try:
    # JSONファイルからテキストストリームを生成
    with open(file_config, 'r') as f:
        # 辞書オブジェクト(dictionary)を取得(JSON形式)
        data_json = json.load(f)
except Exception:
    # JSON形式で読み込めなかった場合のエラー回避
    load_error = True

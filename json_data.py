import json
from practical_package import module_gui_text as mgt
import app_string as astr

# タグ辞書
tag_list = {'path' : "path", 'ext' : "extension"}

# データ保存先
file_config = astr.file_config

# ファイル確認・作成
def file_write_create() -> None:
    lines = [
        "{",
        "    \"inputbox\": {",
        "        \"{}\": [],".format(tag_list['path']),
        "        \"{}\": []".format(tag_list['ext']),
        "    }",
        "}",
    ]
    mgt.file_create(file_config, string=lines)

# 入力データ保存
def save_input_data(paths: list[str], exts: list[str]) -> None:
    # ファイル確認・作成
    file_write_create()

    # データ加工
    data = mgt.cl.OrderedDict()
    data[tag_list['path']] = [i for i in paths]
    data[tag_list['ext']] = [i for i in exts]
    ys = mgt.cl.OrderedDict()
    ys["inputbox"] = data

    # JSONファイルへ出力
    with open(file_config, 'w') as fw:
        json.dump(ys, fw, indent=4)

# jsonファイル作成
file_write_create()

# ファイル読み込み
load_error = False
try:
    # JSONファイルからテキストストリームを生成
    with open(file_config, 'r') as f:
        # 辞書オブジェクト(dictionary)を取得(JSON形式)
        data_json = json.load(f)
except Exception:
    # JSON形式で読み込めなかった場合のエラー回避
    load_error = True
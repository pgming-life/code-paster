from practical_package import module_gui_text as gui
import app_string as astr

def code_txt_create():
    return gui.file_create(path_file=astr.file_code_txt).is_ok

def code_txt_read():
    code_txt_create()
    is_ok, text, line = gui.file_readlines(path_file=astr.file_code_txt)
    result = gui.cl.namedtuple('result', 'is_ok, text, line')
    return result(is_ok=is_ok, text=text, line=line)

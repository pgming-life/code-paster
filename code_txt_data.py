from practical_package import module_gui_text as mgt
import app_string as astr

def code_txt_create() -> mgt.file_create:
    return mgt.file_create(path_file=astr.file_code_txt).is_ok

def code_txt_read() -> mgt.cl.namedtuple:
    code_txt_create()
    reader = mgt.file_read(path_file=astr.file_code_txt)
    result = mgt.cl.namedtuple('result', 'is_ok, text, data')
    return result(is_ok=reader.is_ok, text=reader.text, data=reader.data)
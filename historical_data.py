import app_string as astr
from practical_package import module_gui_text as mgt

def history_folder_create() -> mgt.folder_create:
    return mgt.folder_create(astr.file_history).is_ok

def write_history(data: str) -> None:
    num = 1
    while 1:
        file = "{0}/{0}_{1}.txt".format(astr.file_history, num)
        if mgt.path_search_continue(file).is_ok:
            reader = mgt.file_read(file)
            if reader.data == data:
                break
        else:
            mgt.file_create(file, data)
            break
        num += 1

def get_history() -> mgt.cl.namedtuple:
    lines = []
    output_error = []
    num = 1
    while 1:
        file = "{0}/{0}_{1}.txt".format(astr.file_history, num)
        if mgt.path_search_continue(file).is_ok:
            reader = mgt.file_readlines(file)
            if reader.is_ok:
                lines.append(reader.line)
            else:
                output_error.append(reader.line)
        else:
            break
        num += 1
   
    result = mgt.cl.namedtuple('result', 'log, line')
    return result(log=output_error, line=lines)
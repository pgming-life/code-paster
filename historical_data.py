import app_string as astr
from practical_package import module_gui_text as mgt

def history_folder_create():
    return mgt.folder_create(astr.file_history).is_ok

def get_history():
    list_data = []
    output_error = []
    num = 0
    while 1:
        file = "{0}/{0}{1}.txt".format(astr.file_history, num + 1)
        if mgt.path_search_continue(file).is_ok:
            reader = mgt.file_readlines(file)
            if reader.is_ok:
                list_data.append(reader.line)
            else:
                output_error.append(reader.text)
        else:
            break
    
    result = mgt.cl.namedtuple('result', 'log, data')
    return result(log=output_error, data=list_data)

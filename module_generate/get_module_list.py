"""get_module_list"""

from pydoc import ModuleScanner

modules = []

def callback(path, modname, desc, modules=modules):  
    if modname and modname[-9:] == '.__init__': 
        modname = modname[:-9]  
    if modname.find('.') < 0 and modname not in modules:
        modules.append(modname) 

def onerror(modname): 
    callback(None, modname, None)

ModuleScanner().run(callback, onerror=onerror)

with open("module_list.txt", 'w', encoding='utf_8') as f:
    for line in modules:
        f.writelines("{}\n".format(line))
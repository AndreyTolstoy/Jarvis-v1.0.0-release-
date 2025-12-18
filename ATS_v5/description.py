from ATS_v5.imports_ import *
from Jarvis.plugin_run import plugin_run


description = {
    "libs" : {"os" : os, "web" : requests, "keyboard" : keyboard, "webb" : webbrowser},
    "utils" : {"print" : print, "plugin" : plugin_run},
    "blocks" : {"if" : {"operation_needed" : True}, "for" : {"operation_needed" : False}, "else" : {"operation_needed" : False}}
}

sys_param = ["range"] #системные параметры, которые будут игнорироваться в проверке переменных (get_from_cache_or_params)
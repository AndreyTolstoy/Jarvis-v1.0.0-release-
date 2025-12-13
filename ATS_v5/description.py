from ATS_v5.imports_ import *


description = {
    "libs" : {"os" : os, "web" : requests, "keyboard" : keyboard, "webb" : webbrowser},
    "utils" : {"print" : print},
    "blocks" : {"if" : {"operation_needed" : True}, "for" : {"operation_needed" : False}, "else" : {"operation_needed" : False}}
}

sys_param = ["range"] #системные параметры, которые будут игнорироваться в проверке переменных (get_from_cache_or_params)
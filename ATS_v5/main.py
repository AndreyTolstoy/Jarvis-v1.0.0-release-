
#?         ==ATS==
#?         ==V4.0==
#?   ==By Andrey Tolstoy==
#?     ==With commits==, сам не ожидал что начну наконец их писать, лол


from ATS_v5.description import *
from ATS_v5 import config #Здесь можно сделат отключаемые параметры, например, логи для просмотра этапов парсинга ATS. Полезно для оптимизации
blocks_True_list = [] #Список успешно выполненных блоков (если if ... == True)
cache = {}
logs = {}
line_count = 1
plugin_params_global = {}
version = "ATS v5.0 "
class ElementsSpliter:
    def __init__(self, structure_name=None, structure_body=None, structure_end=None, structure_data=None, structure_operation=None, params={}, param_handler=None, param_data=None, util=None, util_data=None, block_type=None, block_operation_type=None, to_do=None):
        """Главная структура"""
        self.structure_name = structure_name
        self.structure_body = structure_body
        self.structure_end = structure_end
        self.structure_data = structure_data
        self.structure_operation = structure_operation
        self.to_do = to_do

        """Переменные"""
        self.params = params #Словарь, вмещает в себя все переменные и их значания
        self.param_handler = param_handler
        self.param_data = param_data
        
        """Utils""" #Для операций по типу print
        self.util = util
        self.util_data = util_data

        """Blocks""" #Для блоков if, for. В АTS не будет вложенных блоков, например, if внутри for - нет.
        self.block_type = block_type
        self.block_operation_type = block_operation_type

    def main(self, code):
        self.clear_params()
        if code:
         code = code.strip()
         for line in code.split(";"):
             line = line.strip()
             if line !="":
               line_copy = line
               #?"""==Libs=="""
               if line.split(".")[0] in description["libs"]:
                  self.structure_name = line.split(".")[0]
                  if "then" in line:
                     self.to_do = line.split("then")[1].strip()
                     line = line.split("then")[0].strip()
 
                  line = line.split(":")   
                  if line[0].count(".") > 1: #Если более 1 элемента пути после self.structure_name, то...
                   self.structure_body = line[0].split(".")[1:] #Разбиваем строку по метке self.structure_data, а именно по ":". Далее разделяем первую часть строки на точки. Затем срезаем первый индекс, т.к это наше имя структуры
                   self.structure_end = self.structure_body[-1] #Измеряем длину self.structure_body, отнимаем 1 т.к индексы начинаются с нуля и берем последний элемент пути, это и есть self.structure_end или как в прошлой версии, self.checker
                   self.structure_data = f"'{line[1]}'"
  
                  else:
                   if "'" in line_copy:
                      line = line_copy.split("'")
                   self.structure_end = line[0][len(self.structure_name+"."):] #Получаем всю строку до self.structure_data, узнаем длину имени структуры и убираем равные ему символы
                   try:
                    self.structure_data = f"'{line[1]}'" if line[1] not in self.params else line[1] #Ну тут просто получаем по индексу
                   
                   except:
                      self.structure_data = line[0]

 
                  line = line_copy
               
               #?"""==Blocks==""" 
               elif line.split(" ")[0] in description["blocks"]:
                  blocks = description["blocks"]
                  for name, params in blocks.items():
                   if name == line.split(" ")[0]:
                      self.block_type = name
 
                      if self.block_type == "else":
                        if blocks_True_list == []:
                           errors_output(f"Error: u can`t use else without if")

                        if blocks_True_list[-1][0] == "if" and blocks_True_list[-1][1] == True:
                          self.clear_params()
                          continue #полностью игнорим строку с else, так как если if есть в списке и он успешно выполнен, то нет смысла тратить время исполнения на парсинг ненужного кода
                        
 
                      self.to_do = line.split("{")[1].replace("}", "").replace("*", ";").strip().replace("\n", "")
                      line = line.split(" ")[1]
 
                      if params["operation_needed"] == True: 
                         self.structure_end = line.split("?" if "?" in line else "!")[0]    #!(line[1][:1] if line[1][:1] != "'" else "'" + line[1].split("'")[1] + "'")
                         self.structure_data = line.split("?" if "?" in line else "!")[1]  
                         self.block_operation_type = line.split(self.structure_end)[1].split(self.structure_data)[0]

                      elif self.block_type == "for":
                         self.structure_end = line.split(":")[0]
                         self.structure_data = line.split(":")[1]
                         
 
                      line = line_copy
 
               #?"""==Utils=="""
               elif ":" in line and line.split(":")[0] in description["utils"]:
                  line = line.split(":")
                  self.util = line[0]
                  self.util_data = line_copy[len(self.util)+1:]     
               
               #?"""==Params=="""
               elif "=" in line:
                  line = line.split("=")
                  self.param_handler = line[0].strip()
                  self.param_data = line[1].strip()
                  self.param_data = Parser.get_from_cache_or_params(self, self.param_data)
                  self.params[self.param_handler] = self.param_data
 
               self.full_logs_dump(line)  
               self.logs_load() 
 
               Parser(
                  self.structure_name,
                  self.structure_body,
                  self.structure_end,
                  self.structure_data,
                  self.structure_operation,
                  self.params,
                  self.param_handler,
                  self.param_data,
                  self.util,
                  self.util_data,
                  self.block_type,
                  self.block_operation_type,
                  self.to_do
               ).parser()
               self.clear_params()
 
         self.logs_load() 

    

    def clear_params(self):
        self.structure_name = None
        self.structure_body = None
        self.structure_end = None
        self.structure_data = None
        self.structure_operation = None
        self.param_handler = None
        self.param_data = None
        self.util = None
        self.util_data = None
        self.block_type = None
        self.block_operation_type = None

    def full_logs_dump(self, line): 
       global logs
       logs[line_count] = {
          "Code:" : line,
          "Structure_name:" : self.structure_name,
          "Structure_body:" :  self.structure_body,
          "Structure_end:" : self.structure_end,
          "Structure_data:" : self.structure_data,
          "Structure_operation:" : self.structure_operation,
          "Params:" : self.params,
          "Param_handler:" : self.param_handler,
          "Param_data:" : self.param_data, 
          "Util:" : self.util,
          "Util_data:" : self.util_data,
          "Block_type:" : self.block_type,
          "Block_operation_type:" : self.block_operation_type,
          "To_do:" : self.to_do,
          "Cache:" : cache,
       }
      
       
    def logs_load(self):
       if config.logs():
          for line, data in logs.items():
             print(f"Line {line}:\n")
             for names, values in data.items():
                print("---", names, values)
             
             print("\n=======")
      

   
def errors_output(error):
      print(version, error, "Line:", line_count)
      exit()
      


class Parser(ElementsSpliter):
   def __init__(self, structure_name=None, structure_body=None, structure_end=None, structure_data=None, structure_operation=None, params={}, param_handler=None, param_data=None, util=None, util_data=None, block_type=None, block_operation_type=None, to_do=None):
      super().__init__(structure_name, structure_body, structure_end, structure_data, structure_operation, params, param_handler, param_data, util, util_data, block_type, block_operation_type, to_do)
    
   def parser(self):#Раньше тут весь код обработки был, теперь эта функция беспонтовая и чистов вызывает другие функции) Сделано для того чтобы можно было замерять время выполнения каждого отдельного обработчика для будущей оптимизации
       global line_count
       if self.structure_name:
          self.libs_block()
       
       elif self.util:
         self.utils_block()
 
 
       elif self.block_type:
          self.blocks_block()

       line_count +=1

   def libs_block(self): #Обработчик библиотек
         path = None
         if self.structure_body:
            path = description[self.structure_name]
            for path_element in self.structure_body:
             path = path[path_element]
            
         if self.structure_end:
            """Это блок для получения данных в случае если они хранятся в виде ссылки на данные (переменной). А если есть кавычки, то просто они убираются, так как у нас тип данных и так str"""
            if "'" in self.structure_data:
               self.structure_data = self.structure_data.replace("'", "")

            else:
               self.structure_data = self.get_from_cache_or_params(self.structure_data).replace("'", "")
            

            """Выполнение"""   
            try:
               do = getattr(description["libs"][(path if path else self.structure_name)], self.structure_end)
               #print(f"Функция: {self.structure_name}\nПараметры: {self.structure_data}\n\n")
               try:
                if self.structure_data != "":
                   do = do(self.structure_data)
 
                elif self.structure_data == "":
                   do = do()
               
               except TypeError:
                  do = do(int(self.structure_data))
 
               cache[self.structure_name + "." + (self.structure_body + self.structure_end if self.structure_body else self.structure_end)] = do
               if self.to_do:
                  self.to_do_func()
            
            except Exception as e:
               errors_output(e)

   
   def utils_block(self): #Обработчик print и т.п
      if self.util:
            if self.util_data.split(".")[0] in description["libs"] and self.util_data not in cache: #print:web.get'https://youtube.com'; будет работать, так как он передаст 100% рабочую конструкцию, она обработается и выведится
               util_data_structure = self.util_data.split("'")[0]
               if "+" in self.util_data:
                  util_data_structure  += "+" +  self.util_data.split("+")[1] #для do=...+...

               self.to_do = f"{self.util_data} then do={util_data_structure};\nprint:do;"
               ElementsSpliter.main(self, self.to_do)
               return

            self.util_data = self.get_from_cache_or_params(self.util_data)  
            description["utils"][self.util]("ATS output:", self.util_data)
            

   def blocks_block(self): #Обработчик if & for
         global blocks_True_list
         if self.block_type == "if":
            self.structure_end = self.get_from_cache_or_params(self.structure_end)
            self.structure_data = self.get_from_cache_or_params(self.structure_data)
   
            self.structure_end = int(self.structure_end.replace("'", "")) if type(self.structure_end) == str and type(self.structure_data) == int else self.structure_end
            self.structure_data = int(self.structure_data.replace("'", "")) if type(self.structure_data) == str and type(self.structure_end) == int else self.structure_data

            if (self.structure_end == self.structure_data) and self.block_operation_type == "?" or (self.structure_end != self.structure_data) and self.block_operation_type == "!":
               self.to_do_func()
               blocks_True_list.append(["if", True])
               return

            blocks_True_list.append(["if", False])

         elif self.block_type == "for":
            self.structure_end = self.get_from_cache_or_params(self.structure_end)
            for _ in range(int(self.structure_data.replace("'", ""))): #у нас есть заготовка. В будущем можно сделать список и писать вместо structure_data = range, имя списка. Но вряд-ли, т.к нет смысла дальше обновлять ATS
              self.to_do_func()
            

         elif self.block_type == "else":
              self.to_do_func()


   def to_do_func(self):
      global line_count
      line_count +=1
      ElementsSpliter.main(self, self.to_do)

   def get_from_cache_or_params(self, name): #Функция для поиска значения переменной
      name_copy = name
      if "'" not in name and name not in sys_param:
         if "+" in name:
            name = name.split("+")[0]

         if name in self.params:
            name = self.params[name]

         elif name in cache:
            name = cache[name]

         elif name in plugin_params_global:
            name = plugin_params_global[name]
         
         else:
           errors_output(f"Unknow param: {name}")

         if "+" in name_copy:
            name = getattr(name, name_copy.split("+")[1])
            
      return name 
   


def bridge(code, plugin_params):
 global plugin_params_global
 plugin_params_global = plugin_params

 run = ElementsSpliter()
 status = run.main(code)
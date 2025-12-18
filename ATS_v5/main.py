
#?         ==ATS==
#?         ==V4.0==
#?   ==By Andrey Tolstoy==
#?     ==With commits==, сам не ожидал что начну наконец их писать, лол


from ATS_v5.description import *

self_to_do_flag = False #Если код передаваемый в main является to_do кодом (был написан после then или в print был использован код библиотеки print:web.get:''). Нужен для отслеживания строки, если при выполнении возникнет ошибка. Ведь то, что идет в self.todo, считается отдельной строкой, а нужно вывести ошибку и номер строки "родителя"
blocks_True_list = [] #Список успешно выполненных блоков (если if ... == True)
cache = {}
line_count = 1
plugin_params_global = {}
version = "ATS v5.0 "
config = None
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

    def main(self, code, plugins_args, config_):
        global config, plugin_params_global, line_count, self_to_do_flag
        config = config_
        plugin_params_global = plugins_args
        if code:
         code = code.strip()
         for line in code.split(";"):
             self.clear_params()
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
                           self.errors_output(f"Error: u can`t use else without if")

                        if blocks_True_list[-1][0] == "if" and blocks_True_list[-1][1] == True:
                          self.clear_params()
                          continue #полностью игнорим строку с else, так как если if есть в списке и он успешно выполнен, то нет смысла тратить время исполнения на парсинг ненужного кода

                      self.to_do = line.split("{")[1].replace("}", "").replace("*", ";").strip().replace("\n", "")
                      line = line.split(" ")[1]

               
                      if params["operation_needed"] == True: 
                         self.structure_end = line.split("?" if "?" in line else "!")[0]    
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
                  line = line_copy
               
               #?"""==Params=="""
               elif "=" in line:
                  line = line.split("=")
                  self.param_handler = line[0].strip()
                  self.param_data = line[1].strip()
                  self.param_data = Parser.get_from_cache_or_params(self, self.param_data)
                  self.params[self.param_handler] = self.param_data
 
               self.full_logs_dump(line)
 
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
               self_to_do_flag = False
    

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
        self.to_do = None

    def full_logs_dump(self, line): 
        log_line = (
           f"Code:{line}\n"
           f"Structure_name:{self.structure_name}\n"
           f"Structure_body:{self.structure_body}\n"
           f"Structure_end:{self.structure_end}\n"
           f"Structure_data:{self.structure_data}\n"
           f"Structure_operation:{self.structure_operation}\n"
           f"Params:{self.params}\n"
           f"Param_handler:{self.param_handler}\n"
           f"Param_data:{self.param_data}\n"
           f"Util:{self.util}\n"
           f"Util_data:{self.util_data}\n"
           f"Block_type:{self.block_type}\n"
           f"Block_operation_type:{self.block_operation_type}\n"
           f"To_do:{self.to_do}\n"
           f"Cache:{cache}\n"
        )
        self.logs_load(log_line)
      
       
    def logs_load(self, log_line):
         if config["logs"]:
             print(f"Line {line_count}:\n")
             print("---", log_line)
             
             print("\n=======")
   
    def errors_output(self, error):
      print(version, error, "Line:", line_count - 1 if self_to_do_flag == True else line_count)
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
       if self.to_do:
          self.to_do_func()



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
            
            except Exception as e:
               self.errors_output(e)

   
   def utils_block(self): #Обработчик print и т.п
      if self.util:
            if self.util == "print":
             self.util_data = self.get_from_cache_or_params(self.util_data)  
             if type(self.util_data) == str and self.util_data.split(".")[0] in description["libs"] and self.util_data not in cache: #print:web.get'https://youtube.com'; будет работать, так как он передаст 100% рабочую конструкцию, она обработается и выведится
                   get_data = self.util_data.split("'")[0] if "'" in self.util_data else self.util_data.split(":")[0]
                   self.to_do = f"{self.util_data} then do={get_data}; print:do"

                   if "+" in self.util_data:
                      get_data += "+" + self.util_data.split("+")[1]

                   self.to_do = f"{self.util_data} then do={get_data}; print:do"
                   return
      
             description["utils"][self.util]("ATS output:", self.util_data)

            
            elif self.util == "plugin":
               self.util_data = self.get_from_cache_or_params(self.util_data).replace("'", "")
               description["utils"][self.util]([self.util_data], plugin_params_global, config)
            

   def blocks_block(self): #Обработчик if & for
         global blocks_True_list, line_count
         if self.block_type == "if":
            self.structure_end = self.get_from_cache_or_params(self.structure_end)
            self.structure_data = self.get_from_cache_or_params(self.structure_data)
   
            self.structure_end = int(self.structure_end.replace("'", "")) if type(self.structure_end) == str and type(self.structure_data) == int else self.structure_end
            self.structure_data = int(self.structure_data.replace("'", "")) if type(self.structure_data) == str and type(self.structure_end) == int else self.structure_data

            if (self.structure_end == self.structure_data) and self.block_operation_type == "?" or (self.structure_end != self.structure_data) and self.block_operation_type == "!":
               blocks_True_list.append(["if", True])
               return

            blocks_True_list.append(["if", False])

         elif self.block_type == "for":
            self.structure_end = self.get_from_cache_or_params(self.structure_end)
            for _ in range(int(self.structure_data.replace("'", ""))): #у нас есть заготовка. В будущем можно сделать список и писать вместо structure_data = range, имя списка. Но вряд-ли, т.к нет смысла дальше обновлять ATS
              self.to_do_func() #Единственный случай когда self.to_do_func вызывается напрямую, так как нам нужно вызывать определенное кол-во раз.
              line_count+=1
            

         elif self.block_type == "else":
              return


   def to_do_func(self):
      global self_to_do_flag
      self_to_do_flag = True 
      ElementsSpliter.main(self, self.to_do, plugin_params_global, config)

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
           self.errors_output(f"Unknow param: {name}")

         if "+" in name_copy:
            try:
             name = getattr(name, name_copy.split("+")[1])
            
            except Exception as e:
               self.errors_output(e)
            
      return name 
   


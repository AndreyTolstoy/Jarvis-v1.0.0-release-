
         #?==Jarvis==
         #?==by AT==


from Panel.jsons import load, dump
from Jarvis.outside_panel_get import outside_get
from Jarvis.plugin_run import plugin_run

import speech_recognition
import pyglet
import random
import threading

#Для функции hb - happy birthday
import webbrowser
import datetime

def hb():
    data = load("jsons_data/data.json")
    if data["cache"] == {}:
        data["cache"]["hp_status"] = False
        dump("jsons_data/data.json", data)
    
    if "birthday" in data["cache"] and datetime.datetime.strptime(data["cache"]["birthday"], "%Y-%m-%d").strftime("%m-%d") == datetime.datetime.now().strftime("%m-%d") and data["cache"]["hp_status"] != True:
       webbrowser.open("https://youtu.be/Dm2nj8GBASY?si=SBfgscwgE-57bvGG")
       Commands().answer(name="Поздравляю сэр.wav")
       data["cache"]["hp_status"] = True
       dump("jsons_data/data.json", data)

def listen():
        with speech_recognition.Microphone() as mic:
            try:
                sr = speech_recognition.Recognizer()
                sr.pause_threshold = 0.5
                sr.adjust_for_ambient_noise(source=mic, duration=0.5)
                audio = sr.listen(source=mic, timeout=5)
                query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
                print(f"Вы сказали: {query}")
                return query
            except Exception:
                return ""
            
class Commands:
    def __init__(self, name=None, act_phrase=[], plugin=[], plugin_args={}, priority=None):
        self.name = name
        self.act_phrase = act_phrase
        self.plugin = plugin
        self.plugin_args = plugin_args
        self.priority = priority

    def answer(self, name=None): 
        answers = (random.choice(["Всегда к вашим услугам сэр.wav", "Да сэр.wav", "Да сэр(второй).wav", "Есть.wav", "К вашим услугам сэр.wav", "Запрос выполнен сэр.wav"]) if not name else name)
        answer = pyglet.resource.media("Sounds/" + answers)
        answer.play()
        pyglet.app.exit()
                         

    
class CommandDetector(Commands):
  def __init__(self, name=None, act_phrase=None, open=None, plugin=None, priority=None):
      super().__init__(name, act_phrase, open, plugin, priority)

  def main(self):
   hb()
   while True:
    data = load("jsons_data/data.json")
    config = data["cache"]

    if "outside" in config and config["outside"] != False:
     h3 = threading.Thread(target=outside_get, daemon=True).start()
        
    if "панель" not in data["commands"]:
        data["commands"]["панель"] = {"name" : "панель", "act_phrase" : ["открой панель управления", "панель управления"], "plugin" : ["панель"], "plugin_param" : {}, "priority" : 5}
        data["plugins"]["панель"] = {"data" : "webb.open'http://127.0.0.1:256'", "do" : "open"}
        dump("jsons_data/data.json", data)
        data = load("jsons_data/data.json")
    
    
    text = listen()
    if text: 
        commands_find = []
        for command in data["commands"]:
                command = data["commands"][command]
                command = Commands(command["name"], command["act_phrase"], command["plugin"], command["plugin_param"], int(command["priority"]))
                if any(f"джарвис" in text and phrase in text for phrase in command.act_phrase):
                    command.plugin_args["sr_text"] = text #New. Добавляем в список параметров системный параметр для того, чтобы пользователь мог использовать распознанный текст в своих плагинах
                    command.plugin_args["command_name"] = command.name #New. Добавляем в список параметров системный параметр для того, чтобы пользователь мог использовать имя распознанной команды в своих плагинах
                    commands_find.append(command)
                    for phrase in command.act_phrase:
                        if text.count(phrase) > 1:
                            for i in range(text.count(phrase) - 1): #-1 так как один раз мы ее уже записали сверху
                             commands_find.append(command)
         
        for command in sorted(commands_find, key=lambda p: p.priority, reverse=True):
            command.answer()
            plugin_run(command.plugin, command.plugin_args, config)
        
        

from flask import Flask, render_template, request, url_for, redirect
import bcrypt
import os
import logging

base_path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
log = logging.getLogger('werkzeug') 
log.setLevel(logging.ERROR)

@app.route("/", methods=["POST", "GET"])
def home():
    data_load = load_data()
    data = data_load["data"]
    plugins = data_load["plugins"]
    commands = data_load["commands"]
    if data == {}:
        if request.method == "POST":
            data["name"] = request.form.get("name")
            data["birthday"] = request.form.get("birthday")
            data["token"] = bcrypt.hashpw(bytes(request.form.get("token").strip(), encoding='utf-8'), bcrypt.gensalt(14)).decode() #Сохраняем хеш пароля
            data["ats"] = False
            data["outside"] = False
            data["logs"] = False
            jsons.dump("panel/data.json", data)
        
        else:
         return render_template("register.html", password=True)     
 
    active_plugin = request.args.get("active_plugin")
    active_plugin_name = active_plugin
    active_plugin = (plugins[active_plugin] if active_plugin else None)
    active_command = request.args.get("active_command")
    active_command_name = active_command
    active_command = (commands["commands"][active_command_name] if active_command_name else None)
    return render_template("index.html", data = data, plugins = plugins, commands = commands["commands"], active_plugin = active_plugin,active_plugin_name = active_plugin_name, active_command = active_command, active_command_name = active_command_name)

@app.route("/plugin", methods=["POST"])
def plugins():
    plugins = load_data()["plugins"]
    if request.form.get("action") == "plugin_save":
     if request.form.get("plugin") != "Не выбрано" and not request.form.get("plugin_name"):
         active_plugin = request.form.get("plugin")
         return redirect(url_for("home", active_plugin = active_plugin))
       
     else:
        plugin_args = request.form.get("plugin_args")
        if request.form.get("plugin_do") == "open" and plugin_args.startswith("os") == False and plugin_args.startswith("webb") == False:
           data = f"webb.open'{plugin_args}'" if plugin_args.startswith("http") else f"os.system'{plugin_args}'"

        elif request.form.get("plugin_do") == "key" and plugin_args.startswith("keyboard") == False:
            data = f"keyboard.press_and_release'{plugin_args}'"

        elif request.form.get("plugin_do") == "code":
           data = request.form.get("plugin_args")

        else:
           data = plugin_args
    
        if request.form.get("plugin_name") and request.form.get("plugin_name"):
         plugins[request.form.get("plugin_name")] = {"data" : data, "do" : request.form.get("plugin_do").strip()}
         jsons.dump("plugins.json", plugins)
    
    else:
        del plugins[request.form.get("plugin")]
        jsons.dump("plugins.json", plugins)
    
    return redirect(url_for("home"))

@app.route("/command", methods=["POST"])
def commands():
    commands = load_data()["commands"]
    if request.form.get("action") == "command_save":
     if request.form.get("command") != "Не выбрано" and not request.form.get("command_name"):
         active_command = request.form.get("command")
         return redirect(url_for("home", active_command = active_command))
     
     else:
       if request.form.get("command_name") not in commands and request.form.get("command_name") or request.form.get("command") != "Не выбрано" and request.form.get("command_name"):
           commands["commands"][request.form.get("command_name")] = {
               "name" : request.form.get("command_name"), 
               "act_phrase" : data_of_list_strip(request.form.get("command_act").split(","), output=list),
               "plugin" : request.form.getlist("plugin_for_command"),
               "plugin_param" : data_of_list_strip(request.form.get("plugin_args").split(":"), output=dict),
               "priority" : int(request.form.get("priority"))
               }
           jsons.dump("commands.json", commands)
       
    else:
        if request.form.get("command"):
         del commands["commands"][request.form.get("command")]
         jsons.dump("commands.json", commands)
        
    return redirect(url_for("home"))

@app.route("/config", methods=["POST"])
def config():
   data = load_data()["data"]
   data["ats"] = True if request.form.get("ats") else False
   data["outside"] =  True if request.form.get("outside", False) else False
   data["logs"] =  True if request.form.get("logs", False) else False
   jsons.dump("panel/data.json", data)
   return redirect(url_for("home"))


def data_of_list_strip(data:list, output):
    clear_data = []
    for d in data:
        if d != '':
         clear_data.append(d.strip())
     
    if clear_data != []:
     return clear_data if output == list else {clear_data[0] : clear_data[1]}
    
    return [] if output == list else {}

 
def load_data():
    data = jsons.load("panel/data.json")
    plugins = jsons.load("plugins.json")
    commands = jsons.load("commands.json")
    return {"data": data, "plugins" :  plugins, "commands" :  commands}

def run_server():
    app.run()

if __name__ == "__main__":
    import jsons
    run_server()

else:
    import panel.jsons as jsons
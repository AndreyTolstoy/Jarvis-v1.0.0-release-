import json


def load(file):
  try:
   with open(file, "r", encoding='utf-8') as f:
     return json.load(f)
   
  except:
    return {} if file != "commands.json" else {"commands" : {}}
  

def dump(file, data):
  with open(file, "w", encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
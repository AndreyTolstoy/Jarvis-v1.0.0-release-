import hmac, hashlib, requests
from Panel.jsons import load
from Jarvis.plugin_run import bridge


url = '' #*url вашего сервера 
hmac_secret = b"" #*Нужен для подписи данных. Вы можете вписать сюда свой ключ и обращаться к своему серверу или обращаться без подписи данных, при условии что ваши действия не нарушают LICENSE.md

data = load("jsons_data/data.json")
if "token" in data["cache"]:
 hmac_ = hmac.new(hmac_secret, bytes(data["cache"]["token"], encoding='utf-8'), hashlib.sha256).hexdigest() #*Генерация подписи данных

def outside_get():
    try:
     if data != {}:
      ats = requests.post(url, json={"token" : data["cache"]["token"], "signature" : hmac_}).json() #*Запрос. Программа ожидает в ответ данные в формате json, где будет список с ATS-инструкциями. Например: ["print:'Hello World!'", "webb.open'https://example.com'"]
      if ats != []:
       for command in ats:
         bridge(command, {}, config=data["cache"])

    except:
      print("Сервер удаленного доступа не отвечает.")


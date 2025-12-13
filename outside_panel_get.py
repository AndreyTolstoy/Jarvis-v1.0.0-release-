import hmac, hashlib, requests, time
from panel import jsons
from ATS_v5.main import bridge


url = '' #*url вашего сервера 
hmac_secret = b"" #*Нужен для подписи данных. Вы можете вписать сюда свой ключ и обращаться к своему серверу или обращаться без подписи данных, при условии что ваши действия не нарушают LICENSE.md

data = jsons.load("data.json")
if data:
 hmac_ = hmac.new(hmac_secret, bytes(data["token"], encoding='utf-8'), hashlib.sha256).hexdigest() #*Генерация подписи данных

def outside_get():
    try:
     if data != {}:
      ats = requests.post(url, json={"token" : data["token"], "signature" : hmac_}).json() #*Запрос. Программа ожидает в ответ данные в формате json, где будет список с ATS-инструкциями. Например: ["print:'Hello World!'", "webb.open'https://example.com'"]
      if ats != []:
       for command in ats:
         bridge(command, None)

    except:
      print("Сервер удаленного доступа не отвечает.")


from panel import jsons

def logs():
 return True if "logs" in jsons.load("panel/data.json") and jsons.load("panel/data.json")["logs"] == True else False
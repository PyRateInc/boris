from pizette import *
import requests
import json
import random

def dolar():
	try:
		requsd = requests.get("https://economia.awesomeapi.com.br/all")
		coins = json.loads(requsd.text)
		usd = coins['USD']['high']
		message = "Dólar agora: R${:.4}".format(usd)
		sendMessage(message)
	except:
		sendMessage("Agora não...")
		pass

save = catchConversation()